import enum
import hashlib
import sqlite3
from threading import Thread
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import codefast as cf
import flask
from authc import get_redis
from hashids import Hashids

from dofast.cell.api import API


class FlaskPublicHandlerArgs(str, enum.Enum):
    QX = 'TW05eE0wNXNVMVZUZDJsVWNRbz0K'
    HELLO = 'hello'


class FlaskWorker(object):
    def __init__(self) -> None:
        self.redis = get_redis()
        self.conn = sqlite3.connect('/tmp/mybitly.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS mybitly
            (id INTEGER PRIMARY KEY, 
            long_url TEXT, 
            short_url TEXT)''')
        self.conn.commit()

    def public_handler(self,
                       request: flask.request) -> Optional[Union[str, Dict]]:
        arg = request.args.get('arg')
        if arg == FlaskPublicHandlerArgs.QX:
            return self.redis.get(FlaskPublicHandlerArgs.QX.value).decode()
        elif arg == FlaskPublicHandlerArgs.HELLO:
            return flask.Response('hello')

    def hello_world(self) -> Dict:
        return {'status': 'SUCCESS', 'code': 200, 'msg': 'HELLO'}

    def default_route(self, path: str) -> str:
        path_str = str(path)
        cf.info('request path: ' + path_str)
        if not path_str.startswith('s/'):
            return ''
        key = path_str.replace('s/', '')
        out_url = self.conn.execute(
            '''SELECT long_url FROM mybitly WHERE short_url = ?''',
            (key, )).fetchone()
        if out_url:
            return out_url[0]
        return 'https://www.baidu.com'

    def shorten_url(self, req: flask.request) -> Dict[str, str]:
        data = req.get_json(force=True)
        cf.info('input data: ' + str(data))
        if not data:
            return {}
        url = data.get('url', '')
        md5 = hashlib.md5(url.encode()).hexdigest()
        uniq_id = Hashids(salt=md5, min_length=6).encode(42)

        self.cursor.execute(
            '''INSERT INTO mybitly (long_url, short_url) VALUES (?, ?)''',
            (url, uniq_id))
        return {
            'code': 200,
            'status': 'SUCCESS',
            'url': req.host_url + 's/' + uniq_id
        }

    def render_rss(self):
        from rss.base.wechat_rss import create_rss_worker
        wechat_ids = [
            'almosthuman', 'yuntoutiao', 'aifront', 'rgznnds', 'infoq',
            'geekpark', 'qqtech'
        ]
        for wechat_id in wechat_ids:
            worker = create_rss_worker(wechat_id)
            _, all_articles = worker.pipeline()
            cf.info('all_articles: ' + str(all_articles))


class TwitterService(object):
    def __init__(self, api: API) -> None:
        self.api = api

    def post(self, req: flask.request) -> None:
        text = req.args.get('text', '')
        cf.info('input text: ' + text)
        files = req.files.getlist('images')
        cf.info('input files: ' + str(files))
        media = ['/tmp/{}'.format(f.filename) for f in files]
        for m, f in zip(media, files):
            f.save(m)
        self.api.twitter.post([text] + media)
        return {'text': text, 'images': [f.filename for f in files]}


class BarkWorker(object):
    def __call__(self, req: flask.request) -> None:
        print(str(req))
        return {'status': 'SUCCESS', 'code': 200}


class SuperCell(object):
    def __init__(self) -> None:
        self.api = API()
        self.flask_worker = FlaskWorker()
        self.twitter_service = TwitterService(self.api)
        self.bark_worker = BarkWorker()
