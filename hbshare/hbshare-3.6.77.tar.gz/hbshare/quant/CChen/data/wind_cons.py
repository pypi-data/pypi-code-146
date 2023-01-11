sql_l_futures = '''(
    `id` bigint not null AUTO_INCREMENT,
    `symbol`  varchar(255) not null,
    `t_date`  date not null,
    `pre_close`  float null,
    `open`  float null,
    `high`  float null,
    `low`  float null,
    `close`  float null,
    `settle`  float null,
    `volume`  bigint null,
    `amount`  double null COMMENT \'成交额（元）\',
    `oi`  bigint null,
    `oi_amount`  bigint null COMMENT \'持仓额（元）\',
    `underlying` float null,
    `basis` float null,
    `delist_date` date null,
    `product`  varchar(255),
    `code`  varchar(255),
    primary key (`id`)
    )
    '''

sql_info_l = '''
    `id` bigint not null AUTO_INCREMENT,
    `code`  varchar(255),
    `exchange_code`  varchar(255),
    `exchange`  varchar(255),
    `list_date`  date,
    `delist_date`  date,
    `product`  varchar(255),
    `board_lot`  varchar(255),
    primary key (`id`)
    '''

sql_l_bar = '''(
    `id` bigint not null AUTO_INCREMENT,
    `code`  varchar(255) not null,
    `name`  varchar(255),
    `t_date`  date not null,
    `pre_close`  float null,
    `open`  float null,
    `high`  float null,
    `low`  float null,
    `close`  float null,
    `chg`  float null,
    `pct_chg`  float null,
    `volume`  bigint null,
    `amount`  bigint null,
    `oi` bigint,
    `oi_amount` bigint,
    `product`  varchar(255),
    `exchange`  varchar(255),
    primary key (`id`)
    )
    '''

sql_l_stk = '''(
    `id` bigint not null AUTO_INCREMENT,
    `t_date`  date,
    `code`  varchar(255),
    `name`  varchar(255),
    `open`  float,
    `high`  float,
    `low`  float,
    `close`  float,
    `volume`  bigint,
    `amount`  double,
    `adjFactor`  float,
    `freeTurn`  float,
    `freeShare`  bigint,
    `tdState`  varchar(255),
    `stState`  varchar(255),
    primary key (id)
    )
    '''

sql_l_edb = '''(
    `id` bigint not null AUTO_INCREMENT,
    `code`  varchar(255) not null,
    `t_date`  date not null,
    `close`  float null,
    primary key (`id`)
    )
    '''
