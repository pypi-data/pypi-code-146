import argparse
import importlib
import logging
import os
import shutil

from meteo_render import render_weather


def coordinates(s):
    values = s.split(",")
    assert len(values) == 2
    lat, long = (float(a) for a in values)
    return lat, long


def existing_folder(s):
    assert os.path.isdir(s)
    return s


def existing_or_new_file(s):
    if not os.path.exists(s):
        folder = os.path.dirname(s)
        assert os.path.isdir(folder)
    return s


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t", "--template",
        required=True,
    )
    parser.add_argument(
        "-l", "--location",
        required=False,
        type=coordinates
    )
    parser.add_argument(
        "-i", "--images",
        required=False,
        type=existing_folder
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--deploy-static",
        type=existing_folder
    )
    group.add_argument(
        "--render-weather",
        type=existing_or_new_file
    )

    args = parser.parse_args()
    if args.render_weather:
        assert args.location is not None, "You must provide a location to render weather data"

    return args


def get_template_folder(template_name):
    package_name = "meteo_render"
    spec = importlib.util.find_spec(package_name)
    assert len(spec.submodule_search_locations) == 1
    spec_location = spec.submodule_search_locations[0]
    logging.debug("Assuming that %s is the module location" % (spec_location, ))
    path = os.path.join(spec_location, "templates", template_name)
    assert os.path.isdir(path)
    return path


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    args = get_args()

    if args.deploy_static:
        src_folder = get_template_folder(args.template)
        for file in os.listdir(src_folder):
            if file.endswith("j2"):
                continue
            src = os.path.join(src_folder, file)
            if os.path.isdir(src):
                continue
            dest = os.path.join(args.deploy_static, file)
            logging.debug("Copying %s to %s" % (src, dest))
            shutil.copy(src, dest)

        img_folder = os.path.join(src_folder, "img")
        img_dest = os.path.join(args.deploy_static, "img")
        if not os.path.exists(img_dest):
            os.mkdir(img_dest)
        else:
            assert os.path.isdir(img_dest)

        for file in os.listdir(img_folder):
            src = os.path.join(img_folder, file)
            dest = os.path.join(img_dest, file)
            logging.debug("Copying %s to %s" % (src, dest))
            shutil.copy(src, dest)
    else:
        image_folder = args.images or os.path.join(os.path.dirname(args.render_weather), "img")
        logging.debug("Using %s as the images folder" % (image_folder, ))
        page = render_weather(args.location, args.template, image_folder)
        logging.debug("Rendering the weather at %s to %s" % (args.location, args.render_weather))
        with open(args.render_weather, "w") as f:
            f.write(page)
