"""Tests for the ChartsCollection and Chart classes"""
import shutil

import pytest

from sextant import cli

from . import fixtures


@pytest.fixture(name="collection")
def chartscollection() -> cli.ChartsCollection:
    """Get the test chartscollection."""
    chartsdir = str(fixtures / "charts")
    return cli.ChartsCollection(str(fixtures), chartsdir)


def test_collection(collection: cli.ChartsCollection):
    """Test that collection works."""
    # All charts should've been loaded
    assert len(list(collection.charts())) == 3
    assert isinstance(collection.chart("good"), cli.Chart)


def test_query(collection: cli.ChartsCollection):
    """Test that querying works."""
    assert collection.query("bar.beer:1.0.0")[0].chart_dir == collection.chart("good").chart_dir
    assert collection.query("some.other:1.1.1") == []
    # only exact matches
    assert collection.query("bar.beer:1.0") == []
    # bad charts cannot be loaded
    assert collection.query("baz.drunk-unicorn:1.0") == []


def test_lock(collection: cli.ChartsCollection):
    """Test that a lockfile is created"""
    good = collection.chart("good")
    good.create_lock(force=False)
    assert good.package.lockfile.exists()
    good.package.lockfile.unlink()


def test_vendor(collection: cli.ChartsCollection):
    """Test that we can create the vendor directory and fill it"""
    good = collection.chart("good")
    assert not good.vendor_dir.exists()
    try:
        good.vendor(force=False)
        assert good.vendor_dir.is_dir()
    finally:
        shutil.rmtree(str(good.vendor_dir))


# TODO: test force=True
