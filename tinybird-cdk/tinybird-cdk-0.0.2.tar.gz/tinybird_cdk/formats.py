CSV = 'csv'
NDJSON = 'ndjson'
PARQUET = 'parquet'

def mime_type_for(fmt):
    if fmt == 'csv':
        return 'text/csv; charset=utf-8'
    if fmt == 'ndjson':
        return 'application/x-ndjson; charset=utf-8'
    if fmt == 'parquet':
        return 'application/vnd.apache.parquet'
    raise Exception(f'Unknown format: {fmt}')
