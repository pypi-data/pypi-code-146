#pylint: disable=line-too-long
translation = {
"Top Color": "顶部颜色",
"Top Opacity": "顶部透明度",
"Bottom Color": "底部颜色",
"Bottom Opacity": "底部透明度",
"Clear": "透明",
"Language": "语言",
"LanguageSettingHint":
"语言设置将会在重启Visual Sponge后生效",
"Gitee Page": "Gitee主页",
"Official Website": "官方网站",
"Group Page": "课题组主页",
"Command Help": "命令帮助",
"White": "白色",
"Cyan": "青色",
"Black": "黑色",
"Submit": "提交",
"Cancel": "取消",
"Filename": "文件名",
"Format": "格式",
"Hide": "隐藏",
"Show": "显示",
"Delete": "删除",
"Default": "默认",
"forward": "前向",
"backward": "后向",
"backAndForth": "往复",
"Play": "播放",
"Stop": "停止",
"Model": "模型",
"Atom": "原子",
"Frame": "帧",
"Really quit?": "确定退出?",
"File": "文件",
"Display": "显示",
"Settings": "设置",
"placeholder": "占位",
"Help": "帮助",
"Contact Us": "联系我们",
"WelcomeHint": "欢迎使用 Visual Sponge！",
"bgSelectHint": "选择顶部和底部颜色和不透明度或直接输入RGBA函数生成背景颜色",
" Version": "版本",
"addLabelAlert": '请在添加标签前选择原子',
"formCompleteAlert": "请先完成上一个表格",
"MovieHint": "正在录制画幕，请等待完成...",
"MovieOrPrintScreenFinishedHint": "完成。文件已保存为：\n",
"PrintScreenHint": "正在截屏，请等待完成...",
"Open Trajectory File": "打开轨迹文件",
"Open Model File": "打开模型文件",
"Append Trajectory": "追加轨迹",
"Print Screen": "截屏",
"Make Movie": "制作视频",
"Save Configuration": "保存配置",
"Background Color": "背景颜色",
" is not accissible (invalid directory)": "不可访问（目录无效）",
" is not accissible (permission denied)": "不可访问（权限不足）",
"RGBA function:": "RGBA函数：",
"Display Style": "显示样式",
"Style": "样式",
"line": "线形",
"sphere": "球状",
"stick": "棍状",
"cross": "星状",
"cartoon": "卡通",
"Selection": "选择",
"scale": "比例",
"radius": "半径",
"thichness": "厚度",
"Ribbon": "带状",
"Tube": "管状",
"Arrow": "箭头",
"AtomSelectionHint": "<a target=_blank href=http://3dmol.csb.pitt.edu/doc/types.html#AtomSelectionSpec>3dmol.js</a>的原子选择方式来确定需要选择的原子</br>关键词：残基名(resn) 坐标(x),(y),(z) 元素(elem) 残基序号(resi) 原子名(atom) 序号(serial) 成键数(bonds) 模型(model)</br>例: {model: 0, atom: 'OW', byres: true}",
"Invalid Input": "无效的输入",
"New": "新建",
"Label": "标签",
"None": "无",
"Label atom": "标记原子",
"Label bond": "标记键长",
"Label angle": "标记键角",
"Label dihedral": "标记二面角",
"Clear labels": "清除标签",
"Click function": "点击功能",
"Label info": "标签信息",
"Residue name": "残基名",
"Residue index": "残基序号",
"Atom name": "原子名",
"Atom index": "原子序号",
"Atom coordinate": "原子坐标",
"Angle in radians": "弧度制角",
"Auxiliary line": "辅助线",
"Zoom": "居中放大",
"Center": "居中",
"Re-render": "重渲染",
}

translation.update({
"HelpHelpHint":
"""使用 HELP(命令) 来获取该命令的消息帮助
    例子:
        HELP("HELP")
    所有可用的命令: """,
"CommandHelpHelp":
"""HELP(command=None)
    给出命令的帮助

    参数 command：需要帮助的命令的字符串
    返回：命令的帮助""",
"CommandHelpConfigure":
"""CONFIGURE(section, option, value=None)
    获得或设置配置文件中的选项值

    参数 section：选项所处的section
    参数 option：选项名
    参数 value：如果不是None，更改选项的值
    返回： 选项值""",
"CommandHelpDefault":
"""DEFAULT(mid)
    将mid号模型设为默认模型

    参数 mid：模型的id
    返回：默认模型""",
"CommandHelpDelete":
"""DELETE(obj, id_)
    删除obj的id_号实例

    参数 obj：删除的对象，目前只支持模型（Model）
    参数 id_：删除的编号
    返回：被删除的实例""",
"CommandHelpHide":
"""HIDE(obj, id_)
    隐藏obj的id_号实例

    参数 obj：隐藏的对象，目前只支持模型（Model）
    参数 id_：隐藏的编号
    返回：被隐藏的实例""",
"CommandHelpModel":
"""MODEL(m, format_=None, **kwargs)
    加载模型

    参数 m：加载的模型
    参数 format_：模型的格式
    返回：加载的模型""",
"CommandHelpMovie":
"""MOVIE(filename, fps=60, bitRate=8500000, start=0, stop=-1, stride=1, interval=100)
    制作动画

    参数 filename：保存动画的地址。文件格式将会根据后缀名猜测
    参数 fps：动画的帧率
    参数 bitRate：动画的比特率
    参数 start：动画开始帧
    参数 stop：动画结束帧，为负数时则为倒数第|stop|帧
    参数 stride：动画每隔stride帧轨迹动一次
    参数 interval：轨迹每隔interval毫秒动1次
    返回：动画文件的地址""",
"CommandHelpPrintscreen":
"""PRINTSCREEN(filename)
    截图

    参数 filename：保存截图的地址。文件格式将会根据后缀名猜测
    返回：文件的地址""",
"CommandHelpShow":
"""SHOW(obj, id_)
    展示obj的id_号实例

    参数 obj：展示的对象，目前只支持模型（Model）
    参数 id_：展示的编号
    返回：被展示的实例""",
"CommandHelpTraj":
"""TRAJ(traj, format_=None, m=None, append=False, **kwargs):
    加载轨迹

    参数 traj：轨迹
    参数 format_：轨迹的格式
    参数 m：轨迹加载的模型。如果为None，则使用默认模型（Model.WORKING_MODEL）
    参数 append：轨迹是添加到原有的轨迹还是直接替代
    返回：加载轨迹的模型""",
"CommandHelpVersion":
"""VERSION()
    给出版本信息

    返回：版本信息""",
})
