import sys
from layer import flayer


def main() -> None:
    """
    Simple Test Function
    """
    user_data = sys.argv
    print(user_data)
    flayer()
    sys.exit(0)


if __name__ == "__main__":
    main()
