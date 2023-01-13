import json


def serialize_content(content):
    return json.dumps(
        content,
        ensure_ascii=False,
        separators=(',', ':'),
    )


def deserialize_content(content):
    if content is None:
        return

    try:
        deserialized_content = json.loads(content)
        if isinstance(content, str):
            deserialized_content = json.loads(deserialized_content)
    except json.JSONDecodeError:
        deserialized_content = content

    return deserialized_content


def get_suffixed_queue_name(queue, suffix):
    return f'{queue}.{suffix}'


def get_partition_queue_name(*args, **kwargs):
    return get_suffixed_queue_name(*args, **kwargs)


def get_dead_letter_queue_name(queue):
    return get_suffixed_queue_name(queue, 'dlq')


def get_backup_queue_name(queue, partition):
    partition_queue = get_partition_queue_name(queue, partition)
    return get_suffixed_queue_name(partition_queue, 'backup')


def is_backup_queue(queue):
    return queue.endswith('.backup')


def get_queue_name(queue):
    queue_name = queue.replace('.backup', '')
    return queue_name.rsplit('.', 1)[0]
