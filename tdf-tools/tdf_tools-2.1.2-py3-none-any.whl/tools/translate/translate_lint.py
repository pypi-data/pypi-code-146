from tdf_tools.tools.shell_dir import ProjectType, ShellDir
from tdf_tools.tools.translate.flutter.flutter_translate_lint import (
    FlutterTranslateLint,
)
from tdf_tools.tools.translate.ios.ios_translate_lint import iOSTranslateLint


class TranslateLint:
    """
    国际化相关：检测源码中是否还有没国际化的文案
    """

    def start(self):
        """
        以交互的方式选择需要 lint 的模块
        """
        ShellDir.dirInvalidate()
        projectType = ShellDir.getProjectType()
        if projectType == ProjectType.FLUTTER:
            FlutterTranslateLint.start()
        elif projectType == ProjectType.IOS:
            iOSTranslateLint.start()

    def module(self, name: str):
        """
        指定模块 lint
        """
        ShellDir.dirInvalidate()
        projectType = ShellDir.getProjectType()
        if projectType == ProjectType.FLUTTER:
            FlutterTranslateLint.module(name)
        elif projectType == ProjectType.IOS:
            iOSTranslateLint.module(name)

    def path(self, path: str):
        """
        指定模块路径 lint，路径为 lib 路径
        """
        ShellDir.dirInvalidate()
        projectType = ShellDir.getProjectType()
        if projectType == ProjectType.FLUTTER:
            FlutterTranslateLint.path(path)
        elif projectType == ProjectType.IOS:
            iOSTranslateLint.path(path)
