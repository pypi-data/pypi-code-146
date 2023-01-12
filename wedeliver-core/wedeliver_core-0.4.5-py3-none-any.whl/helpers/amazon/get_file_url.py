from app import app
from wedeliver_core.helpers.amazon.get_s3_client import get_s3_client


def get_file_url(s3_path, s3_client=None):
    """
    Upload a file to an S3 bucket
    """
    # return s3_path

    if not s3_path:
        return s3_path

    if not s3_path.startswith("http"):
        s3_path = "https://{}/{}".format(app.config.get("S3_BUCKET"), s3_path)

    path_parts = s3_path.replace("https://", "").split("/")
    bucket = path_parts.pop(0).split(".").pop(0)
    key = "/".join(path_parts)

    response = None
    s3_client = None
    try:
        s3_client = s3_client or get_s3_client()
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=100,
        )
    except Exception as e:
        app.logger.error(str(e))

    # The response contains the presigned URL
    app.logger.debug(response)
    return response


if __name__ == "__main__":
    url = get_file_url(
        s3_path="owner_national_attachment/1660823074_ihbxlpymqxxjuzrqom.jpe"
        # s3_path="https://dev-wedeliver-slips.s3.eu-west-1.amazonaws.com/development/PS/images/cad3b9038e021648.jpg"
    )
    test = url
