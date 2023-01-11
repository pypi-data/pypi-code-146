from big_thing import *
from big_thing_py.tests.tools.utils import *
from big_thing_py.tests.tools.elements import *


'''
Feature for test

Thing Feature test

- [o]  Middleware online check
- [o]  Register
- [o]  Alive
- [o]  Value publish
- [o]  Function execute
    - [o]  success
    - [o]  fail
    - [o]  timeout
    
Scenario Feature test

- [o]  User interaction test
    - [o]  Request test
        - [o]  ADD
        - [o]  VERIFY
        - [o]  DELETE
        - [o]  RUN
        - [o]  STOP
        - [o]  UPDATE
        - [o]  ADD_TAG
        - [o]  DELETE_TAG
    - [o]  Result test
        - [o]  ADD
        - [o]  VERIFY
        - [o]  DELETE
        - [o]  RUN
        - [o]  STOP
        - [o]  UPDATE
        - [o]  ADD_TAG
        - [o]  DELETE_TAG
- [o]  Feature test
    - [o]  loop
    - [o]  if-else
        - [o]  if
        - [o]  else if
        - [o]  else
    - [o]  Logical operator
        - [o]  and
        - [o]  or
    - [o]  value cache
    - [o]  function execute
    - [o]  "all" prefix
    - [o]  wait until
        - [o]  time
        - [o]  condition
    - [o]  tag
        - [o]  one tag scoping
        - [o]  multi tag scoping
    - [o]  variable (`x = (#tag1).function_service()`)
'''


# def print_test_result():
#     pass


# def add_mqtt_client(mqtt_client: SoPMQTTMonitor):
#     def real_decorator(func):
#         def wrap(*args, **kwargs):
#             return func(*args, **kwargs)
#         return wrap
#     return real_decorator


def test_basic_feature():
    scenario_name = 'test_scenario'

    mqtt_monitor_client = make_middleware(
        level=1, with_parent=False, clean_start=True)['mqtt_client']
    basic_test_thing_info1 = make_thing(
        mqtt_monitor_client, level=1, index=1, thing_file_base_name='basic_big_thing')

    check_alive(mqtt_monitor_client,
                basic_test_thing_info1['thing_name_with_mac'], timeout=basic_test_thing_info1['alive_cycle'] * 3)
    check_value_publish(mqtt_monitor_client, basic_test_thing_info1['thing_name_with_mac'],
                        basic_test_thing_info1['value_list'], timeout=10)
    check_function_execute(mqtt_monitor_client,
                           basic_test_thing_info1['thing_name_with_mac'], basic_test_thing_info1['function_list'], scenario_name, timeout=10)

    SOPTEST_LOG_DEBUG(
        f'==== {get_current_function_name()} Test Pass! ====', 0)

    stop_thing_local(mqtt_monitor_client, basic_test_thing_info1)

    return wrapup_env(mqtt_monitor_client)


def test_tag_add_delete():
    mqtt_monitor_client = make_middleware(
        level=1, with_parent=False, clean_start=True)['mqtt_client']
    basic_test_thing_info1 = make_thing(
        mqtt_monitor_client, level=1, index=1, thing_file_base_name='basic_big_thing')

    check_tag_add(mqtt_monitor_client, 'int_function_no_arg',
                  basic_test_thing_info1['thing_name_with_mac'], 'tag1', basic_test_thing_info1['middleware_name'])
    check_tag_delete(mqtt_monitor_client, 'int_function_no_arg',
                     basic_test_thing_info1['thing_name_with_mac'], 'tag1', basic_test_thing_info1['middleware_name'])

    SOPTEST_LOG_DEBUG(f'==== Tag Add & Delete test pass! ====', 0)

    stop_thing_local(mqtt_monitor_client, basic_test_thing_info1)

    return wrapup_env(mqtt_monitor_client)


def test_scenario_function_execute():
    scenario_name = 'function_execute'

    mqtt_monitor_client = make_middleware(
        level=1, with_parent=False, clean_start=True, port=11883)['mqtt_client']
    basic_test_thing_info1 = make_thing(
        mqtt_monitor_client, level=1, index=1, thing_file_base_name='basic_big_thing')

    check_thing_exist(mqtt_monitor_client,
                      basic_test_thing_info1['thing_name_with_mac'],)

    test_dir = os.path.dirname(os.path.realpath(__file__))
    run_result, _ = check_scenario(mqtt_monitor_client,
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.txt',
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.json')

    SOPTEST_LOG_DEBUG(f'==== {scenario_name} test pass! ====', 0)

    stop_thing_local(mqtt_monitor_client, basic_test_thing_info1)

    return wrapup_env(mqtt_monitor_client)


def test_scenario_loop():
    scenario_name = 'loop'

    mqtt_monitor_client = make_middleware(
        level=1, with_parent=False, clean_start=True)['mqtt_client']
    basic_test_thing_info1 = make_thing(
        mqtt_monitor_client, level=1, index=1, thing_file_base_name='basic_big_thing')

    test_dir = os.path.dirname(os.path.realpath(__file__))
    run_result, _ = check_scenario(mqtt_monitor_client, scenario_name,
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.txt',
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.json')

    SOPTEST_LOG_DEBUG(f'==== {scenario_name} test pass! ====', 0)

    stop_thing_local(mqtt_monitor_client, basic_test_thing_info1)

    return wrapup_env(mqtt_monitor_client)


def test_scenario_variable_if_else():
    scenario_name = 'variable_if_else'

    mqtt_monitor_client = make_middleware(
        level=1, with_parent=False, clean_start=True)['mqtt_client']
    basic_test_thing_info1 = make_thing(
        mqtt_monitor_client, level=1, index=1, thing_file_base_name='basic_big_thing')

    test_dir = os.path.dirname(os.path.realpath(__file__))
    run_result, _ = check_scenario(mqtt_monitor_client, scenario_name,
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.txt',
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.json')
    SOPTEST_LOG_DEBUG(f'==== {scenario_name} test pass! ====', 0)

    stop_thing_local(mqtt_monitor_client, basic_test_thing_info1)

    return wrapup_env(mqtt_monitor_client)


def test_scenario_wait_until():
    scenario_name = 'wait_until'

    mqtt_monitor_client = make_middleware(
        level=1, with_parent=False, clean_start=True)['mqtt_client']
    basic_test_thing_info1 = make_thing(
        mqtt_monitor_client, level=1, index=1, thing_file_base_name='basic_big_thing')

    test_dir = os.path.dirname(os.path.realpath(__file__))
    run_result, _ = check_scenario(mqtt_monitor_client, scenario_name,
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.txt',
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.json')
    SOPTEST_LOG_DEBUG(f'==== {scenario_name} test pass! ====', 0)

    stop_thing_local(mqtt_monitor_client, basic_test_thing_info1)

    return wrapup_env(mqtt_monitor_client)


def test_scenario_all_prefix():
    scenario_name = 'all_prefix'

    mqtt_monitor_client = make_middleware(
        level=1, with_parent=False, clean_start=True)['mqtt_client']
    basic_test_thing_info1 = make_thing(
        mqtt_monitor_client, level=1, index=1, thing_file_base_name='basic_big_thing')
    basic_test_thing_info2 = make_thing(
        mqtt_monitor_client, level=1, index=2, thing_file_base_name='basic_big_thing')

    test_dir = os.path.dirname(os.path.realpath(__file__))
    run_result, _ = check_scenario(mqtt_monitor_client, scenario_name,
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.txt',
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.json')
    SOPTEST_LOG_DEBUG(f'==== {scenario_name} test pass! ====', 0)

    stop_thing_local(mqtt_monitor_client, basic_test_thing_info1)
    stop_thing_local(mqtt_monitor_client, basic_test_thing_info2)

    return wrapup_env(mqtt_monitor_client)


def test_scenario_tag_scoping():
    scenario_name = 'tag_scoping'

    mqtt_monitor_client = make_middleware(
        level=1, with_parent=False, clean_start=True)['mqtt_client']
    basic_test_thing_info1 = make_thing(
        mqtt_monitor_client, level=1, index=1, thing_file_base_name='basic_big_thing')

    test_dir = os.path.dirname(os.path.realpath(__file__))
    run_result, _ = check_scenario(mqtt_monitor_client, scenario_name,
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.txt',
                                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.json')
    SOPTEST_LOG_DEBUG(f'==== {scenario_name} test pass! ====', 0)

    stop_thing_local(mqtt_monitor_client, basic_test_thing_info1)

    return wrapup_env(mqtt_monitor_client)


def test_multi_scenario():
    scenario_name = 'multi_scenario'

    mqtt_monitor_client1 = make_middleware(
        level=1, with_parent=False, clean_start=True)['mqtt_client']
    basic_test_thing_info1 = make_thing(
        mqtt_monitor_client1, level=1, index=1, thing_file_base_name='basic_big_thing')

    result_queue = Queue()

    mqtt_monitor_client2 = SoPMQTTMonitor(
        name=f'mqtt_monitor_level{2}', port=11883)
    mqtt_monitor_client2.run()

    test_dir = os.path.dirname(os.path.realpath(__file__))

    check_scenario_thread1 = Thread(target=check_scenario, args=(
        mqtt_monitor_client1, f'{scenario_name}1',
        f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}1.txt',
        f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}1.json', ), kwargs={'result_queue': result_queue})
    check_scenario_thread2 = Thread(target=check_scenario, args=(
        mqtt_monitor_client2, f'{scenario_name}2',
        f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}2.txt',
        f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}2.json', ), kwargs={'result_queue': result_queue})
    check_scenario_thread1.start()
    check_scenario_thread2.start()
    check_scenario_thread1.join()
    check_scenario_thread2.join()

    SOPTEST_LOG_DEBUG(f'==== {scenario_name} test pass! ====', 0)
    # while not result_queue.empty():
    #     run_result = result_queue.get()

    stop_thing_local(mqtt_monitor_client1, basic_test_thing_info1)

    wrapup_env(mqtt_monitor_client1)
    wrapup_env(mqtt_monitor_client2)


if __name__ == '__main__':
    # test_basic_feature()
    # test_tag_add_delete()
    test_scenario_function_execute()
    # test_scenario_loop()
    # test_scenario_variable_if_else()
    # test_scenario_wait_until()
    # test_scenario_all_prefix()
    # test_scenario_tag_scoping()
    # test_multi_scenario()
