import os
from enum import Enum, unique

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .. import Generator
from ..converters import Keil5P27Converter


# Keil5 版本定义
@unique
class Keil5VersionType(Enum):
    V5 = 1  # Keil V5.x   （低于 V5.27）
    V5_27 = 2  # Keil V5.27+ （包括 V5.27）


class Keil5Generator(Generator):
    # Jinja2环境
    __env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
        autoescape=select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    @staticmethod
    def combine_files(base_files: list, append_files: list):
        if append_files is None:
            return
        if len(append_files) != 0:
            for append_file in append_files:
                find_flag = False
                for base_file in base_files:
                    if base_file['name'] == append_file['name']:
                        find_flag = True
                        break
                if not find_flag:
                    base_files.append(append_file)

    def combine_groups(self, base_groups: list, append_groups: list):
        if base_groups is None or append_groups is None:
            return
        if len(append_groups) != 0:
            for append_group in append_groups:
                # 在基础组中寻找是否已经有相同组
                find_flag = False
                for base_group in base_groups:
                    # 有相同组，合并这两组的文件，并递归合并子组
                    if base_group['name'] == append_group['name']:
                        if 'files' in append_group and append_group['files'] is not None:
                            if 'files' not in base_group:
                                base_group['files'] = []
                            self.combine_files(base_group['files'], append_group['files'])
                        if 'groups' in append_group:
                            if 'groups' not in base_group:
                                base_group['groups'] = []
                            self.combine_groups(base_group['groups'], append_group['groups'])
                        find_flag = True
                        break

                # 没有相同组，直接将该组插入
                if not find_flag:
                    base_groups.append(append_group)

    # 生成工程接口
    def generate(self, prj_info, target_info, prj_path, version: Keil5VersionType, **kwargs):
        """
        生成Keil5.x版本工程。
        可选参数：
        1. combine：默认False。控制生成的工程是否与前一次工程进行合并。
        """

        # 设定配置 ---------------------------------------------
        __combine = False
        if 'combine' in kwargs and kwargs['combine'] is True:
            __combine = True

        # 路径处理 ---------------------------------------------
        # 项目文件路径
        prj_file_path = os.path.join(prj_path, 'MDK-ARM')

        # 检查路径是否存在
        if not os.path.exists(prj_file_path):
            os.makedirs(prj_file_path)

        # 检查工程文件是否需要修改target配置 -----------------------
        # 检查工程是否需要添加额外的烧写配置文件
        if prj_info['advanced_options']['keil_flasher_cfg'] is not None:
            target_info['keil_5_flash_algorithms'].extend(prj_info['advanced_options']['keil_flasher_cfg'])

        # 合并工程文件中的文件组、预处理宏定义和包含路径 ---------------
        if __combine:
            # 检查是否已经存在工程文件（*.uvprojx）和选项文件（*.uvoptx）
            f_prj_name = os.path.join(prj_file_path, prj_info['name'] + ".uvprojx")
            f_opt_name = os.path.join(prj_file_path, prj_info['name'] + ".uvoptx")
            if os.path.exists(f_prj_name) and os.path.exists(f_opt_name):
                # 读取工程和选项并进行合并
                if version in [Keil5VersionType.V5, Keil5VersionType.V5_27]:
                    cvt = Keil5P27Converter()
                    cvt_desc = cvt.analyze_project({'uvprojx': f_prj_name, 'uvoptx': f_opt_name})
                    # 合并预处理宏定义
                    prj_info['defines'] = list(set(prj_info['defines'] + cvt_desc['defines']))
                    prj_info['definesASM'] = list(set(prj_info['definesASM'] + cvt_desc['definesASM']))
                    # 合并包含路径
                    prj_info['includePaths'] = list(set(prj_info['includePaths'] + cvt_desc['includePaths']))
                    prj_info['includePathsASM'] = list(set(prj_info['includePathsASM'] + cvt_desc['includePathsASM']))
                    # 合并工程组
                    self.combine_groups(prj_info['groups'], cvt_desc['groups'])

        # 生成工程文件 ------------------------------------------
        # KEIL 5
        if version == Keil5VersionType.V5:
            # KEIL 5 工程文件(*.uvprojx)
            tpl = self.__env.get_template('keil_5_uvprojx.xml')
            uvprojx_name = prj_info['name'] + ".uvprojx"
            with open(os.path.join(prj_file_path, uvprojx_name), mode='w', encoding='utf-8') as f:
                f.write(tpl.render(project=prj_info, target=target_info))

            # KEIL 5 工程选项文件(*.uvoptx)
            tpl = self.__env.get_template('keil_5_uvoptx.xml')
            uvoptx_name = prj_info['name'] + ".uvoptx"
            with open(os.path.join(prj_file_path, uvoptx_name), mode='w') as f:
                f.write(tpl.render(project=prj_info, target=target_info))

            # KEIL 5 JLink 配置文件(JLinkSettings.ini)
            if str.lower(prj_info['debug']['tool']) == 'jlink':
                tpl = self.__env.get_template('keil_5_jlink_setting.ini')
                with open(os.path.join(prj_file_path, 'JLinkSettings.ini'), mode='w', encoding='utf-8') as f:
                    f.write(tpl.render(target=target_info))

        # KEIL 5.27
        elif version == Keil5VersionType.V5_27:
            # KEIL 5.27 工程文件(*.uvprojx)
            tpl = self.__env.get_template('keil_5_27_uvprojx.xml')
            uvprojx_name = prj_info['name'] + ".uvprojx"
            with open(os.path.join(prj_file_path, uvprojx_name), mode='w', encoding='utf-8') as f:
                f.write(tpl.render(project=prj_info, target=target_info))

            # KEIL 5.27 工程选项文件(*.uvoptx)
            tpl = self.__env.get_template('keil_5_27_uvoptx.xml')
            uvoptx_name = prj_info['name'] + ".uvoptx"
            with open(os.path.join(prj_file_path, uvoptx_name), mode='w', encoding='utf-8') as f:
                f.write(tpl.render(project=prj_info, target=target_info))

            # KEIL 5.27 JLink 配置文件(JLinkSettings.ini)
            if str.lower(prj_info['debug']['tool']) == 'jlink':
                tpl = self.__env.get_template('keil_5_27_jlink_setting.ini')
                with open(os.path.join(prj_file_path, 'JLinkSettings.ini'), mode='w', encoding='utf-8') as f:
                    f.write(tpl.render(target=target_info))

    # 获取生成工程的名称
    def project_filepath(self, prj_info, prj_path) -> str:
        filename = prj_info['name'] + '.uvprojx'
        return os.path.join(prj_path, 'MDK-ARM', filename)
