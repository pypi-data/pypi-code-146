import re
from itsicli.content_packs.files import ContentPackConfig
from itsicli.content_packs.validate.result import Level, result
from itsicli.content_packs.workspace import root_path


class ValidateConfig(object):

    in_progress_text = 'Checking {}'.format(ContentPackConfig.file_name)

    def run(self, *args, **kwargs):
        config = ContentPackConfig(root_path())

        results = []

        if not config.exists():
            results.append(
                result(
                    Level.ERROR, "Missing '{}' file.".format(config.path)
                )
            )
            return results

        title = config.title
        if not title:
            results.append(
                result(
                    Level.ERROR, "Add a 'title' setting in '{}'.".format(config.path)
                )
            )

        version = config.version
        if not version:
            results.append(
                result(
                    Level.ERROR, "Add a valid 'version' setting in '{}'.".format(config.path)
                )
            )
        else:
            version_re = r'^(\d+\.)(\d+\.)(\*|\d+)$'
            matched = re.match(version_re, version)
            if not matched:
                results.append(
                    result(
                        Level.ERROR, "'version' {} in '{}' does not conform to x.x.x format.".format(
                            version, config.path)
                    ))

        description = config.description
        if not description:
            results.append(
                result(
                    Level.WARNING, "Add a valid 'description' setting in '{}'.".format(config.path)
                )
            )

        return results
