import os
from enum import Enum, unique

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .. import Generator


# IAR 版本定义
@unique
class IARVersionType(Enum):
    V7 = 1      # IAR V7.x
    V8_32 = 2   # IAR V8.32+，也使用于其他V8.x版本，但是有可能报“broken option“错误，不影响使用


class IARGenerator(Generator):
    # Jinja2环境
    __env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
        autoescape=select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    # 生成工程接口
    def generate(self, prj_info, target_info, prj_path, version: IARVersionType, **kwargs):
        # --------------------- 路径处理 -----------------------
        # 项目文件路径
        prj_file_path = os.path.join(prj_path, 'EWARM')

        # 检查路径是否存在
        if not os.path.exists(prj_file_path):
            os.makedirs(prj_file_path)
        if not os.path.exists(os.path.join(prj_file_path, 'settings')):
            os.makedirs(os.path.join(prj_file_path, 'settings'))

        # ----------- 检查工程文件是否需要修改target配置 -----------
        # 检查工程是否需要覆盖默认的链接配置文件
        if prj_info['advanced_options']['iar_linker_cfg'] is not None:
            target_info['iar_linker_cfg'] = prj_info['advanced_options']['iar_linker_cfg']

        # 检查工程是否需要覆盖默认的烧写配置文件
        if prj_info['advanced_options']['iar_flasher_cfg'] is not None:
            target_info['iar_flasher_cfg'] = prj_info['advanced_options']['iar_flasher_cfg']

        # -------------------- 生成工程文件 ---------------------
        # IAR 8.32
        if version == IARVersionType.V8_32:
            # IAR 8.32 工作空间文件(*.eww)
            tpl = self.__env.get_template('iar_8_32_eww.xml')
            eww_name = 'Project.eww'
            with open(os.path.join(prj_file_path, eww_name), mode='w', encoding='utf-8') as f:
                f.write(tpl.render(project=prj_info, target=target_info))

            # IAR 8.32 工程文件(*.ewp)
            tpl = self.__env.get_template('iar_8_32_ewp.xml')
            ewp_name = prj_info['name'] + '.ewp'
            with open(os.path.join(prj_file_path, ewp_name), mode='w', encoding='utf-8') as f:
                f.write(tpl.render(project=prj_info, target=target_info))

            # IAR 8.32 工程调试选项文件(*.ewd)
            tpl = self.__env.get_template('iar_8_32_ewd.xml')
            ewd_name = prj_info['name'] + '.ewd'
            with open(os.path.join(prj_file_path, ewd_name), mode='w', encoding='utf-8') as f:
                f.write(tpl.render(project=prj_info, target=target_info))

            # IAR 8.32 JLink 配置文件(*.ini)
            if str.lower(prj_info['debug']['tool']) == 'jlink':
                jlink_setting_name = prj_info['name'] + '_' + prj_info['name'] + '.jlink'
                tpl = self.__env.get_template('iar_8_32_jlink_setting.ini')
                with open(os.path.join(prj_file_path, 'settings', jlink_setting_name), mode='w', encoding='utf-8') as f:
                    f.write(tpl.render(target=target_info))

        # IAR 7
        elif version == IARVersionType.V7:
            # IAR 7 工作空间文件(*.eww)
            tpl = self.__env.get_template('iar_7_eww.xml')
            eww_name = 'Project.eww'
            with open(os.path.join(prj_file_path, eww_name), mode='w', encoding='utf-8') as f:
                f.write(tpl.render(project=prj_info, target=target_info))

            # IAR 7 工程文件(*.ewp)
            tpl = self.__env.get_template('iar_7_ewp.xml')
            ewp_name = prj_info['name'] + '.ewp'
            f = open(os.path.join(prj_file_path, ewp_name), mode='w', encoding='utf-8')
            f.write(tpl.render(project=prj_info, target=target_info))
            f.close()

            # IAR 7 工程调试选项文件(*.ewd)
            tpl = self.__env.get_template('iar_7_ewd.xml')
            ewd_name = prj_info['name'] + '.ewd'
            with open(os.path.join(prj_file_path, ewd_name), mode='w', encoding='utf-8') as f:
                f.write(tpl.render(project=prj_info, target=target_info))

            # IAR 7 JLink 配置文件(*.ini)
            if str.lower(prj_info['debug']['tool']) == 'jlink':
                jlink_setting_name = prj_info['name'] + '_' + prj_info['name'] + '.jlink'
                tpl = self.__env.get_template('iar_7_jlink_setting.ini')
                with open(os.path.join(prj_file_path, 'settings', jlink_setting_name), mode='w', encoding='utf-8') as f:
                    f.write(tpl.render(target=target_info))

    # 获取生成工程的名称
    def project_filepath(self, prj_info, prj_path) -> str:
        filename = 'Project.eww'
        return os.path.join(prj_path, 'EWARM', filename)
