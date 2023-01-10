from tdf_tools.tools.shell_dir import ProjectType, ShellDir
from tdf_tools.tools.translate.flutter.flutter_translate_tools import FlutterTranslateTools
from tdf_tools.tools.translate.ios.ios_translate import iOSTranslate
from tdf_tools.tools.translate.translate_lint import TranslateLint


class Translate:
    """
    国际化相关：tl translate -h 查看详情
    """

    def __init__(self) -> None:
        self.lint = TranslateLint()

    def start(self):
        """
        国际化相关：通过交互式的方式处理国际化
        """
        ShellDir.dirInvalidate()
        projectType = ShellDir.getProjectType()
        if projectType == ProjectType.FLUTTER:
            FlutterTranslateTools().translate()
        elif projectType == ProjectType.IOS:
            iOSTranslate().translate()

    def module(self, name):
        """
        国际化相关：指定模块进行国际化
        """
        ShellDir.dirInvalidate()
        projectType = ShellDir.getProjectType()
        if projectType == ProjectType.FLUTTER:
            FlutterTranslateTools().translate_module(name)
        elif projectType == ProjectType.IOS:
            iOSTranslate().translate_module(name)
        exit(0)

    def integrate(self):
        """
        国际化相关：整合所有组件的国际化文件到一个文件中，用来维护一份国际化文件
        """
        ShellDir.dirInvalidate()
        projectType = ShellDir.getProjectType()
        if projectType == ProjectType.FLUTTER:
            FlutterTranslateTools().integrate()
        elif projectType == ProjectType.IOS:
            iOSTranslate().integrate()
        exit(0)
