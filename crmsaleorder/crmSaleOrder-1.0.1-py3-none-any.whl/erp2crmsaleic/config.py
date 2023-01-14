from urllib import parse

bad_password = 'rds@2022'
conn1 = {'DB_USER': 'dms',
         'DB_PASS': parse.quote_plus(bad_password),
         'DB_HOST': '58.211.213.34',
         'DB_PORT': 1433,
         'DATABASE': 'AIS20220926102634',
         }

conn3 = {'DB_USER': 'lingdang',
         'DB_PASS': parse.quote_plus('lingdangcrm123!@#'),
         'DB_HOST': '123.207.201.140',
         'DB_PORT': 33306,
         'DATABASE': 'ldcrm',
         }


conn = {'DB_USER': 'DMS',
        'DB_PASS': parse.quote_plus(bad_password),
        'DB_HOST': '115.159.201.178',
        'DB_PORT': 1433,
        'DATABASE': 'cprds',
        }
