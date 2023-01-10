# -*- coding: utf-8 -*-
import os
import sys
import runcmd

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import shutil
import sys
import ruamel.yaml
from git import Repo
import logging
import re
from urllib.parse import urlparse
from prettytable import PrettyTable, ALL


# yaml 数据模型
class YamlModuleModel:
    module = ''
    pod = ''
    version = ''
    git = ''
    branch = ''
    tag = ''
    path = ''
    new_tag = ''
    configurations = ''
    inhibit_warnings = False

    def __init__(self, module, pod, version, git, branch, tag, path, newtag, configurations, inhibit_warnings):
        """
        :param module:
        :param pod:
        :param version:
        :param git:
        :param branch:
        :param tag:
        :param path:
        :param newtag:
        :param configurations:
        :param inhibit_warnings:
        """
        self.module = module
        self.pod = pod
        self.git = git
        self.branch = branch
        self.tag = tag
        self.path = path
        self.new_tag = newtag
        self.configurations = configurations
        self.inhibit_warnings = inhibit_warnings


# 输出合并结果，如果result = 1 表示成功，result = 0 表示失败
class YamlBranchModel:
    module = ''
    pod = ''
    result = 0
    pod = ''

    def __init__(self, module, res, pod=''):
        """
        :param module: 模块名字
        :param res: 结果 0 表示失败 1 表示成功
        """
        self.module = module
        self.result = res
        self.pod = pod


# 文件状态，如果result = 1 表示成功，result = 0 表示失败 -1 表示其他异常
class ModuleStatusModel:
    module = ''
    pod = ''
    result = 0
    pod = ''
    branch = ''
    msg = ''

    def __init__(self, module, pod, res, branch, msg=''):
        """
        :param module: 模块名字
        :param pod: pod名字
        :param res: 结果 0 表示失败 1 表示成功 -1 表示其他异常
        :param branch: 分支
        :param msg: 错误信息
        """
        self.module = module
        self.result = res
        self.pod = pod
        self.msg = msg
        self.branch = branch


# 读取yaml文件数据
def yaml_data(yaml_path):
    """
    :param yaml_path: ymal路径
    :return: 返回yaml数据
    """
    with open(yaml_path, 'r') as y:
        yaml = ruamel.yaml.YAML()
        temp_yaml = yaml.load(y.read())
        return temp_yaml


# 写入文件
def update_yaml(yaml_path, data):
    """
    :param yaml_path: yaml路径
    :param data: yaml数据
    :return: 无返回值
    """
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml = ruamel.yaml.YAML()
        yaml.dump(data, f)


# 加载yml文件
def load_yaml(data):
    """
    :param data: 读取yaml数据
    :return: 返回转换之后的模型
    """
    convertDepList = []
    for i in range(0, len(data)):
        cur_dep = data[i]
        module = YamlModuleModel(module=cur_dep.get("module", None),
                                 pod=cur_dep["pod"],
                                 version=cur_dep.get("version", None),
                                 git=cur_dep.get("git", None),
                                 branch=cur_dep.get("branch", None),
                                 tag=cur_dep.get("tag", None),
                                 path=cur_dep.get("path", None),
                                 newtag=cur_dep.get("newtag", None),
                                 configurations=cur_dep.get("configurations", None),
                                 inhibit_warnings=cur_dep.get("inhibit_warnings", False)
                                 )
        convertDepList.append(module)

    return convertDepList


# 清空文件夹及目录
def del_file(path_data):
    """
    :param path_data: 文件路径
    :return: 无返回值
    """
    # os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
    shutil.rmtree(path_data)


# 清空或者创建一个新的目录
def create_file(path):
    """
    情况或者创建一个目录
    :param path: 目录
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        del_file(path)
        os.makedirs(path)


class RepoGit:
    """
    项目仓库管理
    """
    proj_path = ""
    repo = Repo

    def __init__(self, proj_path):
        """
        :param proj_path: 路径
        """
        self.proj_path = proj_path
        self.repo = Repo(path=proj_path, search_parent_directories=True)

    def most_recent_commit_message(self, branch):
        """
        当前分支最后一次的提交信息
        :return:
        """
        self.switch_branch(branch)
        commits = list(self.repo.iter_commits(branch, max_count=10))
        for commit in commits:
            message = commit.message
            if message and len(
                    message) > 0 and "Merge" not in message and "no message" not in message and "自动" not in message:
                return message, commit
        return "", ""

    def switch_branch(self, branch):
        """
        切换到新分支
        :param branch: 新分支名字
        :return:
        """
        # self.repo.head.reference = branch
        branch_list = self.repo.git.branch("-r")
        if branch in branch_list:
            self.repo.git.checkout(branch)
        else:
            self.repo.git.branch(branch)

    # 获取所有的分支
    def get_branches(self):
        """
        :return: 返回分支列表
        """
        branch_list = self.repo.git.branch("-r")
        return branch_list

    # 获取当前分支
    def getCurrentBranch(self):
        """
        :return: 当前分支
        """
        return str(self.repo.active_branch)

    # 获取当前工作目录的文件状态，是否有改动
    # True 表示有改动未提交 False表示没有改动
    def is_dirty(self):
        return self.repo.is_dirty(index=True, working_tree=True, untracked_files=True)

    # 查看文件状态
    def status(self):
        return self.repo.git.status()

    @property
    def getStatusFormatStr(self):
        cmd = ["git", "status", "-s"]
        r = runcmd.run(cmd, cwd=self.proj_path)._raise()
        lines = r.out.splitlines()
        return "\n".join(lines)

    def _startswith(self, string):
        """return a list of files startswith string"""
        cmd = ["git", "status", "-s"]
        r = runcmd.run(cmd, cwd=self.proj_path)._raise()
        lines = r.out
        lines = []
        for line in r.out.splitlines():
            if line.find(string) == 0:
                lines.append(" ".join(line.split(" ")[2:]))
        return lines

    def untracked(self):
        """return a list of untracked files"""
        return self._startswith("??")

    # 提交代码
    def commit(self, msg):
        self.repo.index.commit(msg)

    def add(self, files):
        self.repo.git.add(all=True)


# 获取podspec对应的版本号
def get_version_for(pod_spec_path):
    """
    获取tag版本号
    :param pod_spec_path: podspec路径
    :param new_tag: 新的tag名字
    :return:
    """
    with open(pod_spec_path, 'r', encoding="utf-8") as f:
        for line in f:
            if "s.version" in line and "s.source" not in line:
                # 获取版本号
                cur_tag = tag_with_version(line)
                return cur_tag
        f.close()
        return ""


# 重写podspec里对应的版本
def update_versionfor_podspec(pod_spec_path, new_tag):
    """
    重写podspec里对应的版本
    :param pod_spec_path: podspec路径
    :param new_tag: 新tag
    :return:
    """
    file_data = ""
    with open(pod_spec_path, 'r', encoding="utf-8") as f:
        for line in f:
            if "s.version" in line and "s.source" not in line:
                cur_tag = tag_with_version(line)
                line = line.replace(cur_tag, new_tag)
                print("修改tag " + cur_tag + " => " + new_tag)
            file_data += line
    with open(pod_spec_path, 'w', encoding="utf-8") as f:
        f.write(file_data)
        f.close()


# 获取字符串中的版本信息
def tag_with_version(version):
    """
    获取字符串中的版本信息
    :param version: 版本号
    :return:
    """
    p = re.compile(r'\d+\.(?:\d+\.)*\d+')
    vers = p.findall(version)
    ver = vers[0]
    return ver


# 根据tag自增生成新的tag
def incre_tag(tag):
    """
    tag最后一位自增
    :param tag: 原tag
    :return: 返回最后一位自增1后的tag
    """
    tags = tag.split(".")
    tag_len = len(tags)
    if tag_len > 1:
        endtag = tags[tag_len - 1]
        end_tag_num = int(endtag) + 1
        endtag = str(end_tag_num)
        tags[tag_len - 1] = endtag

    new_tag = ".".join(tags)
    return new_tag


def get_filename(url_str):
    """
    获取路径中的文件名
    :param url_str: 文件路径
    :return: 返回文件名
    """
    url = urlparse(url_str)
    i = len(url.path) - 1
    while i > 0:
        if url.path[i] == '/':
            break
        i = i - 1
    folder_name = url.path[i + 1:len(url.path)]
    if not folder_name.strip():
        return False
    if ".git" in folder_name:
        folder_name = folder_name.replace(".git", "")
    return folder_name


# 判断两个版本的大小，去除小数点，变为整数数组，依次比较大小1
# 2.2.3 = [2, 2, 3]
# 2.2.10 = [2, 2, 10]  2.2.10 > 2.2.3
# 相等返回0， v1 > v2 返回 1 v1 < v2 返回 -1
def compare_version(v1, v2):
    """
    比较两个tag， 判断两个版本的大小，去除小数点，变为整数数组，依次比较大小1
    :param v1: v1 tag入参
    :param v2:  v2 tag 入参
    :return: 相等返回0， v1 > v2 返回 1 v1 < v2 返回 -1
    """
    v1_list = v1.split(".")
    v2_list = v2.split(".")
    max_len = max(len(v1_list), len(v2_list))
    idx = 0
    while idx < max_len:
        c_v1 = 0
        c_v2 = 0
        if len(v1_list) > idx:
            c_v1 = int(v1_list[idx])
        if len(v2_list) > idx:
            c_v2 = int(v2_list[idx])
        if c_v2 > c_v1:
            return -1
        else:
            return 1
        idx += 1
    return 0


# 写入文件
def update_yaml(yaml_path, data):
    """
    :param yaml_path: yaml路径
    :param data: yaml数据
    :return: 无返回值
    """
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml = ruamel.yaml.YAML()
        yaml.dump(data, f)


# 更新podfileModule文件
def update_module_files(yaml_path, local_yaml_path, branch_result, n_branch, modules_name):
    """
    更新ymal文件，修改本地依赖和分支依赖
    :param yaml_path: PodfileModule路径
    :param local_yaml_path: PodfileLocal路径
    :param branch_result: 操作成功的模块列表
    :param n_branch: 新分支名
    :param modules_name: 模块仓库的父路径默认为modules
    :return:
    """
    # 获取ymal 数据
    podfile_module_data = yaml_data(yaml_path)
    dependenceList = podfile_module_data["dependencies"]
    # 转换成模型数组
    conver_deplist = load_yaml(dependenceList)

    index = 0
    for a in conver_deplist:
        for mo_re in branch_result:
            if a.module and mo_re.module and a.module == mo_re.module and mo_re.result == 1:
                module_dict = {"module": mo_re.module, "pod": a.pod, "git": a.git, "configurations": a.configurations,
                               "inhibit_warnings": a.inhibit_warnings}
                dependenceList[index] = module_dict
        index += 1
    podfile_data = {"version": "1.0.0", "branch": str(n_branch), "dependencies": dependenceList}
    update_yaml(yaml_path, podfile_data)

    after_convert = []
    if not os.path.exists(local_yaml_path):
        shutil.copy(yaml_path, local_yaml_path)  # 复制文件
        for mo_re in branch_result:
            if mo_re.result == 1:
                module_dict = {"module": mo_re.module, "pod": mo_re.module, "path": modules_name + "/" + mo_re.module}
                after_convert.append(module_dict)
    else:
        # 获取ymal 数据
        podfile_module_data = yaml_data(local_yaml_path)
        local_dependenceList = podfile_module_data["dependencies"]
        # 转换成模型数组
        conver_deplist = load_yaml(local_dependenceList)
        for yamlModel in branch_result:
            contain = False
            for cm in conver_deplist:
                if cm.module == yamlModel.module:
                    contain = True
            if not contain and yamlModel.result == 1:
                # 没有包含，添加一个
                module = YamlModuleModel(module=yamlModel.module,
                                         pod=yamlModel.pod,
                                         version=None,
                                         git=None,
                                         branch=None,
                                         tag=None,
                                         path=None,
                                         newtag=None,
                                         configurations=None,
                                         inhibit_warnings=False)
                conver_deplist.append(module)
        for a in conver_deplist:
            module_dict = {"module": a.module, "pod": a.pod, "path": modules_name + "/" + a.module}
            after_convert.append(module_dict)

    local_module_data = {"version": "1.0.0", "branch": str(n_branch), "dependencies": after_convert}
    update_yaml(local_yaml_path, local_module_data)


# 更新podfileModule文件
def merge_for_module_files(yaml_path, branch_result, n_branch):
    """
    更新ymal文件，修改本地依赖和分支依赖
    :param yaml_path: PodfileModule路径
    :param branch_result: 操作成功的模块列表
    :param n_branch: 新分支名
    :return:
    """
    # 获取ymal 数据
    podfile_module_data = yaml_data(yaml_path)
    dependenceList = podfile_module_data["dependencies"]
    # 转换成模型数组
    conver_deplist = load_yaml(dependenceList)

    index = 0
    for a in conver_deplist:
        for mo_re in branch_result:
            if a.module and mo_re.module and a.module == mo_re.module and mo_re.result == 1:
                module_dict = {"module": mo_re.module, "pod": a.pod, "git": a.git, "tag": mo_re.tag,
                               "configurations": a.configurations,
                               "inhibit_warnings": a.inhibit_warnings}
                dependenceList[index] = module_dict
        index += 1
    podfile_data = {"version": "1.0.0", "branch": n_branch, "dependencies": dependenceList}
    update_yaml(yaml_path, podfile_data)


# 基于master 和 f_tag，创建一个新的分支new_branch, 如果文件目录存在，则判断当前是否在dui'y
# 1. 清空当前工作目录
# 2. 拉取代码
# 3. 新建分支
# 4. 推送分支
# 5. 提交代码
def auto_push_branch(filepath, git, f_branch, f_tag, n_branch):
    """
    将代码提交到n_branch
    1. 如果本地没有组件对应目录，异常提示错误
    2. 存在目录：在当前新分支，直接提交代码，
    3. 存在目录：本地不在新分支，异常提示错误
    :param filepath: 路径
    :param git: git地址
    :param f_branch: 基于哪个分支切一个新的开发分支
    :param f_tag:  基于哪个tag切开发分支
    :param n_branch: 新分支名
    :return: 成功返回新分支名，失败返回空字符串
    """
    (file, ext) = os.path.splitext(git)
    (path, filename) = os.path.split(git)
    module_name = filename.replace(ext, "")
    _branch = f_branch
    if not (f_branch and len(f_branch) > 0):
        _branch = "master"
    # 创建分支
    print(os.getcwd())
    fapath = os.getcwd()
    if os.path.exists(filepath):
        # 存在目录，判断当前处于哪个分支下
        try:
            repo = Repo(path=filepath, search_parent_directories=True)
        except:
            br = new_branch(filepath, git, _branch, f_tag, n_branch)
            return br
        c_branch = repo.active_branch.name
        # 判断当前分支是不是是指定的开发分支
        if c_branch == f_branch:
            # git add 代码
            git_add_command = "git add -A"
            # git commit 代码
            git_commit_command = "git commit -m \'自动提交\'"
            # git pull branch 代码
            git_pull_command = "git pull origin " + c_branch
            # git push
            git_push_command = "git push origin master"
            os.chdir(filepath)
            os.system(git_add_command)
            logging.info("执行 " + git_add_command)
            os.system(git_commit_command)
            logging.info("执行 " + git_commit_command)
            pul_status = os.system(git_pull_command)
            if not pul_status == 0:
                os.chdir(fapath)
                logging.error("模块：" + module_name + " 分支: " + f_branch + " 提交失败")
                return ""
            pul_status += os.system(git_push_command)
            if not pul_status == 0:
                os.chdir(fapath)
                logging.error("模块：" + module_name + " 分支: " + f_branch + " 提交失败")
                return ""

            os.chdir(fapath)
            return n_branch
        else:
            logging.error("模块：" + module_name + " 分支: " + c_branch + " 不在开发分支提交不了")
            return ""

        return n_branch
    else:
        logging.error("模块：" + module_name + "分支: " + f_branch + " 本地没有组件的工作目录，没法自动提交代码")
        return ""


# 自动打tag 自动合并失败时返回空字符串
# 1. 清空当前工作目录
# 2. 拉取代码
# 3. 修改s.version
# 4. 提交代码
# 5. 拉取工作分支
# 5. 推送代码
def auto_release_path(filepath, git, pod, branch, new_tag):
    """
    自动合并branch到master中，并提交tag
    :param filepath: 文件路径
    :param git: git地址
    :param pod: pod模块
    :param branch: 分支
    :param new_tag: 新tag
    :return:
    """
    create_file(filepath)

    # return
    # 进入模块
    # clone 代码
    git_clone_command = "git clone -b master" + " " + git + " " + filepath
    # git add 代码
    git_add_command = "git add -A"
    # git pull branch 代码
    git_pull_command = "git pull origin " + branch

    # git push
    git_push_command = "git push origin master"
    # 用newTag来修改podspec中version
    os.system(git_clone_command)
    print("执行 " + git_clone_command)

    # 获取开发分支最后一次提交的信息
    repogit = RepoGit(proj_path=filepath)
    commit_message, commit = repogit.most_recent_commit_message(branch)
    repogit.switch_branch('master')
    git_commit_command = "git commit -m \'自动提交，修改tag\'"
    # master分支下的版本号
    os.chdir(filepath)
    cur_tag = get_version_for(pod + ".podspec")
    os.system("pwd")
    os.system("ls")
    os.system(git_add_command)
    print("执行 " + git_add_command)
    os.system(git_commit_command)
    print("执行 " + git_commit_command)
    pul_status = os.system(git_pull_command)
    print("执行 " + git_pull_command)
    if not pul_status == 0:
        print("代码冲突了")
        return ""
    dev_branch_tag = get_version_for(pod + ".podspec")
    new_tag_p = dev_branch_tag
    if dev_branch_tag == cur_tag:
        # 版本号一样就最后一位自增
        new_tag_p = incre_tag(cur_tag)
    else:
        # 版本号不一样，就比较如果开发分支比较大就用开发分支，否则还是自增
        res = compare_version(dev_branch_tag, cur_tag)
        if res == -1:
            new_tag_p = incre_tag(cur_tag)

    update_versionfor_podspec(pod + ".podspec", new_tag_p)
    os.system(git_add_command)
    print("执行 " + git_add_command)
    os.system(git_commit_command)
    print("执行 " + git_commit_command)
    print("代码已经提交到master")
    # git pull branch 代码

    full_tag_message = '自动Tag 分支: {0} '.format(branch)
    if commit_message and len(commit_message) > 0:
        full_tag_message = full_tag_message + "最后提交信息： \"{0}\"   提交号：{1}".format(commit_message, commit.hexsha)
    git_tag_command = "git tag -a {0} -m \'{1}\'".format(new_tag_p, full_tag_message)
    os.system(git_tag_command)
    git_push_tag_command = "git push origin {0} ".format(new_tag_p)
    os.system(git_push_tag_command)
    os.system(git_push_command)
    print("执行 " + git_push_command)
    return new_tag_p


# 基于主项目分支切一个新的分支
def checkout_project(filepath, git, c_branch, c_tag, n_branch):
    """
    基于c_branch和c_tag，新建一个分支n_branch
    :param filepath: 主项目本地目录
    :param git: git地址
    :param c_branch: 基于哪个分支切开发分支
    :param c_tag: 基于哪个tag切开发分支
    :param n_branch: 新分支名
    :return:
    """
    # return
    # 进入模块
    # clone 代码
    c_branch = c_branch
    if not (c_branch and len(c_branch) > 0):
        c_branch = "master"

    git_clone_command = "git clone -b " + c_branch + " " + git + " " + filepath
    # remote add origin
    git_remote_origin = "git remote add  origin " + git
    # 创建一个新分支
    git_create_branch = "git branch " + n_branch
    if c_tag and len(c_tag) > 0:
        git_create_branch += c_tag
    # checkout
    git_checkout_command = "git checkout " + n_branch
    # 推送分支
    git_push_branch = "git push origin " + n_branch
    logging.info(git_clone_command)
    # Repo.clone_from(git, to_path=filepath, branch=c_branch)
    # os.chdir(filepath)
    clone_status = os.system(git_clone_command)
    clone_status += os.system(git_remote_origin)
    logging.info(clone_status)
    os.system(git_create_branch)
    os.system(git_checkout_command)
    os.system(git_push_branch)
    logging.info("壳工程目录：" + filepath)


# 基于podfileModule来给每个组件创建一个分支
def create_branch(module_list, module_f_path, n_branch, modules, c_path):
    """
    基于列表，拉取对应代码，并创建一个开发分支
    :param module_list: 模块列表
    :param module_f_path: 路径
    :param n_branch: 新分支
    :param modules: 这些模块新建n_branch分支
    :param c_path: 当前的工作目录
    :return:
    """
    index = 0
    create_branch_result = []
    for a in module_list:
        if a.module in modules:
            if (a.branch and len(str(a.branch)) > 0) or (a.tag and len(str(a.tag)) > 0):
                filename = a.module
                module_path = module_f_path + filename + "/"
                error_info = ''
                if not os.path.exists(module_path):
                    branch_name = auto_create_branch(module_path, a.git, a.branch, a.tag, n_branch)
                else:
                    local_branch = RepoGit(proj_path=module_path).getCurrentBranch()
                    error_info = "本地有工作目录: {0}，当前分支是：{1}".format(a.pod, local_branch)
                    branch_name = ''
                res = 1
                if not (branch_name and len(branch_name) > 0):
                    res = 0
                new_branch_model = ModuleStatusModel(a.module, a.pod, res, n_branch, error_info)
                create_branch_result.append(new_branch_model)
            else:
                new_branch_model = ModuleStatusModel(a.module, a.pod, 0, n_branch,
                                                     "podfileModule.yaml 中组件: " + a.pod + " 的branch或者tag为空, 不能确定要拉取的代码的位置")
                create_branch_result.append(new_branch_model)
        index += 1
        os.chdir(c_path)
    return create_branch_result


# 基于master 和 f_tag，创建一个新的分支new_branch，如果存在仓库则先清空仓库，再拉取分支
# 1. 清空当前工作目录
# 2. 拉取代码
# 3. 新建分支
# 4. 推送分支
def auto_create_branch(filepath, git, f_branch, f_tag, n_branch):
    """
    :param filepath: 文件路径
    :param git: git地址
    :param f_branch: 基于哪个分支切一个新的开发分支
    :param f_tag: 基于哪个tag切开发分支
    :param n_branch: 新分支名
    :return: 成功返回新分支名，失败返回空字符串
    """
    # 创建分支
    create_file(filepath)
    return new_branch(filepath, git, f_branch, f_tag, n_branch)


# 新建分支
def new_branch(filepath, git, f_branch, f_tag, n_branch):
    """
    f_branch 和 f_tag，创建一个新的分支n_branch
    2. 拉取代码
    3. 判断是否存在新分支，有新分支直接切到新分支
    3. 新建分支
    4. 切换到新分支
    4. 推送分支
    :param filepath: 路径
    :param git: git地址
    :param f_branch: 基于哪个分支切一个新的开发分支
    :param f_tag:  基于哪个tag切开发分支
    :param n_branch: 新分支名
    :return: 成功返回新分支名，失败返回空字符串
    """
    pull_branch = f_branch
    if not (f_branch and len(f_branch) > 0):
        pull_branch = "master"
    if f_branch and len(f_branch) > 0 and f_branch == n_branch:
        pull_branch = "master"
    # clone 代码
    git_clone_command = "git clone -b " + pull_branch + " " + git + " " + filepath
    # 创建一个新分支
    git_create_branch = "git branch " + n_branch
    if f_tag and len(f_tag) > 0:
        git_create_branch += " " + f_tag
    # checkout
    git_checkout_command = "git checkout -b " + n_branch
    # git push
    git_push_command = "git push origin {0}".format(n_branch)
    os.system(git_push_command)
    create_status = 0
    create_status += os.system(git_clone_command)
    logging.info("执行 " + git_clone_command)
    # master分支下的版本号
    repoGit = RepoGit(proj_path=filepath)
    branchs = repoGit.get_branches()
    os.chdir(filepath)
    if n_branch in branchs:
        os.system(git_checkout_command)
        logging.info(n_branch + "分支已存在")
        return n_branch
    create_status = os.system(git_create_branch)
    create_status += os.system(git_checkout_command)
    logging.info("新分支已经提交到master")
    create_status += os.system(git_push_command)
    if not create_status == 0:
        logging.warning("新分支创建失败")
        return ""
    return n_branch


# 基于PodfileLocal，提交所有模块开发分支代码
def commit_branch(module_list, module_f_path, msg):
    """
    基于列表，提交对应开发分支代码
    :param module_list: 模块列表
    :param module_f_path: 路径
    :param msg: 提交信息
    :return: 返回操作的分支
    """
    commit_result = []
    for module in module_list:
        filename = module.module
        module_path = module_f_path + filename + "/"
        git = RepoGit(module_path)
        branch = git.getCurrentBranch()
        msg = ''
        result = 0
        if not git.is_dirty():
            msg = "很干净，没有可提交的"
        else:
            # 判断是否有没有追踪的文件
            untracks = git.untracked()
            git.add(untracks)
            git.commit(msg)
            result = not git.is_dirty()
            if result == 0:
                msg = "提交失败"
        modul_branch_model = ModuleStatusModel(module.module, module.pod, result, branch, msg)
        commit_result.append(modul_branch_model)
    return commit_result


# 基于podfileModule，提交模块开发分支代码
def pull_branch(module_list, module_f_path):
    """
    基于列表，提交对应开发分支代码
    :param module_list: 模块列表
    :param module_f_path: 路径
    :return: 返回操作的分支
    """

    index = 0
    pull_result = []
    for module in module_list:
        filename = module.module
        module_path = module_f_path + filename + "/"
        git = RepoGit(module_path)
        branch = git.getCurrentBranch()
        msg = ''
        result = 1
        if git.is_dirty():
            result = -1
            msg = "本地有变动未提交，请确认"
        else:
            # ori = git.repo.remotes.origin
            try:
                git.repo.git.pull('--progress', '--no-rebase', 'origin', branch)
            except Exception as e:
                result = 0
                msg = str(e)

        modul_branch_model = ModuleStatusModel(module.module, module.pod, result, branch, msg)
        pull_result.append(modul_branch_model)
    return pull_result


# 基于podfileModule，提交模块开发分支代码
def push_branch(module_list, module_f_path):
    """
    基于列表，提交对应开发分支代码
    :param module_list: 模块列表
    :param module_f_path: 路径
    :return: 返回操作的分支
    """

    index = 0
    pull_result = []
    for module in module_list:
        filename = module.module
        module_path = module_f_path + filename + "/"
        git = RepoGit(module_path)
        branch = git.getCurrentBranch()
        msg = ''
        result = 1
        if git.is_dirty():
            result = -1
            msg = "本地有变动未提交，请确认"
        else:
            try:
                git.repo.git.push('--progress', 'origin', branch)
            except Exception as e:
                result = 0
                msg = str(e)

        modul_branch_model = ModuleStatusModel(module.module, module.pod, result, branch, msg)
        pull_result.append(modul_branch_model)
    return pull_result


# 基于podfileModule，提交模块开发分支代码
def release_branch(module_list, tag_path, c_path, f_branch):
    """
    基于模块列表，合并对应开发分支代码到master并打新的tag
    :param module_list: 模块列表
    :param tag_path:  这些模块排除在外，不提交n_branch代码
    :param c_path: 当前运行分支
    :param f_branch: 配置的全局统一分支，每个模块可以单独配置分支
    :return: 返回操作成功的分支
    """

    index = 0
    merge_result = []
    for a in module_list:
        if not (a.branch and len(a.branch) > 0) and not (a.tag and len(a.tag) > 0):
            a.branch = f_branch
        if a.branch and len(a.branch) > 0:
            filename = get_filename(a.git)
            module_path = tag_path + filename + "/"
            create_tag = auto_release_path(module_path, a.git, a.pod, a.branch, a.new_tag)
            result = 0
            if create_tag and len(create_tag) > 0:
                result = 1
                a.new_tag = create_tag
            merge_model = ModuleStatusModel(a.module, a.pod, result, a.branch)
            merge_result.append(merge_model)
        index += 1
        os.chdir(c_path)
    return merge_result


# 打印表格
def printTable(list, info):
    table = PrettyTable(["编号", "组件名", "分支", "错误信息"])
    # debugInfo(len(list))
    if len(list) > 0:
        for index in range(len(list)):
            model = list[index]
            table.add_row([index, model.module, model.branch, model.msg])
        table.align[1] = '1'
        table.border = True
        table.junction_char = '+'
        table.horizontal_char = '-'
        table.vertical_char = '|'
        table.sortby = '分支'
        table.hrules = ALL
        debugInfo("\n[!] 以下是 \"{0}\"\n".format(info))
        debugInfo(table)
        debugInfo("\n")
    else:
        debugInfo("\n[!] 暂无 \"{0}\"\n".format(info))


# 创建分支的对象
# branch 组件新分支名字
class yhgit:

    # # 初始化
    # def __init__(self):
    #     """
    #     基于项目git地址拉取代码，并通过读取PodfileModule中的组件依赖，来新建开发分支n_branch，或者更新本地仓库
    #     :param git: 工程git地址
    #     :param branch: 基于哪个分支新建开发分支， 默认master
    #     :param tag: 基于哪个tag来新建开发分支， 默认不指定
    #     :param path: 项目的路径，默认~/Desktop/Project/ + 项目名
    #     :param n_branch: 新分支名， 默认当前年月日
    #     """
    #     _project_path = path
    #     if not (_project_path and len(_project_path) > 0):
    #         (file, ext) = os.path.splitext(git)
    #         (path, filename) = os.path.split(git)
    #         project_name = filename.replace(ext, "")
    #         _project_path = "~/Desktop/Project/" + project_name + "/"
    #     self.path = _project_path
    #
    #     _n_branch = n_branch
    #     if not (_n_branch and len(_n_branch) > 0):
    #         today = datetime.date.today()
    #         for_today = today.strftime("%y%m%d")
    #         _n_branch = for_today
    #     self.n_branch = _n_branch
    #
    #     self.git = git
    #     self.branch = branch
    #     self.tag = tag

    # def __init__(self):

    # 初始化项目仓库，自动拉取组件仓库，并创建新分支
    def install(self, n_branch, modules=[]):
        """
        基于初始化的配置信息，初始化开发分支； 创建工程目录，创建每个模块的工作目录，创建开发分支，创建工作目录
        1. 如果本地有该组件的目录，就跳过，不会切换到新分支（避免造成，手动切换分之后，又自定切换到新分支）
        2. 如果本地没有改组件目录，就新建目录，拉取master下tag的代码，然后创建新分支
        :param n_branch: 新分支的名字
        :param module_list: 拉取这些模块，并创建新分支。
        :return:
        """
        c_path = os.getcwd()
        fa_path = ""
        modules_file_name = "modules"
        new_branch = n_branch

        yamlPath = fa_path + 'PodfileModule.yaml'
        modules_path = fa_path + modules_file_name + "/"
        yamlPath = fa_path + 'PodfileModule.yaml'
        localyamlPath = fa_path + 'PodfileLocal.yaml'

        # 子目录，用来存放子模块仓库, 如果没有需要创建一个
        if not os.path.exists(modules_path):
            create_file(modules_path)
        # 获取ymal 数据
        podfile_module_data = yaml_data(yamlPath)
        # 获取依赖数据
        dependenceList = podfile_module_data["dependencies"]
        # 转换成模型数组
        conver_deplist = load_yaml(dependenceList)
        branch_res = create_branch(conver_deplist, modules_path, new_branch, modules, c_path)
        if len(branch_res) > 0:
            update_module_files(yamlPath, localyamlPath, branch_res, new_branch, modules_file_name)
        if len(branch_res) == 0:
            debugInfo("没有要执行yhgit install的模块")
        else:
            succ_list = []
            fail_list = []
            for merg_Model in branch_res:
                if merg_Model.result == 1:
                    succ_list.append(merg_Model)
                else:
                    fail_list.append(merg_Model)
            printTable(succ_list, "分支创建成功的模块")
            printTable(fail_list, "分支创建失败的模块")

    # 获取podfileLocal.yaml中各模块状态, 提示： 1. 很干净没有未提交的代码 2. 有改动未提交 3. 没有相关文件报错误
    def status(self):
        """
        获取podfileLocal.yaml中各模块状态, 提示： 1. 很干净没有未提交的代码 2. 有改动未提交
        1. 如果podfileLocal.yaml是空则终止
        2. 如果moduls为空则终止
        :return:
        """
        modules_file_name = "modules"
        modules_path = modules_file_name + "/"
        local_yaml_path = 'PodfileLocal.yaml'

        # 子目录，用来存放子模块仓库, 如果没有需要创建一个
        if not os.path.exists(modules_path):
            debugInfo("本地modules为空，无法查看组件的状态")
            return
        if not os.path.exists(local_yaml_path):
            debugInfo("本地local_yaml_path为空，无法查看组件的状态")
            return
        podfile_module_data = yaml_data(local_yaml_path)
        local_dependenceList = podfile_module_data["dependencies"]
        # 转换成模型数组
        module_list = load_yaml(local_dependenceList)
        status_result = []
        for module in module_list:
            result = 0
            branchname = ''
            msg = ''
            if not (module.path and len(module.path) > 0):
                result = -1
                msg = "请检查PodfileLocal.yaml中模块：" + module.module + " 的path"
            else:
                if os.path.exists(module.path):
                    repogit = RepoGit(module.path)
                    result = not repogit.is_dirty()
                    branchname = repogit.getCurrentBranch()
                    # 如果是有改动，列出文件的改动状态
                    if result == 0:
                        msg = repogit.getStatusFormatStr
                else:
                    result = -1
                    msg = "请检查模块：" + module.module + " 的路径 " + module.path + " 是否为空";
            new_branch_model = ModuleStatusModel(module.module, module.pod, result, branchname, msg)
            status_result.append(new_branch_model)

        if len(status_result) == 0:
            debugInfo("没有要执行git status的模块")
        else:
            error_list = []
            fail_list = []
            success_list = []
            for merg_Model in status_result:
                if merg_Model.result == 1:
                    success_list.append(merg_Model)
                elif merg_Model.result == 0:
                    fail_list.append(merg_Model)
                elif merg_Model.result == -1:
                    error_module = error_module + (merg_Model.module + "\n")
                    error_list.append(merg_Model)
            printTable(success_list, "没有代码要提交的模块")
            printTable(fail_list, "有代码要提交的模块")
            printTable(error_list, "检查失败的模块")

    # 自动提交本地修改的内容
    def commit(self, msg):
        """
        基于podfileModules的配置信息，提交本地开发分支代码
        :param msg: 这些模块不需要修改，不能提交代码
        :return:
        """
        fa_path = ""
        modules_file_name = "modules"
        modules_path = fa_path + modules_file_name + "/"
        # 子目录，用来存放子模块仓库
        if not os.path.exists(modules_path):
            debugInfo("没有modules目录，不能提交")
            return

        local_yaml_path = fa_path + 'PodfileLocal.yaml'

        # 子目录，用来存放子模块仓库, 如果没有需要创建一个
        if not os.path.exists(local_yaml_path):
            debugInfo("本地无PodfileLocal.yaml，无法继续提交")
            return
        if not (msg and len(msg) > 0):
            debugInfo("提交信息为空，无法继续提交")
            return
        podfile_module_data = yaml_data(local_yaml_path)
        local_dependenceList = podfile_module_data["dependencies"]
        # 转换成模型数组
        module_list = load_yaml(local_dependenceList)
        branch_res = commit_branch(module_list, modules_path, msg)
        if len(branch_res) == 0:
            debugInfo("没有要提交代码的模块")
        else:
            succ_list = []
            fail_list = []
            for merg_Model in branch_res:
                if merg_Model.result == 1:
                    succ_list.append(merg_Model)
                else:
                    fail_list.append(merg_Model)
            printTable(succ_list, "代码提交成功的模块")
            printTable(fail_list, "代码提交失败的模块")

    # 自动拉取远端代码
    def pull(self):
        """
        基于PodfileLocal的配置信息，提交本地开发分支代码
        :return:
        """
        fa_path = ""
        modules_file_name = "modules"
        modules_path = fa_path + modules_file_name + "/"
        # 子目录，用来存放子模块仓库
        if not os.path.exists(modules_path):
            logging.info("没有modules目录，不能提交")
            print("没有modules目录，不能提交")
            return

        local_yaml_path = fa_path + 'PodfileLocal.yaml'

        # 子目录，用来存放子模块仓库, 如果没有需要创建一个
        if not os.path.exists(local_yaml_path):
            debugInfo("本地无PodfileLocal.yaml，无法继续提交")
            return
        podfile_module_data = yaml_data(local_yaml_path)
        local_dependenceList = podfile_module_data["dependencies"]
        # 转换成模型数组
        module_list = load_yaml(local_dependenceList)
        branch_res = pull_branch(module_list, modules_path)
        if len(branch_res) == 0:
            logging.info("没有要拉取远端代码的模块")
        else:
            succ_list = []
            fail_list = []
            for merg_Model in branch_res:
                if merg_Model.result == 1:
                    succ_list.append(merg_Model)
                else:
                    fail_list.append(merg_Model)
            printTable(succ_list, "代码拉取成功的模块")
            printTable(fail_list, "代码拉取失败的模块")

    # 自动推送本地修改到远端
    def push(self):
        """
        基于PodfileLocal的配置信息，拉取本地开发分支代码
        :return:
        """
        fa_path = ""
        modules_file_name = "modules"
        modules_path = fa_path + modules_file_name + "/"
        # 子目录，用来存放子模块仓库
        if not os.path.exists(modules_path):
            logging.info("没有modules目录，不能提交")
            print("没有modules目录，不能提交")
            return

        local_yaml_path = fa_path + 'PodfileLocal.yaml'

        # 子目录，用来存放子模块仓库, 如果没有需要创建一个
        if not os.path.exists(local_yaml_path):
            debugInfo("本地无PodfileLocal.yaml，无法继续提交")
            return
        podfile_module_data = yaml_data(local_yaml_path)
        local_dependenceList = podfile_module_data["dependencies"]
        # 转换成模型数组
        module_list = load_yaml(local_dependenceList)
        branch_res = push_branch(module_list, modules_path)
        if len(branch_res) == 0:
            logging.info("没有要推送代码的模块")
        else:
            succ_list = []
            fail_list = []
            for merg_Model in branch_res:
                if merg_Model.result == 1:
                    succ_list.append(merg_Model)
                else:
                    fail_list.append(merg_Model)
            printTable(succ_list, "代码推送成功的模块")
            printTable(fail_list, "代码推送失败的模块")

    # 自动提交子模块的代码
    def release(self):
        """
        基于podfileModules的配置信息，merge开发分支到master，获取开发分支的版本号，如果版本号大于master分支，新的tag就为开发分支版本号，如果版本号相等，那那么就末尾自增1，自动打tag
        :return:
        """
        c_path = os.getcwd()
        fa_path = self.path
        modules_file_name = "tagpath"
        modules_path = fa_path + modules_file_name + "/"
        # 子目录，用来存放子模块仓库
        if not os.path.exists(modules_path):
            create_file(modules_path)
        yamlPath = fa_path + 'PodfileModule.yaml'

        # 子目录，用来存放子模块仓库, 如果没有需要创建一个
        if not os.path.exists(yamlPath):
            debugInfo("本地无PodfileModule.yaml，无法继续提交")
            return
        # 获取yaml 数据
        podfile_module_data = yaml_data(yamlPath)
        logging.info("读取yaml数据")
        # 获取依赖数据
        dependenceList = podfile_module_data["dependencies"]
        branch = podfile_module_data["branch"]
        # 转换成模型数组
        conver_deplist = load_yaml(dependenceList)
        logging.info("转换成模型")
        branch_res = release_branch(conver_deplist, modules_path, c_path, branch)
        if len(branch_res) > 0:
            merge_for_module_files(yamlPath, branch_res, branch)
        if len(branch_res) == 0:
            logging.info("没有要realse的模块")
        else:
            succ_list = []
            fail_list = []
            for merg_Model in branch_res:
                if merg_Model.result == 1:
                    succ_list.append(merg_Model)
                else:
                    fail_list.append(merg_Model)
            printTable(succ_list, "release成功的模块")
            printTable(fail_list, "realse失败的模块")

        if os.path.exists(modules_path):
            del_file(modules_path)

    # 自动提交子模块的代码
    def clean(self):
        """
        基于podfileModules的配置信息，merge开发分支到master，获取开发分支的版本号，如果版本号大于master分支，新的tag就为开发分支版本号，如果版本号相等，那那么就末尾自增1，自动打tag
        :return:
        """
        local_yaml_path = 'PodfileLocal.yaml'
        # 子目录，用来存放子模块仓库, 如果没有需要创建一个
        if os.path.exists(local_yaml_path):
            os.remove(local_yaml_path)
        modules_path = "modules/"
        if os.path.exists(modules_path):
            del_file(modules_path)

        debugInfo("执行成功")


def debugInfo(msg):
    logging.info(msg)
    print(msg)


def main(argvs=None):
    """The main routine."""

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.
    # 获取参数
    # print(argvs)
    if argvs is None:
        argvs = sys.argv
    # print(argvs)
    # 获取指令类型
    command = argvs[1]
    branchname = ''
    modules = []
    # debugInfo(len(argvs))
    # debugInfo(command)
    # print(command == "clean")
    if command == "install":
        print(len(argvs))
        if len(argvs) > 2:
            subcommand = argvs[2]
            if subcommand and len(subcommand) > 0 and subcommand == "-b":
                # 需要获取具体的分支名
                branchname = argvs[3]
                if branchname and len(branchname) > 0:
                    # 获取需要创建分支的组件
                    modules = argvs[4:]
            else:
                modules = argvs[2:]

        if not (branchname and len(branchname) > 0):
            # 获取本地配置的分支名称
            # 获取ymal 数据
            cuPath = os.getcwd()
            local_yaml_path = cuPath + '/PodfileLocal.yaml'
            branchname = ""
            if os.path.exists(local_yaml_path):
                podfile_module_data = yaml_data(local_yaml_path)
                branchname = podfile_module_data.get("branch", None)
        print(branchname)
        if not (branchname and len(branchname) > 0):
            logging.error("请指定分支名字，\n 1. 指令后面指定分支 \n2. 在PodfileLoacal.yaml中指定branch")
        if not (modules and len(modules) > 0):
            logging.error("请指定具体的模块")
        else:
            yhgit().install(branchname, modules)
    elif command == "status":
        # 查看本地代码的状态
        yhgit().status()
    elif command == "commit":
        commit_msg = ''
        if len(argvs) > 2:
            subcommand = argvs[2]
            if subcommand and len(subcommand) > 0 and subcommand == "-m":
                # 需要获取具体的分支名
                commit_msg = argvs[3]
        if not (commit_msg and len(commit_msg) > 0):
            debugInfo("必须添加-m 和 commit_msg")
        else:
            yhgit().commit(commit_msg)

    elif command == "pull":
        yhgit().pull()

    elif command == "push":
        yhgit().push()

    elif command == "release":
        yhgit().release()

    elif command == "clean":
        yhgit().clean()


if __name__ == '__main__':
    cuPath = os.getcwd()
    main()
    # fa_path = "../../Desktop/Project/yh-rme-srm-purchase-ios/"
    # project_git = "http://gitlab.yonghui.cn/operation-pc-mid-p/yh-rme-srm-purchase-ios.git"
    # # 分支的名字，如果没有指定将用年月日表示
    # n_branch = "221107"

    # cb = yhmgit(git=project_git, path=fa_path, n_branch=n_branch)
    # cb.init_project(clean_proj=False)
    # cb.pull_modules()
    # cb.push_modules()
    # cb.merge_modules()
    # os.chdir(fa_path)
    # os.system("pod install")

    """
    argv[0]:  获取命令的类型 如下
    install  

    argv[1]:  命令的


    """
