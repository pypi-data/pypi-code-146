# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 18:47:53 2022

@author: Antonio
"""
#  Copyright (c) 2022.  Antonio Bulgheroni.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
#  Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
#  WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
#  OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#
import random
from pathlib import Path

import pytest

from autologbook.attachment import Attachment, AttachmentDict
from autologbook.containers import ResettableDict
from autologbook.autoerror import DuplicatedKey, ParentSampleError, SampleNameAlreadyExisting
from autologbook.autoprotocol import Protocol, Sample, SampleDict
from autologbook.autotools import PictureType
from autologbook.microscope_picture import FEIPicture, MicroscopePicture, QuattroFEIPicture, VersaFEIPicture
from autologbook.video import Video, VideoDict

not_existing_path = Path('i-dont-exists.odx')
existing_path = Path(__file__)


def test_microscope_picture_creation():
    # creation of a picture without path
    # risky but doable
    MicroscopePicture(path=None, pic_type=None)

    # creation of a picture with a not existing path
    # should throw an exception
    with pytest.raises(FileNotFoundError):
        MicroscopePicture(path='this_pic.tiff')


def test_get_picture_type():
    assert MicroscopePicture().get_pic_type() == PictureType.GENERIC_MICROSCOPE_PICTURE
    assert FEIPicture().get_pic_type() == PictureType.FEI_MICROSCOPE_PICTURE
    assert QuattroFEIPicture().get_pic_type() == PictureType.QUATTRO_MICROSCOPE_PICTURE
    assert VersaFEIPicture().get_pic_type() == PictureType.VERSA_MICROSCOPE_PICTURE


def test_sample():
    sample_full_name = 'Sample1/SubSample1.2/ThisSubSample'
    sample = Sample(sample_full_name)
    assert sample_full_name == sample.full_name
    last_name = 'ThisSubSample'
    assert last_name == sample.last_name
    parent_name = 'Sample1/SubSample1.2'  # full_name, remember!
    assert parent_name == sample.parent

    subsample_full_name = sample_full_name + '/1stSubSample'

    subsample = Sample(subsample_full_name)

    # add subsample using sample obj
    sample.add_subsample(subsample)
    assert subsample.parent == sample.full_name
    assert len(sample.subsamples) == 1
    # remove subsample using sample obj
    sample.remove_subsample(subsample)
    assert len(sample.subsamples) == 0

    # add subsample using just a string
    sample.add_subsample(subsample_full_name)
    assert len(sample.subsamples) == 1
    # remove subsample using just a string
    sample.remove_subsample(subsample_full_name)
    assert sample.is_empty()

    another_subsample_full_name = 'Sample2/SubSample1.2/ThisSubSample/2stSubSample'
    with pytest.raises(ParentSampleError):
        # add a subsample with a wrong hierarchy.
        # it will raise an exception
        sample.add_subsample(another_subsample_full_name)

    # the sample has no subsamples
    assert len(sample.subsamples) == 0

    mp = MicroscopePicture(path=None, pic_type=None)
    with pytest.raises(KeyError):
        # expected behavior because it cannot add a picture with
        # no path.
        sample.add_microscope_picture(mp)
    assert len(sample.images) == 0

    # add a video
    sample.add_video(Video(existing_path))
    assert not sample.is_empty()


def test_successful_attachment_creation():
    Attachment(existing_path)
    Attachment(str(existing_path))
    Attachment(None)


def test_failed_attachment_creation():
    exc_caught = 0

    test = [not_existing_path, str(not_existing_path), True, 3.14, Path.cwd()]
    for t in test:
        with pytest.raises((TypeError, FileNotFoundError, IsADirectoryError)):
            Attachment(t)


def test_successful_attachment_equality():
    assert (Attachment(existing_path)
            == Attachment(str(existing_path))) is True


def test_failed_attachment_equality():
    emptyfile = Path('existing-but-empty.txt')
    emptyfile.touch()

    try:
        assert (Attachment(existing_path) == Attachment(emptyfile)) is False
    except AssertionError:
        # it should not happen!
        raise AssertionError
    finally:
        emptyfile.unlink()


def test_attachment_is_empty_method():
    assert Attachment(existing_path).is_empty() is False
    empty_file = Path('existing-but-empty.txt')
    empty_file.touch()
    a = Attachment(empty_file)
    empty_file.unlink()
    with pytest.raises(FileNotFoundError):
        a.is_empty()

    empty_file.touch()
    a = Attachment(empty_file)
    try:
        assert a.is_empty() is True
    except AssertionError:
        # it should not happen!
        raise AssertionError
    finally:
        empty_file.unlink()


def test_successful_attachments_dict_operations():
    attach_dict = AttachmentDict()
    attach = Attachment(existing_path)
    attach_dict.add(attach)

    assert isinstance(attach_dict, ResettableDict) is True

    assert len(attach_dict) == 1
    assert attach == attach_dict.get(attach.key)

    del attach_dict[attach.key]
    assert len(attach_dict) == 0

    attach_dict.add(str(existing_path))
    with pytest.raises(DuplicatedKey):
        attach_dict.add(existing_path)

    assert len(attach_dict) == 1
    assert not attach_dict.is_empty()

    attach_dict.remove(existing_path)
    assert len(attach_dict) == 0
    assert attach_dict.is_empty()


def test_successful_sample_dict_operations():
    sample_dict = SampleDict()

    sample1 = 'sample/full/name'
    sample2 = 'another/sample/full/name'
    sample = Sample(sample1)
    sample_dict.add(sample)
    sample_dict.add(sample2)

    assert isinstance(sample_dict, ResettableDict) is True

    assert len(sample_dict) == 2

    del sample_dict[sample2]
    assert len(sample_dict) == 1

    with pytest.raises(SampleNameAlreadyExisting):
        sample_dict.add(sample1)
    assert len(sample_dict) == 1

    sample_dict.remove(sample)
    assert sample_dict.is_empty()


def test_protocol_operations():
    protocol = Protocol(path=Path.cwd(), protocol=123,
                        project='my_project', responsible='myself')

    samples = ['sample1', 'sample1/sample1.1', 'sample1/sample1.1/sample2.1']

    for sample in samples:
        protocol.add_sample(sample)

    problematic_samples = [
        'sample2/sample1.1', 'sample1/sample1.1/sample2.1', 'sample1/sample2.1/sample2.1']

    for sample in problematic_samples:
        with pytest.raises((ParentSampleError, SampleNameAlreadyExisting)):
            protocol.add_sample(sample)

    for sample in reversed(samples):
        # removing samples is mostly done in reversed order.
        protocol.remove_sample(sample)

    for sample in samples:
        protocol.add_sample(sample)

    for sample in samples:
        # but it works also in direct order
        protocol.remove_sample(sample)

    for sample in samples:
        protocol.add_sample(sample)

    shuffle = random.sample(samples, len(samples))
    for sample in shuffle:
        # but it works also in any order
        protocol.remove_sample(sample)

    assert protocol.samples.is_empty()
    assert protocol.is_empty()


def test_resettable_components():
    protocol = Protocol(path=Path.cwd(), protocol=123,
                        project='my_project', responsible='myself')

    samples = ['sample1', 'sample1/sample1.1', 'sample1/sample1.1/sample2.1']

    for sample in samples:
        protocol.add_sample(sample)

    assert len(protocol.samples) == len(samples)
    assert protocol.is_empty() is False

    protocol.clear_resettable_content()

    assert protocol.is_empty() is True


def test_video_creation():
    # creation of a video object pointing to a not existing file
    file = Path.cwd() / 'file.avi'
    video = Video(file)
    assert video.get('key') == str(file)
    assert video.get('path') == file
    assert video.get('ext') == file.suffix
    assert video.get('filename') == file.name
    assert video.get('size') is None


def test_successful_video_dict_operations():
    video_dict = VideoDict()
    video = Video(existing_path)
    video_dict.add(video)

    assert isinstance(video_dict, ResettableDict) is True
    assert len(video_dict) == 1
    assert video == video

    del video_dict[video.key]
    assert len(video_dict) == 0

    video_dict.add(str(existing_path))
    with pytest.raises(DuplicatedKey):
        video_dict.add(existing_path)

    assert len(video_dict) == 1
    assert not video_dict.is_empty()

    video_dict.remove(existing_path)
    assert len(video_dict) == 0
    assert video_dict.is_empty()
