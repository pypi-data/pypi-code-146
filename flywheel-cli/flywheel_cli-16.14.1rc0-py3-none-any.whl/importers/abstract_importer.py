"""Provides interface for importers"""
import collections
import copy
import datetime
import logging
import sys
from abc import ABC, abstractmethod

import fs

from .. import util
from ..walker import create_archive_walker
from .audit_log import AuditLog
from .container_factory import ContainerFactory
from .upload_queue import UploadQueue

log = logging.getLogger(__name__)


class AbstractImporter(ABC):
    """Abstract importer class"""

    # Whether or not archive filesystems are supported
    support_archive_fs = True
    support_subject_mapping = False

    def __init__(self, group, project, repackage_archives, context, config):
        """Abstract class that handles state for flywheel imports

        Arguments:
            group (str): The optional group id
            project (str): The optional project label or id in the format <id:xyz>
            repackage_archives (bool): Whether or not to repackage (and validate and de-identify) zipped packfiles. Default is False.
            context (dict): The optional additional context fields
            config (Config): The config object
        """
        self.resolver = config.get_resolver()
        self.container_factory = ContainerFactory(self.resolver, uids=config.use_uids)

        self.group = group
        self.project = project
        self.messages = []
        self.context = context
        self.config = config
        self.repackage_archives = repackage_archives

        if config:
            self.deid_profile = config.deid_profile
        else:
            self.deid_profile = None

        self.audit_log = self.init_audit_log(config.audit_log)

    @property
    def assume_yes(self):
        """Get 'assume_yes' from config"""
        if self.config:
            return self.config.assume_yes
        return False

    @property
    def max_retries(self):
        """Get 'max_retries' from config"""
        if self.config:
            return self.config.max_retries
        return 0

    @property
    def retry_wait(self):
        """Get 'retry_wait' from config"""
        if self.config:
            return self.config.retry_wait
        return 0

    def initial_context(self):
        """Creates the initial context for folder import.

        Returns:
            dict: The initial context
        """
        context = {}

        if self.context:
            for key, value in self.context.items():
                util.set_nested_attr(context, key, value)

        if self.group:
            util.set_nested_attr(context, "group._id", self.group)

        if self.project:
            # TODO: Check for <id:xyz> syntax
            util.set_nested_attr(context, "project.label", self.project)

        return context

    def print_summary(self, file=sys.stdout):
        """Print a summary of the import operation in tree format.

        Arguments:
            file (fileobj): A file-like object that supports write(string)
        """
        # Generally - Print current container, print files, walk to next child
        spacer_str = "|   "
        if sys.stdout.encoding == "UTF-8":
            entry_str = "├── "
        else:
            entry_str = "|-- "

        def write(level, msg):
            print(f"{level*spacer_str}{entry_str}{msg}", file=file)

        groups = self.container_factory.get_groups()
        queue = collections.deque(
            [(0, group) for group in util.sorted_container_nodes(groups)]
        )

        counts = {
            "group": 0,
            "project": 0,
            "subject": 0,
            "session": 0,
            "acquisition": 0,
            "file": 0,
            "packfile": 0,
        }

        while queue:
            level, current = queue.popleft()
            cname = current.label or current.id
            status = "using" if current.exists else "creating"

            write(level, f"{cname} ({status})")

            level = level + 1
            for path in sorted(current.files, key=str.lower):
                write(level, fs.path.basename(path))

            for desc in current.packfiles:
                label = desc.name if desc.name else desc.packfile_type
                write(level, f"{label} ({desc.count} files)")
            for child in util.sorted_container_nodes(current.children):
                queue.appendleft((level, child))

            # Update counts
            counts[current.container_type] = counts[current.container_type] + 1
            counts["file"] = counts["file"] + len(current.files)
            counts["packfile"] = counts["packfile"] + len(current.packfiles)

        print("\n", file=file)
        print(f'This scan consists of: {counts["group"]} groups,', file=file)
        print(f'                       {counts["project"]} projects,', file=file)
        print(f'                       {counts["subject"]} subjects,', file=file)
        print(f'                       {counts["session"]} sessions,', file=file)
        print(
            f'                       {counts["acquisition"]} acquisitions,', file=file
        )
        print(f'                       {counts["file"]} attachments, and', file=file)
        print(f'                       {counts["packfile"]} packfiles.', file=file)

        return counts

    def verify(self):
        """Verify the upload plan, returning any messages that should be logged, with severity.

        Returns:
            list: A list of tuples of severity, message to be logged
        """
        results = copy.copy(self.messages)

        for _, container in self.container_factory.walk_containers():
            if container.container_type == "project" and not self.config.output_folder:
                self.resolver.fw.can_import_into(container.parent.id, container.label)
            if container.container_type in util.NO_FILE_CONTAINERS:
                cname = container.label or container.id
                for path in container.files:
                    fname = fs.path.basename(path)
                    msg = f"File {fname} cannot be uploaded to {container.container_type} {cname} - files are not supported at this level"
                    results.append(("warn", msg))

                for _ in container.packfiles:
                    msg = f"pack-file cannot be uploaded to {container.container_type} {cname} - files are not supported at this level"
                    results.append(("warn", msg))

        # Unique UID Check
        if self.config.check_unique_uids:
            (
                uid_count,
                conflict_containers,
            ) = self.container_factory.check_container_unique_uids()

            if not uid_count:
                results.append(
                    (
                        "warn",
                        "No UIDs found, even though check-unique-ids was requested!",
                    )
                )

            for container in conflict_containers:
                msg = (
                    f'{container.container_type} {getattr(container, "label", "UNKNOWN")}'
                    f" has duplicates the UID of an existing container (uid={container.uid})"
                )
                results.append(("warn", msg))

        return results

    def discover(self, walker):
        """Performs discovery of containers to create and files to upload in the given folder.

        Arguments:
            walker (AbstractWalker): The filesystem to walk
        """
        context = self.initial_context()
        self.perform_discover(walker, context)

    @abstractmethod
    def perform_discover(self, walker, context):
        """Performs discovery of containers to create and files to upload in the given folder.

        Arguments:
            walker (AbstractWalker): The filesystem to query
            context (dict): The initial context for discovery
        """

    def interactive_import(self, folder):
        """Performs interactive import of the discovered hierarchy"""
        # pylint: disable=too-many-branches, too-many-statements
        # Sanity check
        if (
            not self.support_subject_mapping
            and self.deid_profile
            and self.deid_profile.map_subjects
        ):
            log.error("Subject mapping not supported with this import type!")
            sys.exit(1)

        if not self.config.output_folder:
            grp = getattr(self, "override_group", self.group)
            prj = getattr(self, "override_project", self.project)
            self.resolver.fw.can_import_into(grp, prj)

        fs_url = util.to_fs_url(folder, self.support_archive_fs)

        # Log the root directory of the scan
        self.audit_log.log_root_dir(folder)

        try:
            log.debug(f"Using source filesystem: {fs_url}")
            walker = self.config.create_walker(fs_url)
        except fs.errors.CreateFailed:
            log.error(f'Could not open filesystem at "{folder}"')
            sys.exit(1)

        # Perform discovery on target filesystem
        self.discover(walker)

        if self.container_factory.is_empty():
            log.error("Nothing found to import!")
            sys.exit(1)

        # Print summary
        print("The following data hierarchy was found:\n")
        counts = self.print_summary()

        # Print warnings
        print("")
        have_errors = False
        for severity, msg in self.verify():
            severity = severity.upper()
            if severity == "ERROR":
                have_errors = True
            print(f"{severity} - {msg}")
        print("")

        if have_errors:
            sys.exit(1)

        fw = util.get_sdk_client_for_current_user()
        confirmation_prompt = f"Confirm upload to {fw.host}?"
        if not self.assume_yes and not util.confirmation_prompt(confirmation_prompt):
            return

        self.before_begin_upload()

        # Initialize profile
        if self.deid_profile:
            self.deid_profile.initialize()

        # Create containers
        self.container_factory.create_containers()

        # Walk the hierarchy, uploading files
        upload_queue = UploadQueue(
            self.config,
            self.audit_log,
            upload_count=counts["file"],
            packfile_count=counts["packfile"],
        )
        upload_queue.start()

        for _, container in self.container_factory.walk_containers():
            cname = container.label or container.id

            for path in container.files:
                file_name = util.sanitize_filename(fs.path.basename(path))

                if self.repackage_archives and util.is_archive(path):
                    archive_walker = create_archive_walker(walker, path)
                    if archive_walker:
                        if util.contains_dicoms(archive_walker):
                            # Repackage upload
                            upload_queue.upload_packfile(
                                archive_walker,
                                "dicom",
                                self.deid_profile,
                                container,
                                file_name,
                            )
                            continue
                        archive_walker.close()

                # Normal upload
                upload_queue.upload_file(container, file_name, walker, path)

            # packfiles
            for desc in container.packfiles:
                if desc.name:
                    file_name = desc.name
                else:
                    # Don't call things foo.zip.zip
                    packfile_name = cname
                    if desc.packfile_type == "zip":
                        file_name = f"{packfile_name}.zip"
                    else:
                        file_name = f"{packfile_name}.{desc.packfile_type}.zip"

                if isinstance(desc.path, str):
                    upload_queue.upload_packfile(
                        walker,
                        desc.packfile_type,
                        self.deid_profile,
                        container,
                        file_name,
                        subdir=desc.path,
                    )
                else:
                    upload_queue.upload_packfile(
                        walker,
                        desc.packfile_type,
                        self.deid_profile,
                        container,
                        file_name,
                        paths=desc.path,
                    )

        upload_queue.wait_for_finish()
        # Retry loop for errored jobs
        retries = 0
        while upload_queue.has_errors():

            upload_queue.suspend_reporting()
            print("")
            if self.assume_yes:
                if retries >= self.max_retries:
                    log.error("Maximum number of retries has been reached!")
                    break
                retries += 1
                import time  # pylint: disable=import-outside-toplevel

                log.info(f"Retrying in {self.retry_wait} seconds...")
                time.sleep(self.retry_wait)

            elif not util.confirmation_prompt("One or more errors occurred. Retry?"):
                break

            # Requeue and wait for finish
            upload_queue.requeue_errors()
            upload_queue.resume_reporting()
            upload_queue.wait_for_finish()

        # Shutdown de-id profile
        if self.deid_profile:
            self.deid_profile.finalize()

        self.audit_log.finalize(self.container_factory)

        upload_queue.shutdown()
        walker.close()

    def before_begin_upload(self):
        """Called before actual upload begins"""

    @staticmethod
    def init_audit_log(audit_log_path):
        """Initialize audit log"""
        if audit_log_path:
            if audit_log_path is True:
                audit_log_path = (
                    f'audit_log-{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}.csv'
                )
        else:
            audit_log_path = None
        return AuditLog(audit_log_path)
