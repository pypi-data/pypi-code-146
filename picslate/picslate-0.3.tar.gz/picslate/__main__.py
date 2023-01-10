import argparse

from .core import convert


def script():
    p = argparse.ArgumentParser(description="")

    p.add_argument("image", type=str, help="image to be translated")
    p.add_argument("from_lang", type=str, help="picture's language in ISO 639-1")
    p.add_argument("to_lang", type=str, help="language to translate in ISO 639-1")
    p.add_argument(
        "-o", "--output", type=str, default="", help="save the newly translated picture"
    )
    p.add_argument("--show", action="store_true", help="show the picture")
    p.add_argument(
        "--translator",
        type=str,
        default="auto",
        help="translator to be used, can be 'auto','translate' or 'argos' ",
    )
    p.add_argument(
        "--corrector",
        type=str,
        default="False",
        help="Use a corrector, can be False, or a dictionnary like aspell.",
    )
    p.add_argument(
        "--debug", action="store_true", help="show text bouding box of the picture"
    )

    args = p.parse_args()
    convert(
        args.image,
        args.from_lang,
        args.to_lang,
        path_save=args.output,
        show=args.show,
        translator=args.translator,
        corrector=args.corrector,
        debug=args.debug,
    )
