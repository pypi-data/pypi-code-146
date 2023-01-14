import os
import shutil
from filecmp import dircmp

from sonotoria.jinja import template_folder, template_file

TEST_DEST = 'tests/test_tmp'

def reset_dest_folder():
    if os.path.exists(TEST_DEST):
        shutil.rmtree(TEST_DEST)
    os.mkdir(TEST_DEST)

def use_test_dest(ftest):
    reset_dest_folder()
    ftest()
    reset_dest_folder()

def same_res(res_folder):
    comp = dircmp(TEST_DEST, res_folder)
    assert len(comp.left_only) == 0
    assert len(comp.right_only) == 0
    assert len(comp.diff_files) == 0

@use_test_dest
def test_templating_file():
    # Given
    src = 'tests/test_files/src/file'
    dest = f'{TEST_DEST}/test'

    # When
    template_file(src, dest, context={'foo': 'bar'})

    # Then
    with open(dest, encoding='utf-8') as fd:
        assert fd.read() == 'bar'

@use_test_dest
def test_templating_file_no_path_in_dest():
    # Given
    src = 'tests/test_files/src/file'
    dest = '__test'

    # When
    template_file(src, dest, context={'foo': 'bar'})

    # Then
    with open(dest, encoding='utf-8') as fd:
        assert fd.read() == 'bar'
    os.system('rm test')

@use_test_dest
def test_templating_default_values():
    # Given
    src = 'tests/test_files/src'

    # When
    template_folder(src, TEST_DEST)

    # Then
    same_res('tests/test_files/res_default')

@use_test_dest
def test_templating_overridden_names():
    # Given
    src = 'tests/test_files/src'

    # When
    template_folder(src, TEST_DEST, context={'male_names':['chaest', 'polkka'], 'female_names':[]})

    # Then
    same_res('tests/test_files/res_override')

@use_test_dest
def test_templating_no_config():
    # Given
    src = 'tests/test_files/no_config'

    # When
    template_folder(src, TEST_DEST, context={'value': 'test'})

    # Then
    same_res('tests/test_files/res_no_config')

@use_test_dest
def test_templating_two_dockerfiles():
    # Given
    src = 'tests/test_files/two_dockerfiles'

    # When
    template_folder(src, TEST_DEST, context={'value': 'test'})

    # Then
    same_res('tests/test_files/res_two_dockerfiles')
