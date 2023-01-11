import json
import os
import socketserver
import sys

import codefast as cf
from codefast.argparser import PLACEHOLDER

from dofast.flask.config import AUTH_KEY


from .network import (Bookmark, CoinMarketCap,
                      CustomHTTPRequestHandler, Douban, InputMethod,
                      LunarCalendar, Phone)
from .pipe import author
from .security._hmac import generate_token
from .utils import download as getfile
from dofast.toolkits.telegram import Channel
import ast
from rich import print


def hemabot():
    from dofast.bots.hemabot import Psycho
    Psycho.main()


def jsonify() -> dict:
    if len(sys.argv) > 1:
        cf.info("formatting {}".format(sys.argv[1]))
        jsf = sys.argv[1]
        assert cf.io.exists(jsf), "file {} not found".format(jsf)
        js = cf.eval(cf.io.reads(jsf).lstrip().rstrip())
        cf.js.write(js, jsf + '-formated.json')
        from dofast.scripts.pyoss import Client as PyossClient
        client = PyossClient()
        url = client.upload(jsf + '-formated.json')
        from dofast.network import bitly
        url = bitly(url, printout=False)
        cf.info('online url : "{}"'.format(url))
    else:
        _stdin = sys.stdin
        x = _stdin.buffer.read().decode('utf-8')
        x = ast.literal_eval(x)
        _dict = json.dumps(x, indent=4)
        print(_dict)


def nsq_sync():
    cli = Bucket()
    if len(sys.argv) > 1:
        cf.utils.shell('zip -r9 -P syncsync63 -FSr /tmp/sync.zip {}'.format(
            ' '.join(sys.argv[1:])))
        cf.info('Files zipped.')
        cli.upload('/tmp/sync.zip')
        token = generate_token(AUTH_KEY, expire=5)
        _uuid = cf.utils.uuid(),
        cf.js.write({'uuid': _uuid}, '/tmp/syncfile.json')
        js = {
            'token': token,
            'topic': 'file',
            'channel': 'sync',
            'uuid': _uuid,
            'data': {
                'uuid': _uuid,
                'filename': 'sync.zip'
            }
        }
        SERVER_HOST = author.get('SERVER_HOST')
        res = cf.net.post(f'http://{SERVER_HOST}:6363/nsq', json=js)
        cf.info('FileSync', res.text)


def _hint_wubi():
    if len(sys.argv) > 1:
        InputMethod().entry(sys.argv[1])


def main():
    sp = cf.argparser.ArgParser()
    from dofast.apps import Apps
    # PLACEHOLDER = cf.argparser.PLACEHOLDER
    sp.input('-d', '--ddfile')
    sp.input('-ip',
             '--ip',
             sub_args=[['p', 'port']],
             default_value="localhost")
    sp.input('-rc', '--roundcorner', sub_args=[['r', 'radius']])
    sp.input('-gu', '--githubupload')
    sp.input('-sm', '--smms')
    sp.input('-fd', '--find', sub_args=[['dir', 'directory']])
    sp.input('-m', '--msg', sub_args=[['r', 'read'], ['w', 'write']])
    sp.input('-fund', '--fund', sub_args=[['ba', 'buyalert']])
    sp.input('-stock', '--stock')
    sp.input('-gcr', '--githubcommitreminder')
    sp.input('-pf', '--phoneflow')
    sp.input('-tgbot', '--telegrambot')
    sp.input('-snapshot',
             '--snapshot',
             description='post a snapshot message to Channel')
    sp.input('-db', '--doubaninfo', description='Get douban film information.')
    sp.input(
        '-lunar',
        '-lunarcalendar',
        default_value="",
        description='Lunar calendar. Usage:\n sli -lc or sli -lc 2088-09-09.')
    sp.input('-fi', '-fileinfo', description='Get file meta information.')

    sp.input('-coin',
             sub_args=[['-q', '-quote']],
             description='Coin Market API. Usage: \n sli -coin -q \n sli -coin -q btc')
    sp.input('-http',
             '-httpserver',
             sub_args=[['p', 'port']],
             description='Simple HTTP server. Usage:\n sli -http -p 8899')

    sp.input('-uni', description='Unicom data flow usage.')

    sp.input('-e2c', '-excel2csv', description='Extract sheets to CSVs')
    sp.input('-gg', '-google_translate', description='Google translation API.')
    sp.input('-botsync', description='sync files from Hema bot')
    sp.input('-ccard',
             sub_args=[['-len', '--length']],
             description='Credit card generator.')
    sp.input('-avatar', description='Generate random avatar.')
    sp.parse()
    apps = Apps()
    # ------------------------------------
    if sp.avatar:
        import dofast.pyavatar as pa
        pa.PyAvataaar().random()

    elif sp.ccard:
        from dofast.toolkits.credit_card_generator import create_cc_numbers
        _len = 16 if not sp.ccard.length else int(sp.ccard.length)
        _bin = '537630' if sp.ccard.value == PLACEHOLDER else sp.ccard.value
        cf.info(_bin, _len)
        for n in create_cc_numbers(_bin, ccnumber_length=_len):
            print(n)

    elif sp.botsync:
        from dofast.toolkits.telegram import download_latest_file
        download_latest_file()

    elif sp.google_translate:
        apps.translator.run(client='google')

    elif sp.excel2csv:
        os.system('mkdir -p /tmp/excel/')
        cf.reader.Excel(sp.excel2csv.value).to_csv('/tmp/excel/')

    elif sp.httpserver:
        port = 8899 if not sp.httpserver.port else int(sp.httpserver.port)
        Handler = CustomHTTPRequestHandler
        with socketserver.TCPServer(("", port), Handler) as httpd:
            cf.logger.info(f"serving at port {port}")
            httpd.serve_forever()

    elif sp.fileinfo:
        info = cf.io.info(sp.fileinfo.value)
        important_features = {
            'channel_layout', 'channels', 'duration', 'sample_rate'
        }
        for key in ('bit_rate', 'channel_layout', 'channels',
                    'codec_tag_string', 'codec_long_name', 'codec_name',
                    'duration', 'filename', 'format_name', 'sample_rate',
                    'size', 'width'):
            if key == 'duration':
                v = info[key]
                info[key] = "{} ({})".format(v, cf.io.readable_duration(v))
            colortext = cf.fp.green(info.get(key, None), attrs=[
                'bold'
            ]) if key in important_features else info.get(key, None)
            print('{:<20} {}'.format(key, colortext))

    elif sp.doubaninfo:
        Douban.query_film_info(sp.doubaninfo.value)

    elif sp.tgbot:
        Channel('messalert').post(sp.tgbot.value)

    elif sp.snapshot:
        show_time = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        Channel('messalert').snapshot(sp.snapshot.value, show_time)

    elif sp.githubcommitreminder:
        from .crontasks import GithubTasks
        GithubTasks.git_commit_reminder()
        GithubTasks.tasks_reminder()


    elif sp.ddfile:
        from .utils import create_random_file
        create_random_file(int(sp.ddfile.value or 100))

    elif sp.ip:
        v_ip, v_port = sp.ip.value, sp.ip.port
        from .utils import shell
        if not sp.ip.port:
            print(shell("curl -s cip.cc"))
        else:
            print("Checking on:", v_ip, v_port)
            curl_socks = f"curl -s --connect-timeout 5 --socks5 {v_ip}:{v_port} ipinfo.io"
            curl_http = f"curl -s --connect-timeout 5 --proxy {v_ip}:{v_port} ipinfo.io"
            res = shell(curl_socks)
            if res != '':
                print(res)
            else:
                print('FAILED(socks5 proxy check)')
                print(shell(curl_http))

    elif sp.roundcorner:
        from .utils import rounded_corners
        image_path, radius = sys.argv[2], -1
        if len(sys.argv) == 4:
            radius = int(sys.argv[3])
        elif len(sys.argv) == 5:
            radius = int(sys.argv[4])
        rounded_corners(image_path, radius)

    elif sp.githubupload:
        from .network import githup_upload
        githup_upload(sp.githubupload.value)

    elif sp.smms:
        from .utils import smms_upload
        smms_upload(sp.smms.value)

    elif sp.find:
        from .utils import findfile
        print(sp.find.value, sp.find.directory or '.')
        findfile(sp.find.value, sp.find.directory or '.')

    elif sp.fund:
        from .fund import invest_advice, tgalert
        if sp.fund.buyalert:
            tgalert()
        else:
            invest_advice(None if sp.fund.value ==
                          PLACEHOLDER else sp.fund.value)

    elif sp.stock:
        from .stock import Stock
        if sp.stock.value != PLACEHOLDER:
            Stock().trend(sp.stock.value)
        else:
            Stock().my_trend()

    elif sp.lunarcalendar:
        date: str = sp.lunarcalendar.value.replace('PLACEHOLDER', '')
        LunarCalendar.display(date)

    else:
        from .data.msg import display_message
        display_message()
        sp.help()
        done, total = sp._arg_counter, 50
        print('✶' * done + '﹆' * (total - done) +
              "({}/{})".format(done, total))


if __name__ == '__main__':
    main()
