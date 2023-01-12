"""gateway 的类型"""

from vxsched import vxengine
from vxutils import vxWrapper, logger


@vxengine.event_handler("__init__")
def gateway_init(context, event) -> None:
    db_settings = context.settings.get("database", None)
    if db_settings is None:
        logger.warning("没有正确配置数据库，请核实后重新运行...")
        return

    context.db = vxWrapper.init_by_config(context.settings.database)
