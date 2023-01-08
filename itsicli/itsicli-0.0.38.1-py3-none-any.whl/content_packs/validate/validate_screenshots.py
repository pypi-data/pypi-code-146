from itsicli.content_packs.files import CONTENT_PACK_SCREENSHOTS_DIR, ContentPackManifest
from itsicli.content_packs.validate.result import Level, result


class ValidateScreenshots(object):

    in_progress_text = 'Checking for screenshots'

    def run(self, home_path, *args, **kwargs):
        results = []

        manifest = ContentPackManifest(home_path)

        if not manifest.path.exists():
            results.append(
                result(
                    Level.ERROR, "Missing manifest '{}' file.".format(manifest.path)
                )
            )
            return results

        if not manifest.main_screenshot:
            results.append(
                result(
                    Level.ERROR, "Define a '{}' property in '{}'.".format(manifest.attr_main_screenshot, manifest.path)
                )
            )
        else:
            results.extend(
                self.validate_screenshot(manifest.main_screenshot,
                                         home_path=home_path,
                                         name=manifest.attr_main_screenshot)
            )

        screenshots = manifest.screenshots or []
        if not screenshots:
            results.append(
                result(
                    Level.WARNING, "Try to include some screenshots with the '{}' property in '{}'.".format(
                        manifest.screenshots, manifest.path)
                )
            )
        else:
            for index, screenshot in enumerate(screenshots):
                name = 'screenshot {}'.format(index + 1)
                results.extend(
                    self.validate_screenshot(screenshot, home_path=home_path, name=name)
                )

        return results

    def validate_screenshot(self, screenshot, home_path, name):
        results = []

        def validate_screenshot_attr(attr):
            file_name = screenshot.get(attr)

            if not file_name:
                results.append(
                    result(Level.ERROR, "Add a valid '{}' property for '{}'".format(attr, name))
                )

            else:
                screenshots_dir = home_path.joinpath(*CONTENT_PACK_SCREENSHOTS_DIR)

                image_path = screenshots_dir.joinpath(file_name)

                if not image_path.exists() or image_path.is_dir():
                    results.append(
                        result(Level.ERROR, "Add a valid screenshot image at '{}'".format(image_path))
                    )

        validate_screenshot_attr('thumb')
        validate_screenshot_attr('path')

        return results
