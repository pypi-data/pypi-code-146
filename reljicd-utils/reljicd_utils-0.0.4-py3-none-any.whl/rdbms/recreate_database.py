import fire
from sqlalchemy.exc import ProgrammingError
from sqlalchemy_utils import create_database, drop_database

from reljicd_utils.rdbms.scoped_session import engine


def recreate_database(name: str = None, template: str = None) -> None:
    engine.dispose()

    url = str(engine.url)
    database = engine.url.database
    if name:
        url = url.replace(database, name)

    try:
        drop_database(url)
    except ProgrammingError:
        pass

    create_database(url=url, template=template)

    engine.dispose()


if __name__ == '__main__':
    fire.Fire(recreate_database)
