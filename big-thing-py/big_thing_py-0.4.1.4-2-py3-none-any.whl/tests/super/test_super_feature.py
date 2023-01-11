from big_thing import *
from tests.tools.build_env import *
from tests.tools.check import *


'''
Feature for Super Service

Super Service Feature test

- [ ]  Super Service
    - [ ]  Super thing register
    - [ ]  Super thing detect on child middleware
    - [ ]  Super Service execute
        - [ ]  on parent middleware
        - [ ]  on child middleware
    - [ ]  Scenario
        - [ ]  on child middleware
            - [ ]  Verify
            - [ ]  Add
            - [ ]  Schedule
            - [ ]  Run
            - [ ]  Stop
            - [ ]  Update
            - [ ]  Re-Run
            - [ ]  Delete
    - [ ]  SuperThing1을 MWLv2에 Register — MWLv1에서 Thing 목록 확인
    - [ ]  MWLv1에서 SuperThing1.SuperService1 포함 시나리오 Scene1 생성 — 제대로 스케줄 되는지 확인
    - [ ]  MWLv1에서 Scene1 실행 — 제대로 결과가 오는지 확인
    - [ ]  MWLv1에서 Scene1 업데이트 — 제대로 스케줄 되는지 확인
    - [ ]  MWLv1에서 Scene1 다시 실행 — 제대로 결과가 오는지 확인
    - [ ]  **SuperThing1(같은 이름)**을 MWLv3에 Register — MWLv1에서 Thing 목록 확인
    - [ ]  MWLv2에서 **MWLv3의** SuperThing1.SuperService1 포함 시나리오 **Scene1(같은 이름)** 생성 — 제대로 스케줄 되는지 확인
    - [ ]  MWLv2에서 Scene1 실행 — 제대로 결과가 오는지 확인
    - [ ]  MWLv2에서 Scene1 업데이트 — 제대로 스케줄 되는지 확인
    - [ ]  MWLv2에서 Scene1 다시 실행 — 제대로 결과가 오는지 확인
    - [ ]  MWLv2에서 Scene1 삭제 — 제대로 삭제 결과가 오는지 확인
'''


def test_basic_super_feature():
    scenario_name = 'execute_level1_by_level2'

    mqtt_monitor_client3 = make_middleware(
        level=3, with_parent=False, clean_start=True)['mqtt_client']
    mqtt_monitor_client2 = make_middleware(
        level=2, with_parent=True, clean_start=True)['mqtt_client']
    mqtt_monitor_client1 = make_middleware(
        level=1, with_parent=True, clean_start=True)['mqtt_client']

    basic_test_super_thing_info1 = make_thing(
        mqtt_monitor_client2, level=2, index=1, thing_file_base_name='basic_super_thing', timeout=15)
    basic_test_thing_info1 = make_thing(
        mqtt_monitor_client1, level=1, index=1, thing_file_base_name='basic_big_thing', timeout=15)
    basic_test_thing_info2 = make_thing(
        mqtt_monitor_client1, level=1, index=2, thing_file_base_name='basic_big_thing', timeout=15)

    test_dir = os.path.dirname(os.path.realpath(__file__))
    check_pc_service_list(mqtt_monitor_client1)
    check_thing_exist(mqtt_monitor_client1,
                      basic_test_super_thing_info1['thing_name_with_mac'], is_super=True)
    check_scenario([mqtt_monitor_client1, mqtt_monitor_client2, mqtt_monitor_client3], scenario_name,
                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.txt',
                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.json')

    SOPTEST_LOG_DEBUG(
        f'Super Service Basic Test Pass!', 0)

    stop_thing_local(mqtt_monitor_client2, basic_test_super_thing_info1)
    stop_thing_local(mqtt_monitor_client1, basic_test_thing_info1)
    stop_thing_local(mqtt_monitor_client1, basic_test_thing_info2)

    wrapup_env(mqtt_monitor_client3)
    wrapup_env(mqtt_monitor_client2)
    return wrapup_env(mqtt_monitor_client1)


def test_multi_level_exeuction_feature():
    scenario_name = 'execute_level1_by_level3'

    mqtt_monitor_client3 = make_middleware(
        level=3, with_parent=False, clean_start=True)['mqtt_client']
    mqtt_monitor_client2 = make_middleware(
        level=2, with_parent=True, clean_start=True)['mqtt_client']
    mqtt_monitor_client1 = make_middleware(
        level=1, with_parent=True, clean_start=True)['mqtt_client']

    basic_test_super_thing_info1 = make_thing(
        mqtt_monitor_client3, level=3, index=1, thing_file_base_name='basic_super_thing', timeout=15)
    basic_test_thing_info1 = make_thing(
        mqtt_monitor_client1, level=1, index=1, thing_file_base_name='basic_big_thing', timeout=15)
    basic_test_thing_info2 = make_thing(
        mqtt_monitor_client1, level=1, index=2, thing_file_base_name='basic_big_thing', timeout=15)

    test_dir = os.path.dirname(os.path.realpath(__file__))
    check_pc_service_list(mqtt_monitor_client1)
    check_thing_exist(mqtt_monitor_client1,
                      basic_test_super_thing_info1['thing_name_with_mac'], is_super=True)
    check_scenario([mqtt_monitor_client1, mqtt_monitor_client2, mqtt_monitor_client3], scenario_name,
                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.txt',
                   f'{test_dir}/scenario_code/{scenario_name}/{scenario_name}.json')

    SOPTEST_LOG_DEBUG(
        f'Super Service multi level Test Pass!', 0)

    stop_thing_local(mqtt_monitor_client3, basic_test_super_thing_info1)
    stop_thing_local(mqtt_monitor_client1, basic_test_thing_info1)
    stop_thing_local(mqtt_monitor_client1, basic_test_thing_info2)

    wrapup_env(mqtt_monitor_client3)
    wrapup_env(mqtt_monitor_client2)
    return wrapup_env(mqtt_monitor_client1)


if __name__ == '__main__':
    test_basic_super_feature()
    test_multi_level_exeuction_feature()
