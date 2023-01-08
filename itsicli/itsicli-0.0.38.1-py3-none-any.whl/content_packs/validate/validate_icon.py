from itsicli.content_packs.workspace import root_path
from itsicli.content_packs.validate.result import Level, result


class ValidateIcon(object):

    in_progress_text = 'Checking for icon'
    icon_dir = ('appserver', 'static')

    def run(self, *args, **kwargs):
        path = root_path()
        icon_path = path.joinpath(*self.icon_dir, 'icon.png')

        if not icon_path.exists():
            results = [
                result(Level.ERROR, "Add a 200x200px icon file at '{}'.".format(icon_path))
            ]
        else:
            results = []

        return results
