"""Database test fixtures"""
import copy
import functools
import os
import uuid

import pytest

from flywheel_cli.ingest import models
from flywheel_cli.ingest.client.db import DBClient


def pytest_generate_tests(metafunc) -> None:
    """Parametrize tests with any additional DB urls from envvar INGEST_DB"""
    if "db" in metafunc.fixturenames:
        db_urls = os.getenv("INGEST_DB", "sqlite:///:memory:").split()
        metafunc.parametrize("db", db_urls, indirect=True)


def pytest_itemcollected(item):
    """Mark db tests"""
    if "db" in item.fixturenames:
        item.add_marker("db")


@pytest.fixture(scope="function")
def db(request):  # pylint: disable=invalid-name
    """DB init, yield and teardown - for each db_url, per test"""
    test_db = TestDB(request.param)
    meta = models.Base.metadata  # pylint: disable=no-member
    meta.create_all(test_db.client.engine)
    yield test_db
    test_db.close()
    meta.drop_all(test_db.client.engine)
    test_db.client.engine.dispose()


class TestDB:
    """Ingest test database helper for easy record creation and session access"""

    def __init__(self, db_url: str):
        self.url = db_url
        self.client = DBClient(db_url)
        self.session = self.client.sessionmaker()
        self.last_id = {}

    def __getattr__(self, name: str):
        """
        Return create() method partial for given model name (eg. create_ingest).
        Pass through any other attribute access to the underlying sqla Session.
        """
        if name.startswith("create_"):
            model_name = name.replace("create_", "")
            if model_name not in self.models:
                raise AttributeError(name)
            return functools.partial(self.create, model_name)
        return getattr(self.session, name)

    def create(self, model_name, defaults=True, **kwargs):
        """
        Create a test DB record for given model name and columns from kwargs.
        If defaults is True, then kwargs are deep merged onto self.defaults.
        Models with an ingest_id FK will reference the last inserted ingest.
        Items will also automatically reference the last inserted container.
        Inserting an ingest will automatically bind the db.client to it.
        """
        model_cls = self.models[model_name]
        add_stats = False
        if defaults:
            kwargs.setdefault("id", uuid.uuid4())
            kwargs = merge_dicts(kwargs, copy.deepcopy(self.defaults[model_name]))
            if model_name != "ingest" and "ingest_id" not in kwargs:
                kwargs["ingest_id"] = self._last_id("ingest")
            if model_name == "item" and "container_id" not in kwargs:
                kwargs["container_id"] = self._last_id("container")
        if "id" in kwargs:
            self.last_id[model_name] = kwargs["id"]
            if model_name == "ingest":
                self.client.bind(kwargs["id"])
                add_stats = True
        model = model_cls(**kwargs)
        # pylint: disable=no-member
        self.session.add(model)
        self.session.commit()

        if add_stats:
            self.client.create_ingest_stats()

        return model

    def _last_id(self, model_name):
        if model_name not in self.last_id:
            model = self.create(model_name)
            self.last_id[model_name] = model.id
        return self.last_id[model_name]

    # map of snake-case model names to sqla model classes
    models = {
        "container": models.Container,
        "deid_log": models.DeidLog,
        "error": models.Error,
        "ingest": models.Ingest,
        "item": models.Item,
        "review": models.Review,
        "subject": models.Subject,
        "task": models.Task,
        "uid": models.UID,
        "fw_container_metadata": models.FWContainerMetadata,
    }

    # map of model names to test record creation defaults
    defaults = dict(
        ingest=dict(
            api_key="flywheel.test:admin-apikey",
            fw_host="flywheel.test",
            fw_user="admin@flywheel.test",
            config=dict(src_fs="/tmp"),
            strategy_config={},
            status="created",
        ),
        task=dict(
            type="scan",
            status="pending",
        ),
        container=dict(level=0, path="src", src_context={"label": "src"}),
        item=dict(
            type="file",
            dir="/dir",
            files=["file"],
            files_cnt=1,
            bytes_sum=1,
            filename="file",
            existing=False,
            context={"group": {"_id": "grp"}, "project": {"label": "prj"}},
        ),
        error={},
        review=dict(path="path"),
        subject={},
        uid={},
        deid_log=dict(
            src_path="path",
            tags_before={},
            tags_after={},
        ),
        fw_container_metadata=dict(path="path", content=dict(test_attr="test_value")),
    )


def merge_dicts(src, dst):
    """Deep merge two dicts src and dst into dst"""
    for key, value in src.items():
        if isinstance(value, dict):
            merge_dicts(value, dst.setdefault(key, {}))
        else:
            dst[key] = value
    return dst
