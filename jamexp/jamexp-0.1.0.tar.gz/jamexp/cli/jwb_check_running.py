from datetime import datetime

import typer

from jamexp.wandb_clean import get_proj_runs


def check(
    proj: str,
    thres: float = typer.Argument(100, help="threshold for device dead runs~(min)"),
    is_all: bool = typer.Option(False, "--a", help="list all running"),
):
    """
    check running runs in wandb project, print how long it does not update, its create time, and last update time
    """
    rtn_run = []
    for run in get_proj_runs(proj):
        if run.state == "running":
            url = run.url
            run.create
            last_update_time = datetime.fromtimestamp(run.summaryMetrics["_timestamp"])
            create_time = datetime.strptime(run.createdAt, "%Y-%m-%dT%H:%M:%S")
            now_time = datetime.now()
            timegap_lastupdate_now = (now_time - last_update_time).seconds // 60
            if is_all or timegap_lastupdate_now > thres:
                print(
                    f"{run.name:<50}\n \t{timegap_lastupdate_now} min! Create! {create_time} Last! {last_update_time} {url}"
                )
                rtn_run.append(run)
    return rtn_run


def main():
    typer.run(check)


if __name__ == "__main__":
    main()
