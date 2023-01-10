from pokie.contrib.base.constants import SVC_VALIDATOR, SVC_SETTINGS, SVC_FIXTURE
from pokie.contrib.base.validators import init_validators
from pokie.core import BaseModule


class Module(BaseModule):
    name = "base"
    description = "Pokie base module"

    cmd = {
        # base commands
        "list": "pokie.contrib.base.cli.ListCmd",
        "help": "pokie.contrib.base.cli.HelpCmd",
        "version": "pokie.contrib.base.cli.VersionCmd",
        "runserver": "pokie.contrib.base.cli.RunServerCmd",
        # database-related commands
        "db:init": "pokie.contrib.base.cli.DbInitCmd",
        "db:check": "pokie.contrib.base.cli.DbCheckCmd",
        "db:update": "pokie.contrib.base.cli.DbUpdateCmd",
        # worker job commands
        "job:list": "pokie.contrib.base.cli.JobListCmd",
        "job:run": "pokie.contrib.base.cli.JobRunCmd",
        # code generation
        "codegen:dto": "pokie.contrib.base.cli.GenDtoCmd",
        "codegen:request": "pokie.contrib.base.cli.GenRequestRecordCmd",
        # fixtures
        "fixture:run": "pokie.contrib.base.cli.RunFixtureCmd",
        "fixture:check": "pokie.contrib.base.cli.CheckFixtureCmd",
    }

    services = {
        # db-related validators
        SVC_VALIDATOR: "pokie.contrib.base.service.ValidatorService",
        # settings service
        SVC_SETTINGS: "pokie.contrib.base.service.SettingsService",
        # fixture service
        SVC_FIXTURE: "pokie.contrib.base.service.FixtureService",
    }

    jobs = [
        "pokie.contrib.base.job.IdleJob",
    ]

    fixtures = []

    def build(self, parent=None):
        init_validators(self.get_di())
