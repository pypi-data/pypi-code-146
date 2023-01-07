import argparse
import onnx
from onnx_diff.diff import OnnxDiff


def run() -> None:
    parser = argparse.ArgumentParser(
        description="A tool to find differences between ONNX files."
    )
    parser.add_argument("model_a", metavar="A", help="ONNX model A to compare")
    parser.add_argument("model_b", metavar="B", help="ONNX model B to compare")
    parser.add_argument("-v", "--verbose", required=False, help="Print verbose output")
    args = parser.parse_args()

    model_a = onnx.load(args.model_a)
    model_b = onnx.load(args.model_b)

    diff = OnnxDiff(model_a=model_a, model_b=model_b, verbose=args.verbose)

    results = diff.summary(output=True)
