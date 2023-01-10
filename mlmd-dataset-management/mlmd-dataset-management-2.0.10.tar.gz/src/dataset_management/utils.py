import uuid

def generate_version_id():
    return "_" + str(uuid.uuid4()).replace("-", "")
