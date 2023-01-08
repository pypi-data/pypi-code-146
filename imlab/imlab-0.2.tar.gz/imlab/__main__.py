import argparse
import os

from .core import detect, load

path_dir = os.path.dirname(os.path.abspath(__file__))


def script():
    p = argparse.ArgumentParser(description="")

    p.add_argument("image", type=str, help="image to be processed")
    p.add_argument(
        "-o",
        "--output",
        type=str,
        default="",
        help="save newly created image with  bouding box",
    )
    p.add_argument("--show", action="store_true", help="show the picture")
    p.add_argument(
        "--score",
        type=int,
        default=0,
        help="show the score on the picture, number of decimals",
    )

    p.add_argument(
        "-m",
        "--model",
        type=str,
        default=os.path.join(path_dir, "model", "yoloV7_coco.extractor"),
        help="load the model path",
    )
    args = p.parse_args()
    model = load(args.model)
    detect(args.image, model, show=args.show, save=args.output, score=args.score)
