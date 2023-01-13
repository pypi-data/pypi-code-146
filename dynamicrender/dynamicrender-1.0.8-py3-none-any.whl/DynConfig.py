from loguru import logger
from os import path, getcwd
from pydantic import BaseModel
from typing import Optional, Union, Tuple
from zipfile import ZipFile


class DynColor(BaseModel):
    dyn_blue: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]]
    dyn_green: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]]
    dyn_pink: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]]
    dyn_black: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]]
    dyn_white: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]]
    dyn_gray: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]]
    dyn_silver_gray: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]]


class DynFontPath(BaseModel):
    text: str
    extra_text: str
    emoji: str


class DynSize(BaseModel):
    uname: int
    text: int
    sub_text: int
    emoji: int
    title: int
    sub_title: int


class ConfigInit:
    def __init__(self, data_path: Optional[str] = None, font_path: Union[None, str, dict] = None) -> None:
        """Initialize configuration

        Parameters
        ----------
        cache_path : Optional[str]

            The path to the cache directory. If the value is None, the program's run directory is used by default, by default None

        font_path : Union[None,str,Dict]

            If the type of the parameter is str, the font_path will be the path to the text font.

            If the type of the  parameter is dict, the font_path must be like below:

            {"text":path to text font,"extra_text":text":path to extra_text font,"emoji": path to emoji font}.

            If the value is None, the font in the cache directory is used by default, by default None
        """
        self.data_path: str = data_path
        self.text_font_path: Union[str, dict, None] = font_path
        self.static_path: str = None
        self.dyn_color: Optional[DynColor] = None
        self.dyn_font: Optional[DynFontPath] = None
        self.dy_size: Optional[DynSize] = None
        self.check_cache_file()
        self.set_user_font()
        self.set_size()
        self.set_color()

    def check_cache_file(self) -> None:
        # 查询是否有data_path参数
        # 没有的话静态文件目录就设置在程序的运行目录
        if self.data_path is None:
            self.set_font_and_static_path()

        # 有data_path参数参数
        else:
            # 确认当前运行的文件所在的目录
            current_dir = path.dirname(path.abspath(__file__))
            # 如果data_path存在
            if path.exists(self.data_path):
                # 设置静态文件的目录
                static_path = path.join(self.data_path, "Static")
                # 如果静态文件的目录不存在就直接解压文件
                if not path.exists(static_path):
                    logger.info("未检测到static目录")
                    logger.info("使用用户传入路径创建static目录中...")
                    file = ZipFile(path.join(current_dir, "Static.zip"))
                    file.extractall(self.data_path)
                    logger.info("static目录创建成功")
                # 设置所有字体目录
                self.dyn_font = DynFontPath(**{
                    "text": path.join(static_path, "Font", "HanaMinA.ttf"),
                    "extra_text": path.join(static_path, "Font", "Unifont.ttf"),
                    "emoji": path.join(static_path, "Font", "nte.ttf")
                })
                # 设置静态文件的目录
                self.static_path = static_path
            # 如果data_path卜存在,直接使用程序的运行目录
            else:
                self.set_font_and_static_path()

    def set_user_font(self) -> None:

        if self.text_font_path is not None:
            if isinstance(self.text_font_path, str):
                if path.exists(self.text_font_path):
                    self.dyn_font.text = self.text_font_path
                else:
                    logger.warning("用户字体文件不存在，将使用默认字体")
            elif isinstance(self.text_font_path, dict):
                try:
                    self.dyn_font = DynFontPath(**self.text_font_path)
                except Exception as e:
                    logger.warning("传入字体路径信息错误，将使用默认字体")
            else:
                logger.warning("传入错误的字体路径信息格式，将使用默认字体")

    def set_font_and_static_path(self) -> None:
        # 确定程序的运行目录的路径
        program_running_path = getcwd()
        # 当前文件所在的目录的路径
        current_dir = path.dirname(path.abspath(__file__))
        # 静态文件的路径
        static_path = path.join(program_running_path, "Static")
        # 如果不存在静态目录将自带的压缩文件解压过去
        if not path.exists(static_path):
            logger.info("未检测到static目录")
            logger.info("用户未传入data路径,将在程序运行目录创建static目录")
            logger.info("创建static目录中...")
            file = ZipFile(path.join(current_dir, "Static.zip"))
            file.extractall(program_running_path)
            logger.info("static目录创建成功")

        # 设置所有字体的路径
        self.dyn_font = DynFontPath(**{
            "text": path.join(static_path, "Font", "HanaMinA.ttf"),
            "extra_text": path.join(static_path, "Font", "Unifont.ttf"),
            "emoji": path.join(static_path, "Font", "nte.ttf")
        })
        # 设置静态目录所在的路径
        self.static_path = static_path

    def set_color(self, kargs: Optional[dict] = None) -> None:
        if not kargs:
            self.dyn_color = DynColor(**{
                "dyn_blue": "#00a1d6",
                "dyn_green": "#3ce84e",
                "dyn_pink": "#fb6b94",
                "dyn_black": "black",
                "dyn_white": "#ffffff",
                "dyn_gray": "#f4f5f7",
                "dyn_silver_gray": "#99a2aa"
            })
        else:
            self.dyn_color = DynColor(**kargs)

    def set_size(self, kargs: Optional[dict] = None) -> None:
        if not kargs:
            self.dy_size = DynSize(**{
                "uname": 45,
                "text": 40,
                "sub_text": 35,
                "title": 30,
                "sub_title": 20,
                "emoji": 109
            })
        else:
            self.dy_size = DynSize(**kargs)
