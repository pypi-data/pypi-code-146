from sun.utils import slack_ver


def test_slackware_version():
    version = '15.0'
    distribution = 'Slackware'
    assert distribution == slack_ver()[0]
    assert version == slack_ver()[1]
