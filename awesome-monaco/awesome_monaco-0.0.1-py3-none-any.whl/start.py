from brains.build_data import build_report
from brains.parser import get_args
from brains.report import print_report


def main():
    args = get_args()
    report = build_report(folder = args.files, driver=args.driver, reverse=args.desc)
    print_report(report, reverse=args.desc)

if __name__ == "__main__":
    main()
