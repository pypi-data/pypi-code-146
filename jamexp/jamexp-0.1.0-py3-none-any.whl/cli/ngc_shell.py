import json
import os
from collections import defaultdict
from datetime import datetime, timedelta, timezone

import typer
from loguru import logger
from plumbum.commands.processes import ProcessExecutionError
from pyfzf.pyfzf import FzfPrompt

from jamexp.utils.os_shell import run_simple_command


def get_job_info(team, key):
    team = 'lpr-imagine' if team else 'deep-imagination'

    stdout, stderr = run_simple_command(f'ngc batch list --format_type json --team {team}')
    jobs_info = defaultdict(list)
    latest_run, latest_td = None, timedelta(365)
    if stderr:
        print('ngc batch list error')
        print(stderr)
    else:
        list_job = json.loads(stdout)
        for job in list_job:
            status = job['jobStatus']['status']
            name = job['jobDefinition']['name']
            job_id = job['id']
            if key in name:
                if status in ['STARTING', 'RUNNING', 'QUEUED']:
                    if status == 'RUNNING':
                        s_t = datetime.strptime(job['jobStatus']['startedAt'], '%Y-%m-%dT%H:%M:%S.000Z')
                        cur_t = datetime.now(timezone.utc).replace(tzinfo=None)
                        td = (cur_t - s_t)
                        _info = f"{job_id:<15} {name:<35} {status:<10} {td.days}D {td.seconds//3600}H {(td.seconds//60)%60}M"
                        jobs_info[status].append(_info)
                        if td < latest_td:
                            latest_run = _info
                            latest_td = td
                    elif status == 'QUEUED':
                        s_t = datetime.strptime(job['jobStatus']['queuedAt'], '%Y-%m-%dT%H:%M:%S.000Z')
                        cur_t = datetime.now(timezone.utc).replace(tzinfo=None)
                        td = (cur_t - s_t)
                        jobs_info[status].append(f"{job_id:<15} {name:<35} {status:<10} {td.days}D {td.seconds//3600}H {(td.seconds//60)%60}M")
                    else:
                        jobs_info[status].append(f"{job_id:<15} {name:<35} {status:<10}")
    return jobs_info, latest_run

def _ngcbash(
    team : bool = typer.Option(True, "-t/-T", help="defualt use lpr-imagine, otherwise use deep-imagination"),
    latest : bool = typer.Option(True, "-l/-L", help="defualt exec latest job bash, otherwise use fzf"),
    key : str = typer.Argument('ml', help='filter key, only show jobs whose names contain the key'),
):
    jobs_info,latest_run = get_job_info(team, key)
    if latest:
        if latest_run:
            select_run = latest_run
        else:
            exit(0)
    else:
        try:
            fzf = FzfPrompt()
            select_run = fzf.prompt(jobs_info['RUNNING'])
        except ProcessExecutionError:
            exit(1)
        except Exception as error:  # pylint: disable=broad-except
            raise RuntimeError(  # pylint: disable=raise-missing-from
                "FZF error: {}".format(error)
            )

    logger.warning(f"bash exec {select_run}")
    job_id = select_run[:7]
    os.system(f'ngc batch exec {job_id}')

def _ngckill(
    team : bool = typer.Option(True, "-t/-T", help="defualt use lpr-imagine, otherwise use deep-imagination"),
    live : bool = typer.Option(False, "-l/-L", help="live run or dryrun, default dryrun"),
    kill_all : bool = typer.Option(False, "-a/-A", help="kill all jobs or not, default not"),
    key : str = typer.Argument('ml', help='filter key, only show jobs whose names contain the key')
):
    jobs_info = get_job_info(team, key)[0]

    _keys = []
    for k,v in jobs_info.items():
        _keys.extend([f'{k:<10}{_v}' for _v in v])

    if kill_all:
        for cur_line in _keys:
            _job_id = cur_line[10:10+7]
            run_simple_command(f"ngc batch kill {_job_id}")
            logger.warning(f"KILL   {cur_line}")
    elif live:
        try:
            fzf = FzfPrompt()
            select = fzf.prompt(_keys, "-m")
        except ProcessExecutionError:
            exit(1)
        except Exception as error:  # pylint: disable=broad-except
            raise RuntimeError(  # pylint: disable=raise-missing-from
                "FZF error: {}".format(error)
            )
        for cur_line in select:
            _job_id = cur_line[10:10+7]
            run_simple_command(f"ngc batch kill {_job_id}")
            logger.warning(f"KILL   {cur_line}")

    if not live:
        for k,v in jobs_info.items():
            print("#"*10 + f" {team}  {k}  Total {len(v):<10}" + "#"*10)
            for item in v:
                print(item)

def ngc_kill():
    typer.run(_ngckill)


def ngc_bash():
    typer.run(_ngcbash)
