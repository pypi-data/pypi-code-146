"""
异构仓库同步升级工具

前置条件:
    1. 安装git
Usage:
    sync init [-r ROOT] [-c CONFIG]
    sync start [-r ROOT] [-c CONFIG]
    sync remote <url>
Options:
    -h,--help  显示帮助菜单
    -c,--config=CONFIG  配置文件  [default: sync.yaml]
    -r,--root=ROOT  根目录  [default: .]
Example:
    sync init
    sync start
"""
import datetime
import shutil
import stat
import time

from docopt import docopt
import json
import os
import yaml
import git
from git import RemoteProgress

from lib.api.index import api_clients
from lib.http import Http
from lib.util import get_dict_value, set_dict_value, log, shell, get_git_modify_file_count, save_file


def cli():
    """
    异构仓库同步升级工具入口
    """
    args = docopt(__doc__)
    root = get_root(args)
    config_file = f"{root}/{args['--config']}"
    f = open(config_file, 'r', encoding='utf-8')
    config = yaml.load(f, Loader=yaml.FullLoader)
    if args['init']:
        handle_init(root, config)
    elif args['start']:
        handle_start(root, config)
    elif args['remote']:
        handle_remote(root, config, args)
    else:
        log(__doc__)


class CloneProgressPrinter(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=""):
        print(
            op_code,
            cur_count,
            max_count,
            cur_count / (max_count or 100.0),
            message or "NO MESSAGE",
        )


def handle_init(root, config):
    """
    处理 init 命令
    """
    if not os.path.exists(root):
        os.mkdir(root)
    os.chdir(root)
    log(f"即将在{root}目录初始化同步项目")
    log(f"git init : {root}")
    shell('git init')
    repo = git.Repo(path=root)
    print(repo.heads)
    if len(repo.heads) == 0:
        save_ignore_file(root)
        shell("git add .")
        shell('git commit -m "sync init start"')
    log("get submodules")
    sms = repo.iter_submodules()
    print(sms)
    conf_repos = config['repo']
    conf_options = config['options']
    conf_repo_root = conf_options['repo_root']
    for key in conf_repos:
        item = conf_repos[key]
        log(f"add submodule:{item['url']}")
        path = f"{conf_repo_root}/{item['path']}"
        # repo.create_submodule(key, path, url=item['url'], branch=item['branch'])
        shell(f"git submodule add -b {item['branch']} --name {key} {item['url']} {path}")

    log("更新所有仓库")

    shell(f"git submodule update --init --recursive --progress")
    repo.iter_submodules()
    repo.submodule_update(recursive=True)
    shell("git add .")
    shell('git commit -m "sync init success"')

    os.chdir(os.getcwd())
    log("初始化完成")


def handle_start(root, config):
    """
    处理 start 命令
    """
    log("开始同步...")
    log("更新所有仓库")
    repo = git.Repo.init(path=root)
    sms = repo.submodules
    if not sms:
        log("还未初始化，请先执行初始化命令")
        return
    shell(f"git submodule update --init --recursive --progress")
    time.sleep(0.2)
    repo.iter_submodules()
    log("仓库更新完成")

    conf_repo = config['repo']
    conf_options = config['options']
    conf_repo_root = conf_options['repo_root']
    conf_sync_map = config['sync']

    proxy_fix = get_dict_value(conf_options, 'proxy_fix')
    http = Http(proxy_fix=proxy_fix)

    status = read_status(root)
    for key in conf_sync_map:
        time.sleep(0.2)
        conf_sync = conf_sync_map[key]
        conf_src = conf_sync['src']
        conf_target = conf_sync['target']
        conf_src_repo = conf_repo[conf_src['repo']]
        conf_target_repo = conf_repo[conf_target['repo']]
        repo_src = sms[conf_src['repo']].module()
        repo_target = sms[conf_target['repo']].module()

        def back_to_main_branch():
            # 切换回主分支
            shell(f"git checkout -f {conf_target_repo['branch']}")
            time.sleep(1)

        def create_and_checkout(cur_rep, branch):
            log(f"checkout同步分支：{branch}")
            if branch not in cur_rep.heads:
                shell(f"git branch {branch}")
                time.sleep(1)
            shell(f"git checkout {branch}")
            time.sleep(1)

        def do_sync():
            dir_src_sync = f"{repo_src.working_dir}/{conf_src['dir']}"
            dir_target_sync = f"{repo_target.working_dir}/{conf_target['dir']}"
            log(f"同步目录：{dir_src_sync}->{dir_target_sync}")
            if os.path.exists(dir_target_sync):
                shutil.rmtree(dir_target_sync)
                time.sleep(0.2)
            shutil.copytree(dir_src_sync, dir_target_sync)
            git_file = f"{dir_target_sync}/.git"
            if os.path.exists(git_file):
                os.unlink(git_file)
            log(f"{key} 复制完成,准备提交:{conf_target['dir']}")
            time.sleep(1)

        def do_commit():
            shell(f"git add .")
            time.sleep(0.2)
            count = get_git_modify_file_count()
            time.sleep(0.2)
            print(f"modify count : {count}")
            if count <= 0:
                log(f"{key} 没有变化，无需提交")
                return False
            else:
                # 提交更新
                now = datetime.datetime.now()
                shell(f'git commit -m "sync {key} success [{now}]"')
                # repo_target.index.commit(f"sync {key} success [{now}]")
                log(f"{key} 提交成功")
                time.sleep(0.2)
                # 记录最后提交hash
                src_last_hash = repo_src.head.commit.hexsha
                target_last_hash = repo_target.head.commit.hexsha

                set_dict_value(status, f"sync.{key}.last_commit_src", src_last_hash)
                set_dict_value(status, f"sync.{key}.last_commit_target", target_last_hash)
                save_status(root, status)
                return True

        def do_push():
            if not get_dict_value(conf_options, 'push'):
                return False
            log("检测是否需要push")
            # 检测是否需要push
            local_hash = repo_target.head.commit.hexsha
            remote_hash = None
            refs = repo_target.refs
            log(f"refs:{refs}")
            origin_key = f"origin/{conf_target['branch']}"
            if origin_key in refs:
                remote_hash = refs[origin_key].commit.hexsha
            log(f"local_hash:{local_hash} -> remote_hash:{remote_hash} ")
            if remote_hash == local_hash:
                log("无需push")
                return False
            else:
                log("需要push")
                log(f"{key} pushing")
                shell(f'git push --set-upstream origin {conf_target["branch"]}')
                log(f"{key} push success")
                time.sleep(0.2)
                return True

        def do_pull_request(has_push):
            if not get_dict_value(conf_options, 'pr'):
                return False
            # if not has_push:
            #     return False
            token = get_dict_value(conf_target_repo, 'token')
            repo_type = get_dict_value(conf_target_repo, 'type')

            if not repo_type or not token:
                log(f"{conf_target['repo']} 未配置token 或 type，无法提交PR")
                return False
            else:
                client = api_clients[repo_type](http, token)
                title = f"{key} sync merge request"
                body = f""
                log(f"准备提交pr, {conf_target['branch']} -> {conf_target_repo['branch']} , url:{conf_target_repo['url']}")
                client.create_pull_request(title, body, conf_target_repo['url'], conf_target['branch'],
                                           conf_target_repo['branch'])
                time.sleep(0.2)
                return True

        # 同步任务开始
        # 当前目录切换到目标项目
        os.chdir(repo_target.working_dir)
        # 先强制切换回主分支
        back_to_main_branch()
        # 创建同步分支，并checkout
        create_and_checkout(repo_target, conf_target['branch'])
        # 开始复制文件
        do_sync()
        # 提交代码
        do_commit()
        # push更新
        has_push = do_push()
        # 创建PR
        do_pull_request(has_push)

        # TODO 通知用户？

        # 切换回主分支
        back_to_main_branch()
        log(f"{key} 同步任务已完成")

    # 所有任务已完成
    # 当前目录切换回主目录
    os.chdir(root)
    log(f"同步结束")


def handle_remote(root, config, args):
    repo = git.Repo().init(root)
    url = args['<url>']
    if not url:
        origin = repo.create_remote("origin", url)
        log('关联远程地址成功:' + url)
    else:
        origin = repo.remotes["origin"]
    if origin:
        origin.push()
        log('push 成功')


def readonly_handler(func, path, execinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def read_status(root):
    file_path = f'{root}/status.json'
    if not os.path.exists(file_path):
        return {}
    fo = open(file_path, "r")
    config_str = fo.read()
    fo.close()
    if config_str is None:
        return {}
    try:
        return json.loads(config_str)
    except Exception as e:
        print(e)
        return {}


def save_status(root, status):
    # 创建配置文件
    file_path = f'{root}/status.json'
    # 写入配置文件
    config_str = json.dumps(status)
    fo = open(file_path, "w")
    fo.write(config_str)
    fo.close()
    return status


def save_ignore_file(root):
    ignore_file = f"{root}/.gitignore"
    ignore = '''
            .idea
            .vscode
            .git
            __pycache__
            '''
    save_file(ignore_file, ignore)


def get_root(args):
    root = args["--root"]
    return f"{os.getcwd()}/{root}"


if __name__ == '__main__':
    cli()
