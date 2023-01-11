from datetime import datetime

def directory_path(instance, filename):
    if instance.author:
        return f"documents/{instance.author.username}/{datetime.now()}/{filename}"
    else:
        return f"documents/{datetime.now()}/{filename}"
