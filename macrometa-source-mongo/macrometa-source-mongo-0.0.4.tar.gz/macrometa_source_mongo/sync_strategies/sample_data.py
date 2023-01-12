from collections import Counter
from singer import metadata
from macrometa_source_mongo.db_utils import get_singer_data_type


def fetch_table(client, conn_info, stream):
    database = client[conn_info['dbname']]
    collection = database[stream["table_name"]]
    schemas = []
    schema_map = {}
    data_map = {}
    cursor = collection.find({}, {'_id': False})
    for rec in cursor:
        h = str(hash(rec.keys().__str__()))
        schema_map[h] = rec.keys()
        schemas.append(h)
        if h in data_map:
            data_map[h].append(rec)
        else:
            data_map[h] = [rec]
    schema = {"data": "object"}
    data = []
    if len(schemas) > 0:
        most_common, _ = Counter(schemas).most_common(1)[0]
        schema_keys = schema_map[most_common]
        data = data_map[most_common]
        schema = {
            k: get_singer_data_type(data[0][k]) for k in schema_keys
        }
    return schema, data


def fetch_samples(client, conn_config, stream):
    """
    Fetch samples for the stream.
    """
    md_map = metadata.to_map(stream['metadata'])
    conn_config['dbname'] = md_map.get(()).get('database-name')
    # Add support for views if needed here
    state = fetch_table(client, conn_config, stream)
    return state
