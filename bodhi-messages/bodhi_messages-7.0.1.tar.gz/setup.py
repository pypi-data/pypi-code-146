# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bodhi', 'bodhi.messages', 'bodhi.messages.schemas', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['fedora-messaging>=3.0.0']

entry_points = \
{'fedora.messages': ['bodhi.buildroot_override.tag.v1 = '
                     'bodhi.messages.schemas.buildroot_override:BuildrootOverrideTagV1',
                     'bodhi.buildroot_override.untag.v1 = '
                     'bodhi.messages.schemas.buildroot_override:BuildrootOverrideUntagV1',
                     'bodhi.compose.complete.v1 = '
                     'bodhi.messages.schemas.compose:ComposeCompleteV1',
                     'bodhi.compose.composing.v1 = '
                     'bodhi.messages.schemas.compose:ComposeComposingV1',
                     'bodhi.compose.start.v1 = '
                     'bodhi.messages.schemas.compose:ComposeStartV1',
                     'bodhi.compose.sync.done.v1 = '
                     'bodhi.messages.schemas.compose:ComposeSyncDoneV1',
                     'bodhi.compose.sync.wait.v1 = '
                     'bodhi.messages.schemas.compose:ComposeSyncWaitV1',
                     'bodhi.errata.publish.v1 = '
                     'bodhi.messages.schemas.errata:ErrataPublishV1',
                     'bodhi.repo.done.v1 = '
                     'bodhi.messages.schemas.compose:RepoDoneV1',
                     'bodhi.update.comment.v1 = '
                     'bodhi.messages.schemas.update:UpdateCommentV1',
                     'bodhi.update.complete.stable.v1 = '
                     'bodhi.messages.schemas.update:UpdateCompleteStableV1',
                     'bodhi.update.complete.testing.v1 = '
                     'bodhi.messages.schemas.update:UpdateCompleteTestingV1',
                     'bodhi.update.edit.v1 = '
                     'bodhi.messages.schemas.update:UpdateEditV1',
                     'bodhi.update.eject.v1 = '
                     'bodhi.messages.schemas.update:UpdateEjectV1',
                     'bodhi.update.karma.threshold.v1 = '
                     'bodhi.messages.schemas.update:UpdateKarmaThresholdV1',
                     'bodhi.update.request.obsolete.v1 = '
                     'bodhi.messages.schemas.update:UpdateRequestObsoleteV1',
                     'bodhi.update.request.revoke.v1 = '
                     'bodhi.messages.schemas.update:UpdateRequestRevokeV1',
                     'bodhi.update.request.stable.v1 = '
                     'bodhi.messages.schemas.update:UpdateRequestStableV1',
                     'bodhi.update.request.testing.v1 = '
                     'bodhi.messages.schemas.update:UpdateRequestTestingV1',
                     'bodhi.update.request.unpush.v1 = '
                     'bodhi.messages.schemas.update:UpdateRequestUnpushV1',
                     'bodhi.update.requirements_met.stable.v1 = '
                     'bodhi.messages.schemas.update:UpdateRequirementsMetStableV1',
                     'bodhi.update.status.testing.v1 = '
                     'bodhi.messages.schemas.update:UpdateReadyForTestingV1',
                     'bodhi.update.status.testing.v2 = '
                     'bodhi.messages.schemas.update:UpdateReadyForTestingV2']}

setup_kwargs = {
    'name': 'bodhi-messages',
    'version': '7.0.1',
    'description': 'JSON schema for messages sent by Bodhi',
    'long_description': 'Bodhi Messages\n==============\n\nThis package contains the schema for messages published by Bodhi.\n',
    'author': 'Fedora Infrastructure Team',
    'author_email': 'None',
    'maintainer': 'Fedora Infrastructure Team',
    'maintainer_email': 'infrastructure@lists.fedoraproject.org',
    'url': 'https://bodhi.fedoraproject.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
