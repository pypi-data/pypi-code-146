import json


def create_command(command: str, args: dict):
    command_populated = command.format(command, **args)
    array_command = command_populated.split(' ')
    array_filtered = [i for i in array_command if len(i) > 0 and i != '\n']
    return array_filtered


def create_search_query(protocol: str, event_type: str, chain: str, from_date: str, to_date: str):
    query = {
        "bool":
        {
            "must": [
                {
                    "query_string": {
                        "query": f'*{protocol}*', "fields": ["service.attributes.main.name"]}
                },
                {
                    "match": {
                        "service.attributes.additionalInformation.categories": f"EventType:{event_type}"}
                },
                {
                    "match": {
                        "service.attributes.additionalInformation.blockchain": f'{chain.lower()}'}
                },
                {
                    "range": {
                        "service.attributes.main.datePublished": {
                            "time_zone": "+01:00",
                            "gte": f"{from_date}",
                            "lte": f"{to_date}"
                        }
                    }
                }
            ]}}

    return json.dumps(query).replace(' ', '')
