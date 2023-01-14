from unittest.suite import TestSuite
import argparse
import unittest
import sys


def unit_test() -> TestSuite:
    loader = unittest.TestLoader()
    return loader.discover('.', pattern='test_*.py')


def integration_test() -> TestSuite:
    loader = unittest.TestLoader()
    return loader.discover('.', pattern='integration_test_*.py')


def lint_tests() -> TestSuite:
    loader = unittest.TestLoader()
    return loader.discover('.', pattern='lint_test_*.py')


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument('-u', '--unit', dest='unit',
                        action='store_true', help='Run unit tests')
    parser.add_argument('-i', '--integration', dest='integration',
                        action='store_true', help='Run integration tests')
    parser.add_argument('-l', '--lint', dest='lint',
                        action='store_true', help='Run lint tests')
    parser.add_argument('-a', '--all', dest='all',
                        action='store_true', help='Run all tests')

    args = parser.parse_args()

    test_suites: list[TestSuite] = []

    if args.unit:
        test_suites.append(unit_test())

    if args.integration:
        test_suites.append(integration_test())

    if args.lint:
        test_suites.append(lint_tests())

    if args.all:
        test_suites.append(unit_test())
        test_suites.append(integration_test())
        test_suites.append(lint_tests())

    combined_suite = unittest.TestSuite(test_suites)
    result = unittest.TextTestRunner().run(combined_suite)

    exit_code = 0 if result.wasSuccessful() else 1
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
