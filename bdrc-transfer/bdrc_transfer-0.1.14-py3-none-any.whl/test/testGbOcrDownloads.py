from log_ocr.GbOcrTrack import GbOcrContext
from log_ocr.models.drs import *

import pytest

# See https://www.jetbrains.com/help/pycharm/pytest.html#pytest-bdd
# for running under pycharm

_work = 'UnitTestWork1'
_vol = 'UnitTestW1Volume1'
_vol2 = 'UnitTestW1Volume2'


def test_removal():
    global _work, _vol
    with GbOcrContext() as gbo:
        gbo.remove_volumes([_vol, _vol2])
        gbo.remove_works([_work])


@pytest.fixture
def cleanup():
    global _work, _vol
    with GbOcrDownload() as gbo:
        gbo.remove_volumes([_vol])
        gbo.remove_works([_work])


def test_volume_add_existing_or_new_work():
    global _work, _vol
    with GbOcrContext() as gbo:
        try:
            v: Volumes = gbo.get_or_create_volume(_work, _vol)
            assert v.work.WorkName == _work
            assert v.label == _vol
            gbo.session.commit()
        finally:
            pass
        # del gbo.session


def test_add_new_volume_existing_work():
    global _work, _vol
    test_volume_add_existing_or_new_work()
    with GbOcrContext() as gbo:
        v: Volumes = gbo.get_or_create_volume(_work, _vol2)
        assert len(v.work.volumes) == 2
        w_vols: [str] = [x.label for x in v.work.volumes]
        for vv in w_vols:
            assert vv.startswith('UnitTestW1Volume')


class testDownloadModel:

    def __init__(self):
        self._work = 'UnitTestWork1'
        self._vol = 'UnitTestW1Volume1'

    @pytest.fixture
    def cleanup(self):
        with GbOcrContext() as gbo:
            gbo.remove_volumes([self._vol])
            gbo.remove_works([self._work])

    def test_get(self):
        with GbOcrContext() as gbo:
            expected_name = 'W1FPL2251'
            works: Works = gbo.get_work_by_name(expected_name)

            assert expected_name == works.WorkName
            assert len(works.volumes) == 1

    def x_test_add(self):
        gbo = GbOcrDownload()
        w = gbo.get_or_create_work('Blurgew')
        print(w)

    def test_volume_add_existing_work(self):
        with GbOcrDownload() as gbo:
            try:
                v: Volumes = gbo.get_or_create_volume(self._work, self._vol)
                assert v.work.WorkName == self._work
                assert v.label == self._vol
                gbo.session.commit()
            finally:
                pass
            # del gbo.session

    def test_add_new_volume_existing_work(self):
        self.test_volume_add_existing_work()
        with GbOcrDownload() as gbo:
            v: Volumes = gbo.get_or_create_volume(self._work, self._vol)
            assert len(v.work.volumes) == 2
            w_vols: [str] = [x.label for x in v.work.volumes]
            for vv in w_vols:
                assert vv.beginswith('UnitTestW1Volume')

            # del gbo.session
