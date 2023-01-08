import os
import pkgutil
from inspect import stack
from logging import Logger, getLogger

from com.enovation.toolbox.excel_dashboard.excel_dashboarder import ExcelDashboarder

_logger: Logger = getLogger(__name__)

_logger.info(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

_str_the_widgets_sub_directory: str = os.path.join(
    os.path.dirname(__file__),
    ExcelDashboarder.const_str__sub_directory_for_widgets
)
_logger.info(f"\tDirectory '{_str_the_widgets_sub_directory}' will be screened to load widget modules.")

__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages([_str_the_widgets_sub_directory]):

    __all__.append(module_name)
    _module = loader.find_module(module_name).load_module(module_name)
    globals()[module_name] = _module
    _logger.info(f"\t-- {module_name}: added")

_logger.info(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning, after having loaded "
             f"'{len(__all__)}' modules.")
