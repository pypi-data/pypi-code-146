host_config = {
    'test': {
        'host': '10.20.16.102',
        'port': 10989,
        'server_url': 'https://dcctest.kxll.com/dccapi',
        'server_port': 10988,
        'store_url': 'http://10.20.16.87/api/test'
    },
    'pro': {
        'host': '10.20.20.9',
        'port': 10989,
        'server_url': 'https://cjzt.kxll.com/dccapi',
        'server_port': 10988,
        'store_url': 'http://10.158.0.23:18080/crawler/collect/logs'
    },
    'vps': {
        'host': '183.129.169.171',
        'port': 10989,
        'server_url': 'https://cjzt.kxll.com/dccapi',
        'server_port': 10988,
        'store_url': 'http://211.140.27.195:18080/crawler/collect/logs'
    },
    'cloud': {
        'host': '120.26.192.28',
        'port': 10989,
        'server_url': 'http://hzfgwl.com/dccapi',
        'server_port': 10988,
        'store_url': 'http://211.140.27.195:18080/crawler/collect/logs'
    }
}

date_type_map = {
    'week': 'W',
    'month': 'M',
    'day': 'D',
    'normal': 'N',
}
