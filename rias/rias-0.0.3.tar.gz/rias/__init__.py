import sys
import func

def main() -> None:
    """
    Simple Test Function
    """
    user_data = sys.argv
    print(user_data)
    func.flayer()
    sys.exit(0)

if __name__ == "__main__":
    main()