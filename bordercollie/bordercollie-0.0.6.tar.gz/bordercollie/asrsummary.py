#!/usr/bin/env python
import ast
import asyncio
import secrets
import time
from typing import Callable, Dict, List, Optional, Set, Tuple, Union

import aiohttp
import codefast as cf
from codefast.io._json import Gzip 
import pandas as pd
import redis
import requests
from codefast.patterns.pipeline import Component, Pipeline
from pydub.utils import mediainfo as mi

from bordercollie.auth import auth
from bordercollie.sql import exec, insert_many

# racc = auth.redis_account
# cli = redis.Redis(host=racc['host'],
#                   port=racc['port'],
#                   password=racc['password'])

class ASRRecordCollector(Component):

    def process(self, logfile: str) -> List[Dict]:
        self.print_log = False
        records = []
        with open(logfile, 'r') as f:
            for line in f:
                if 'POST /api/transcript' not in line:
                    continue
                date_str = line.split(']')[0].replace('[', '')
                date = pd.to_datetime(date_str)
                now = pd.Timestamp.now()
                seconds_diff = (now - date).total_seconds()
                if seconds_diff > 60:
                    continue
                data = line
                records.append(data)
        return records


class GetRecordInfo(Component):

    def process(self, records: List[str]):
        res = []
        for r in records:
            try:
                str_date = r.split(']')[0].replace('[', '')
                str_js = r.split('|DATA: ')[1]
                js = ast.literal_eval(str_js)
                cid = js['conversation_id']
                link = js['file_link']
                audio = mi(link)
                cf.info(f'get audio info {audio}')
                duration = audio['duration']
                industry_id = js['industry_id']
                j_pruned = {
                    'date': str_date,
                    'conversation_id': cid,
                    'duration': duration,
                    'industry_id': industry_id
                }
                res.append(j_pruned)
            except:
                pass
        return res


class PostToMessageQueue(Component):

    def __init__(self):
        super().__init__()
        self.print_log = False

    def process(self, summary: List[str]) -> List[str]:
        topic = f'{auth.nsqd}/pub?topic=transcript_record'
        for v in summary:
            requests.post(topic, json=v)
        return summary


def save_record() -> str:
    """collect transcription records and save to redis"""
    pipeline = Pipeline(
        [ASRRecordCollector(),
            GetRecordInfo(),
            PostToMessageQueue()])
    pipeline.process('/log/serving/serving.log')


# ---------------------------------------------
# ^_^
# ---------------------------------------------


class _SQLConsole(object):

    @staticmethod
    def get_records_by_date(date_str) -> List[str]:
        cmd = "SELECT value FROM `kvpair` WHERE `value` REGEXP '{}'".format(
            date_str)
        res = asyncio.run(exec(cmd))
        return [_[0] for _ in res] if res else []

    @staticmethod
    def get_summary_by_date(date_str) -> Dict[str, Union[str, int]]:
        records = _SQLConsole.get_records_by_date(date_str)
        total_duration = 0
        for r in records:
            j = ast.literal_eval(r)
            if j['duration'] != 'N/A':
                total_duration += float(j['duration'])
        return {
            'date': date_str,
            'total_duration': total_duration,
            'total_number': len(records)
        }


class SyncToSQL(Component):
    
    def get_data_from_sqlite(self)->List[str]:
        import sqlite3 
        today = pd.Timestamp.now().strftime('%Y-%m-%d')
        cmd = "SELECT msg FROM `trans_records` WHERE `msg` LIKE '%{}%'".format(today)
        records = []
        for f in cf.io.walk('local/data'):
            if f.endswith('.db'):
                conn = sqlite3.connect(f)
                cur = conn.cursor()
                cur.execute(cmd)
                resp = cur.fetchall()
                records.extend([_[0] for _ in resp])
        return records

    def process(self) -> List[str]:
        records = self.get_data_from_sqlite()
        cf.info('found {} records'.format(len(records)))
        data = {cf.md5sum(e): e for e in records}
        try:
            asyncio.run(insert_many(data))
            return None
        except Exception as e:
            cf.error(e)
            return None


class CalculateSummary(Component):

    def find_max_duration(self, records: List[str]) -> Tuple[int, int]:
        max_duration, cid = 0, -1
        for r in records:
            j = ast.literal_eval(r)
            try:
                duration = float(j['duration'])
                if duration > max_duration:
                    max_duration = duration
                    cid = j['conversation_id']
            except Exception as e:
                cf.warning(e)
        return max_duration, cid

    def get_summary(self) -> str:
        today_str = pd.Timestamp.now()
        yesterday_str = (today_str - pd.Timedelta(days=1)).strftime("%Y-%m-%d")
        day_before_yesterday_str = (today_str -
                                    pd.Timedelta(days=2)).strftime("%Y-%m-%d")
        yesterday_summary = _SQLConsole.get_summary_by_date(yesterday_str)
        day_before_yesterday_summary = _SQLConsole.get_summary_by_date(
            day_before_yesterday_str)

        yesterday_records = _SQLConsole.get_records_by_date(yesterday_str)
        max_duration, cid = self.find_max_duration(yesterday_records)

        sign = '增长' if yesterday_summary[
            'total_duration'] > day_before_yesterday_summary[
                'total_duration'] else '减少'

        ratio = abs(yesterday_summary['total_duration'] -
                    day_before_yesterday_summary['total_duration']) / max(
                        1, day_before_yesterday_summary['total_duration'])

        n_sign = '增长' if yesterday_summary[
            'total_number'] > day_before_yesterday_summary[
                'total_number'] else '减少'

        n_ratio = abs(yesterday_summary['total_number'] -
                      day_before_yesterday_summary['total_number']) / max(
                          1, day_before_yesterday_summary['total_number'])

        text = "日期: {}\n".format(yesterday_summary['date']) + \
                "转录总时长: {} 小时\n".format(round(yesterday_summary['total_duration']/3600, 2)) + \
                "转录总次数: {} 次\n".format(yesterday_summary['total_number']) + \
                "平均时长: {} 秒\n".format(round(yesterday_summary['total_duration']/yesterday_summary['total_number'], 2)) + \
                "最长时长: {} 秒 (会话 ID {})\n".format(round(max_duration, 2), cid) + \
                "时长较前一日{}: {}%\n".format(sign, round(ratio*100, 2)) + \
                "次数较前一日{}: {}%\n".format(n_sign, round(n_ratio*100, 2))

        cf.info(day_before_yesterday_summary)
        cf.info(yesterday_summary)
        cf.info(text)
        return text

    def process(self) -> Dict[str, str]:
        return self.get_summary()


class PostToWebhook(Component):

    def process(self, text: str) -> bool:

        date = pd.Timestamp.now()
        msg = {'msg_type': 'text', 'content': {'text': text}}
        is_succ = False
        if date.hour == 7 and date.minute == 50:     # personal
            resp = cf.net.post(auth.webhook, json=msg)
            cf.info(resp.text)
            is_succ = True
        if date.hour == 10 and date.minute == 5:     # group
            resp = cf.net.post(auth.asr_group, json=msg)
            cf.info(resp.text)
            is_succ = True
        return is_succ


def calculate_summary():
    pipeline = Pipeline([
        SyncToSQL(),
        CalculateSummary(),
        PostToWebhook(),
    ])
    pipeline.process()


if __name__ == '__main__':
    calculate_summary()
