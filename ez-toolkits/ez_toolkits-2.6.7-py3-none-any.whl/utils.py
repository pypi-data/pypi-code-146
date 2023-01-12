import json
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from multiprocessing import Pool
from os import remove
from os.path import basename
from pathlib import Path
from shutil import rmtree
from subprocess import run
from time import mktime, strptime

from loguru import logger

# ----------------------------------------------------------------------

'''
函数内部变量, 变量名一律以 _ (下划线) 开头, 避免改变上层相同名称的变量

except 一律输出 Exception, 即:

    try:
        ...
    except Exception as e:
        logger.exception(e)
        return None
'''

# ----------------------------------------------------------------------

def vTrue(variable, type, true_list=None, false_list=None):
    '''
    检查变量类型, 以及变量是否为真

    常见变量类型:

        Boolean     bool            False
        Numbers     int/float       0/0.0
        String      str             ''
        List        list/tuple/set  []/()/{}
        Dictionary  dict            {}

    函数使用 callable(func) 判断
    '''
    try:
        if isinstance(variable, type):
            if true_list != None and false_list == None and (
                isinstance(true_list, list) or
                isinstance(true_list, tuple) or
                isinstance(true_list, set) or
                isinstance(true_list, str)
            ):
                return True if variable in true_list else False
            elif true_list == None and false_list != None and (
                isinstance(false_list, list) or
                isinstance(false_list, tuple) or
                isinstance(false_list, set) or
                isinstance(false_list, str)
            ):
                return True if variable not in false_list else False
            elif true_list != None and false_list != None and (
                isinstance(true_list, list) or
                isinstance(true_list, tuple) or
                isinstance(true_list, set) or
                isinstance(true_list, str)
            ) and (
                isinstance(false_list, list) or
                isinstance(false_list, tuple) or
                isinstance(false_list, set) or
                isinstance(false_list, str)
            ):
                return True if (variable in true_list) and (variable not in false_list) else False
            else:
                return True if variable not in [False, None, 0, 0.0, '', (), [], {*()}, {*[]}, {*{}}, {}] else False
        else:
            return False
    except:
        return False

# ----------------------------------------------------------------------

def nums_mam(numbers=None, number_type=None, **kwargs):
    ''' 返回一组数字中的 最大值, 平均值, 最小值 '''
    _num_max, _num_avg, _num_min = None, None, None
    try:
        if vTrue(numbers, list):
            _numbers = deepcopy(numbers)
            match True:
                case True if number_type == 'float':
                    _numbers = [float(i) for i in numbers]
                case True if number_type == 'int':
                    _numbers = [int(i) for i in numbers]
            _num_max = max(_numbers)
            _num_avg = sum(_numbers) / len(_numbers)
            _num_min = min(_numbers)
        return _num_max, _num_avg, _num_min
    except Exception as e:
        logger.exception(e)
        return None, None, None

def division(dividend, divisor, *args, **kwargs):
    ''' 除法 '''
    return dividend / divisor

def divisor_1000(dividend, *args, **kwargs):
    return dividend / 1000

def divisor_1024(dividend, *args, **kwargs):
    return dividend / 1024

def divisor_square_1000(dividend, *args, **kwargs):
    return dividend / (1000 * 1000)

def divisor_square_1024(dividend, *args, **kwargs):
    return dividend / (1024 * 1024)

# ----------------------------------------------------------------------

def stat(target=None, type=None, **kwargs):
    ''' 检查目标类型 '''
    try:
        _stat = Path(target)
        match True:
            case True if _stat.exists() == False:
                return False
            case True if type == 'absolute' and _stat.is_absolute() == True:
                return True
            case True if type == 'block_device' and _stat.is_block_device() == True:
                return True
            case True if type == 'dir' and _stat.is_dir() == True:
                return True
            case True if type == 'fifo' and _stat.is_fifo() == True:
                return True
            case True if type == 'file' and _stat.is_file() == True:
                return True
            case True if type == 'mount' and _stat.is_mount() == True:
                return True
            case True if type == 'relative_to' and _stat.is_relative_to() == True:
                return True
            case True if type == 'reserved' and _stat.is_reserved() == True:
                return True
            case True if type == 'socket' and _stat.is_socket() == True:
                return True
            case True if type == 'symlink' and _stat.is_symlink() == True:
                return True
            case _:
                return False
    except Exception as e:
        logger.exception(e)
        return False

# ----------------------------------------------------------------------

def list_sort(data=None, deduplication=None, **kwargs):
    '''
    列表排序
    - https://stackoverflow.com/a/4183538
    - https://blog.csdn.net/u013541325/article/details/117530957
    示例: list_sort(['1.2.3.4', '2.3.4.5'], key=inet_aton)
    '''
    try:

        # if vTrue(data, list) and key != None and key != '':
        if vTrue(data, list):

            # from ipaddress import ip_address
            # _ips = [str(i) for i in sorted(ip_address(ip.strip()) for ip in ips)]
            # 注意: list.sort() 是直接改变 list, 不会返回 list

            # 拷贝数据, 去重, 排序, 返回
            _data = deepcopy(data)
            if deduplication == True:
                _data = list(set(_data))
            _data.sort(**kwargs)
            return _data

        else:

            return None

    except Exception as e:
        logger.exception(e)
        return None

def list_dict_sorted_by_key(data=None, key=None, **kwargs):
    '''
    列表字典排序
    https://stackoverflow.com/a/73050
    '''
    try:
        if vTrue(data, list) and key != None and key != '':
            _data = deepcopy(data)
            return sorted(_data, key=lambda x: x[key], **kwargs)
        else:
            return None
    except Exception as e:
        logger.exception(e)
        return None

def list_step_number(data, number=None, offset=None):

    if vTrue(data, list):

        if number == None:
            number = 10

        if offset == None:
            offset = 1

        _data_length = len(data)

        if _data_length % number == 0:
            return int(_data_length / number)
        else:
            return int(_data_length / number + offset)

    else:

        return None

def list_range_by_step(data=None, number=None):
    '''
    列表按照 步长 生成新的列表
    '''
    try:

        match False:
            case False if vTrue(data, list) == False:
                print('data type error')
                return None
            case False if vTrue(number, int) == False:
                print('number type error')
                return None

        _original_list = deepcopy(data)

        _target_list = []

        _original_list_length = len(_original_list)

        if _original_list_length == 0 or _original_list_length <= number:

            return _target_list.append(_original_list)

        else:

            _index_list = list(range(0, _original_list_length, number))

            if _index_list[-1] != _original_list_length:
                _index_list.append(_original_list_length)

            for _index in _index_list:
                if _index_list[-1] != _index:
                    _target_list.append(deepcopy(_original_list[_index:_index + number]))

            return _target_list

    except:
        return None

def list_print_by_step(data=None, number=None, separator=None):
    '''
    列表按照 步长 和 分隔符 有规律的输出
    '''
    try:

        match False:
            case False if vTrue(data, list) == False:
                print('data type error')
                return
            case False if vTrue(number, int) == False:
                print('number type error')
                return
            case False if vTrue(separator, str) == False:
                print('separator type error')
                return

        _data_list = list_range_by_step(data, number)

        for _item in _data_list:
            print(*_item, sep=separator)

    except Exception as e:
        print(e)

def list_remove_list(original, remove):
    _original = deepcopy(original)
    _remove = deepcopy(remove)
    return [i for i in _original if i not in _remove]

# ----------------------------------------------------------------------

def dict_nested_update(data=None, key=None, value=None, **kwargs):
    '''
    dictionary nested update
    https://stackoverflow.com/a/58885744
    '''
    try:
        if vTrue(data, dict):
            for _k, _v in data.items():
                # callable() 判断是非为 function
                if (key != None and key == _k) or (callable(key) == True and key() == _k):
                    if callable(value) == True:
                        data[_k] = value()
                    else:
                        data[_k] = value
                elif isinstance(_v, dict) == True:
                    dict_nested_update(_v, key, value)
                elif isinstance(_v, list) == True:
                    for _o in _v:
                        if isinstance(_o, dict):
                            dict_nested_update(_o, key, value)
                else:
                    pass
        else:
            pass
    except Exception as e:
        logger.exception(e)

# ----------------------------------------------------------------------

def filename(file, split=None, **kwargs):
    '''
    获取文件名称
    https://stackoverflow.com/questions/678236/how-do-i-get-the-filename-without-the-extension-from-a-path-in-python
    https://stackoverflow.com/questions/4152963/get-name-of-current-script-in-python
    '''
    try:
        if split == None:
            split = '.'
        if vTrue(file, str) and file[-1] != '/' and vTrue(split, str):
            _basename = str(basename(file))
            _index_of_dot = _basename.index(split)
            return _basename[:_index_of_dot]
        else:
            return None
    except Exception as e:
        logger.exception(e)
        return None

# ----------------------------------------------------------------------

def work_dir(*args, **kwargs):
    ''' 获取当前目录名称 '''
    try:
        return str(Path().resolve())
    except Exception as e:
        logger.exception(e)
        return None

def parent_dir(path=None, **kwargs):
    ''' 获取父目录名称 '''
    try:
        return str(Path(path).parent.resolve()) if vTrue(path, str) else None
    except Exception as e:
        logger.exception(e)
        return None

# ----------------------------------------------------------------------

def retry(times=None, func=None, *args, **kwargs):
    '''
    重试 
    函数传递参数: https://stackoverflow.com/a/803632
    callable() 判断类型是非为函数: https://stackoverflow.com/a/624939
    '''
    try:
        if type(times) == int and times >= 0 and callable(func):
            _num = 0
            while True:
                # 重试次数判断 (0 表示无限次数, 这里条件使用 > 0, 表示有限次数)
                if times > 0:
                    _num += 1
                    if _num > times:
                        return
                # 执行函数
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.exception(e)
                    logger.success('retrying ...')
                    continue
                # break
        else:
            return None
    except Exception as e:
        logger.exception(e)
        return None

# ----------------------------------------------------------------------


'''
日期时间有两种: UTC datetime (UTC时区日期时间) 和 Local datetime (当前时区日期时间)

Unix Timestamp 仅为 UTC datetime 的值

但是, Local datetime 可以直接转换为 Unix Timestamp, UTC datetime 需要先转换到 UTC TimeZone 再转换为 Unix Timestamp

相反, Unix Timestamp 可以直接转换为 UTC datetime, 要获得 Local datetime, 需要再将 UTC datetime 转换为 Local datetime

    https://stackoverflow.com/a/13287083
    https://stackoverflow.com/a/466376
    https://stackoverflow.com/a/7999977
    https://stackoverflow.com/a/3682808
    https://stackoverflow.com/a/63920772
    https://www.geeksforgeeks.org/how-to-remove-timezone-information-from-datetime-object-in-python/

pytz all timezones

    https://stackoverflow.com/a/13867319
    https://stackoverflow.com/a/15692958

    import pytz
    pytz.all_timezones
    pytz.common_timezones
    pytz.timezone('US/Eastern')

timezone

    https://stackoverflow.com/a/39079819
    https://stackoverflow.com/a/1681600
    https://stackoverflow.com/a/4771733
    https://stackoverflow.com/a/63920772
    https://toutiao.io/posts/sin4x0/preview

其它:

    dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

    (dt.replace(tzinfo=timezone.utc).astimezone(tz=None)).strftime(format)
    datetime.fromisoformat((dt.replace(tzinfo=timezone.utc).astimezone(tz=None)).strftime(format))
    string_to_datetime((dt.replace(tzinfo=timezone.utc).astimezone(tz=None)).strftime(format), format)

    datetime.fromisoformat(time.strftime(format, time.gmtime(dt)))
'''

def local_timezone(*args, **kwargs):
    ''' 获取当前时区 '''
    return datetime.now(timezone.utc).astimezone().tzinfo

def datetime_now(*args, **kwargs):
    ''' 获取日期和时间 '''
    _utc = kwargs.pop("utc", False)
    try:
        return datetime.utcnow(*args, **kwargs) if _utc == True else datetime.now(*args, **kwargs)
    except Exception as e:
        logger.exception(e)
        return None

def datetime_offset(date_time=None, *args, **kwargs):
    ''' 获取 向前或向后特定日期时间 的日期和时间 '''
    _utc = kwargs.pop("utc", False)
    try:
        if isinstance(date_time, datetime) == True:
            return date_time + timedelta(*args, **kwargs)
        else:
            return datetime.utcnow() + timedelta(*args, **kwargs) if _utc == True else datetime.now() + timedelta(*args, **kwargs)
    except Exception as e:
        logger.exception(e)
        return None

def datetime_to_string(date_time=None, format='%Y-%m-%d %H:%M:%S', **kwargs):
    ''' 日期时间格式 转换为 字符串格式 '''
    try:
        return datetime.strftime(date_time, format) if isinstance(date_time, datetime) == True else None
    except Exception as e:
        logger.exception(e)
        return None

def datetime_to_timestamp(date_time=None, utc=False, **kwargs):
    '''
    Datatime 转换为 Unix Timestamp
    Local datetime 可以直接转换为 Unix Timestamp
    UTC datetime 需要先替换 timezone 再转换为 Unix Timestamp
    '''
    try:
        if isinstance(date_time, datetime) == True:
            return int(date_time.replace(tzinfo=timezone.utc).timestamp()) if utc == True else int(date_time.timestamp())
        else:
            return None
    except Exception as e:
        logger.exception(e)
        return None

def datetime_local_to_timezone(date_time=None, tz=timezone.utc, **kwargs):
    '''
    Local datetime to TimeZone datetime (默认转换为 UTC datetime)
    replace(tzinfo=None) 移除结尾的时区信息
    '''
    try:
        return (datetime.fromtimestamp(date_time.timestamp(), tz=tz)).replace(tzinfo=None) if isinstance(date_time, datetime) == True else None
    except Exception as e:
        logger.exception(e)
        return None

def datetime_utc_to_timezone(date_time=None, tz=datetime.now(timezone.utc).astimezone().tzinfo, **kwargs):
    '''
    UTC datetime to TimeZone datetime (默认转换为 Local datetime)
    replace(tzinfo=None) 移除结尾的时区信息
    '''
    try:
        return date_time.replace(tzinfo=timezone.utc).astimezone(tz).replace(tzinfo=None) if isinstance(date_time, datetime) == True else None
    except Exception as e:
        logger.exception(e)
        return None

def timestamp_to_datetime(timestamp=None, tz=timezone.utc, **kwargs):
    ''' Unix Timestamp 转换为 Datatime '''
    try:
        return (datetime.fromtimestamp(timestamp, tz=tz)).replace(tzinfo=None) if vTrue(timestamp, int) else None
    except Exception as e:
        logger.exception(e)
        return None

def string_to_datetime(date_time=None, format='%Y-%m-%d %H:%M:%S', **kwargs):
    try:
        return datetime.strptime(date_time, format) if vTrue(date_time, str) else None
    except Exception as e:
        logger.exception(e)
        return None

def string_to_timestamp(date_time=None, format='%Y-%m-%d %H:%M:%S', **kwargs):
    try:
        return int(mktime(strptime(date_time, format))) if vTrue(date_time, str) else None
    except Exception as e:
        logger.exception(e)
        return None

# ----------------------------------------------------------------------


'''
run_cmd = bash('echo ok', universal_newlines=True, stdout=PIPE)

if run_cmd != None:
    returncode = run_cmd.returncode
    outputs = run_cmd.stdout.splitlines()
    print(returncode, type(returncode))
    print(outputs, type(outputs))

# echo 'echo ok' > /tmp/ok.sh
run_script = bash('/tmp/ok.sh', file=True, universal_newlines=True, stdout=PIPE)

if run_script != None:
    returncode = run_script.returncode
    outputs = run_script.stdout.splitlines()
    print(returncode, type(returncode))
    print(outputs, type(outputs))
'''

def bash(cmd=None, isfile=False, sh='/bin/bash', **kwargs):
    ''' run bash command or script '''
    try:
        match True:
            case True if not stat(sh, 'file'):
                return None
            case True if vTrue(sh, str) and vTrue(cmd, str):
                if isfile == True:
                    return run([sh, cmd], **kwargs)
                else:
                    return run([sh, "-c", cmd], **kwargs)
            case _:
                return None
    except Exception as e:
        logger.exception(e)
        return None

# ----------------------------------------------------------------------

def json_file_parser(file):
    try:
        if stat(file, 'file'):
            with open(file) as json_raw:
                json_dict = json.load(json_raw)
            return json_dict
        else:
            logger.error(f"No such file: {file}")
            return None
    except Exception as e:
        logger.exception(e)
        return None


"""
json_raw = '''
{
    "markdown.preview.fontSize": 14,
    "editor.minimap.enabled": false,
    "workbench.iconTheme": "vscode-icons",
    "http.proxy": "http://127.0.0.1:1087"

}
'''

print(json_sort(json_raw))

{
    "editor.minimap.enabled": false,
    "http.proxy": "http://127.0.0.1:1087",
    "markdown.preview.fontSize": 14,
    "workbench.iconTheme": "vscode-icons"
}
"""
def json_sort(string=None, **kwargs):
    try:
        return json.dumps(json.loads(string), indent=4, sort_keys=True, **kwargs) if vTrue(string, str) else None
    except Exception as e:
        logger.exception(e)
        return None

# ----------------------------------------------------------------------

def delete_files(files=None, **kwargs):
    ''' delete file '''
    try:

        if vTrue(files, str) and stat(files, 'file'):

            remove(files)
            logger.success('deleted file: {}'.format(files))
            return True

        elif vTrue(files, list):

            for _file in files:

                if vTrue(_file, str) and stat(_file, 'file'):
                    try:
                        remove(_file)
                        logger.success('deleted file: {}'.format(_file))
                    except Exception as e:
                        logger.error('error file: {} {}'.format(_file, e))
                else:
                    logger.error('error file: {}'.format(_file))

            return True

        else:

            logger.error('error file: {}'.format(files))
            return False

    except Exception as e:
        logger.error('error file: {} {}'.format(files, e))
        return False

def delete_dirs(dirs=None, **kwargs):
    '''
    delete directory

    https://docs.python.org/3/library/os.html#os.rmdir

        os.rmdir(path, *, dir_fd=None)

    Remove (delete) the directory path.

    If the directory does not exist or is not empty, an FileNotFoundError or an OSError is raised respectively.

    In order to remove whole directory trees, shutil.rmtree() can be used.

    https://docs.python.org/3/library/shutil.html#shutil.rmtree

        shutil.rmtree(path, ignore_errors=False, onerror=None)

    Delete an entire directory tree; path must point to a directory (but not a symbolic link to a directory).

    If ignore_errors is true, errors resulting from failed removals will be ignored;

    if false or omitted, such errors are handled by calling a handler specified by onerror or, if that is omitted, they raise an exception.
    '''
    try:

        if vTrue(dirs, str) and stat(dirs, 'dir'):

            rmtree(dirs)
            logger.success('deleted directory: {}'.format(dirs))
            return True

        elif vTrue(dirs, list):

            for _dir in dirs:

                if vTrue(_dir, str) and stat(_dir, 'dir'):
                    try:
                        rmtree(_dir)
                        logger.success('deleted directory: {}'.format(_dir))
                    except Exception as e:
                        logger.error('error directory: {} {}'.format(_dir, e))
                else:
                    logger.error('error directory: {}'.format(_dir))

            return True

        else:

            logger.error('error directory: {}'.format(dirs))
            return False

    except Exception as e:
        logger.error('error directory: {} {}'.format(dirs, e))
        return False

# ----------------------------------------------------------------------

def pool_process(process_func, process_data, process_num=None, *args, **kwargs):

    if callable(process_func) == False:
        logger.error('process function error')
        return False

    if vTrue(process_data, list) == False:
        logger.error('process data error')
        return False

    if process_num == None:
        process_num = 1

    try:
        if vTrue(process_num, int):
            with Pool(process_num, *args, **kwargs) as p:
                return p.map(process_func, process_data)
        else:
            return False
    except Exception as e:
        logger.error(e)
        return False
