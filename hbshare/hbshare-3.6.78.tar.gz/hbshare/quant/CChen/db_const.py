
sql_user_work = {
    'ip': 'localhost',
    'user': 'root',
    'pass': '123456',
    'port': '3306'
}

sql_write_path_work = {
    'commodities':
        'mysql+mysqlconnector://%s:%s@%s:%s/commodities?charset=utf8'
        % (sql_user_work['user'], sql_user_work['pass'], 'localhost', sql_user_work['port']),
    'stocks':
        'mysql+mysqlconnector://%s:%s@%s:%s/stocks?charset=utf8'
        % (sql_user_work['user'], sql_user_work['pass'], 'localhost', sql_user_work['port']),
    'work':
        'mysql+mysqlconnector://%s:%s@%s:%s/work?charset=utf8'
        % (sql_user_work['user'], sql_user_work['pass'], 'localhost', sql_user_work['port']),
    'daily':
        'mysql+mysqlconnector://%s:%s@%s:%s/daily_data?charset=utf8'
        % (sql_user_work['user'], sql_user_work['pass'], 'localhost', sql_user_work['port']),
}


ali_ip = 'rm-bp1d9m7p1ljot31p1yo.mysql.rds.aliyuncs.com'

sql_user_ali = {
    'ip': ali_ip,
    'user': 'db_cc',
    'pass': 'db_ccsdysywj',
    'port': '3306'
}

sql_write_path_ali = {
    'commodities':
        'mysql+mysqlconnector://%s:%s@%s:%s/commodities?charset=utf8'
        % (sql_user_ali['user'], sql_user_ali['pass'], ali_ip, sql_user_ali['port']),
    'stocks':
        'mysql+mysqlconnector://%s:%s@%s:%s/stocks?charset=utf8'
        % (sql_user_ali['user'], sql_user_ali['pass'], ali_ip, sql_user_ali['port']),
    'work':
        'mysql+mysqlconnector://%s:%s@%s:%s/work?charset=utf8'
        % (sql_user_ali['user'], sql_user_ali['pass'], ali_ip, sql_user_ali['port']),
    'daily':
        'mysql+mysqlconnector://%s:%s@%s:%s/daily_data?charset=utf8'
        % (sql_user_ali['user'], sql_user_ali['pass'], ali_ip, sql_user_ali['port']),
}


hb_ip = '192.168.223.152'

sql_user_hb = {
    'ip': hb_ip,
    'user': 'admin',
    'pass': 'mysql',
    'port': '3306'
}

sql_write_path_hb = {
    'commodities':
        'mysql+mysqlconnector://%s:%s@%s:%s/commodities?charset=utf8'
        % (sql_user_hb['user'], sql_user_hb['pass'], hb_ip, sql_user_hb['port']),
    'stocks':
        'mysql+mysqlconnector://%s:%s@%s:%s/stocks?charset=utf8'
        % (sql_user_hb['user'], sql_user_hb['pass'], hb_ip, sql_user_hb['port']),
    'work':
        'mysql+mysqlconnector://%s:%s@%s:%s/work?charset=utf8'
        % (sql_user_hb['user'], sql_user_hb['pass'], hb_ip, sql_user_hb['port']),
    'daily':
        'mysql+mysqlconnector://%s:%s@%s:%s/daily_data?charset=utf8'
        % (sql_user_hb['user'], sql_user_hb['pass'], hb_ip, sql_user_hb['port']),
    'fut':
        'mysql+mysqlconnector://%s:%s@%s:%s/fut_data?charset=utf8'
        % (sql_user_hb['user'], sql_user_hb['pass'], hb_ip, sql_user_hb['port']),
}
