from dataclasses import dataclass


@dataclass
class PresignedS3:
    jobId: str = ""
    key: str = ""
    metaAuthor: str = ""
    metaVersion: str = ""
    contentType: str = ""
    url: str = ""
