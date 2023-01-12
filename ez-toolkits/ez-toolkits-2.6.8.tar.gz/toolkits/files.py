import re
from copy import deepcopy
from socket import inet_aton

from loguru import logger

from . import plots, utils


class files(object):
    ''' 文件 '''

    ''' Markdown 和 HTML 文件 '''
    _markdown_file, _html_file = None, None

    def __init__(self, markdown_file=None, html_file=None):
        ''' Initiation '''
        self._markdown_file = markdown_file
        self._html_file = html_file

    '''
        def multiple_pieces(
            self,
            title='',
            description='',
            data=[],
            image={},
            number_type=None,
            number_unit=None,
            number_handling=None,
            sort_by_ip=False
        ):

    '''

    def unavailable_hosts(self, hosts=[], **kwargs):
        ''' 异常服务器处理 '''

        logger.success('unavailable hosts | start')

        try:

            # 如果存在异常服务器, 则写入文件
            if hosts != []:
                with open(self._markdown_file, 'a') as _file:
                    _file.writelines([
                        '\n',
                        '**异常服务器:**\n',
                        '\n',
                    ])
                    for _host in hosts:
                        _file.write('- <span style="color: red">{}</span>\n'.format(_host))

            logger.success('unavailable hosts | end')

            return True

        except Exception as e:
            logger.exception(e)
            logger.error('unavailable hosts | end')
            return False

    def single_piece(
        self,
        title='',
        description='',
        data=[],
        image={},
        number_type=None,
        number_unit=None,
        number_handling=None,
        table_header_title='Host',
        table_header_data='Data',
        sort_by_ip=False,
        **kwargs
    ):
        ''' 单条数据 '''

        match True:
            case True if type(title) != str or title == '':
                logger.error('ERROR!! title is not string or none')
                return None
            case True if type(description) != str or description == '':
                logger.error('ERROR!! description is not string or none')
                return None
            case True if type(data) != list or data == []:
                logger.error('ERROR!! data is not list or none')
                return None
            case True if type(image) != dict or image == 0:
                logger.error('ERROR!! image is not dictionary or none')
                return None

        # 拷贝数据
        _data = deepcopy(data)

        # 根据 IP 排序
        if sort_by_ip == True:
            _ips = utils.list_sort_by_key([_host['interfaces'][0]['ip'] for _host in _data], key=inet_aton, deduplication=True)
            _data = [_host for _ip in _ips for _host in _data if _ip == _host['interfaces'][0]['ip']]

        logger.success('{} | start'.format(title))

        try:

            # 初始化变量
            _data_idx, _data_result = [], []

            for _host in _data:
                _value = None
                if _host.get('history') != None:
                    match True:
                        case True if number_type == 'int':
                            _value = int(_host['history']['value'])
                        case True if number_type == 'float':
                            _value = float(_host['history']['value'])
                        case _:
                            _value = _host['history']['value']
                _data_idx.append(_host['name'])
                _data_result.append(number_handling(_value) if callable(number_handling) == True else _value)

            # 判断结果
            if (len(_data_idx) > 0) and (image != {}):

                with open(self._markdown_file, 'a') as _file:

                    _file.writelines([
                        '\n',
                        '## {}\n'.format(title),
                        '\n',
                        '{}\n'.format(description),
                        '\n',
                        '| {} | {} |\n'.format(table_header_title, table_header_data),
                        '| --- | --: |\n'
                    ])

                    for _i, _v in enumerate(_data_idx):
                        _file.write('| {0} | {1:.2f}{2} |\n'.format(_v, _data_result[_i], number_unit))

                    _plot_image = {
                        'title': title,
                        'kind': image['kind'],
                        'size': (20, (len(_data_idx) / 5) * 2),
                        'path': image['path'],
                        'dpi': 300,
                        'width': 0.8
                    }

                    _plot_result = plots.bar({image['label']: _data_result}, _data_idx, _plot_image)

                    # '<img src="cid:{}">\n'.format(_image['cid'])
                    # '![](cid:{})\n'.format(_image['cid'])
                    # 图片显示大小: 仅设置 width, height 自适应
                    if _plot_result == True:
                        _file.writelines([
                            '\n',
                            '<img src="cid:{}" width="1000px">\n'.format(image['cid'])
                        ])

            logger.success('{} | end'.format(title))

            return True

        except Exception as e:
            logger.exception(e)
            logger.error('{} | end'.format(title))
            return False

    def multiple_pieces(
        self,
        title='',
        description='',
        data=[],
        image={},
        number_type=None,
        number_unit=None,
        number_handling=None,
        table_header_title='Host',
        sort_by_ip=False,
        **kwargs
    ):
        ''' 多条数据 '''

        match True:
            case True if type(title) != str or title == '':
                logger.error('ERROR!! title is not string or none')
                return None
            case True if type(description) != str or description == '':
                logger.error('ERROR!! description is not string or none')
                return None
            case True if type(data) != list or data == []:
                logger.error('ERROR!! data is not list or none')
                return None
            case True if type(image) != dict or image == 0:
                logger.error('ERROR!! image is not dictionary or none')
                return None

        # 拷贝数据
        _data = deepcopy(data)

        # 根据 IP 排序
        if sort_by_ip == True:
            _ips = utils.list_sort_by_key([_host['interfaces'][0]['ip'] for _host in _data], key=inet_aton, deduplication=True)
            _data = [_host for _ip in _ips for _host in _data if _ip == _host['interfaces'][0]['ip']]

        logger.success('{} | start'.format(title))

        try:

            # 初始化变量 (用于 pandas 处理数据)
            _data_idx, _data_max, _data_avg, _data_min = [], [], [], []

            # 提取数据
            for _host in _data:
                _num_max, _num_avg, _num_min = utils.nums_mam([_x['value'] for _x in _host['history']], number_type)
                if (_num_max != None) and (_num_avg != None) and (_num_min != None):
                    _data_idx.append(_host['name'])
                    _data_max.append(number_handling(_num_max) if callable(number_handling) == True else _num_max)
                    _data_avg.append(number_handling(_num_avg) if callable(number_handling) == True else _num_avg)
                    _data_min.append(number_handling(_num_min) if callable(number_handling) == True else _num_min)

            # 判断结果
            if (len(_data_idx) > 0) and (image != None):

                # 写入文件
                with open(self._markdown_file, 'a') as _file:

                    _file.writelines([
                        '\n',
                        '## {}\n'.format(title),
                        '\n',
                        '{}\n'.format(description),
                        '\n',
                        '| {} | Min | Average | Max |\n'.format(table_header_title),
                        '| --- | --: | --: | --: |\n'
                    ])

                    for _i, _v in enumerate(_data_idx):
                        _file.write('| {0} | {1:.2f}{4} | {2:.2f}{4} | {3:.2f}{4} |\n'.format(_v, _data_min[_i], _data_avg[_i], _data_max[_i], number_unit))

                    _plot_data = [
                        {'key': 'max', 'label': 'Max', 'kind': 'barh', 'data': _data_max, 'color': '#E74C3C', 'width': 0.8},
                        {'key': 'avg', 'label': 'Avg', 'kind': 'barh', 'data': _data_avg, 'color': '#3498DB', 'width': 0.8},
                        {'key': 'min', 'label': 'Min', 'kind': 'barh', 'data': _data_min, 'color': '#2ECC71', 'width': 0.8}
                    ]

                    _plot_image = {
                        'title': title,
                        'size': (20, (len(_data_idx) / 5) * 2),
                        'path': image['path'],
                        'dpi': 300
                    }

                    _plot_result = plots.bar_cover(_plot_data, _data_idx, _plot_image)

                    # '<img src="cid:{}">\n'.format(_image['cid'])
                    # '![](cid:{})\n'.format(_image['cid'])
                    # 图片显示大小: 仅设置 width, height 自适应
                    if _plot_result == True:
                        _file.writelines([
                            '\n',
                            '<img src="cid:{}" width="1000px">\n'.format(image['cid'])
                        ])

            logger.success('{} | end'.format(title))

            return True

        except Exception as e:
            logger.exception(e)
            logger.error('{} | end'.format(title))
            return False

    def handling_html(self, *args, **kwargs):
        ''' 处理 HTML '''

        logger.success('handling HTML | start')

        try:

            if utils.stat(self._html_file, 'file'):

                # HTML内容
                _html_lines = None

                # 移除自带样式
                with open(self._html_file, "r") as _html_input:
                    _html_lines = _html_input.readlines()
                    del _html_lines[7:161]

                # 遍历内容
                for _i, _v in enumerate(_html_lines):

                    # 移除表格宽度
                    _table_width = re.compile(r'<table style="width:100%;">')
                    if len(_table_width.findall(_v)) > 0:
                        _html_lines[_i] = re.sub(_table_width, '<table>', _v)

                    # 移除 colgroup
                    _colgroup = re.compile(r'</?colgroup>')
                    if len(_colgroup.findall(_v)) > 0:
                        _html_lines[_i] = re.sub(_colgroup, '', _v)

                    # 移除列宽度
                    _col_width = re.compile(r'<col style="width: .*%" />')
                    if len(_col_width.findall(_v)) > 0:
                        _html_lines[_i] = re.sub(_col_width, '', _v)

                # 写入文件
                with open(self._html_file, "w") as _html_output:
                    _html_output.writelines(_html_lines)

            logger.success('handling HTML | end')
            return True

        except Exception as e:
            logger.exception(e)
            logger.error('handling HTML | end')
            return False

    def markdown_to_html(self, dir='.', **kwargs):
        '''
        Markdown to HTML
        使用 MacDown 生成 HTML, 然后提取样式到 markdown.html
        pandoc 生成的 HTML 默认 max-width: 36em, 如果表格内容很长, 会导致表格样式难看
        所以在 markdown.html 的 body{...} 中添加配置 max-width: unset, 解决内容过长的样式问题
        所有 a 标签添加 text-decoration: none; 去除链接下划线
        pandoc --no-highlight -s --quiet -f markdown -t html -H markdown.html -o history.html history.md
        '''

        logger.success('markdown to html | start')

        try:

            _result = utils.bash(
                'pandoc --no-highlight -s --quiet -f markdown -t html -H {}/markdown.html -o {} {}'.format(dir, self._html_file, self._markdown_file)
            )

            if _result != None and _result.returncode == 0:
                logger.success('markdown to html | end')
                return True
            else:
                logger.error('markdown to html | end')
                return False

        except Exception as e:
            logger.exception(e)
            logger.error('markdown to html | end')
            return False
