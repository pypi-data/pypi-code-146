from tabulate import tabulate
from colorama import init as colorama_init
from colorama import Fore

from onnx_diff.structs import SummaryResults

colorama_init()

def color(text: str, success: bool) -> str:
    return f"{Fore.GREEN if success else Fore.RED}{text}{Fore.RESET}"


def passfail_string(success: bool):
    text = "Pass" if success else "Fail"
    return color(text=text, success=success)


def matches_string(count: int, total: int):
    text = f"{count}/{total}"
    return color(text=text, success=(count == total))


def print_summary(results: SummaryResults) -> None:
    print("---- ONNX Diff Summary ----")

    text = (
        "Exact Match"
        if results.exact_match and results.score == 1.0
        else "Difference Detected"
    )
    print(f"{text} ({round(results.score * 100, 6)}%)")

    print("")
    # validation results to table.
    data = [
        [
            "Validate",
            passfail_string(results.a_valid),
            passfail_string(results.b_valid),
        ],
    ]
    # matches to table.
    for key, matches in results.matches.items():
        data.append(
            [
                key.capitalize(),
                matches_string(matches[0], matches[1]),
                matches_string(matches[0], matches[2]),
            ]
        )

    print(tabulate(data, headers=["", "A", "B"]))
