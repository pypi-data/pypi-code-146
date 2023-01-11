import boto3


def get_s3_resource(key, secret):
    try:
        return boto3.resource(
            "s3",
            aws_access_key_id=key,
            aws_secret_access_key=secret,
        )
    except:
        return None


def download_file(resource, local_filename, bucket, cloud_filename):
    try:
        resource.Object(bucket, cloud_filename).download_file(local_filename)
        return True
    except:
        return False


def upload_file(resource, local_filename, bucket, cloud_filename):
    try:
        resource.meta.client.upload_file(local_filename, bucket, cloud_filename)
        return True
    except:
        return False
