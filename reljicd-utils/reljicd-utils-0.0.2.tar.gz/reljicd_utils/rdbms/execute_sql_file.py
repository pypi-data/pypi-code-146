import fire
from sqlalchemy import text

from reljicd_utils.rdbms.scoped_session import engine


def execute_sql_file(file: str) -> None:
    with open(file) as f:
        engine.execute(text(f.read())).execution_options(autocommit=True)


if __name__ == '__main__':
    fire.Fire(execute_sql_file)
