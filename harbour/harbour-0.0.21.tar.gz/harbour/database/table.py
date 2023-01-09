class Table:

    def __init__(self, db, name, *args, **kwargs):

        self.schema = db.credentials.get('db', db.credentials.get('dbname'))
        self.name = name

        # Default state
        self.sql = None
        self.columns = '*'
        self.filter = None
        self._limit = None
        self.order = None
        self.primary_key = None
        self._sequence = None

        # Database connections
        self.db = db
        self.conn, self.curs = db.conn, db.curs
        self.host = db.credentials['host']

    def select(self, columns, *args, **kwargs):
        """Defines the columns selected"""

        # Type checking
        if columns == '*':

            self.columns = ['*']

        elif isinstance(columns, str):

            self.columns = [columns]

        elif not isinstance(columns, list):

            raise TypeError('columns must be str or list')

        return self

    def order_by(self, order, *args, **kwargs):
        """Appends a ORDER BY clausule to the query"""

        if not isinstance(order, dict):
            raise TypeError('order must be a dict {"column": "ASC|DESC"}')

        for value in order.values():

            if value not in ['ASC', 'DESC']:
                raise AttributeError('order directoin must be ASC or DESC')

        self.order = order

        return self

    def sequence(self, value: str):
        self._sequence = value
        
        return self

    def where(self, filter:str):
        """Appends a where clausule to the query.
        Premisses:
            This filter is only a string 
        """

        if filter is not None:
            if "where " in filter.lower():
                filter = filter.replace("where ", "")
            if filter[:3].lower() == "and":
                filter = filter[3:]
        self.filter = filter

        return self

    def limit(self, limit, *args, **kwargs):
        """Appends a LIMIT clausule to the query"""

        if not isinstance(limit, int):
            raise TypeError('limit must be a int')

        if limit != 0:

            self._limit = limit

        return self

    def build(self, *args, **kwargs):
        """Builds the SQL"""

        self.sql = "/*Application: Tethys - Dumper*/\n"
        self.sql += "SELECT {}".format(', '.join(self.columns))
        
        if self._sequence is None:
            if self.db.engine == 'postgresql':
                self.sql += ", CAST(extract(epoch from now() at time zone 'utc' at time zone 'utc') * POW(10, 6) AS DECIMAL(25,9)) AS _sequence\n"
                self.sql += 'FROM "{}".{}\n'.format(self.schema, self.name)
            else:
                self.sql += ", CAST(UNIX_TIMESTAMP() * POW(10, 6) AS DECIMAL(25,9)) AS _sequence\n"
                self.sql += "FROM `{}`.{}\n".format(self.schema, self.name)
        else:
            if self.db.engine == 'postgresql':
                self.sql += f", {self._sequence} AS _sequence\n"
                self.sql += 'FROM "{}".{}\n'.format(self.schema, self.name)
            else:
                self.sql += f", {self._sequence} AS _sequence\n"
                self.sql += "FROM `{}`.{}\n".format(self.schema, self.name)


        if self.filter is not None:

            self.sql += "WHERE\n\t1=1 AND {}\n".format(self.filter)

        if self.order is not None:

            self.sql += "ORDER BY {}\n".format(','.join(
                ['{} {}'.format(k, v) for k, v in self.order.items()]))

        if self._limit is not None:
            self.sql += "LIMIT {}".format(self._limit)

        return self

    def execute(self):
        """Executes a query to check the table metadata and then executes the
        built sql"""

        self.build()

        self.curs.execute(self.sql)

        return self

    @property
    def fields(self):
        """Returns the table schema"""

        from harbour.database.mappings import MYSQL_TYPE_MAP, POSTGRESQL_TYPE_MAP

        return {
            field[0]: {
                'type':
                POSTGRESQL_TYPE_MAP.get(field[1]) if self.db.engine
                == 'postgresql' else MYSQL_TYPE_MAP.get(field[1])
            }
            for field in self.curs.description if field[0] != '_sequence'
        }

    @property
    def pk(self):
        """Returns the table primary key"""

        # This a cache. Do not remove!
        if self.primary_key is None:

            sql = f"""
            SELECT
                u.COLUMN_NAME AS column_name
            FROM information_schema.TABLE_CONSTRAINTS c
            INNER JOIN information_schema.KEY_COLUMN_USAGE u
                ON c.TABLE_SCHEMA = u.TABLE_SCHEMA
                AND c.TABLE_NAME = u.TABLE_NAME
                AND c.CONSTRAINT_NAME = u.CONSTRAINT_NAME
            WHERE
                c.TABLE_SCHEMA = '{self.schema}'
                AND c.TABLE_NAME = '{self.name}'
                AND c.CONSTRAINT_TYPE = 'PRIMARY KEY'
            ORDER BY u.ORDINAL_POSITION ASC;
            """

            self.curs.execute(sql)

            self.primary_key = [
                row['column_name'] for row in self.curs.fetchall()
            ]

        return self.primary_key

    def fetchall(self):
        """Fetches all the records."""

        for row in self.curs.fetchall():
            yield row

    def fetchmany(self, n=1000):
        """Fetches as many records as specified. Defaul: 1000"""

        return self.curs.fetchmany(n)

    def __iter__(self):
        """Iterates over the table records."""

        return self.fetchall()
