from enough import settings
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

from enough.common.gitlab import GitLab


class Command(BaseCommand):
    help = 'Create an API user'

    def add_arguments(self, parser):
        parser.add_argument('--config', default=f'{settings.CONFIG_DIR}')
        parser.add_argument('domain')
        parser.add_argument('username')
        parser.add_argument('password')

    def setup_gitlab_auth(self, *args, **kwargs):
        provider = 'gitlab'
        name = 'GitLab'

        existing = SocialApp.objects.filter(provider=provider)
        if existing:
            return False

        gitlab = GitLab(f'https://lab.{kwargs["domain"]}')
        gitlab.login('root', kwargs['password'])
        gitlab.ensure_group_exists('enough', request_access_enabled=True, visibility='public')
        (client_id, client_secret) = gitlab.create_api_application(kwargs['domain'])

        a = SocialApp(provider=provider, name=name, secret=client_secret,
                      client_id=client_id, key='')
        a.save()

        # Now associate this provider with all site instances.
        sites = [i for i in Site.objects.all()]
        a.sites.add(*sites)

        return True

    def handle(self, *args, **kwargs):
        changed = False
        changed |= self.setup_gitlab_auth(*args, **kwargs)

        if changed:
            self.stdout.write('Changed')
        else:
            self.stdout.write('Up to date')
