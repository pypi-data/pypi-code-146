from soyuz.dx.sentinels import SentinelBase


class SeqFolderUploadStart(object):
    def __init__(self, seq_folder, sentinel):
        # type: (SeqFolderBase, SentinelBase) -> None
        self.seq_folder = seq_folder
        self.sentinel = sentinel


class SeqFolderUploadComplete(object):
    def __init__(self, seq_folder):
        # type: (SeqFolderBase) -> None

        self.seq_folder = seq_folder


class SeqFolderUploadTerminated(object):
    def __init__(self, seq_folder):
        # type: (SeqFolderBase) -> None

        self.seq_folder = seq_folder


class UploadJobTerminated(object):
    def __init__(self, seq_folder_name):
        # type: (str) -> None
        self.seq_folder_name = seq_folder_name


class NewUploadJob(object):
    def __init__(self, job_id, seq_folder_name):
        # type: (str, str) -> None
        self.job_id = job_id
        self.seq_folder_name = seq_folder_name
