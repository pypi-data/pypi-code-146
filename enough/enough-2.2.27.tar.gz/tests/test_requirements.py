import filecmp
import os


def test_requirements(tmpdir):
    requirements = f'{tmpdir}/r.txt'
    requirements_dev = f'{tmpdir}/r-dev.txt'
    os.system('pipenv run pipenv_to_requirements -f '
              f'-o {requirements} -d {requirements_dev}')
    r = filecmp.cmp('requirements.txt', requirements, shallow=False)
    r_dev = filecmp.cmp('requirements-dev.txt', requirements_dev, shallow=False)
    assert r and r_dev, ('requirements.txt needs updating from Pipfile, run'
                         ' pipenv run pipenv_to_requirements -f')
