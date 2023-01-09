from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
import click
from tinybird.client import TinyB
import yaml

from tinybird.feedback_manager import FeedbackManager


@dataclass
class TestCase:
    name: str
    sql: str
    max_time: Optional[float]
    max_bytes_read: Optional[float]

    def __init__(self, name, sql, max_time: float = None, max_bytes_read: int = None):
        self.name = name
        self.sql = sql
        self.max_time = max_time
        self.max_bytes_read = max_bytes_read

    def __iter__(self):
        yield (self.name, {'sql': self.sql, 'max_time': self.max_time, 'max_bytes_read': self.max_bytes_read})


def parse_file(file: str) -> Iterable[TestCase]:
    with Path(file).open('r') as f:
        definitions: List[Dict[str, Any]] = yaml.safe_load(f)

    for definition in definitions:
        try:
            for name, properties in definition.items():
                yield TestCase(
                    name,
                    properties.get('sql'),
                    properties.get('max_time'),
                    properties.get('max_bytes_read'))
        except Exception as e:
            click.echo(f"""Error: {FeedbackManager.error_exception(error=e)} reading file, check "{file}"->"{definition.get('name')}" """)


def generate_file(file: str, overwrite: bool = False) -> None:
    definitions = [
        dict(TestCase('this_test_should_pass', sql='SELECT * FROM numbers(5) WHERE 0')),
        dict(TestCase('this_test_should_fail', 'SELECT * FROM numbers(5) WHERE 1')),
        dict(TestCase('this_test_should_pass_over_time', 'SELECT * FROM numbers(5) WHERE 0', max_time=0.0000001)),
        dict(TestCase('this_test_should_pass_over_bytes', 'SELECT sum(number) AS total FROM numbers(5) HAVING total>1000', max_bytes_read=5)),
        dict(TestCase('this_test_should_pass_over_time_and_bytes', 'SELECT sum(number) AS total FROM numbers(5) HAVING total>1000', max_time=0.0000001, max_bytes_read=5)),
    ]

    p = Path(file)
    if((not p.exists()) or overwrite):
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('w') as f:
            yaml.safe_dump(definitions, f)
        click.echo(FeedbackManager.success_generated_local_file(file=p))
    else:
        click.echo(FeedbackManager.error_file_already_exists(file=p))

    return


async def run_test_file(tb_client: TinyB, file: str) -> Dict[str, Dict[str, Any]]:
    responses: Dict[str, Dict[str, Any]] = {}
    for test_case in parse_file(file):
        responses[test_case.name] = {}
        test_result: str = 'Check the SQL of this test'
        test_code_arr: List[str] = ['error']
        test_elapsed_time: float = 0
        test_max_time: float = -1.0
        if test_case.sql:
            q = f"SELECT * FROM ({test_case.sql}) LIMIT 20 FORMAT JSON"
            try:
                test_response = await tb_client.query(q)

                test_result = test_response['data']
                test_elapsed_time = test_response.get('statistics', {}).get('elapsed', 0) * 1000.0
                test_read_bytes = test_response.get('statistics', {}).get('bytes_read', 0)

                if(test_case.max_time):
                    test_max_time = test_case.max_time
                if(test_case.max_bytes_read):
                    test_max_bytes_read = test_case.max_bytes_read

                if(len(test_result) > 0):
                    test_code_arr = ['fail']
                else:
                    test_code_arr = ['pass']
                if(test_case.max_time and (test_elapsed_time > test_max_time)):
                    test_code_arr.extend(['over_time'])
                if(test_case.max_bytes_read and (test_read_bytes > test_max_bytes_read)):
                    test_code_arr.extend(['over_bytes'])
            except Exception as e:
                test_result = str(e)

        responses[test_case.name]['result'] = test_result
        responses[test_case.name]['test_time'] = test_elapsed_time
        responses[test_case.name]['test_read_bytes'] = test_read_bytes
        responses[test_case.name]['code_array'] = test_code_arr
        if(test_case.max_time):
            responses[test_case.name]['time_max'] = test_max_time

    return responses


def test_run_summary(test_file_results: Dict[str, Dict[str, Dict[str, str]]], only_fail: bool = False, verbose_level: int = 0):
    code_status_long = {
        'P': 'Pass',
        'P*OT': 'Pass Over Time',
        'P*OB': 'Pass Over Read Bytes',
        'P*OT*OB': 'Pass Over Time and Over Read Bytes',
        'F': 'Fail',
        'E': 'Error'}

    code_status_color = {
        'P': 'green',
        'P*OT': 'cyan',
        'P*OB': 'cyan',
        'P*OT*OB': 'cyan',
        'F': 'red',
        'E': 'bright_yellow'}

    def get_status(in_code_array):
        status = {'status_short': 'E'}

        if('pass' in in_code_array):
            status = 'P'
            if('over_time' in in_code_array):
                status = status + '*OT'
            if('over_bytes' in in_code_array):
                status = status + '*OB'
        elif('fail' in in_code_array):
            status = 'F'
        elif('error' in in_code_array):
            status = 'E'

        status = {
            'status_short': status,
            'status_long': code_status_long.get(status),
            'color': code_status_color.get(status)}

        return status

    total_counts: Dict[str, int] = {}
    for test_file, test_results in test_file_results.items():
        for test_name, result in test_results.items():
            test_status = get_status(result.get('code_array', ['error']))
            total_counts[test_status.get('status_short')] = total_counts.get(test_status.get('status_short'), 0) + 1

            if((not only_fail) or (test_status.get('status_short') not in ['P'])):
                test_color = test_status.get('color')
                test_summary = f"{test_status.get('status_short')}:{test_file} -> {test_name}: {result.get('test_time', 0):.5f} ms"

                if(verbose_level > 0):
                    test_summary = f"{test_summary}\nResult:\n\n{result.get('result', '[Check the sql field of this test]')}\n"

                click.secho(test_summary, fg=test_color, bold=True, nl=True)

    if(len(total_counts)):
        click.echo("\nTotals:")
        for key_status, value_total in total_counts.items():
            code_summary = f"Total {code_status_long.get(key_status, None)}: {value_total}"
            click.secho(code_summary, fg=code_status_color.get(key_status, None), bold=True, nl=True)


def get_bare_url(url: str) -> str:
    if url.startswith("http://"):
        return url[7:]
    elif url.startswith("https://"):
        return url[8:]
    else:
        return url
