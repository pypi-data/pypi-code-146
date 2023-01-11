import argparse
from pathlib import Path
from lxml import etree


def get_xunit_result_xml():
    root_node = etree.Element("testsuites")
    root_node.set('failures', '0')
    root_node.set('tests', '0')
    return root_node


def add_test_results_to_xunit_results_xml(results_xml, test_suit_name, passed_test, failed_tests, test_id):
    number_of_failed_test = len(failed_tests)
    results_xml.set('failures', results_xml.get('failures') + str(number_of_failed_test))

    number_of_test_in_suit = len(passed_test) + number_of_failed_test
    results_xml.set('tests', results_xml.get('tests') + str(number_of_test_in_suit))

    testsuite_node = etree.Element("testsuite")
    testsuite_node.set('id', str(test_id))
    testsuite_node.set('name', test_suit_name)
    testsuite_node.set('tests', str(number_of_test_in_suit))
    testsuite_node.set('failures', str(number_of_failed_test))
    for test_name in passed_test:
        test_node = etree.Element("testcase")
        test_node.set('name', test_name)
        test_node.set('assertions', '3')
        test_node.set('classname', test_name)
        test_node.set('status', 'PASS')
        testsuite_node.append(test_node)

    for test_name in failed_tests:
        test_node = etree.Element("testcase")
        test_node.set('name', test_name)
        test_node.set('assertions', '3')
        test_node.set('classname', test_name)
        test_node.set('status', 'FAILED')
        failure_node = etree.Element("failure")
        failure_node.set('exception-type', 'no clue')
        message_node = etree.Element("message")
        message_node.text = etree.CDATA('message')
        stack_trace_node = etree.Element("stack-trace")
        stack_trace_node.text = etree.CDATA('stack-trace')
        failure_node.append(message_node)
        failure_node.append(stack_trace_node)
        test_node.append(failure_node)
        testsuite_node.append(test_node)

    results_xml.append(testsuite_node)
    return test_id + 1


def filter_out_black_list_files(black_list, files, name_pattern):
    tmp = {}
    for file_path in files:
        if file_path.is_file():
            res = [ele for ele in black_list if (ele in str(file_path.relative_to(src)))]
            if len(res) > 0:
                pass
            else:
                device_name = file_path.name.replace(name_pattern, '')
                if device_name in tmp:
                    pass
                else:
                    tmp[device_name] = file_path
    return tmp


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('project_path', help='TwinCAT project folder path')
    args = parser.parse_args()
    src = args.project_path
    pou_suffix = '.TcPOU'
    config_suffix = '_config.xml'

    folderIgnoreList = ['_internal', 'Utilities']
    pous = filter_out_black_list_files(folderIgnoreList, Path(src).rglob(f'*{pou_suffix}'), pou_suffix)
    configs = filter_out_black_list_files(folderIgnoreList, Path(src).rglob(f'*{config_suffix}'), config_suffix)

    pou_names = set(pous.keys())
    configs_names = set(configs.keys())
    pous_without_config = (pou_names - configs_names)
    config_without_pou = (configs_names - pou_names)
    the_good_ones = pou_names - pous_without_config

    for x in the_good_ones:
        if str(pous[x].joinpath()).replace(f'{x}{pou_suffix}', '') == str(configs[x].joinpath()).replace(f'{x}{config_suffix}', ''):
            pass
        else:
            print(f'POU and config of {x} are not in the same folder.')
            print(f'POU files is in folder {pous[x].joinpath()}')
            print(f'Config files is in folder {configs[x].joinpath()}')

    xunit_results_xml = get_xunit_result_xml()
    test_id = 0
    # check if POU has config
    test_id = add_test_results_to_xunit_results_xml(xunit_results_xml,
                                                    'Test if POU has config',
                                                    the_good_ones,
                                                    pous_without_config,
                                                    test_id)

    # check if config has POU
    test_id = add_test_results_to_xunit_results_xml(xunit_results_xml,
                                                    'Test if config has POU',
                                                    the_good_ones,
                                                    config_without_pou,
                                                    test_id)

    # check if pou and config are in the same folder

    tree = etree.ElementTree(xunit_results_xml)
    tree.write('TcArch_results.xml', pretty_print=True)
    if len(pous_without_config) > 0 or len(config_without_pou) > 0:
        exit(1)
    else:
        exit(0)



