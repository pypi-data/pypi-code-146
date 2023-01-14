import os
from collections import namedtuple
from operator import attrgetter
from typing import Generator, Tuple
from urllib.parse import urlparse

import boto3


def write_to_s3(body: str,
                s3_path: str) -> None:
    s3_bucket, s3_key = parse_s3_path(s3_path)

    boto3.resource('s3').Object(s3_bucket, s3_key).put(Body=body)


def parse_s3_path(s3_path: str) -> Tuple[str, str]:
    s3_urlparse = urlparse(s3_path)
    s3_bucket = s3_urlparse.netloc
    s3_key = s3_urlparse.path[1:]

    return s3_bucket, s3_key


def read_file(s3_path: str) -> str:
    s3_bucket, s3_key = parse_s3_path(s3_path)
    resource = boto3.resource('s3')
    obj = resource.Object(s3_bucket, s3_key)
    return obj.get()['Body'].read().decode('utf-8')


def read_files(s3_path: str) -> Generator[str, None, None]:
    for filename in get_filenames(s3_path, full_names=True):
        yield read_file(filename)


def get_filenames(s3_path: str,
                  full_names: bool = False) -> Generator[str, None, None]:
    s3_path = s3_path.rstrip('/')
    s3_bucket, s3_key = parse_s3_path(s3_path)
    resource = boto3.resource('s3')
    bucket = resource.Bucket(s3_bucket)
    objects = bucket.objects.filter(Prefix=s3_key)

    filenames = (obj.key[len(f'{s3_key}/'):]
                 for obj in objects
                 if obj.key != f'{s3_key}/')

    if full_names:
        return (f'{s3_path}/{filename}' for filename in filenames)
    else:
        return filenames


def get_directories(s3_path: str) -> Generator[str, None, None]:
    s3_path = s3_path.rstrip('/')
    s3_bucket, s3_key = parse_s3_path(s3_path)
    resource = boto3.resource('s3')
    bucket = resource.Bucket(s3_bucket)

    return (f's3://{s3_bucket}/{directory.key}'
            for directory
            in s3list(bucket, s3_key, recursive=False, list_objs=False))


S3Obj = namedtuple('S3Obj', ['key', 'mtime', 'size', 'ETag'])


def s3list(bucket, path, start=None, end=None, recursive=True, list_dirs=True,
           list_objs=True, limit=None):
    """
    Iterator that lists a bucket's objects under path, (optionally)
    starting with start and ending before end.

    If recursive is False, then list only the "depth=0"
    items (dirs and objects).

    If recursive is True, then list recursively all objects (no dirs).

    Args:
        bucket:
            a boto3.resource('s3').Bucket().
        path:
            a directory in the bucket.
        start:
            optional: start key, inclusive (may be a relative path under path,
            or absolute in the bucket)
        end:
            optional: stop key, exclusive (may be a relative path under path, or
            absolute in the bucket)
        recursive:
            optional, default True. If True, lists only objects. If False, lists
            only depth 0 "directories" and objects.
        list_dirs:
            optional, default True. Has no effect in recursive listing. On
            non-recursive listing, if False, then directories are omitted.
        list_objs:
            optional, default True. If False, then directories are omitted.
        limit:
            optional. If specified, then lists at most this many items.

    Returns:
        an iterator of S3Obj.

    Examples:
    # set up
    # >>> s3 = boto3.resource('s3')
    # ... bucket = s3.Bucket(name)
    #
    # # iterate through all S3 objects under some dir
    # >>> for p in s3ls(bucket, 'some/dir'):
    # ...     print(p)
    #
    # # iterate through up to 20 S3 objects under some dir, starting with
    # foo_0010
    # >>> for p in s3ls(bucket, 'some/dir', limit=20, start='foo_0010'):
    # ...     print(p)
    #
    # # non-recursive listing under some dir:
    # >>> for p in s3ls(bucket, 'some/dir', recursive=False):
    # ...     print(p)
    #
    # # non-recursive listing under some dir, listing only dirs:
    # >>> for p in s3ls(bucket, 'some/dir', recursive=False, list_objs=False):
    # ...     print(p)
"""

    def __prev_str(s):
        if len(s) == 0:
            return s
        s, c = s[:-1], ord(s[-1])
        if c > 0:
            s += chr(c - 1)
        s += ''.join(['\u7FFF' for _ in range(10)])
        return s

    kwargs = dict()
    if start is not None:
        if not start.startswith(path):
            start = os.path.join(path, start)
        # note: need to use a string just smaller than start, because
        # the list_object API specifies that start is excluded (the first
        # result is *after* start).
        kwargs.update(Marker=__prev_str(start))
    if end is not None:
        if not end.startswith(path):
            end = os.path.join(path, end)
    if not recursive:
        kwargs.update(Delimiter='/')
        if not path.endswith('/'):
            path += '/'
    kwargs.update(Prefix=path)
    if limit is not None:
        kwargs.update(PaginationConfig={'MaxItems': limit})

    paginator = bucket.meta.client.get_paginator('list_objects')
    for resp in paginator.paginate(Bucket=bucket.name, **kwargs):
        q = []
        if 'CommonPrefixes' in resp and list_dirs:
            q = [S3Obj(f['Prefix'], None, None, None) for f in
                 resp['CommonPrefixes']]
        if 'Contents' in resp and list_objs:
            q += [S3Obj(f['Key'], f['LastModified'], f['Size'], f['ETag']) for f
                  in resp['Contents']]
        # note: even with sorted lists, it is faster to sort(a+b)
        # than heapq.merge(a, b) at least up to 10K elements in each list
        q = sorted(q, key=attrgetter('key'))
        if limit is not None:
            q = q[:limit]
            limit -= len(q)
        for p in q:
            if end is not None and p.key >= end:
                return
            yield p
