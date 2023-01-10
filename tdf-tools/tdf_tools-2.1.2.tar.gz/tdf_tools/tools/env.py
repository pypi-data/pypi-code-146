from environs import Env

from tdf_tools.tools.print import Print

# 通过 .env 文件定义以下字段调试用
# DEBUG=true
# WORKSPACE=/Users/imwcl/Desktop/2dfire/business_card/flutter_reset_module


class EnvTool:
    def is_debug() -> bool:
        try:
            env = Env()
            env.read_env()
            _debug = env.bool("TDFTOOLS_DEBUG")
            return _debug
        except:
            return False

    def workspace() -> str:
        try:
            env = Env()
            env.read_env()
            _workspace = env.str("TDFTOOLS_WORKSPACE")
            return _workspace
        except:
            return None
