from testdata.test_data_manager import TestDataManager


def main():
    try:
        manager = TestDataManager()
        manager.menu()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(__package__)
    main()
