import json

from django.core.files.base import ContentFile

from recomb_to_s3.models import RecombToS3, User


def send_dict_to_s3(data: dict, file_name: str, author: User | None) -> RecombToS3:
    """creates a new object of type RecombToS3 and returns it

    Args:
        data (dict): the data to be saved
        file_name (str): the name of the file to be saved
        author (User | None): reference to user author of this file

    Returns:
        RecombToS3: created object
    """
    return RecombToS3.objects.create(
        file=ContentFile(
            json.dumps(data).encode("utf-8"),
            name=file_name,
        ),
        author=author,
        file_type=file_name.split(".")[-1],
    )
