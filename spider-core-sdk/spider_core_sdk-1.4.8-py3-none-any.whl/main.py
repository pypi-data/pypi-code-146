import os
import sys
import shutil
import subprocess
import importlib
import time
import requests
import json
import logging

import likeshell
from likeshell.shell import run_cls
from logging.handlers import RotatingFileHandler
from jinja2 import FileSystemLoader, Environment
from termcolor import colored
from .config import host_config
from .utils import sign_headers

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
HOME_PATH = os.getenv('HOME') or os.getenv('HOMEPATH')
CJZT_PATH = os.path.join(HOME_PATH, '.cjzt')
if HOME_PATH and not os.path.exists(CJZT_PATH):
    os.mkdir(CJZT_PATH)

logger = logging.getLogger(__name__)

log_file = os.path.join(CJZT_PATH, 'cjzt-sdk.log')
simple_fmt = logging.Formatter('[%(asctime)s-%(levelname)s] %(message)s')
log_handler = RotatingFileHandler(
    filename=log_file, maxBytes=2048000, backupCount=5, encoding='utf-8'
)
log_handler.setFormatter(simple_fmt)
log_handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)


def load_spider_name():
    pwd = os.getcwd()
    sys.path.append(pwd)
    # scrapy项目根目录下只能存在一个文件夹(除隐藏文件外)
    spider_paths = [i for i in os.walk(pwd).__next__()[1] if not i.startswith('.')]
    if not spider_paths:
        return
    spider_module_path = f'{spider_paths[0]}.spiders'
    spider_path = spider_module_path.replace('.', '/')
    if not os.path.exists(spider_path):
        return

    try:
        # scrapy项目spiders包中只能有一个py文件(除__init__.py文件外)
        spider_files = [
            i for i in os.walk(spider_path).__next__()[2] if i != '__init__.py' and i.endswith('.py')
        ]
        spider_file = spider_files[0][:-3]
        module = importlib.import_module(f'{spider_module_path}.{spider_file}')
        for k, v in module.__dict__.items():
            base = None
            if hasattr(v, '__base__'):
                base = v.__base__.__name__
            if isinstance(v, type) and base == 'HttpSpider':
                return v.name
    except Exception as e:
        logger.info(f'未获取到项目名称, 异常: {e}')
        return


class CjztCrawler(likeshell.Main):
    def crawl(self, iid, sid, env):
        spider_name = load_spider_name()
        if spider_name is None:
            logger.info(f'未获取到Scrapy项目名称, 实例ID: {iid}, 项目ID: {sid}, 环境:{env}')
            cmd = f'python3 main.py {iid} {sid} {env}'
        else:
            logger.info(f'获取到Scrapy项目名称: {spider_name} 实例ID: {iid}, 项目ID: {sid}, 环境:{env}')
            cmd = f'scrapy crawl {spider_name} ' \
                  f'-a instance_id={iid} -a spider_id={sid} -a env={env} -a cjzt_log=./log_{iid}.log --nolog'
        os.system(cmd)

    def stats(self, iid, env):
        while True:
            cmd = f"ps -aux | grep -v grep | grep scrapy | grep {iid} | awk '{{print $3,$4}}'"
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            stats = p.stdout.read()
            if stats:
                cup_pst, mem_pst = stats.decode().split(' ')
                print(cup_pst, mem_pst)
            time.sleep(120)

    @likeshell.Options(arg='spider_name', tag=('-s', '-S', '--spiders'))
    @likeshell.Options(arg='alias', tag=('-a', '-A', '--alias'))
    @likeshell.Options(arg='git_address', tag=('-g', '-G', '--git'))
    @likeshell.Options(arg='platform', tag=('-p', '-P', '--platform'))
    @likeshell.Options(arg='default_branch', tag=('-b', '-B', '--branch'))
    @likeshell.Options(arg='frame', tag=('-f', '-F', '--frame'))
    @likeshell.Options(arg='data_type', tag=('-d', '-D', '--dtype'))
    @likeshell.Options(arg='worker_number', tag=('-w', '-W', '--worker'))
    @likeshell.Options(arg='desc', tag='--desc')
    @likeshell.Options(arg='project_type', tag='--ptype')
    @likeshell.Options(arg='ak', tag='--ak')
    @likeshell.Options(arg='secret', tag='--secret')
    def addproject(
            self,
            project_name,
            spider_name,
            *,
            alias='',
            git_address='',
            platform='',
            default_branch='master',
            frame='scrapy',
            data_type='goods',
            worker_number: int = 1,
            project_type='goods',
            desc='无',
            ak='',
            secret='',
    ):
        """
        创建项目
        cjzt addproject <project_name> -g <git_remote> -a <alias> -s <spider_name>
        -d <data_type> -P <platform> --worker <worker_number> --ptype <project_type>
        参数:
            project_name: 项目名称
            spider_name: 爬虫名称 tag: [-s, -S, --spiders]
            alias: 优先用于采集中台项目名称 tag: [-a, -A, --alias]
            git_address: git仓库地址,保证是一个全新创建的仓库 tag: [-g, -G, --git]
            platform: 平台 tag: [-p, -P, --platform]
            default_branch: 默认的分支，默认为`master` tag: [-b, -B, --branch]
            frame: 使用的框架，影响生产的模板，默认为`scrapy` tag: [-f, -F, --frame]
            data_type: 数据类型，默认为`goods` tag: [-d, -D, --dtype]
            worker_number: 运行实例数，默认为`1` tag: [-w, -W, --worker]
            project_type: 项目类型，默认为`goods` tag: --ptype
            desc: 项目简介 tag: --desc
            ak: 账号access key tag: --ak
            secret: 账号access secret tag: --secret
        """
        project_name_camel_case = ''.join([i.capitalize() for i in project_name.split('_')])
        spider_name_camel_case = ''.join([i.capitalize() for i in spider_name.split('_')])
        temp_info = {
            'project_name': project_name,
            'project_name_camel_case': project_name_camel_case,
            'git_address': git_address,
            'spider_name_camel_case': spider_name_camel_case,
            'spider_name': spider_name,
            'default_branch': default_branch,
            'data_type': data_type,
        }
        if frame == 'scrapy':
            temp_files = {
                'http_scrapy_temp/scrapy.cfg.temp': f'{project_name}/scrapy.cfg',
                '.gitignore': f'{project_name}/.gitignore',
                'http_scrapy_temp/project/__init__.py': f'{project_name}/{project_name}/__init__.py',
                'http_scrapy_temp/project/items.py.temp': f'{project_name}/{project_name}/items.py',
                'http_scrapy_temp/project/middlewares.py.temp': f'{project_name}/{project_name}/middlewares.py',
                'http_scrapy_temp/project/pipelines.py.temp': f'{project_name}/{project_name}/pipelines.py',
                'http_scrapy_temp/project/settings.py.temp': f'{project_name}/{project_name}/settings.py',
                'http_scrapy_temp/project/spiders/__init__.py': f'{project_name}/{project_name}/spiders/__init__.py',
                'http_scrapy_temp/project/spiders/spider.py.temp': f'{project_name}/{project_name}/spiders/spider.py',
            }
            os.makedirs(os.path.join(project_name, project_name, 'spiders'))
        else:
            temp_files = {
                'main.py.temp': f'{project_name}/main.py',
                '.gitignore': f'{project_name}/.gitignore',
            }
        env = Environment(loader=FileSystemLoader(os.path.join(BASE_PATH, 'temp')))
        for source, target in temp_files.items():
            if source.endswith('.temp'):
                template = env.get_template(source)
                with open(target, 'w') as f:
                    f.write(template.render(project_info=temp_info))
            else:
                source_fp = os.path.join(BASE_PATH, 'temp', source)
                shutil.copyfile(source_fp, target)

        if not git_address:
            print(colored('WARNING: 参数未获取到git地址，只创建本地项目', 'yellow'))

        access_key = ak
        access_secret = secret
        if not ak or not secret:
            access_key = os.getenv('CJZT_ACCESS_KEY')
            access_secret = os.getenv('CJZT_ACCESS_SECRET')
            if not access_key or not access_secret:
                print(colored('WARNING: 参数与环境变量中都未获取到账户信息，只创建本地项目', 'yellow'))
                print(colored('WARNING: 环境变量KEY:\n  CJZT_ACCESS_KEY, CJZT_ACCESS_SECRET', 'yellow'))

        if git_address:
            os.system(f'cd {project_name}')
            os.chdir(project_name)
            os.system('git init')
            os.system(f'git remote add origin {git_address}')
            os.system(f'git checkout -b {default_branch}')
            os.system('git add .')
            os.system('git commit -m "Initial Commit"')
            os.system(f'git push -u origin {default_branch}')

        cjzt_env = os.getenv('CJZT_ENV')
        if access_key and access_secret:
            hosts = host_config.get(cjzt_env)
            if not hosts:
                print(colored('WARNING: 环境变量中未获取到CJZT_ENV，默认使用测试环境地址', 'yellow'))
                hosts = host_config.get('test')

            url = hosts['server_url']
            if not platform:
                print(colored('WARNING: 未获取到平台参数，只创建本地项目', 'yellow'))
                return
            if not project_type:
                print(colored('WARNING: 未获取到项目类型参数，只创建本地项目', 'yellow'))
                return

            body = {
                'name': alias or project_name,
                'instance_num': worker_number,
                'type': project_type,
                'platform': platform,
                'file': git_address,
                'description': desc,
            }
            headers = sign_headers(
                method='POST',
                params={},
                body=body,
                key=access_key,
                secret=access_secret
            )
            headers['user-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
            r = requests.post(
                f'{url}/spider/project',
                json=body,
                headers=headers,
                timeout=60
            ).json()
            if r['code'] != 200:
                print(colored(f'ERROR: Message: {r["msg"]} Data: {r["data"]},只创建本地项目', 'red'))
                return
            else:
                project_map_file = os.path.join(CJZT_PATH, '_project_id_map.json')
                if os.path.exists(project_map_file):
                    with open(project_map_file) as f:
                        try:
                            project_map = json.load(f)
                        except ValueError:
                            project_map = {}
                else:
                    project_map = {}

                project_map[project_name] = {
                    'cjzt_pname': alias,
                    'spider_name': spider_name,
                    'git': git_address,
                    'project_id': r['data']['id']
                }
                with open(project_map_file, 'w') as f:
                    json.dump(project_map, f)

    @likeshell.Options(arg='project_name', tag='--name')
    @likeshell.Options(arg='project_id', tag='--pid')
    @likeshell.Options(arg='ak', tag='--ak')
    @likeshell.Options(arg='secret', tag='--secret')
    @likeshell.Options(arg='tag', tag=['-t', '--tag'])
    @likeshell.Options(arg='comment', tag='-m')
    @likeshell.Options(arg='machine_type', tag='--mtype')
    def online(
            self,
            comment,
            *,
            project_name=None,
            project_id=None,
            tag='master',
            machine_type='normal',
            ak=None,
            secret=None,
    ):
        access_key = ak
        access_secret = secret
        if not ak or not secret:
            access_key = os.getenv('CJZT_ACCESS_KEY')
            access_secret = os.getenv('CJZT_ACCESS_SECRET')
            if not access_key or not access_secret:
                print(colored('ERROR: 参数与环境变量中都未获取到账户信息', 'red'))
                print(colored('ERROR: 环境变量KEY:\n  CJZT_ACCESS_KEY, CJZT_ACCESS_SECRET', 'red'))
                return

        cjzt_env = os.getenv('CJZT_ENV')
        hosts = host_config.get(cjzt_env)
        if not hosts:
            print(colored('WARNING: 环境变量中未获取到CJZT_ENV，默认使用测试环境地址', 'yellow'))
            hosts = host_config.get('test')

        url = hosts['server_url']

        project_name = project_name or os.getcwd().split(os.path.sep)[-1]
        project_map_file = os.path.join(CJZT_PATH, '_project_id_map.json')
        if os.path.exists(project_map_file):
            with open(project_map_file) as f:
                project_map = json.load(f)
            project_info = project_map.get(project_name)
            if project_info:
                project_id = project_info['project_id']

        if not project_id:
            print(colored('ERROR: 未匹配到可上线的项目，在项目根目录下执行或提供项目ID重试', 'red'))
            return

        os.system(f'git add .')
        os.system(f'git commit -m "{comment}"')
        os.system(f'git push origin {tag}')

        body = {
            'id': project_id,
            'allocation': 'auto',
            'desc': comment,
            'machine_type': machine_type,
            'tag': tag,
        }
        headers = sign_headers(
            method='POST',
            params={},
            body=body,
            key=access_key,
            secret=access_secret
        )
        r = requests.post(
            f'{url}/spider/project/online',
            data=body,
            headers=headers,
            timeout=60
        ).json()
        if r['code'] != 200:
            print(colored(f'ERROR: Message: {r["msg"]} Data: {r["data"]},上线失败', 'red'))
            return

    def offline(
            self,
            *,
            project_name=None,
            project_id=None,
            ak=None,
            secret=None,
    ):
        pass


def main():
    run_cls(CjztCrawler, CjztCrawler.__dict__)
