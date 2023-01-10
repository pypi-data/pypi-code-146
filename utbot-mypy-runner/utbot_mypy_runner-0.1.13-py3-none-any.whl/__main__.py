import argparse

import utbot_mypy_runner.mypy_main as mypy_main
import utbot_mypy_runner.extract_annotations as extraction
import utbot_mypy_runner.expression_traverser as expression_traverser


parser = argparse.ArgumentParser()
parser.add_argument('--config', required=True)
parser.add_argument('--sources', required=True, nargs='+')
parser.add_argument('--annotations_out')
parser.add_argument('--mypy_stdout')
parser.add_argument('--mypy_stderr')
parser.add_argument('--mypy_exit_status')
parser.add_argument('--file_for_types')

args = parser.parse_args()

stdout, stderr, exit_status, build_result = mypy_main.run(
     args.sources + ["--config-file", args.config]
)

if args.mypy_stdout is not None:
    with open(args.mypy_stdout, "w") as file:
        file.write(stdout)
    print("Wrote mypy stdout to", args.mypy_stdout)

if args.mypy_stderr is not None:
    with open(args.mypy_stderr, "w") as file:
        file.write(stderr)
    print("Wrote mypy stderr to", args.mypy_stderr)

if args.mypy_exit_status is not None:
    with open(args.mypy_exit_status, "w") as file:
        file.write(str(exit_status))
    print("Wrote mypy exit status to", args.mypy_exit_status)

if args.annotations_out is not None:
    if build_result is not None:
        with open(args.annotations_out, "w") as file:
            file.write(extraction.get_result_from_mypy_build(build_result, args.sources, args.file_for_types))
        print("Extracted annotations and wrote to", args.annotations_out)
