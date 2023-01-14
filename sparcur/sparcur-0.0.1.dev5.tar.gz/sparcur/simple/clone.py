#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::clone.py][clone.py]]
from pathlib import Path


# clone top level
def from_path_id_and_backend_project_top_level(parent_path,
                                               project_id,
                                               RemotePath,
                                               symlink_objects_to=None,):
    """ given the enclosing path to clone to, the project_id, and a fully
        configured (with Local and Cache) backend remote path, anchor the
        project pointed to by project_id along with the first level of children """

    project_path = _from_path_id_remote_project(parent_path,
                                                project_id,
                                                RemotePath,
                                                symlink_objects_to)
    return _from_project_path_top_level(project_path)


def from_path_project_backend_id_dataset(parent_path,
                                         project_id,
                                         dataset_id,
                                         RemotePath,
                                         symlink_objects_to=None,):
    project_path = _from_path_id_remote_project(parent_path,
                                                project_id,
                                                RemotePath,
                                                symlink_objects_to)
    return _from_project_path_id_dataset(project_path, dataset_id)


def _from_path_id_remote_project(parent_path, project_id, RemotePath, symlink_objects_to):
    RemotePath.init(project_id)  # calling init is required to bind RemotePath._api
    anchor = RemotePath.smartAnchor(parent_path)
    anchor.local_data_dir_init(symlink_objects_to=symlink_objects_to)
    project_path = anchor.local
    return project_path


def _from_project_path_top_level(project_path):
    """ given a project path with existing cached metadata
        pull the top level children

        WARNING: be VERY careful about using this because it
        does not gurantee that rmeta is available to mark
        sparse datasets. It may be the case that the process
        will fail if the rmeta is missing, or it may not. Until
        we are clear on the behavior this warning will stay
        in place. """
    # this is a separate function in case the previous step fails
    # which is also why it is hidden, it makes too many assuptions
    # to be used by itself

    anchor = project_path.cache
    list(anchor.children)  # this fetchs data from the remote path to the local path
    return project_path  # returned instead of anchor & children because it is needed by next phase


def _from_project_path_id_dataset(project_path, dataset_id):
    anchor = project_path.cache
    remote = anchor._remote_class(dataset_id)
    cache = anchor / remote
    return cache.local


def main(parent_path=None,
         project_id=None,
         parent_parent_path=Path.cwd(),
         project_id_auth_var='remote-organization',  # FIXME move default to clifun
         symlink_objects_to=None,
         id=None,
         dataset_id=None,
         **kwargs):
    """ clone a project into a random subfolder of the current folder
        or specify the parent path to clone into """

    from sparcur.simple.utils import backend_pennsieve

    if parent_path is None:
        breakpoint()  # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX FIXME
        import tempfile
        parent_path = Path(tempfile.mkdtemp(dir=parent_parent_path))

    if project_id is None:
        from sparcur.config import auth
        from sparcur.utils import PennsieveId
        project_id = auth.get(project_id_auth_var)
        project_id = PennsieveId(project_id)  # FIXME abstract the hardcoded backend

    RemotePath = backend_pennsieve()

    if id and dataset_id:
        # FIXME doesn't check for existing so if the name changes we get duped folders
        # this issue possibly upstream in retrieve, clone just clones whatever you tell
        # it to clone, but maybe it should check the existing metadata and fail or warn?
        dataset_path = from_path_project_backend_id_dataset(
            parent_path,
            project_id,
            id,  # FIXME multiple datasets
            RemotePath,
            symlink_objects_to,)

        return dataset_path

    project_path = from_path_id_and_backend_project_top_level(
        parent_path,
        project_id,
        RemotePath,
        symlink_objects_to,)

    return project_path


if __name__ == '__main__':
    from sparcur.simple.utils import pipe_main
    pipe_main(main, after=print)
# clone.py ends here
