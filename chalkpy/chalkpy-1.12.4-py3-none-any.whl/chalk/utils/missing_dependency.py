class MissingDependencyException(ImportError):
    ...


def missing_dependency_exception(name: str):
    return MissingDependencyException(
        f"Missing pip dependency '{name}'. Please add this to your requirements.txt file and pip install."
    )
