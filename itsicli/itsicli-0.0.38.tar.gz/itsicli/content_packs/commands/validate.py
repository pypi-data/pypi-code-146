from itsicli.setup_logging import logger, set_content_pack_id
from itsicli.content_packs.commands.base import WorkspaceCommand
from itsicli.content_packs.files import ContentPackConfig
from itsicli.content_packs.validate.registry import VALIDATORS
from itsicli.content_packs.validate.result import Level, result
from pathlib import Path


class ValidateCommand(WorkspaceCommand):

    HELP = 'validates whether a content pack is in a proper state'

    NAME = 'validate'

    @classmethod
    def add_to_parser(cls, parser):
        subparser = parser.add_parser(cls.NAME, help=cls.HELP)
        return subparser

    def run(self, args):
        #Setting the content pack id in the global dictionary so that it is added in the logger
        content_pack_config = ContentPackConfig(Path.cwd())
        set_content_pack_id(content_pack_config.get_cp_id())
        
        num_passed = 0
        num_failed = 0

        for validator_class in VALIDATORS:
            validator = validator_class()

            in_progress_text = "\n{}...".format(validator.in_progress_text)
            logger.info(in_progress_text)

            try:
                results = validator.run(
                    home_path=self.home_path
                )
            except Exception as exc:
                logger.exception(exc)

                results = [
                    result(Level.ERROR, 'Yikes, an error occurred. See the above stack trace.')
                ]

            passed = self.print_results(results)
            if passed:
                num_passed += 1
            else:
                num_failed += 1

        logger.info('\nDone with {} passed, and {} failures.'.format(num_passed, num_failed))

    def print_results(self, results):
        passed = True

        for res in results:
            log = self.get_logger_func(res.level)
            log('\t[{}] {}'.format(res.level, res.message))

            if res.level == Level.ERROR:
                passed = False

        return passed

    def get_logger_func(self, level):
        if level == Level.WARNING:
            return logger.warning

        if level == Level.ERROR:
            return logger.error

        return logger.info
