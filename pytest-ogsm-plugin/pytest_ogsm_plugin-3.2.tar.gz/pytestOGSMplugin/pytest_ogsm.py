#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/10 3:29 PM
# @Author  : cw
import datetime
import json
import os
import time

import pytest
from jinja2 import Environment, FileSystemLoader


def pytest_report_teststatus(report, config):
    """控制台展示测试结果时，√代替.，x代替F"""
    if report.when == 'call' and report.failed:
        return report.outcome, 'X', 'failed'
    if report.when == 'call' and report.passed:
        return report.outcome, 'Y', 'passed'


test_result = {
    "title": "",
    "tester": "",
    "desc": "",
    "cases": {},
    'rerun': 0,
    "failed": 0,
    "passed": 0,
    "skipped": 0,
    "error": 0,
    "start_time": 0,
    "run_time": 0,
    "begin_time": "",
    "all": 0,
    "testModules": set()
}


def pytest_make_parametrize_id(config, val, argname):
    if isinstance(val, dict):
        return val.get('title') or val.get('desc')


def pytest_collection_modifyitems(session, items, config):
    """
    测试用例收集完成时，将收集到的用例二次过滤
    :return:
    """
    cmd_project = config.getoption('--project')
    cmd_product = config.getoption('--product')
    cmd_mark = config.getoption('-m')

    selected_items = []
    deselected_items = []
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
        def_prefix = item._nodeid
        print(def_prefix, '我在这里')
        print(type(def_prefix))
        print(type(cmd_project))
        if cmd_project == 'all' and cmd_product == 'all':
            if cmd_mark == 'initial':
                if 'initdata' in def_prefix:
                    # if any(name in def_prefix for name in ['initdata',cmd_project[0],cmd_product[0]]):
                    selected_items.append(item)
            elif cmd_mark == 'base':
                if 'initdata' not in def_prefix:
                    # if any(name in def_prefix for name in ['initdata',cmd_project[0],cmd_product[0]]):
                    selected_items.append(item)
            elif cmd_mark == 'cleanup':
                if cmd_mark in def_prefix:
                    selected_items.append(item)
        elif cmd_project == 'all' and cmd_product != 'all':
            if cmd_mark == 'initial':
                if 'initdata' in def_prefix and cmd_product in def_prefix:
                    selected_items.append(item)
            elif cmd_mark in ['base', 'all']:
                if 'initdata' not in def_prefix and cmd_product in def_prefix:
                    # if any(name in def_prefix for name in ['initdata',cmd_project[0],cmd_product[0]]):
                    selected_items.append(item)
            elif cmd_mark == 'cleanup':
                if cmd_product in def_prefix and cmd_mark in def_prefix:
                    selected_items.append(item)
        elif cmd_project != 'all' and cmd_product == 'all':
            if cmd_mark == 'initial':
                if 'initdata' in def_prefix and cmd_project in def_prefix:
                    selected_items.append(item)
            elif cmd_mark in ['base', 'all']:
                if 'initdata' not in def_prefix and cmd_project in def_prefix:
                    # if any(name in def_prefix for name in ['initdata',cmd_project[0],cmd_product[0]]):
                    selected_items.append(item)
            elif cmd_mark == 'cleanup':
                if cmd_project in def_prefix and cmd_mark in def_prefix:
                    selected_items.append(item)
        else:
            print('[][][][][][][][]') # TODO 此处有bug，执行不正确
            '''
            pytest --project=openapi --product=inpaas -m='cleanup' -s
            应该只执行openapi 但是执行了gic2api
            failed initdata/test_p.py::test_cleanup[inpaas-openapi] - assert 1 == 2
            failed initdata/test_p.py::test_cleanup[inpaas-gic2api] - assert 1 == 2

            '''
            if cmd_project in def_prefix and cmd_product in def_prefix:
                selected_items.append(item)
        config.hook.pytest_deselected(items=deselected_items)
    items[:] = selected_items
    print(items, '运行的')


def pytest_runtest_logreport(report):
    report.duration = '{:.6f}'.format(report.duration)
    test_result['testModules'].add(report.fileName)
    if report.when == 'call':
        test_result[report.outcome] += 1
        test_result["cases"][report.nodeid] = report
    elif report.outcome == 'failed':
        report.outcome = 'error'
        test_result['error'] += 1
        test_result["cases"][report.nodeid] = report
    elif report.outcome == 'skipped':
        test_result[report.outcome] += 1
        test_result["cases"][report.nodeid] = report


def pytest_sessionstart(session):
    start_ts = datetime.datetime.now()
    test_result["start_time"] = start_ts.timestamp()
    test_result["begin_time"] = start_ts.strftime("%Y-%m-%d %H:%M:%S")


def handle_history_data(report_dir, test_result):
    """
    处理历史数据
    :return:
    """
    try:
        with open(os.path.join(report_dir, 'history.json'), 'r', encoding='utf-8') as f:
            history = json.load(f)
    except:
        history = []
    history.append({'success': test_result['passed'],
                    'all': test_result['all'],
                    'fail': test_result['failed'],
                    'skip': test_result['skipped'],
                    'error': test_result['error'],
                    'runtime': test_result['run_time'],
                    'begin_time': test_result['begin_time'],
                    'pass_rate': test_result['pass_rate'],
                    })

    with open(os.path.join(report_dir, 'history.json'), 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=True)
    return history


def pytest_sessionfinish(session):
    """在整个测试运行完成之后调用的钩子函数,可以在此处生成测试报告"""
    report2 = session.config.getoption('--report')

    if report2:
        test_result['title'] = session.config.getoption('--title') or '测试报告'
        test_result['tester'] = session.config.getoption('--tester') or 'QA'
        test_result['desc'] = session.config.getoption('--desc') or '无'
        # templates_name = session.config.getoption('--template') or '1'
        name = report2
    else:
        return

    if not name.endswith('.html'):
        file_name = time.strftime("%Y-%m-%d_%H_%M_%S") + name + '.html'
    else:
        file_name = time.strftime("%Y-%m-%d_%H_%M_%S") + name

    if os.path.isdir('reports'):
        pass
    else:
        os.mkdir('reports')
    file_name = os.path.join('reports', file_name)
    test_result["run_time"] = '{:.6f} S'.format(time.time() - test_result["start_time"])
    test_result['all'] = len(test_result['cases'])
    if test_result['all'] != 0:
        test_result['pass_rate'] = '{:.2f}'.format(test_result['passed'] / test_result['all'] * 100)
    else:
        test_result['pass_rate'] = 0
    # 保存历史数据
    test_result['history'] = handle_history_data('reports', test_result)
    # 渲染报告
    template_path = os.path.join(os.path.dirname(__file__), './templates')
    env = Environment(loader=FileSystemLoader(template_path))

    # if templates_name == '1':
    #     template = env.get_template('templates.html')
    # else:
    #     template = env.get_template('templates.html')
    template = env.get_template('templates.html')
    report = template.render(test_result)
    with open(file_name, 'wb') as f:
        f.write(report.encode('utf8'))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    fixture_extras = getattr(item.config, "extras", [])
    plugin_extras = getattr(report, "extra", [])
    report.extra = fixture_extras + plugin_extras
    report.fileName = item.location[0]
    report.desc = item._obj.__doc__
    report.method = item.location[2].split('[')[0]


def pytest_addoption(parser):
    group = parser.getgroup("testreport")
    project_choices_value = ['all', 'openapi', 'gic2api']
    product_choices_value = ['all', 'inpaas', 'mongodb', 'ccs', 'bms', 'network', 'ecs_vm', 'nas', 'ecs_server', ]
    group.addoption(
        "--report",
        action="store",
        metavar="path",
        default=None,
        help="在指定路径创建html报告文件",
    )
    group.addoption(
        "--title",
        action="store",
        metavar="path",
        default=None,
        help="报告标题",
    )
    group.addoption(
        "--tester",
        action="store",
        metavar="path",
        default=None,
        help="报告人员/团队",
    )
    group.addoption(
        "--desc",
        action="store",
        metavar="path",
        default=None,
        help="报告描述",
    )
    parser.addoption(
        "--project",
        action='store',
        default=None,
        required=True,
        choices=project_choices_value,
        help='项目名'
    )
    parser.addoption(
        "--product",
        action='store',
        default=None,
        required=True,
        choices=product_choices_value,
        help='产品线名称'
    )
