import time
from copy import deepcopy

import requests
from loguru import logger

from .utils import list_dict_sorted_by_key, vTrue


class api(object):
    ''' API '''

    ''' Zabbix API URL, User Login Result '''
    _zabbix_api_url, _zabbix_auth, _zabbix_version = None, None, None

    '''
    https://www.zabbix.com/documentation/current/en/manual/api#performing-requests
    The request must have the Content-Type header set to one of these values:
        application/json-rpc, application/json or application/jsonrequest.
    '''
    _header = {'Content-Type': 'application/json-rpc'}

    def __init__(self, zabbix_api_url, zabbix_username, zabbix_password, zabbix_version=None):
        ''' Initiation '''
        self._zabbix_api_url = zabbix_api_url
        _response = None
        if zabbix_version == 5.0:
            _response = self.request('user.login', {'user': zabbix_username, 'password': zabbix_password})
        else:
            _response = self.request('user.login', {'username': zabbix_username, 'password': zabbix_password})
        self._zabbix_auth = _response['result']
        self._zabbix_version = zabbix_version

    def request(self, method, params=None, **kwargs):
        '''
        Request

            request 相关的方法, 除了 logout 方法, 其它方法一律不添加 try, 使用 utils.retry 控制

        Request Data

            https://www.zabbix.com/documentation/current/en/manual/api#authentication

            id - an arbitrary identifier of the request
            id - 请求标识符, 这里使用UNIX时间戳作为唯一标示
        '''

        _data = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params,
            'auth': self._zabbix_auth,
            'id': int(time.time())
        }
        _response = requests.post(self._zabbix_api_url, headers=self._header, json=_data, timeout=10, **kwargs)

        return _response.json()

    def logout(self):
        ''' User Logout '''
        try:
            return self.request('user.logout', [])
        except Exception as e:
            logger.exception(e)
            return None

    def logout_exit(self, str='Error'):
        ''' Logout and Exit '''
        logger.info(str)
        try:
            self.logout()
        except:
            exit(1)
        exit(1)

    def get_ids_by_template_name(self, name='', **kwargs):
        '''
        Get ids by template name

            name: string/array
            example: 'Linux by Zabbix agent' / ['Linux by Zabbix agent', 'Linux by Zabbix agent active']

            如果 name 为 '' (空), 返回所有 template id
        '''
        _response = self.request('template.get', {'output': 'templateid', 'filter': {'name': name}})
        if vTrue(_response, dict) and vTrue(_response['result'], list):
            return [i['templateid'] for i in _response['result']]
        else:
            return None

    def get_ids_by_hostgroup_name(self, name='', **kwargs):
        '''
        Get ids by hostgroup name

            name: string/array
            example: 'Linux servers' / ['Linux servers', 'Discovered hosts']

            如果 name 为 '' (空), 返回所有 hostgroup id
        '''
        _response = self.request('hostgroup.get', {'output': 'groupid', 'filter': {'name': name}})
        if vTrue(_response, dict) and vTrue(_response.get('result', []), list):
            return [i['groupid'] for i in _response['result']]
        else:
            return None

    def get_hosts_by_template_name(self, name='', output='extend', **kwargs):
        '''
        Get hosts by template name

            name: string/array
            example: 'Linux by Zabbix agent' / ['Linux by Zabbix agent', 'Linux by Zabbix agent active']

            如果 name 为 '' (空), 返回所有 host
        '''
        _response = self.request('template.get', {'output': ['templateid'], 'filter': {'host': name}})
        if vTrue(_response, dict) and vTrue(_response.get('result', []), list):
            _ids = [i['templateid'] for i in _response['result']]
            _hosts = self.request('host.get', {'output': output, 'templateids': _ids, **kwargs})
            if vTrue(_hosts, dict) and vTrue(_hosts.get('result', []), list):
                return _hosts['result']
            else:
                return None
        else:
            return None

    def get_hosts_by_hostgroup_name(self, name='', output='extend', **kwargs):
        '''
        Get hosts by hostgroup name

            name: string/array
            example: 'Linux servers' / ['Linux servers', 'Discovered hosts']

            如果 name 为 '' (空), 返回所有 hosts
        '''
        _ids = self.get_ids_by_hostgroup_name(name)
        if _ids == []:
            return None
        _hosts = self.request('host.get', {'output': output, 'groupids': _ids, **kwargs})
        if vTrue(_hosts, dict) and vTrue(_hosts.get('result', []), list):
            return _hosts['result']
        else:
            return None

    def get_interface_by_host_id(self, hostid='', output='extend', **kwargs):
        '''
        Get interface by host id

            hostids: string/array
            example: '10792' / ['10792', '10793']

            如果 name 为 '' (空), 则返回 []
        '''
        _response = self.request('hostinterface.get', {'output': output, 'hostids': hostid})
        if vTrue(_response, dict) and vTrue(_response.get('result', []), list):
            return _response['result']
        else:
            return None

    def available_hosts(self, hosts=[], **kwargs):
        ''' 可用服务器 '''

        # 可用服务器, 不可用服务器
        _available_hosts, _unavailable_hosts = [], []

        # 服务器排查
        for _host in hosts:
            if _host['interfaces'][0]['available'] != '1':
                _unavailable_hosts.append(_host['name'])
            else:
                _available_hosts.append(_host)

        return _available_hosts, _unavailable_hosts

    def get_history_by_item_key(self, hosts=[], time_from=0, time_till=0, item_key='', data_type=3, **kwargs):
        '''
        1. 根据 item key 获取 item id, 通过 item id 获取 history
        2. 根据 host 的 item id 和 history 的 item id 将数据提取为一个 history list
        3. 根据 history list 中的 clock 排序, 然后将 history list 整合到 host 中
        4. 返回包含有 item key, item id 和 history list 的 host 的 host list

        通过 Item Key 获取 Item history

            hosts: 主机列表
            time_from: 开始时间
            time_till: 结束时间
            item_key: Item Key
            data_type: 数据类型

        参考文档:

            https://www.zabbix.com/documentation/6.0/en/manual/api/reference/history/get

        history

            0 - numeric float
            1 - character
            2 - log
            3 - numeric unsigned
            4 - text

            Default: 3

        默认数据类型是 numeric unsigned (整数), 如果 history.get 返回的数据为 None, 有可能是 data_type 类型不对
        '''

        match True:
            case True if type(hosts) != list or hosts == []:
                logger.error('ERROR!! hosts is not list or none')
                return None
            case True if type(time_from) != int or time_from == 0:
                logger.error('ERROR!! time_from is not integer or zero')
                return None
            case True if type(time_till) != int or time_till == 0:
                logger.error('ERROR!! time_till is not integer or zero')
                return None
            case True if type(item_key) != str or item_key == '':
                logger.error('ERROR!! item_key is not string or none')
                return None

        # 初始化变量
        # _item_ids 获取历史数据时使用
        # _item_history 历史数据集合, 最后返回
        _item_ids, _item_history = [], []

        '''
        Deep Copy (拷贝数据)
        父函数的变量是 list 或者 dict 类型, 父函数将变量传递个子函数, 如果子函数对变量数据进行了修改, 那么父函数的变量的数据也会被修改
        为了避免出现这种问题, 可以使用 Deep Copy 拷贝一份数据, 避免子函数修改父函数的变量的数据
        '''
        _hosts = deepcopy(hosts)

        # ----------------------------------------------------------------------------------------------------

        # Get Item
        _hostids = [i['hostid'] for i in _hosts]
        _item_params = {
            'output': ['name', 'itemid', 'hostid'],
            'hostids': _hostids,
            'filter': {'key_': item_key}
        }
        _items = self.request('item.get', _item_params)

        # ----------------------------------------------------------------------------------------------------

        # 因为 history 获取的顺序是乱的, 为了使输出和 hosts 列表顺序一致, 将 Item ID 追加到 hosts, 然后遍历 hosts 列表输出
        if vTrue(_items, dict) and vTrue(_items.get('result', []), list):
            for _host in _hosts:
                _item = next((_item_object for _item_object in _items['result'] if _host['hostid'] == _item_object['hostid']), '')
                if vTrue(_item, dict) and _item.get('itemid') != None:
                    _host['itemkey'] = item_key
                    _host['itemid'] = _item['itemid']
                    _item_ids.append(_item['itemid'])
                    _item_history.append(_host)
        else:
            logger.error('ERROR!! item key {} not find'.format(item_key))
            return None

        # 如果 ID 列表为空, 则返回 None
        if _item_ids == []:
            logger.error('ERROR!! item key {} not find'.format(item_key))
            return None

        # ----------------------------------------------------------------------------------------------------

        # Get History
        _history_params = {
            'output': 'extend',
            'history': data_type,
            'itemids': _item_ids,
            'time_from': time_from,
            'time_till': time_till
        }
        _history = self.request('history.get', _history_params)

        # ----------------------------------------------------------------------------------------------------

        if vTrue(_history, dict) and vTrue(_history.get('result', []), list):

            for _item in _item_history:
                # 根据 itemid 提取数据
                _item_history_data = [_history_result for _history_result in _history['result'] if _item['itemid'] == _history_result['itemid']]
                # 根据 clock 排序
                _item_history_data = list_dict_sorted_by_key(_item_history_data, 'clock')
                # 整合数据
                _item['history'] = _item_history_data

            return _item_history

        else:
            logger.error('ERROR!! item history not find')
            return None

    def get_history_by_interface(self, hosts=[], interfaces=[], time_from=0, time_till=0, direction='', **kwargs):
        ''' 获取网卡历史数据 '''

        match True:
            case True if type(hosts) != list or hosts == []:
                logger.error('ERROR!! hosts is not list or none')
                return None
            case True if type(interfaces) != list or interfaces == []:
                logger.error('ERROR!! interfaces is not list or none')
                return None
            case True if type(time_from) != int or time_from == 0:
                logger.error('ERROR!! time_from is not integer or zero')
                return None
            case True if type(time_till) != int or time_till == 0:
                logger.error('ERROR!! time_till is not integer or zero')
                return None
            case True if type(direction) != str or direction == '':
                logger.error('ERROR!! direction is not string or none')
                return None

        # 创建一个只有 网卡名称 的 list
        _interfaces_names = list(set(_interface['interface'] for _interface in interfaces))

        # 创建一个 Key 为 网卡名称 的 dictionary
        _interfaces_dict = {_key: [] for _key in _interfaces_names}

        # 汇集 相同网卡名称 的 IP
        for _interface in interfaces:
            _interfaces_dict[_interface['interface']].append(_interface['host'])

        # 获取历史数据
        _history = []
        for _key, _value in _interfaces_dict.items():
            _hosts_by_ip = [_host for _v in _value for _host in hosts if _v == _host['interfaces'][0]['ip']]
            _history += self.get_history_by_item_key(
                hosts=_hosts_by_ip,
                time_from=time_from,
                time_till=time_till,
                item_key='net.if.{}["{}"]'.format(direction, _key),
                data_type=3
            )

        # 根据 name 排序
        _history = list_dict_sorted_by_key(_history, 'name')

        return _history

    def create_process_object(self, ips=[], name='', item_type=0, proc_name='', proc_user='', proc_cmdline='', ignore_cpu=False, ignore_mem=False, **kwargs):
        '''
        创建进程对象

            ips: IP列表
            name: 名称 (Item, Trigger, Graph 的名称前缀)
            item_type: Item Type (默认 0: Zabbix agent)
            proc_name: 进程名称
            proc_user: 进程用户
            proc_cmdline: 进程参数
            ignore_cpu: 是否创建 CPU Item 和 Graph
            ignore_mem: 是否创建 Memory Item 和 Graph

        参考文档:

            https://www.zabbix.com/documentation/6.0/en/manual/api/reference/item/object
            https://www.zabbix.com/documentation/6.0/en/manual/config/items/itemtypes/zabbix_agent#process-data

        type:

            0 - Zabbix agent;
            2 - Zabbix trapper;
            3 - Simple check;
            5 - Zabbix internal;
            7 - Zabbix agent (active);
            9 - Web item;
            10 - External check;
            11 - Database monitor;
            12 - IPMI agent;
            13 - SSH agent;
            14 - Telnet agent;
            15 - Calculated;
            16 - JMX agent;
            17 - SNMP trap;
            18 - Dependent item;
            19 - HTTP agent;
            20 - SNMP agent;
            21 - Script

        value_type:

            0 - numeric float;
            1 - character;
            2 - log;
            3 - numeric unsigned;
            4 - text.

        测试:

            zabbix_get -s 47.109.22.195 -p 10050 -k 'proc.num[java,karakal,,server.port=8011]'
            zabbix_get -s 47.109.22.195 -p 10050 -k 'proc.cpu.util[java,karakal,,server.port=8011]'
            zabbix_get -s 47.109.22.195 -p 10050 -k 'proc.mem[java,karakal,,server.port=8011,rss]'
            zabbix_get -s 47.109.22.195 -p 10050 -k 'proc.mem[java,karakal,,server.port=8011,pmem]'

            Memory used (rss) 的值除以 1024 就和 Zabbix Web 显示的一样了

        创建 Item:

            Number of processes 进程数量
            CPU utilization     CPU使用率
            Memory used (rss)   内存使用量
            Memory used (pmem)  内存使用率

            value type:

                Number of processes 3
                CPU utilization     0
                Memory used (rss)   0
                Memory used (pmem)  0

            获取 Item history 时, 如果返回结果为 None, 有可能是 value type 不一致

        创建 Trigger:

            Number of processes 如果进程数量为 0, 表示进程不存在 (应用或服务挂了)

        创建 Graph:

            CPU utilization CPU使用率
            Memory used (rss) 内存使用量
            Memory used (pmem) 内存使用率

            如果创建 Graph 后显示 [no data], 可以在 Items 中进入对应的 Item, 然后点击最下方的 Latest data
            在 Latest data 的右边的 Info 下面会有黄色感叹号, 将鼠标移动到上面, 可以看到相关的提示
        '''

        match True:
            case True if type(ips) != list or ips == []:
                logger.error('ERROR!! ips is not list or none')
                return False
            case True if type(name) != str or name == '':
                logger.error('ERROR!! name is not string or none')
                return False
            case True if type(proc_name) != str or proc_name == '':
                logger.error('ERROR!! proc_name is not string or none')
                return False

        # The number of processes
        # proc.num[<name>,<user>,<state>,<cmdline>,<zone>]
        _proc_num_item_name = '{} Number of processes'.format(name)
        _proc_num_item_key = 'proc.num[{},{},,{}]'.format(proc_name, proc_user, proc_cmdline)

        _proc_num_trigger_name = '{} is down'.format(name)

        # Process CPU utilization percentage
        # proc.cpu.util[<name>,<user>,<type>,<cmdline>,<mode>,<zone>]
        _proc_cpu_util_item_name = '{} CPU utilization'.format(name)
        _proc_cpu_util_item_key = 'proc.cpu.util[{},{},,{}]'.format(proc_name, proc_user, proc_cmdline)

        # Memory used by process in bytes
        # https://www.zabbix.com/documentation/6.0/en/manual/appendix/items/proc_mem_notes
        # proc.mem[<name>,<user>,<mode>,<cmdline>,<memtype>]
        # pmem: 内存使用量百分比, 即 top 显示的百分比
        # rss: 内存使用量实际数值, 即 总内存 x pmem(百分比)
        # Value Type 要使用 numeric float, 即 0, 否则会报错:
        # Value of type 'string' is not suitable for value type 'Numeric (unsigned)'.
        _proc_mem_rss_item_name = '{} Memory used (rss)'.format(name)
        _proc_mem_rss_item_key = 'proc.mem[{},{},,{},rss]'.format(proc_name, proc_user, proc_cmdline)

        _proc_mem_pmem_item_name = '{} Memory used (pmem)'.format(name)
        _proc_mem_pmem_item_key = 'proc.mem[{},{},,{},pmem]'.format(proc_name, proc_user, proc_cmdline)

        # Create Item, Trigger, Graph
        for _ip in ips:

            # Host Info
            _hostinterface = self.request('hostinterface.get', {'filter': {'ip': _ip}, 'selectHosts': ['host']})
            _host = _hostinterface['result'][0]['hosts'][0]['host']
            _host_id = _hostinterface['result'][0]['hostid']
            _interface_id = _hostinterface['result'][0]['interfaceid']

            # --------------------------------------------------------------------------------

            # Number of processes

            # Create Item
            _params = {
                'name': _proc_num_item_name,
                'key_': _proc_num_item_key,
                'hostid': _host_id,
                'type': item_type,
                'value_type': 3,
                'interfaceid': _interface_id,
                'delay': '1m',
                'history': '7d',
                'trends': '7d'
            }
            _ = self.request('item.create', _params)
            logger.success(_)

            # Create Trigger
            _params = [
                {
                    'description': _proc_num_trigger_name,
                    'priority': '2',
                    'expression': 'last(/{}/{})=0'.format(_host, _proc_num_item_key),
                    'manual_close': '1'
                }
            ]
            _ = self.request('trigger.create', _params)
            logger.success(_)

            # --------------------------------------------------------------------------------

            # CPU utilization

            if ignore_cpu == False:

                # Create Item
                _params = {
                    'name': _proc_cpu_util_item_name,
                    'key_': _proc_cpu_util_item_key,
                    'hostid': _host_id,
                    'type': item_type,
                    'value_type': 0,
                    'interfaceid': _interface_id,
                    'delay': '1m',
                    'history': '7d',
                    'trends': '7d'
                }
                _ = self.request('item.create', _params)
                logger.success(_)

                # Item Info
                _item_params = {
                    'output': 'itemid',
                    'hostids': _host_id,
                    'filter': {'key_': _proc_cpu_util_item_key}
                }
                _item = self.request('item.get', _item_params)
                _item_id = _item['result'][0]['itemid']

                # Create Graph
                _graph_params = {
                    'name': _proc_cpu_util_item_name,
                    'width': 900,
                    'height': 200,
                    'yaxismin': 0,
                    'yaxismax': 100,
                    'ymin_type': 1,
                    'ymax_type': 1,
                    'gitems': [{'itemid': _item_id, 'color': '0040FF'}]
                }
                _ = self.request('graph.create', _graph_params)
                logger.success(_)

            # --------------------------------------------------------------------------------

            # Memory used

            if ignore_mem == False:

                # Memory used (rss)

                # Create Item
                _params = {
                    'name': _proc_mem_rss_item_name,
                    'key_': _proc_mem_rss_item_key,
                    'hostid': _host_id,
                    'type': item_type,
                    'value_type': 0,
                    'interfaceid': _interface_id,
                    'delay': '1m',
                    'history': '7d',
                    'trends': '7d'
                }
                _ = self.request('item.create', _params)
                logger.success(_)

                # Total memory
                _vm_params = {
                    'output': 'itemid',
                    'hostids': _host_id,
                    'filter': {'key_': 'vm.memory.size[total]'}
                }
                _vm_total = self.request('item.get', _vm_params)
                _vm_total_itemid = _vm_total['result'][0]['itemid']

                # Item Info
                _item_params = {
                    'output': 'itemid',
                    'hostids': _host_id,
                    'filter': {'key_': _proc_mem_rss_item_key}
                }
                _item = self.request('item.get', _item_params)
                _item_id = _item['result'][0]['itemid']

                # Create Graph
                # gitems 需要注意顺序
                _graph_params = {
                    'name': _proc_mem_rss_item_name,
                    'width': 900,
                    'height': 200,
                    'graphtype': 1,
                    'gitems': [
                        {'itemid': _item_id, 'color': '00FF00'},
                        {'itemid': _vm_total_itemid, 'color': '1E88E5'}
                    ]
                }
                _ = self.request('graph.create', _graph_params)
                logger.success(_)

                # --------------------------------------------------------------------------------

                # Memory used (pmem)

                # Create Item
                # Units: %
                _params = {
                    'name': _proc_mem_pmem_item_name,
                    'key_': _proc_mem_pmem_item_key,
                    'hostid': _host_id,
                    'type': item_type,
                    'value_type': 0,
                    'interfaceid': _interface_id,
                    'units': '%',
                    'delay': '1m',
                    'history': '7d',
                    'trends': '7d'
                }
                _ = self.request('item.create', _params)
                logger.success(_)

                # Item Info
                _item_params = {
                    'output': 'itemid',
                    'hostids': _host_id,
                    'filter': {'key_': _proc_mem_pmem_item_key}
                }
                _item = self.request('item.get', _item_params)
                _item_id = _item['result'][0]['itemid']

                # Create Graph
                _graph_params = {
                    'name': _proc_mem_pmem_item_name,
                    'width': 900,
                    'height': 200,
                    'graphtype': 1,
                    'yaxismin': 0,
                    'yaxismax': 100,
                    'ymin_type': 1,
                    'ymax_type': 1,
                    'gitems': [
                        {'itemid': _item_id, 'color': '66BB6A'}
                    ]
                }
                _ = self.request('graph.create', _graph_params)
                logger.success(_)

        return True

    def create_tcp_port_check(self, ips=None, name=None, item_type=0, ip=None, port=None, **kwargs):
        '''
        创建进程对象

            ips: IP列表
            name: 名称 (Item, Trigger, Graph 的名称前缀)
            item_type: Item Type (默认 0: Zabbix agent)
            ip: IP地址
            port: 目标端口

        参考文档:

            https://www.zabbix.com/documentation/6.0/en/manual/api/reference/item/object
            https://www.zabbix.com/documentation/6.0/en/manual/config/items/itemtypes/zabbix_agent#network-data

        type:

            0 - Zabbix agent;
            2 - Zabbix trapper;
            3 - Simple check;
            5 - Zabbix internal;
            7 - Zabbix agent (active);
            9 - Web item;
            10 - External check;
            11 - Database monitor;
            12 - IPMI agent;
            13 - SSH agent;
            14 - Telnet agent;
            15 - Calculated;
            16 - JMX agent;
            17 - SNMP trap;
            18 - Dependent item;
            19 - HTTP agent;
            20 - SNMP agent;
            21 - Script

        value_type:

            0 - numeric float;
            1 - character;
            2 - log;
            3 - numeric unsigned;
            4 - text.

        测试:

            zabbix_get -s 10.26.20.141 -p 20050 -k 'net.tcp.port[10.25.182.10,20051]'

        创建 Item:

            TCP connection 进程数量

            value type:

                TCP connection 3

            获取 Item history 时, 如果返回结果为 None, 有可能是 value type 不一致

        创建 Trigger:

            TCP connection 结果如果为 0, 端口无法访问
        '''

        match True:
            case True if type(ips) != list or ips == None:
                logger.error('ERROR!! ips is not list or none')
                return False
            case True if type(name) != str or name == None:
                logger.error('ERROR!! name is not string or none')
                return False
            case True if type(ip) != str or ip == None:
                logger.error('ERROR!! ip is not string or none')
                return False
            case True if type(port) != int or port == None:
                logger.error('ERROR!! port is not integer or none')
                return False

        # Checks if it is possible to make TCP connection to specified port.
        # net.tcp.port[<ip>,port]
        _item_name = 'TCP connection: {}'.format(name)
        _item_key = 'net.tcp.port[{},{}]'.format(ip, port)
        _trigger_name = 'Failed to connect to {} port {}'.format(ip, port)

        # Create Item, Trigger
        for _ip in ips:

            # Host Info
            _hostinterface = self.request('hostinterface.get', {'filter': {'ip': _ip}, 'selectHosts': ['host']})
            _host = _hostinterface['result'][0]['hosts'][0]['host']
            _host_id = _hostinterface['result'][0]['hostid']
            _interface_id = _hostinterface['result'][0]['interfaceid']

            # Create Item
            _params = {
                'name': _item_name,
                'key_': _item_key,
                'hostid': _host_id,
                'type': item_type,
                'value_type': 3,
                'interfaceid': _interface_id,
                'delay': '1m',
                'history': '7d',
                'trends': '7d'
            }
            _ = self.request('item.create', _params)
            logger.success(_)

            # Create Trigger
            _expression = None
            if self._zabbix_version == 5.0:
                _expression = '{' + '{}:{}'.format(_host, _item_key) + '.last()}=0'
            else:
                _expression = 'last(/{}/{})=0'.format(_host, _item_key)
            _params = [
                {
                    'description': _trigger_name,
                    'priority': '2',
                    'expression': _expression,
                    'manual_close': '1'
                }
            ]
            _ = self.request('trigger.create', _params)
            logger.success(_)

        return True
