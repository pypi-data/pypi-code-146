import os
import shutil
from pathlib import Path

import yiflow
from colorama import Fore, Style


def main(name, model_dir=None):
    # 检查项目名是否合法
    assert name != ''
    assert name[0].isalpha()
    for s in name:
        assert s.isalpha() or s == '_'

    # 复制项目示例
    source_dir_path = Path(yiflow.__file__).parent / 'resources' / 'example'
    target_dir_path = Path(os.getcwd()) / name

    # 判断目标文件夹是否存在
    if target_dir_path.exists():
        print('Directory ' + Fore.GREEN + name + Style.RESET_ALL + ' already exists.')
        return

    shutil.copytree(str(source_dir_path), str(target_dir_path))

    # 修改项目变量
    wf_proj_path = str(target_dir_path)
    if model_dir == None:
        wf_model_path = 'somewhere_containing_your_models'
    else:
        wf_model_path = model_dir

    sourceme_path = target_dir_path / 'sourceme.sh'
    with sourceme_path.open('r') as fi:
        content = fi.read()
        content = content.replace('__WF_PROJ_PATH__', wf_proj_path)
        content = content.replace('__WF_MODEL_PATH__', wf_model_path)
    with sourceme_path.open('w') as fo:
        fo.write(content)

    print(f'Project ' + Fore.GREEN + name + Style.RESET_ALL + ' initialized in the current place.')
