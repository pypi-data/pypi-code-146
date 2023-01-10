# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gqlauth',
 'gqlauth.captcha',
 'gqlauth.core',
 'gqlauth.jwt',
 'gqlauth.migrations',
 'gqlauth.user']

package_data = \
{'': ['*'],
 'gqlauth': ['templates/email/*', 'templates/email/images/*'],
 'gqlauth.captcha': ['fonts/*']}

install_requires = \
['Django>=3.2,<4.2',
 'Pillow>=9.2.0,<10.0.0',
 'PyJWT>=2.6.0,<3.0',
 'strawberry-django-plus>=1.25.2,<2.0.0',
 'strawberry-graphql-django>=0.2.5,<4.0',
 'strawberry-graphql>=0.128,<0.171.0']

setup_kwargs = {
    'name': 'strawberry-django-auth',
    'version': '0.374.0',
    'description': 'Graphql authentication system with Strawberry for Django.',
    'long_description': "[![Tests](https://img.shields.io/github/actions/workflow/status/nrbnlulu/strawberry-django-auth/tests.yml?label=Tests&style=for-the-badge)](https://github.com/nrbnlulu/strawberry-django-auth/actions/workflows/tests.yml)\n[![Codecov](https://img.shields.io/codecov/c/github/nrbnlulu/strawberry-django-auth?style=for-the-badge)](https://app.codecov.io/gh/nrbnlulu/strawberry-django-auth)\n[![Pypi](https://img.shields.io/pypi/v/strawberry-django-auth.svg?style=for-the-badge&logo=appveyor)](https://pypi.org/project/strawberry-django-auth/)\n[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=for-the-badge&logo=appveyor)](https://github.com/nrbnlulu/strawberry-django-auth/blob/master/CONTRIBUTING.md)\n[![Pypi downloads](https://img.shields.io/pypi/dm/strawberry-django-auth?style=for-the-badge)](https://pypistats.org/packages/strawberry-django-auth)\n[![Python versions](https://img.shields.io/pypi/pyversions/strawberry-django-auth?style=social)](https://pypi.org/project/strawberry-django-auth/)\n\n# Strawberry-django Auth\n[Django](https://github.com/django/django) registration and authentication with [Strawberry](https://strawberry.rocks/).\n\n## Demo\n\n![Demo Video](https://github.com/nrbnlulu/strawberry-django-auth/blob/main/demo.gif)\n\n## About\n#### This Library was inspired by [Django-graphql-auth](https://github.com/pedrobern/django-graphql-auth/).\n\nAbstract all the basic logic of handling user accounts out of your app,\nso you don't need to think about it and can **get you up and running faster**.\n\nNo lock-in. When you are ready to implement your own code or this package\nis not up to your expectations , it's *easy to extend or switch to\nyour implementation*.\n\n\n### Docs can be found [here](https://nrbnlulu.github.io/strawberry-django-auth/)\n\n## Features\n\n* [x] Awesome docs!\n* [x] Captcha validation\n* [x] Async/Sync supported!\n* [x] Works with default or custom user model\n* [x] Builtin JWT authentication using [PyJWT](https://github.com/jpadilla/pyjwt)\n* [x] User registration with email verification\n* [x] Retrieve/Update user\n* [x] Archive user\n* [x] Permanently delete user or make it inactive\n* [x] Turn archived user active again on login\n* [x] Track user status <small>(archived, verified)</small>\n* [x] Password change\n* [x] Password reset through email\n* [x] Revoke user tokens on account archive/delete/password change/reset\n* [x] All mutations return `success` and `errors`\n* [x] Default email templates <small>(you will customize though)</small>\n* [x] Customizable, no lock-in\n* [x] Passwordless registration\n\n\n### Full schema features\n\n```python\n\n@strawberry.type\nclass AuthMutation:\n    # include here your mutations that interact with a user object from a token.\n\n    verify_token = mutations.VerifyToken.field\n    update_account = mutations.UpdateAccount.field\n    archive_account = mutations.ArchiveAccount.field\n    delete_account = mutations.DeleteAccount.field\n    password_change = mutations.PasswordChange.field\n    swap_emails = mutations.SwapEmails.field\n\n@strawberry.type\nclass Mutation:\n    @field(directives=[TokenRequired()])\n    def auth_entry(self) -> Union[AuthMutation, GQLAuthError]:\n        return AuthOutput(node=AuthMutation())\n\n    # these are mutation that does not require authentication.\n    captcha = Captcha.field\n    token_auth = mutations.ObtainJSONWebToken.field\n    register = mutations.Register.field\n    verify_account = mutations.VerifyAccount.field\n    resend_activation_email = mutations.ResendActivationEmail.field\n    send_password_reset_email = mutations.SendPasswordResetEmail.field\n    password_reset = mutations.PasswordReset.field\n    password_set = mutations.PasswordSet.field\n    refresh_token = mutations.RefreshToken.field\n    revoke_token = mutations.RevokeToken.field\n    verify_secondary_email = mutations.VerifySecondaryEmail.field\n\n\nschema = strawberry.Schema(query=Query, mutation=Mutation)\n\n```\n\n## Contributing\n\nSee [CONTRIBUTING.md](https://github.com/nrbnlulu/strawberry-django-auth/blob/main/CONTRIBUTING.md)\n",
    'author': 'Nir.J Benlulu',
    'author_email': 'nrbnlulu@gmail.com',
    'maintainer': 'Nir.J Benlulu',
    'maintainer_email': 'nrbnlulu@gmail.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
