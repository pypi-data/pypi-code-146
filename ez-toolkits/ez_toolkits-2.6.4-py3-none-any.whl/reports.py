from . import files, utils

'''
reports.logout()

    生成报告完成以后, 退出 Zabbix

return _image

    返回图片信息, 发邮件时使用
'''

class reports(object):

    # Zabbix Instance
    _zabbix = None

    # Files Instance
    _files = None

    # Image Object
    _image_dir = '.'
    _image_name_prefix = 'image'

    def __init__(self, zabbix, markdown_file, html_file, image_dir, image_name_prefix):
        ''' Initiation '''
        self._zabbix = zabbix
        self._files = files.files(markdown_file, html_file)
        self._image_dir = image_dir
        self._image_name_prefix = image_name_prefix

    def generic(
        self,
        pieces=None,
        hosts=None,
        time_from=None,
        time_till=None,
        item_keys=None,
        data_type=None,
        data_proc=None,
        title=None,
        description=None,
        number_type=None,
        number_unit=None,
        number_handling=None,
        table_header_title='Host',
        table_header_data='Data',
        sort_by_ip=None,
        image_cid=None,
        image_label=None,
        image_kind=None
    ):

        _history = []

        if utils.vTrue(item_keys, str):
            _history = utils.retry(10, self._zabbix.get_history_by_item_key, hosts, time_from, time_till, item_keys, data_type)

        if utils.vTrue(item_keys, list):
            for _item_key in item_keys:
                _history_slice = utils.retry(10, self._zabbix.get_history_by_item_key, hosts, time_from, time_till, _item_key, data_type)
                if _history_slice != None:
                    if callable(data_proc) == True:
                        _history_slice = data_proc(_history_slice)
                    _history += _history_slice

        if _history != None:

            _files_func = self._files.multiple_pieces

            if pieces == 'single':

                _files_func = self._files.single_piece

                for _data in _history:
                    if len(_data['history']) > 0:
                        _history_last = max(_data['history'], key=lambda i: i['clock'])
                        _data['history'] = _history_last

            _image = {
                'cid': '{}'.format(image_cid),
                'path': '{}/{}_{}.png'.format(self._image_dir, self._image_name_prefix, image_cid),
                'label': image_label,
                'kind': image_kind
            }

            _files_result = _files_func(
                title=title,
                description=description,
                data=_history,
                image=_image,
                number_type=number_type,
                number_unit=number_unit,
                number_handling=number_handling,
                table_header_title=table_header_title,
                table_header_data=table_header_data,
                sort_by_ip=sort_by_ip
            )

            if _files_result == True:
                return _image
            else:
                return None

        else:

            return None

    def system_interface(self, hosts, interfaces, time_from, time_till, direction='in'):
        ''' System Interface '''

        _direction_name = 'Received'
        _direction_alias = 'received'
        _direction_info = '接收数据'

        if direction == 'out':
            _direction_name = 'Sent'
            _direction_alias = 'sent'
            _direction_info = '发送数据'

        _history = utils.retry(10, self._zabbix.get_history_by_interface, hosts, interfaces, time_from, time_till, direction)

        if utils.vTrue(_history, list):

            _image = {
                'cid': 'system_interface_'.format(_direction_alias),
                'path': '{}/{}_system_interface_{}.png'.format(self._image_dir, self._image_name_prefix, _direction_alias)
            }

            _ = self._files.multiple_pieces(
                title='System Interface {}'.format(_direction_name),
                description='说明: 网卡**{}**的速度'.format(_direction_info),
                data=_history,
                image=_image,
                number_type='int',
                number_unit='Kbps',
                number_handling=utils.divisor_1000,
                sort_by_ip=True
            )

            if _ == True:
                return _image
            else:
                return None

        else:

            return None

    def base_system(self, hosts, time_from, time_till, interfaces=None):

        # Images
        _images = []

        # System CPU utilization
        _image = self.generic(
            hosts=hosts,
            time_from=time_from,
            time_till=time_till,
            item_keys='system.cpu.util',
            data_type=0,
            title='System CPU utilization',
            description='说明: 系统 CPU 使用率',
            number_type='float',
            number_unit='%',
            sort_by_ip=True,
            image_cid='system_cpu_utilization'
        )
        if _image != None:
            _images.append(_image)

        # System Memory utilization
        _image = self.generic(
            hosts=hosts,
            time_from=time_from,
            time_till=time_till,
            item_keys='vm.memory.utilization',
            data_type=0,
            title='System Memory utilization',
            description='说明: 系统 内存 使用率',
            number_type='float',
            number_unit='%',
            sort_by_ip=True,
            image_cid='system_memory_utilization'
        )
        if _image != None:
            _images.append(_image)

        # System root partition utilization
        _image = self.generic(
            pieces='single',
            hosts=hosts,
            time_from=time_from,
            time_till=time_till,
            item_keys='vfs.fs.size[/,pused]',
            data_type=0,
            title='System root partition utilization',
            description='说明: 系统 根目录(/) 使用率',
            number_type='float',
            number_unit='%',
            table_header_data='Used',
            sort_by_ip=True,
            image_cid='system_root_partition_utilization',
            image_label='Used (%)',
            image_kind='barh'
        )
        if _image != None:
            _images.append(_image)

        if interfaces != None:

            # System Interface Received
            _image = self.system_interface(hosts, interfaces, time_from, time_till, 'in')
            if _image != None:
                _images.append(_image)

            # System Interface Sent
            _image = self.system_interface(hosts, interfaces, time_from, time_till, 'out')
            if _image != None:
                _images.append(_image)

        return _images

    def base_generic(self, hosts, time_from, time_till, items=None):

        # Images
        _images = []

        if items != None:

            for _item in items:

                # CPU utilization
                _image = self.generic(
                    hosts=hosts,
                    time_from=time_from,
                    time_till=time_till,
                    item_keys=_item['keys'][0],
                    data_type=_item['types'][0],
                    data_proc=_item.get('data_proc'),
                    title='{} CPU utilization'.format(_item['name']),
                    description='说明: {} CPU 使用率'.format(_item['name']),
                    number_type='float',
                    number_unit='%',
                    table_header_title=_item.get('table_header_title', 'Host'),
                    table_header_data=_item.get('table_header_data', 'Data'),
                    sort_by_ip=True,
                    image_cid='{}_cpu_utilization'.format(_item['alias'])
                )
                if _image != None:
                    _images.append(_image)

                # Memory used (RSS)
                _image = self.generic(
                    hosts=hosts,
                    time_from=time_from,
                    time_till=time_till,
                    item_keys=_item['keys'][1],
                    data_type=_item['types'][1],
                    data_proc=_item.get('data_proc'),
                    title='{} Memory used (RSS)'.format(_item['name']),
                    description='说明: {} 内存 使用量'.format(_item['name']),
                    number_type='int',
                    number_unit='MB',
                    number_handling=utils.divisor_square_1024,
                    table_header_title=_item.get('table_header_title', 'Host'),
                    table_header_data=_item.get('table_header_data', 'Data'),
                    sort_by_ip=True,
                    image_cid='{}_memory_used_rss'.format(_item['alias'])
                )
                if _image != None:
                    _images.append(_image)

        return _images
