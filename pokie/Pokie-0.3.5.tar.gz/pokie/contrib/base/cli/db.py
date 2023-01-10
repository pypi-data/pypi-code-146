import inspect
import os
from argparse import ArgumentParser
from pathlib import Path
from typing import Optional, List

from rick_db.conn import Connection

from pokie.constants import DI_DB, DI_APP
from pokie.core import CliCommand
from rick_db.util import MigrationRecord


class DbCliCommand(CliCommand):
    # migrations folder
    folder = Path("sql")

    # common error messages
    error_nodb = "error: no database connection found in the application"
    error_noinit = "error: migration manager not installed; run 'db:init' command first"

    def get_db(self) -> Optional[Connection]:
        di = self.get_di()
        if not di.has(DI_DB):
            return None
        return di.get(DI_DB)

    def load_migrations(self, module_name: str, path: Path) -> List[tuple]:
        """
        Scan path for sql files and loads contents into a list
        :param module_name: module name to use
        :param path: path to scan
        :return: list of (MigrationRecord, content)
        """
        mig_dict = {}
        for entry in sorted(path.glob("*.sql")):
            if entry.is_file():
                with open(entry, encoding="utf-8") as f:
                    mig_dict[entry.name] = f.read()

        result = []
        for name, contents in mig_dict.items():
            record = MigrationRecord(name="{}/{}".format(module_name, name))
            result.append((record, contents))
        return result


class DbInitCmd(DbCliCommand):
    description = "initialize database migrations"

    def run(self, args) -> bool:
        db = self.get_db()
        if not db:
            self.tty.error(self.error_nodb)
            return False

        mgr = db.migration_manager()
        if not mgr.has_manager():
            self.tty.write("installing migration manager...", False)
            result = mgr.install_manager()
            if result.success:
                self.tty.write(self.tty.colorizer.green("success"))
                return True
            else:
                self.tty.write(self.tty.colorizer.green("error: " + result.error))
                return False

        self.tty.write("migration manager already installed")
        return True


class DbCheckCmd(DbCliCommand):
    description = "show existing database migrations status"

    def run(self, args) -> bool:
        db = self.get_db()
        if not db:
            self.tty.error(self.error_nodb)
            return False

        mgr = db.migration_manager()
        if not mgr.has_manager():
            self.tty.error(self.error_noinit)
            return False

        for name, module in self.get_di().get(DI_APP).modules.items():
            self.tty.write("Checking migrations for module {}:".format(name))
            path = (
                Path(os.path.dirname(inspect.getfile(module.__class__))) / self.folder
            )
            if path.exists() and path.is_dir():
                try:
                    for record in self.load_migrations(name, path):
                        mig, content = record
                        self.tty.write("\t{name}... ".format(name=mig.name), False)

                        # check if migration is duplicated
                        record = mgr.fetch_by_name(mig.name)
                        if record is not None:
                            self.tty.write(
                                self.tty.colorizer.white("already applied", attr="bold")
                            )

                        # check if migration is obviously empty
                        elif content.strip() == "":
                            self.tty.write(
                                self.tty.colorizer.yellow(
                                    "empty migration", attr="bold"
                                )
                            )
                        else:
                            self.tty.write(
                                self.tty.colorizer.green("new migration", attr="bold")
                            )

                except Exception as e:
                    self.tty.error("Error : " + str(e))
                    return False
        return True


class DbUpdateCmd(DbCliCommand):
    description = "apply pending migrations"

    def arguments(self, parser: ArgumentParser):
        parser.add_argument(
            "--dry",
            help="Dry run - no database changes are performed",
            action="store_true",
            default=False,
        )

    def run(self, args) -> bool:
        db = self.get_db()
        if not db:
            self.tty.error(self.error_nodb)
            return False

        mgr = db.migration_manager()
        if not mgr.has_manager():
            self.tty.error(self.error_noinit)
            return False

        for module_name, module in self.get_di().get(DI_APP).modules.items():
            self.tty.write("Checking migrations for module {}:".format(module_name))
            path = (
                Path(os.path.dirname(inspect.getfile(module.__class__))) / self.folder
            )
            if path.exists() and path.is_dir():
                try:
                    for record in self.load_migrations(module_name, path):
                        mig, content = record
                        self.tty.write("\t{name}... ".format(name=mig.name), False)

                        # check if migration is duplicated
                        record = mgr.fetch_by_name(mig.name)
                        if record is not None:
                            self.tty.write(
                                self.tty.colorizer.white("already applied", attr="bold")
                            )

                        # check if migration is obviously empty
                        elif content.strip() == "":
                            self.tty.write(
                                self.tty.colorizer.yellow(
                                    "empty migration", attr="bold"
                                )
                            )
                        else:
                            # apply migration
                            if not args.dry:
                                # try to execute migration and register on the migration manager
                                result = mgr.execute(mig, content)
                                if result.success:
                                    self.tty.write(
                                        self.tty.colorizer.green("success", attr="bold")
                                    )
                                else:
                                    # in case of error, abort
                                    self.tty.write("\n")
                                    self.tty.error("Error: " + result.error)
                                    return False
                            else:
                                # dry run, just assume everyting is fine
                                self.tty.write(
                                    self.tty.colorizer.green("success", attr="bold")
                                )

                except Exception as e:
                    self.tty.write("\n")
                    self.tty.error("Error : " + str(e))
                    return False
        return True
