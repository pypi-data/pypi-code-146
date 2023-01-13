class FilenameAlreadyExists(Exception):
    """
    Represents an error occurring when filename already exists in the filesystem.
    """

    def __init__(self, file_name: str, path: str):
        self.file_name = file_name
        self.path = path
        self.root_path = path if path else "root"
        super().__init__(f"File {file_name} already exists in {self.root_path} directory")
