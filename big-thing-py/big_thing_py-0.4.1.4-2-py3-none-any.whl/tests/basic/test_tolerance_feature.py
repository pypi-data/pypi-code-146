from big_thing import *
from tests.tools.build_env import *
from tests.tools.check import *
from big_thing_py.tests.tools.utils import *


'''
Feature for test

Thing Tolerance Feature test

- [ ]  Torlerence test
    - [o]  Thing register & unregister while scenario running
        - 아무런 조치가 없는 경우 시나리오가 stuck이 된다.
        - 만약 running 상태에서 update를 하게되면 정상적으로 run이 된다
    - [o]  Thing tag delete while scenario running
        - update를 안하면 기존대로 잘 execute가 되지만 update를 하면 update자체가 실패한다
    - [ ]  Multi scenario concorrent running
        - 여러 시나리오를 읽어서 등록하고 expect 파일도 여러개가 동시에 되는 방법을 생각해야한다.
'''


def test_thing_tolerance():
    scenario_name = 'thing_tolerance'

    mqtt_monitor_client = make_middleware(
        level=1, with_parent=False, clean_start=True)['mqtt_client']
    basic_test_thing_info1 = make_thing(
        mqtt_monitor_client, level=1, index=1, thing_file_base_name='basic_big_thing')
    basic_test_thing_info2 = make_thing(
        mqtt_monitor_client, level=1, index=2, thing_file_base_name='basic_big_thing')

    check_thing_exist(mqtt_monitor_client,
                      basic_test_thing_info1['thing_name_with_mac'],)

    test_dir = os.path.dirname(os.path.realpath(__file__))
    run_result, _ = check_scenario(mqtt_monitor_client, scenario_name,
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.txt',
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.json')

    run_result, _ = check_scenario(mqtt_monitor_client,  scenario_name,
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.txt',
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.json',
                                   stop=False, update=False, delete=False)

    stop_thing_local(mqtt_monitor_client, basic_test_thing_info2)

    check_scenario_update(mqtt_monitor_client, scenario_name)
    run_result, _ = check_scenario(mqtt_monitor_client,  scenario_name,
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.txt',
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.json',
                                   verify=False, add=False, run=True, stop=False, update=False, delete=False)

    check_scenario_stop(mqtt_monitor_client, scenario_name)
    check_scenario_delete(mqtt_monitor_client, scenario_name)

    SOPTEST_LOG_DEBUG(f'==== {scenario_name} test pass! ====', 0)

    stop_thing_local(mqtt_monitor_client, basic_test_thing_info1)
    stop_thing_local(mqtt_monitor_client, basic_test_thing_info2)

    return wrapup_env(mqtt_monitor_client)


def test_thing_tolerance_all_prefix():
    scenario_name = 'thing_tolerance_all_prefix'

    mqtt_monitor_client = make_middleware(
        level=1, with_parent=False, clean_start=True)['mqtt_client']
    basic_test_thing_info1 = make_thing(
        mqtt_monitor_client, level=1, index=1, thing_file_base_name='basic_big_thing')

    test_dir = os.path.dirname(os.path.realpath(__file__))
    run_result, _ = check_scenario(mqtt_monitor_client,  scenario_name,
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.txt',
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}1.json',
                                   stop=False, update=False, delete=False)

    basic_test_thing_info2 = make_thing(
        mqtt_monitor_client, level=1, index=2, thing_file_base_name='basic_big_thing')
    check_scenario_update(mqtt_monitor_client, scenario_name)
    run_result, _ = check_scenario(mqtt_monitor_client,  scenario_name,
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.txt',
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}2.json',
                                   verify=False, add=False, run=True, stop=True, update=False, delete=True)

    SOPTEST_LOG_DEBUG(f'==== {scenario_name} test pass! ====', 0)

    stop_thing_local(mqtt_monitor_client, basic_test_thing_info1)
    stop_thing_local(mqtt_monitor_client, basic_test_thing_info2)

    return wrapup_env(mqtt_monitor_client)


def test_thing_tolerance_tag_delete_with_substitute():
    scenario_name = 'thing_tolerance_tag_delete_with_substitute'

    mqtt_monitor_client = make_middleware(
        level=1, with_parent=False, clean_start=True)['mqtt_client']
    basic_test_thing_info1 = make_thing(
        mqtt_monitor_client, level=1, index=1, thing_file_base_name='basic_big_thing')
    basic_test_thing_info2 = make_thing(
        mqtt_monitor_client, level=1, index=2, thing_file_base_name='basic_big_thing')

    test_dir = os.path.dirname(os.path.realpath(__file__))
    run_result, _ = check_scenario(mqtt_monitor_client,  scenario_name,
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.txt',
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.json',
                                   stop=False, update=False, delete=False)

    check_tag_delete(mqtt_monitor_client, 'str_function_with_arg',
                     basic_test_thing_info1['thing_name'], 'normal_string1', basic_test_thing_info1['middleware_name'])
    check_scenario_update(mqtt_monitor_client, scenario_name)
    run_result, _ = check_scenario(mqtt_monitor_client, scenario_name,
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.txt',
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.json',
                                   verify=False, add=False, run=True, stop=True, update=False, delete=True)

    SOPTEST_LOG_DEBUG(f'==== {scenario_name} test pass! ====', 0)

    stop_thing_local(mqtt_monitor_client, basic_test_thing_info1)
    stop_thing_local(mqtt_monitor_client, basic_test_thing_info2)

    return wrapup_env(mqtt_monitor_client)


def test_thing_tolerance_tag_delete_no_substitute():
    scenario_name = 'thing_tolerance_tag_delete_no_substitute'

    mqtt_monitor_client = make_middleware(
        level=1, with_parent=False, clean_start=True)['mqtt_client']
    basic_test_thing_info1 = make_thing(
        mqtt_monitor_client, level=1, index=1, thing_file_base_name='basic_big_thing')

    test_dir = os.path.dirname(os.path.realpath(__file__))
    run_result, _ = check_scenario(mqtt_monitor_client,  scenario_name,
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.txt',
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.json',
                                   stop=False, update=False, delete=False)

    tag_name = 'normal_string1'
    check_tag_delete(mqtt_monitor_client, 'str_function_with_arg',
                     basic_test_thing_info1['thing_name'], tag_name, basic_test_thing_info1['middleware_name'])

    update_result = check_scenario_update(mqtt_monitor_client, scenario_name)
    if not update_result:
        SOPTEST_LOG_DEBUG(
            f'Scenario update failed! -- thing not found! -- omited tags: {tag_name}', 0)
        check_scenario_stop(mqtt_monitor_client, scenario_name)
        check_scenario_delete(mqtt_monitor_client, scenario_name)
        SOPTEST_LOG_DEBUG(f'==== {scenario_name} test pass! ====', 0)

    stop_thing_local(mqtt_monitor_client, basic_test_thing_info1)

    return wrapup_env(mqtt_monitor_client)


if __name__ == '__main__':
    test_thing_tolerance()
    test_thing_tolerance_all_prefix()
    test_thing_tolerance_tag_delete_with_substitute()
    test_thing_tolerance_tag_delete_no_substitute()
