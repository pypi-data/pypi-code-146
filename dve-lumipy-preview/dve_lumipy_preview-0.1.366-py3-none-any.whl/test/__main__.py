import argparse
import inspect
import time

from lumipy.test.integration import ClientTests, AtlasBuildQueryTests
import lumipy.test.unit as unit
import lumipy.test.integration as integration
import lumipy.test.provider as provider
import lumipy.test.meta_test as meta

from multiprocessing import Queue

from lumipy.test.test_infra import LumipyTestWorker
from termcolor import colored
from lumipy.common.string_utils import indent_str
import sys


parser = argparse.ArgumentParser(
    prog='Lumipy Testing',
    description='This module runs the lumipy tests',
)
parser.add_argument('manifest', choices=['everything', 'unit', 'integration', 'provider', 'merge-request', 'meta'])
parser.add_argument('-n', '--max_workers', default=16, dest='max_workers', type=int)
parser.add_argument('-v', '--verbosity', default=2, dest='verbosity', type=int)


def get_test_suite(label):

    def get_test_cases(module):

        test_cases = []
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                test_cases.append(obj)

        return test_cases

    if label == 'integration':
        return get_test_cases(integration)
    elif label == 'unit':
        return get_test_cases(unit)
    elif label == 'everything':
        return get_test_cases(unit) + get_test_cases(integration) + get_test_cases(provider)
    elif label == 'provider':
        return get_test_cases(provider)
    elif label == 'merge-request':
        return get_test_cases(unit) + [ClientTests, AtlasBuildQueryTests]
    elif label == 'meta':
        return get_test_cases(meta)
    else:
        raise NotImplementedError(
            f'Unimplemented value for manifest "{label}"'
        )


def hline(width=64):
    print('―' * width)


def make_label(label):
    return colored(label, attrs=['reverse'])


if __name__ == '__main__':

    args = parser.parse_args()

    suite = get_test_suite(args.manifest)

    n_workers = args.max_workers if len(suite) >= args.max_workers else len(suite)

    sub_manifests = {i: [] for i in range(n_workers)}
    for i, test_case in enumerate(suite):
        sub_manifests[i % n_workers].append(test_case)

    queue = Queue()
    processes = [LumipyTestWorker(s, args.verbosity, queue) for s in sub_manifests.values()]

    hline()
    print(f'Running the {args.manifest} test suite 🧪 (workers = {n_workers})')
    hline()

    start = time.time()
    for process in processes:
        process.start()

    logs = {process.name: [] for process in processes}
    total_tests, errors, failures = 0, [], []

    done_count = 0
    while done_count != n_workers:
        name, el_type, x = queue.get()
        if el_type == 'log_line':
            logs[name].append(x)
        elif el_type == 'exception':
            msg = colored(f'Exception outside a test in {name}: no results were recorded!\n', 'red')
            logs[name].append(msg)
            logs[name].append(x)
            done_count += 1
            print(f'{name:21s} has errored! ({done_count/n_workers})')
        elif el_type == 'result':
            total_tests += x[0]
            errors += x[1]
            failures += x[2]
            done_count += 1
            print(f'{name:21s} has finished. ({done_count}/{n_workers})')
        else:
            raise NotImplementedError(f'Unrecognised queue element type: {el_type}.')

    for process in processes:
        process.join()

    hline()
    logs_str = ''.join(f'\n{make_label(name)}\n' + ''.join(lines) for name, lines in logs.items())
    print('Logs:\n' + indent_str(logs_str), end='\n\n')

    hline()
    print('Stats:')
    print(f'   Elapsed time:  {time.time() - start:>2.1f}s')
    print(f'   Passed Tests:  {total_tests - len(failures) - len(errors)}')
    print(f'   Errored Tests: {len(errors)}')
    print(f'   Failed Tests:  {len(failures)}')

    hline()
    if len(errors) > 0 or len(failures) > 0:
        print('Failed Tests Summary:')

        for test_name, error in errors:
            print(f"{colored(f'   ERRORED: {test_name}', 'red')}\n{indent_str(error, 6)}")

        for test_name, failure in failures:
            print(f"{colored(f'   FAILURE: {test_name}', 'red')}\n{indent_str(failure, 6)}")

        sys.exit(colored('🚨 There are unsuccessful tests! 🚨', 'red'))
