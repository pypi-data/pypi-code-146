import os
import re
import shlex
import tempfile
import time
import subprocess
import sys
import charade
import signal
import pyutils.fsext as fsext
import pyutils.simplelogger as logger
import pyutils.shorthand as shd
import yaml
from typing import Union
from deprecated import deprecated
from threading import Thread, Event
from pathlib import Path


@deprecated(version='0.2.7', reason="Please use 'from pyutils.fsext import detect_encoding' instead.")
def detect_encoding(input):
    """
    猜测 bytes | str 的编码

    Args:
        input (str | bytes): 待猜测的内容
    """
    try:
        # check it in the charade list
        if isinstance(input, str):
            return charade.detect(input.encode())
        # detecting the string
        else:
            return charade.detect(input)
    # in case of error
    # encode with 'utf -8' encoding
    except UnicodeDecodeError:
        return charade.detect(input.encode('utf-8'))


######################
######################
#   执行脚本or模块    #
######################
######################


class ExecuteResult:
    def __init__(self):
        self.cmd_line = None
        self.code = 0
        self.out = None
        self.error = None
        self.exception = None
        self.out_str = None

    def __str__(self) -> str:
        return f'cmd_line : {str(self.cmd_line)}\ncode : {str(self.code)}\nout : {str(self.out_str)}\n error : {str(self.error)}'


class Executor:
    def __init__(self, verbose=True, exit_hook=None):
        """_summary_

        Args:
            verbose (bool, optional): 是否输出详细执行信息. Defaults to True.
            exit_hook (_type_, optional): 记录执行前的工作目录. Defaults to None.
        """
        self.verbose = verbose
        self.previous_cwd: str = None
        if not callable(exit_hook):
            exit_hook = None
        self.exit_hook = exit_hook

    def format_args(self, args):
        """统一转换命令参数

        Args:
            args (list | str | None): _description_

        Returns:
            str: _description_
        """
        if type(args) is list:
            return ' '.join(args)
        elif type(args) is str:
            return args
        elif args is not None:
            logger.error(f'Unsupported args type : {type(args)}')
        return ''

    def common_error_out(self, result, exit_code=-1):
        """
        输出错误信息的

        Args:
            result ([class ExecuteResult]): 收集的执行结果
            exit_code (number, optional): sys.exit() 参数. Defaults to -1
        """
        error_message = f'{result.error}\n{result.out_str}' if result.error != '' else result.out_str
        logger.error(f'\nCommand failed: {result.cmd_line}\n'
                     f'code: {result.code}\n'
                     f'message: {error_message}', True)
        if self.exit_hook is not None:
            self.exit_hook(exit_code)
        else:
            sys.exit(exit_code)

    def path_to_temp_dir(self):
        """
        获得（且创建）临时文件夹地址

        Returns:
            string: 临时文件夹地址
        """
        dir = os.path.join(os.getcwd(), '.temp')
        if not os.path.exists(dir):
            os.mkdir(dir)
        return dir

    def execute_with_tempfile(self, cmd, args, tempfile_ext, ignore_error=False, use_direct_stdout=False, exit_at_once=False, env=None, shell=True, work_dir: str = None, wrap_blank_with_double_quotes=False):
        """
        将待执行的命令（ cmd 和 args ）写入临时文件中，
        以后缀名的形式让 OS 决定用什么程序来执行。

        Args:
            cmd (str): 命令
            args (list or str): 参数列表
            tempfile_ext (str): 临时文件的后缀名
            ignore_error (bool, optional): 是否忽略报错. Defaults to False.
            use_direct_stdout (bool, optional): 是否将输出接到 sys.stdout . Defaults to False.
            exit_at_once (bool, optional): 是否在进程开启后直接返回. Defaults to False.
            env (str, optional): Popen env argument. Defaults to None.
            shell (bool, optional): Popen shell argument. Defaults to True.
        """
        self.__change_cwd(work_dir)
        tf = tempfile.mkstemp(suffix=tempfile_ext, prefix=None, dir=self.path_to_temp_dir(), text=True)
        cmd_line = f'{cmd} {self.format_args(args)}'
        with open(tf[1], 'w+') as f:
            f.write(cmd_line)
        result = self.execute_file(tf[1], None, ignore_error=ignore_error, use_direct_stdout=use_direct_stdout, exit_at_once=exit_at_once, env=env, shell=shell, wrap_blank_with_double_quotes=wrap_blank_with_double_quotes)
        os.close(tf[0])
        os.unlink(tf[1])
        self.__restore_cwd()
        return result

    def execute_by_git_bash(self, cmd, args, ignore_error=False, use_direct_stdout=False, exit_at_once=False, env=None, shell=True, work_dir: str = None, wrap_blank_with_double_quotes=False):
        """
        通过 git-bash 程序来运行该临时文件，
        这是为了解决 windows cmd 对某些特殊字符处理错误的问题。

        Args:
            cmd (str): 命令
            args (list or str): 参数列表
            ignore_error (bool, optional): 是否忽略报错. Defaults to False.
            use_direct_stdout (bool, optional): 是否将输出接到 sys.stdout . Defaults to False.
            exit_at_once (bool, optional): 是否在进程开启后直接返回. Defaults to False.
            env (str, optional): Popen env argument. Defaults to None.
            shell (bool, optional): Popen shell argument. Defaults to True.
        """
        return self.execute_with_tempfile(cmd, args, '.sh', ignore_error=ignore_error, use_direct_stdout=use_direct_stdout, exit_at_once=exit_at_once, env=env, shell=shell, work_dir=work_dir, wrap_blank_with_double_quotes=wrap_blank_with_double_quotes)

    def execute_by_cmd(self, cmd, args, ignore_error=False, use_direct_stdout=False, exit_at_once=False, env=None, shell=True, work_dir: str = None, wrap_blank_with_double_quotes=False):
        """
        通过 cmd 程序来运行该临时文件。

        Args:
            cmd (str): 命令
            args (list or str): 参数列表
            ignore_error (bool, optional): 是否忽略报错. Defaults to False.
            use_direct_stdout (bool, optional): 是否将输出接到 sys.stdout . Defaults to False.
            exit_at_once (bool, optional): 是否在进程开启后直接返回. Defaults to False.
            env (str, optional): Popen env argument. Defaults to None.
            shell (bool, optional): Popen shell argument. Defaults to True.
        """
        if not shd.is_win():
            logger.error('You are not running on Windows!')
        return self.execute_with_tempfile(cmd, args, '.bat', ignore_error=ignore_error, use_direct_stdout=use_direct_stdout, exit_at_once=exit_at_once, env=env, shell=shell, work_dir=work_dir, wrap_blank_with_double_quotes=wrap_blank_with_double_quotes)

    def execute_straight(self, cmd, args, ignore_error=False, use_direct_stdout=False, exit_at_once=False, env=None, shell=True, work_dir: str = None, wrap_blank_with_double_quotes=False, before_communicate_callback=None):
        """
        启动subprocess , 直接执行命令

        @cmd
            命令
        @args
            可以是 dict 参数列表也可以直接是 str 参数
        @ignore_error
            忽略遇到的错误继续执行，否则会遇到错误会调用 sys.exit(-1)
        @use_direct_stdout
            是否使用 sys.stdout 作为输出
        @exit_at_once
            是否直接返回，否则同步等待命令结束
        @env
            Popen env argument
        @shell
            Popen shell argument
        Args:
            wrap_blank_with_double_quotes (bool, optional): 将含有空白字符的内容用双引号包装。
            before_communicate_callback (function) : 在 process 的 communicate 调用前做一些外部处理。
        """
        # NOTE:on windows and shell set to True, any path with double slashes will cause Popen to fail ( maybe it is caused by the shell ). so we normpath the cmd.
        if shell:
            cmd = os.path.normpath(cmd)
        if wrap_blank_with_double_quotes:
            # NOTE: shell 为 False 的情况下如果包装了 cmd 在 windows 上会出现 ‘PermissionError: [WinError 5] 拒绝访问。’ 的问题。
            cmd = cmd if not shell or re.search(r'\s', cmd) is None or re.search(r'\"', cmd) is not None else f'"{cmd}"'
            if isinstance(args, list):
                args = [arg if re.search(r'\s', arg) is None or re.search(r'\"', arg) is not None else f'"{arg}"' for arg in args]
        joined_args = f'{cmd} {self.format_args(args)}'
        # ref to https://docs.python.org/2/library/subprocess.html#module-subprocess
        # if shell than passing string else passing sequence
        if shell:
            popen_args = joined_args
        else:
            popen_args = [cmd]
            if isinstance(args, str):
                popen_args.extend(shlex.split(args))
            elif isinstance(args, list):
                popen_args.extend(args)
            else:
                logger.error(f'Unsupported args type : {type(args)}')

        self.__change_cwd(work_dir)

        if self.verbose:
            via = 'Shell' if shell else 'Program'
            logger.info(f'=> Exec[{via}]: {joined_args}', True)
            if work_dir is not None:
                logger.info(f'=> WorkDir: {work_dir}', True)

        start_time = time.time()
        process = subprocess.Popen(popen_args, stdout=sys.stdout if use_direct_stdout else subprocess.PIPE,
                                   stderr=subprocess.PIPE, env=env, shell=shell)
        before_communicate_callback and before_communicate_callback(process)
        result = ExecuteResult()
        result.cmd_line = joined_args
        if exit_at_once:
            result.code = 0
        else:
            def stop_process(*args):
                logger.error(f'The shell process[{process.pid}] have been killed!')
                process.kill()
                sys.exit(-1)

            event = Event()
            signal.signal(signal.SIGINT, stop_process)
            signal.signal(signal.SIGTERM, stop_process)

            def run():
                result.out, result.error = process.communicate()
                result.out = "" if result.out is None else result.out.strip()
                error_encoding = fsext.detect_encoding(result.error)['encoding']
                # python3 str 默认编码为 utf-8
                result.error = "" if result.error is None else str(result.error.strip(), error_encoding if error_encoding is not None else 'utf-8')
                result.code = process.returncode
                out_encoding = fsext.detect_encoding(result.out)['encoding']
                result.out_str = result.out if isinstance(result.out, str) else str(result.out, out_encoding if out_encoding is not None else 'utf-8')
                event.set()
            # NOTE:executor popen communicate in another thread for receive kill command
            thread = Thread(target=run, daemon=True)
            thread.start()
            while not event.is_set():
                time.sleep(0)
        if self.verbose:
            logger.info(f'<= Finished: {os.path.basename(cmd)} {time.time() - start_time:.2f} seconds', True)

        if not ignore_error and result.code != 0:
            self.common_error_out(result)
        self.__restore_cwd()

        return result

    # https://blog.csdn.net/doots/article/details/86705182
    SET_ENV = r'''
    @echo off
    set %{key}%={value}

    if {user}==sys (
        setx /M {key} "{value}"
    ) else (
        setx {key} "{value}"
    )
    '''

    ADD_ENV = r'''
    @echo off

    if {user}==sys (
        set regPath= HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session" "Manager\Environment
    ) else (
        set regPath= HKEY_CURRENT_USER\Environment
    )

    set key={key}
    set value={value}
    :: 判断是否存在该路径
    reg query %regPath% /v %key% 1>nul 2>nul
    if %ERRORLEVEL%==0 (
        :: 取值
        For /f "tokens=3* delims= " %%i in ('Reg Query %regPath% /v %key% ') do (
            if "%%j"=="" (Set oldValue=%%i) else (Set oldValue=%%i %%j)
        )
    ) else Set oldValue=

    :: 备份注册表
    @REM reg export %regPath% %~dp0%~n0.reg
    :: 写入环境变量
    if "%oldValue%"=="" (
        reg add %regPath% /v %key% /t REG_EXPAND_SZ /d "%value%" /f
    ) else (
        if {override}==True (
            reg add %regPath% /v %key% /t REG_EXPAND_SZ /d "%value%" /f
        ) else (
            reg add %regPath% /v %key% /t REG_EXPAND_SZ /d "%oldValue%;%value%" /f
        )
    )
    '''

    def set_env_win(self, key: str, value: str, override=False):
        """
        windows 设置系统环境变量
        使用生成 bat 文件并执行的方式

        Args:
            key (str): 环境变量的键
            value (str): 环境变量的值
            override (bool, optional): 如果环境变量已存在，是否采用覆盖的方式. Defaults to False.
        """
        if not shd.is_win():
            logger.error('set_env_win failed! your OS is not windows.')
            return
        if value[-1] == '\\':
            value = value[:-1] + '/'
        # 运行设置环境变量命令
        bat_cmd = self.ADD_ENV.format(user='me', key=key, value=value, override=override)
        tf = tempfile.mkstemp(suffix='.bat', prefix=None, dir=self.path_to_temp_dir(), text=True)
        with open(tf[1], 'w+', encoding='utf-8') as f:
            f.write(bat_cmd)
        self.execute_file(tf[1], None)
        os.close(tf[0])
        os.unlink(tf[1])
        if override:
            logger.info(f'=> Set system environment {key}={value} finished.')
        else:
            logger.info(f'=> Append {key} to system environment key {value}.')

    def get_git_path(self):
        """
        先尝试从环境变量获取，如果失败则搜索本地路径以获取 git 安装路径

        Args:
            executor ([class Executor]): 执行 git-bash 的终端接口
        """
        git_path = os.getenv('GIT_PATH')

        if git_path is None:
            logger.info('=> Begin searching git path, it may take a long time...', False)
            # windows 先搜索默认路径
            if shd.is_win():
                git_path = fsext.search('/Program*/Git/git-bash.exe')
                if git_path is None:
                    git_path = fsext.search('/**/Git/git-bash.exe')
                if git_path is not None:
                    git_path = git_path.replace('git-bash.exe', '')
                    self.set_env_win('GIT_PATH', git_path, override=True)
            # TODO: 目前 macOS 搜索路径是写死的
            elif shd.is_macOS():
                git_path = fsext.search('/usr/bin/git')

        if git_path is None:
            # TODO: 这里用返回 None 替代终结程序
            logger.error('=> Cannot find git install path. ??')
            exit(-2)
        return git_path

    def get_unity_path(self, full_version_str=None):
        """搜索Unity可执行文件的路径，
        这里 unity 程序在不同平台和机器下需要做不同的处理，
        默认是通过 hub 安装的，如果不是的话可能找不到。

        Args:
            full_version_str (str): 指定 unity 版本全称，如果不指定则随便找一个版本
        Returns:
            str: 搜索结果，如果没找到则返回 None
        """
        def validation(unity_exec):
            if unity_exec is None:
                return False
            result = self.execute_straight(unity_exec, ['-version'], shell=False)
            if full_version_str is None:
                return True
            return result.out_str.startswith(full_version_str)
        unity_path_config_yaml = Path(os.path.join(Path.home(), 'unity_path_config.yaml'))

        def update_unity_path_config(unity_path):
            result = self.execute_straight(unity_path, ['-version'], shell=False)
            version = result.out_str.split(' ')[0]
            if not unity_path_config_yaml.exists():
                config_yaml = {version: unity_path}
                with open(unity_path_config_yaml, 'w') as f:
                    yaml.dump(config_yaml, f)
            else:
                with open(unity_path_config_yaml, 'r') as f:
                    config_yaml = yaml.safe_load(f)
                config_yaml[version] = unity_path
                with open(unity_path_config_yaml, 'w') as f:
                    yaml.dump(config_yaml, f)

        def load_unity_path_config():
            """尝试读取上一次 搜索 保存的配置 以 加快速度
            如果配置中找不到合适的 unity 路径则返回 None
            Returns:
                _type_: _description_
            """
            if not unity_path_config_yaml.exists():
                return
            with open(unity_path_config_yaml, 'r') as f:
                config_yaml = yaml.safe_load(f)
            if full_version_str is None:
                for key in config_yaml.keys():
                    return config_yaml[key]
            if full_version_str in config_yaml:
                return config_yaml[full_version_str]
        # 先尝试直接从环境变量中获取
        unity_exec_location = os.environ.get('UNITY_PATH')
        # NOTE:这里如果有多个路径只取最后一个
        if unity_exec_location is not None and ';' in unity_exec_location:
            unity_exec_location = unity_exec_location.split(';')[-1]
        if validation(unity_exec_location):
            return unity_exec_location

        # 再尝试从上次保存的配置中获取
        unity_exec_location = load_unity_path_config()

        # 再搜索本地
        if unity_exec_location is None:
            if shd.is_win():
                search_pattern = f'/Program*/**/{full_version_str}/Editor/Unity.exe' if full_version_str is not None else '/Program*/**/Editor/Unity.exe'
                unity_exec_location = fsext.search(search_pattern)
                if unity_exec_location is None:
                    search_pattern = f'/**/{full_version_str}/Editor/Unity.exe' if full_version_str is not None else '/**/Editor/Unity.exe'
                    unity_exec_location = fsext.search(search_pattern)
            else:
                search_pattern = f'/Applications/**/Editor/{full_version_str}/Unity.app/Contents/MacOS/Unity' if full_version_str is not None else '/Applications/**/Unity.app/Contents/MacOS/Unity'
                unity_exec_location = fsext.search(search_pattern)
            if unity_exec_location is not None:
                os.environ['UNITY_PATH'] = unity_exec_location
                update_unity_path_config(unity_exec_location)

        # 都不行就返回 None
        if not validation(unity_exec_location):
            return
        logger.info(f'find Unity executor path at {unity_exec_location}')
        return unity_exec_location

    def __ext2exe(self, ext):
        """
        按传入的后缀名称选择对应的可执行程序

        Args:
            ext (str): 待执行文件后缀
        """
        if ext.endswith('.sh'):
            if shd.is_win():
                # NOTE:windows调用sh
                p = os.path.join(self.get_git_path(), 'usr/bin/bash.exe')
                return f'"{p}"'
            else:
                return '/bin/bash'
        if ext.endswith('.py'):
            return sys.executable

    def __change_cwd(self, work_dir):
        """修改当前工作目录

        Args:
            work_dir (str): 指定的工作目录
        """
        if work_dir is None:
            return
        full_work_dir = os.path.realpath(work_dir)
        if self.previous_cwd is not None:
            if self.previous_cwd == full_work_dir:
                return
            logger.warning('try change_cwd twice in execution process is not valid.')
            return
        self.previous_cwd = os.getcwd()
        # should be restore
        os.chdir(full_work_dir)

    def __restore_cwd(self):
        """恢复到修改前的工作目录
        """
        if self.previous_cwd is not None:
            os.chdir(self.previous_cwd)
        self.previous_cwd = None

    def execute_file(self, script, args: Union[str, list] = None, work_dir: str = None, ignore_error=False, use_direct_stdout=False, exit_at_once=False, env=None, shell=True, wrap_blank_with_double_quotes=False):
        """
        执行脚本文件并传入参数

        Args:
            script (str): 脚本文件路径
            args (list or str): 参数
            work_dir (str, optional): 工作目录. Defaults to None.
            ignore_error (bool, optional): 是否忽略执行过程中的报错. Defaults to False.
            use_direct_stdout (bool, optional): 是否使用 sys.stdout 作为输出流. Defaults to False.
            exit_at_once (bool, optional): 是否异步执行. Defaults to False.
            env (dict, optional): 传入给 popen 的 env. Defaults to None.
            shell (bool, optional): 传入给 popen 的 shell. Defaults to True.
            wrap_blank_with_double_quotes (bool, optional): 将含有空白字符的内容用双引号包装
        Returns:
            [type]: [description]
        """
        self.__change_cwd(work_dir)
        split_result = os.path.splitext(script)
        result = None
        exe = self.__ext2exe(split_result[1])
        if exe is None:
            result = self.execute_straight(
                script, args, ignore_error, use_direct_stdout, exit_at_once, env, shell, wrap_blank_with_double_quotes=wrap_blank_with_double_quotes)
        else:
            if args is None:
                args = [script]
            elif isinstance(args, list):
                args = [script].extend(args)
            elif isinstance(args, str):
                # NOTE: 如果 args 是字符串形式的话不做特殊处理，直接拼接
                args = f'{script} {args}'
            result = self.execute_straight(
                exe, args, ignore_error, use_direct_stdout, exit_at_once, env, shell, wrap_blank_with_double_quotes=wrap_blank_with_double_quotes)

        self.__restore_cwd()
        return result

    @deprecated(version='0.2.9', reason="You should always use importlib and sys.modules for python module execution.")
    def execute_module(self, module, *module_parameters):
        module_name = module.__name__
        logger.info('=> Module: {}'.format(module_name), True)
        start_time = time.time()
        result = module.main(*module_parameters)
        logger.info('<= Finished: {0} {1:.2f} seconds '.format(module_name, time.time() - start_time), True)
        return result
