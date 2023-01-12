import codecs
import ctypes
import filecmp
import fnmatch
import glob
import os
import shutil
import base64
import charade

import pyutils.shorthand as shd
import pyutils.simplelogger as logger
########################
########################
#    文件系统扩展方法    #
########################
########################


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


def convert_encoding(file_path, target_encoding='utf-8'):
    """converting the target file encoding.

    Args:
        file_path (str): target file path
        target_encoding (str, optional): target encoding to convert. Defaults to 'utf-8'.
    """
    if not os.path.exists(file_path) or os.path.isdir(file_path):
        print(f"{file_path} isn't a valid path to specific file.")
        return
    try:
        with open(file_path, 'rb') as f_in:
            raw_content = f_in.read()
        detect_result = detect_encoding(raw_content)
        if detect_result['confidence'] < 0.9:
            logger.warning("detect_result confidence less than 0.9,"
                           f"You should confirm than transform encoding of the file {file_path} manually.")
            return
        if detect_result['encoding'] != target_encoding:
            logger.info(f'{file_path} processed with detect_result {detect_result}.')
            with codecs.open(file_path, 'r',
                             encoding=detect_result['encoding']) as f_in:
                content = f_in.read()
            with codecs.open(file_path, 'w', encoding=target_encoding) as f_out:
                f_out.write(content)
    except IOError as err:
        logger.error(f"I/O error: {err}")


def search(pattern: str, validator=None, params={}):
    """按指定路径模式搜索单路径，可以添加自定义验证函数来过滤匹配的路径

    Args:
        pattern (str): 路径匹配模式，在 windows 下会自动搜索所有盘符
        validator (function, optional): 自定义验证函数，回调参数为匹配的路径和 params. Defaults to None.
        params (dict, optional): 自定义验证函数的剩余回调参数. Defaults to {}.

    Returns:
        str | None: 搜索到的路径，未搜索到则返回 None
    """
    def glob_wrap(path):
        logger.info('=> Searching at {}'.format(path), False)
        result = glob.glob(path, recursive=True)
        if len(result) > 0:
            for find_path in result:
                if validator is None or validator(find_path, **params):
                    return find_path
    if shd.is_win():
        volumes = get_all_volumes_win()
        for volume in volumes:
            search_path = os.path.join(volume, pattern)
            result = glob_wrap(search_path)
            if result is not None:
                return result
    else:
        return glob_wrap(pattern)


def copy_files(target_path, src_file_list, logs=False):
    """复制并覆盖目标路径下所有同名内容，如果 src_file 是文件夹，使用 shutil.copytree 复制，否则使用 shutil.copy2

    Args:
        target_path (str): 目标路径。
        src_file_list (list): 被复制的文件列表。
        logs (bool) : 是否输出日志。
    """
    for src_file in src_file_list:
        if os.path.exists(src_file):
            src_basename = os.path.basename(src_file)
            deploy_file_path = os.path.join(target_path, src_basename)
            deploy_dir = os.path.dirname(deploy_file_path)
            if not os.path.exists(deploy_dir):
                os.makedirs(deploy_dir)
                if logs:
                    logger.info('Makedirs => {}'.format(deploy_dir))
            if os.path.isfile(deploy_file_path):
                os.remove(deploy_file_path)
                if logs:
                    logger.info('Removed => {}'.format(deploy_file_path))
            if os.path.isfile(src_file):
                shutil.copy2(src_file, deploy_file_path)
            else:
                if os.path.exists(deploy_file_path):
                    shutil.rmtree(deploy_file_path)
                    if logs:
                        logger.info('Removed => {}'.format(deploy_file_path))
                shutil.copytree(src_file, deploy_file_path)
            if logs:
                logger.info('Copy file from {} to => {}'.format(src_file, deploy_file_path))


def read_file(file, decode='utf-8'):
    if os.path.isfile(file):
        content = ''
        with open(file, 'rb') as fo:
            content = fo.read()
        content = content.decode(decode)
        return content
    else:
        logger.error('{} is not found or is not a file'.format(file))


def get_all_volumes_win():
    if shd.is_win():
        lp_buffer = ctypes.create_string_buffer(78)
        ctypes.windll.kernel32.GetLogicalDriveStringsA(
            ctypes.sizeof(lp_buffer), lp_buffer)
        all_volumes = lp_buffer.raw.split(b'\x00')
        legal_volumes = []
        for vol in all_volumes:
            s = str(vol, encoding='utf-8')
            if os.path.isdir(s):
                legal_volumes.append(s)
        return legal_volumes


def get_dirs(work_dir, recursive=False, ignore_patterns=None):
    """获取指定路径下所有文件夹

    Args:
        work_dir (str): _description_
        recursive (bool, optional): _description_. Defaults to False.
        ignore_patterns (list[str], optional): 文件忽略规则. Defaults to True.

    Returns:
        list[str]: 文件夹列表
    """
    def match_ignore_pattern(dir):
        if ignore_patterns is not None:
            valid = True
            for ignore_pattern in ignore_patterns:
                match_result = fnmatch.fnmatch(dir, ignore_pattern)
                valid = valid and not match_result
                if not valid:
                    return True
        return False
    result = []
    if os.path.isdir(work_dir):
        list_dirs = [os.path.join(work_dir, name) for name in os.listdir(work_dir) if os.path.isdir(os.path.join(work_dir, name))]
        list_dirs = [dir for dir in list_dirs if not match_ignore_pattern(dir)]
        result.extend(list_dirs)
        if recursive:
            for dir in list_dirs:
                result.extend(get_dirs(dir, recursive, ignore_patterns))
    return result


def get_files(work_dir, include_patterns=None, ignore_patterns=None, follow_links=False, recursive=True, apply_ignore_when_conflict=True):
    """
    NOTE:这里的 patterns 用的是 UNIX 通配符，而非语言正则表达式
    TODO: replace with glob.glob
    Args:
        ignore_patterns (list[str], optional): 文件忽略规则. Defaults to True.

    """
    if os.path.isfile(work_dir):
        result = [work_dir]
    else:
        result = []
        walk_result = os.walk(work_dir, followlinks=follow_links)
        if not recursive:
            try:
                walk_result = [next(walk_result)]
            except Exception:
                walk_result = None
        if walk_result is not None:
            for dirpath, _, filenames in walk_result:
                for filename in filenames:
                    full_path = os.path.join(dirpath, filename)
                    valid = True
                    if ignore_patterns is not None:
                        for ignore_pattern in ignore_patterns:
                            match_result = fnmatch.fnmatch(full_path, ignore_pattern)
                            valid = valid and not match_result
                            if not valid:
                                break
                    if include_patterns is not None:
                        for include_pattern in include_patterns:
                            match_result = fnmatch.fnmatch(full_path, include_pattern)
                            if apply_ignore_when_conflict:
                                valid = match_result and valid
                            else:
                                valid = match_result or valid
                            if valid:
                                break
                    if valid:
                        result.append(full_path)
    return sorted(result)


def to_base64(src, tar=None):
    """将 src 路径指定文件转为 base64 并返回，如果提供了 tar 目标文件路径，则将返回值同时存储在 tar 目标文件

    Args:
        src (str): 源文件路径
        tar (str): 目标文件路径
    """
    if not os.path.isfile(src):
        logger.warning(f'{src} is not a file path.')
        return ''
    filename = os.path.split(src)[1]
    ext = os.path.splitext(src)[1][1:]
    with open(src, 'rb') as f_img:
        base64_out = base64.b64encode(f_img.read())
    content = f"{filename} = [img]:data:image/{ext};base64,{base64_out.decode('utf-8')}\n"
    if tar is not None:
        if os.path.exists(tar):
            logger.warning(f'{tar} is not a file or target file exist.')
            return content
        with open(tar, 'w+', encoding='utf-8') as f:
            f.write(content)
    return content


def sync_folder(src_parent_path, dst_path,
                files_to_sync: list,
                remove_diff=False,
                compare_content=False,
                remove_original=False,
                verbose=False):
    """同步两个目录内的内容
    如果同步过程中有任何修改返回 True 否则返回 False

    Args:
        src_path (_type_): 待同步的目录
        dst_path (_type_): 同步的目标目录
        files_to_sync (_type_, optional): _description_. Defaults to None.
        remove_diff (bool, optional): 删除本地不存在而同步目标内存在的文件，并清理同步目标的空目录
        compare_content (bool, optional): 是否使用 filecmp.cmp 比较，否则仅比较 mtime. Defaults to False.
        remove_original (bool, optional): 是否在同步后删除源文件. Defaults to False.
    """
    def path_is_parent(parent_path, child_path):
        # Smooth out relative path names, note: if you are concerned about symbolic links, you should use os.path.realpath too
        parent_path = os.path.abspath(parent_path)
        child_path = os.path.abspath(child_path)

        # Compare the common path of the parent and child path with the common path of just the parent path. Using the commonpath method on just the parent path will regularise the path name in the same way as the comparison that deals with both paths, removing any trailing path separator
        return os.path.commonpath([parent_path]) == os.path.commonpath([parent_path, child_path])

    def make_parent_dir_if_absent(path):
        """如果父级目录不存在则构造父级目录

        Args:
            path (_type_): _description_
        """
        dst_dir = os.path.dirname(path)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
            if verbose:
                logger.info('Makedirs => {}'.format(dst_dir))

    def remove_empty_dirs(folder):
        if os.path.isdir(folder):
            for file in os.listdir(folder):
                sub_folder = os.path.join(folder, file)
                if os.path.isdir(sub_folder):
                    remove_empty_dirs(sub_folder)
            # can't remove symlink folder
            if len(os.listdir(folder)) == 0 and not os.path.islink(folder):
                os.rmdir(folder)

    if src_parent_path is None or not os.path.isdir(src_parent_path) or dst_path is None or files_to_sync is None:
        return False

    src_parent_path = os.path.realpath(src_parent_path)
    dst_path = os.path.realpath(dst_path)
    previous_cwd = os.getcwd()
    os.chdir(src_parent_path)
    # 清理相对目录不对的文件 （此处默认了不区分大小写的文件系统）
    abs_src_pathes = [os.path.realpath(file) for file in files_to_sync if os.path.realpath(file).lower().startswith(src_parent_path.lower())]
    os.chdir(previous_cwd)
    # 清理不存在的文件
    abs_src_pathes = [path for path in abs_src_pathes if os.path.exists(path)]
    # 清理递归的目录
    abs_dirs = [path for path in abs_src_pathes if os.path.isdir(path)]
    abs_src_pathes = [path for path in abs_src_pathes if not os.path.isdir(path) or not any([path_is_parent(other_dir, path) for other_dir in abs_dirs if other_dir != path])]
    if len(abs_src_pathes) == 0:
        return False

    sync_result = False
    if remove_diff:
        dst_files = get_files(dst_path)
        for dst_file in dst_files:
            rel_dst_path = os.path.relpath(dst_file, dst_path)
            reflected_src_path = os.path.join(src_parent_path, rel_dst_path)
            if not os.path.isfile(reflected_src_path):
                # dst_file 不会是目录
                sync_result = True
                os.remove(dst_file)

        # 清理空目录，因为刚才删除了一波文件，再清空文件目录即可得到与源目标同步的目录结构
        remove_empty_dirs(dst_path)

    for abs_src_path in abs_src_pathes:
        rel_dst_path = os.path.relpath(abs_src_path, src_parent_path)
        dst_file = os.path.join(dst_path, rel_dst_path)
        if os.path.isfile(abs_src_path):
            need_sync = not os.path.isfile(dst_file) or (not filecmp.cmp(abs_src_path, dst_file) if compare_content else os.path.getmtime(abs_src_path) - os.path.getmtime(dst_file) > 1)
            # for files
            if need_sync:
                sync_result = True
                # 先检查父级目录是否存在
                make_parent_dir_if_absent(dst_file)
                shutil.copy2(abs_src_path, dst_file)
            if remove_original:
                sync_result = True
                os.remove(abs_src_path)
        else:
            # for dirs
            make_parent_dir_if_absent(dst_file)
            sync_result = True
            shutil.copytree(abs_src_path, dst_file)
            if remove_original:
                shutil.rmtree(abs_src_path)
    return sync_result
