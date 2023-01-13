import psycopg2
import psycopg2.extras
from tinybird_cdk import connector, export, formats, errors

# The environment variables supported by this connector are documented here:
#
#     https://www.postgresql.org/docs/14/libpq-envars.html
#
class Connector(connector.SQLConnector):
    def get_scopes(self):
        raise 'Not implemented'

    def list_scope(self, _parents={}):
        raise 'Not implemented'

    def suggest_schema(self, parents):
        raise 'Not implemented'

    def _query(self, sql):
        with psycopg2.connect() as connection:
            with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(sql)
                return [dict(row) for row in cursor.fetchall()]

    def _export(self, query, fmt):
        if fmt == formats.CSV:
            return self._export_to_csv(query)
        if fmt == formats.NDJSON:
            return self._export_to_ndjson(query)
        raise errors.UnsupportedFormat(fmt)

    # https://www.postgresql.org/docs/14/sql-copy.html.
    def _export_to_csv(self, query):
        tmp = self._binary_tempfile(extension='csv')
        with psycopg2.connect() as connection:
            with connection.cursor() as cursor:
                cursor.copy_expert(f'COPY ({query}) TO STDIN WITH (FORMAT CSV)', tmp)
                tmp.close()
        return export.LocalFile(tmp.name)

    # This is not implemented with row_to_json() and COPY ... TO because COPY
    # escapes backlashes. So, for example, a string column that contained JSON
    # would have quotes escaped incorrectly. Instead of \", you'd get \\".
    def _export_to_ndjson(self, query):
        with psycopg2.connect() as connection:
            with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(query)
                fname = self._to_ndjson_tempfile(cursor)
        return export.LocalFile(fname)
