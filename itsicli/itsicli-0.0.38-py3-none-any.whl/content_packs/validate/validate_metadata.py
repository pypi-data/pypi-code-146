from itsicli.content_packs.workspace import root_path
from itsicli.content_packs.validate.result import Level, result


class ValidateMetadata(object):

    in_progress_text = 'Checking for metadata'
    meta_data_dir = ['metadata']

    def run(self, *args, **kwargs):
        path = root_path()
        metadata_dir_path = path.joinpath(*self.meta_data_dir)
        matadata_default_conf_file = path.joinpath(
            *self.meta_data_dir, 'default.meta')

        if metadata_dir_path.exists():
            results = [
                result(Level.WARNING, "metadata directory found at '{}', please remove this directory or reach out to Content Library team in case of concerns.".format(
                    metadata_dir_path))
            ]
            if matadata_default_conf_file.exists():
                results.append(
                    result(Level.WARNING, "default.meta file found at '{}', please remove this file or reach out to Content Library team in case of concerns.".format(
                        matadata_default_conf_file))
                )
        else:
            results = []

        return results
