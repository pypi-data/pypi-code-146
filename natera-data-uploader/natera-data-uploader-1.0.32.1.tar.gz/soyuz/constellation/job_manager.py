import logging
import time
from threading import Thread

import dxpy
import zope.event.classhandler
from dxpy import DXRecord, DXJobFailureError, DXJob

from soyuz.constellation.api import ConstellationApi
from soyuz.dx.context import Context
from soyuz.dx.sentinels import SentinelBase
from soyuz.dx.variables import Type, Property
from soyuz.event.upload import SeqFolderUploadStart, UploadJobTerminated, SeqFolderUploadTerminated, NewUploadJob, \
    SeqFolderUploadComplete


class UploadJobWatcher(object):
    SOYUZ_JOB_MARKER = 'soyuzJob'

    def __init__(self, context, constellation_api, check_interval=30):
        # type: (Context, ConstellationApi, float) -> None

        self.__seq_folder_name_to_job_ids = {}

        self.__context = context
        self.__constellation_api = constellation_api
        self.__check_interval = check_interval

        self.__stop = False
        self.__watcher_thread = Thread(target=self._check_jobs, args=())
        self.__watcher_thread.daemon = True

    def watch_job(self, seq_folder_name, job_id):
        # type: (str, str) -> None

        self.__seq_folder_name_to_job_ids[seq_folder_name] = job_id

    def start(self):
        self.__watcher_thread.start()

    def stop(self):
        self.__stop = True

    def wait_upload_job_completion(self, run_folder_name):
        # type: (str) -> None

        if run_folder_name in self.__seq_folder_name_to_job_ids:
            job_id = self.__seq_folder_name_to_job_ids[run_folder_name]
            logging.info('Waiting until upload job with id: {} will be finished'.format(job_id))

            try:
                DXJob(job_id).wait_on_done(interval=10, timeout=60 * 5)
            except DXJobFailureError:
                logging.info(
                    'Upload job with id: {} has been terminated or reached timeout (5 min) while waiting for the job to finish.'.format(
                        job_id))

                self.cleanup_seq_folder(run_folder_name)

    def cleanup_seq_folder(self, seq_folder_name):
        # type: (str) -> None

        logging.info('Cleanup {} folder'.format(seq_folder_name))

        manifest = self._get_manifest(seq_folder_name)

        details = manifest.get_details()
        properties = manifest.get_properties()
        types = manifest.types
        manifest_name = manifest.name

        full_run_folder_name = "{}/{}".format(self.__context.get_settings().get_base_dir(), details['runFolder'])

        self._remove_data_from_run_folder(full_run_folder_name)
        self._remove_marker_from_upload_job(properties['jobId'])

        self._create_new_manifest(details, properties, types, manifest_name, full_run_folder_name)

    def _get_manifest(self, seq_folder_name):
        # type: (str) -> DXRecord | None

        try:
            return next(dxpy.bindings.find_data_objects(classname="record",
                                                        typename=Type.UPLOAD_MANIFEST,
                                                        properties={Property.RUN_FOLDER: seq_folder_name},
                                                        describe=True,
                                                        project=self.__context.get_project_id(),
                                                        return_handler=True))
        except StopIteration:
            return None

    def _remove_data_from_run_folder(self, full_run_folder):
        # type: (str) -> None

        logging.debug("Removing data from {}".format(full_run_folder))

        dx_project = dxpy.DXProject(self.__context.get_project_id())
        dx_project.remove_folder(full_run_folder, recurse=True, force=True)
        dx_project.new_folder(full_run_folder, parents=True)

    def _remove_marker_from_upload_job(self, job_id):
        # type: (str) -> None

        logging.debug("Removing marker property from {}".format(job_id))

        dxpy.DXJob(job_id).set_properties({self.SOYUZ_JOB_MARKER: None})

    def _create_new_manifest(self, details, properties, types, manifest_name, full_run_folder_name):
        # type: (dict, dict, list, str, str) -> None

        properties[Property.TERMINATED] = "true"
        record = dxpy.new_dxrecord(types=types,
                                   folder=full_run_folder_name,
                                   name=manifest_name,
                                   project=self.__context.get_project_id(),
                                   properties=properties,
                                   details=details).close()
        logging.debug("Manifest copied to {}".format(record))

    def _check_jobs(self):
        while not self.__stop:
            finished_seq_folder_names = set()

            for job in self._get_upload_jobs_in_project(self.__context.get_project_id()):
                job_id = job['id']
                state = job['describe']['state'].upper()
                seq_folder_name = job['describe']['properties']['runFolder']

                if state == 'DONE' and job_id in self.__seq_folder_name_to_job_ids.values():
                    finished_seq_folder_names.add(seq_folder_name)
                elif state == 'TERMINATED' and job_id in self.__seq_folder_name_to_job_ids.values():
                    finished_seq_folder_names.add(seq_folder_name)
                    zope.event.notify(UploadJobTerminated(seq_folder_name))
                elif state == 'WAITING_ON_INPUT' and seq_folder_name not in self.__seq_folder_name_to_job_ids:
                    self.__seq_folder_name_to_job_ids[seq_folder_name] = job_id
                    zope.event.notify(NewUploadJob(job_id, seq_folder_name))

            for seq_folder_name in finished_seq_folder_names:
                del self.__seq_folder_name_to_job_ids[seq_folder_name]

            time.sleep(self.__check_interval)

    @staticmethod
    def _get_upload_jobs_in_project(project_id):
        # type: (str) -> list

        return dxpy.find_executions(classname='job',
                                    properties={Property.PRODUCT: 'UPLOAD'},
                                    project=project_id,
                                    describe=True)


class UploadJobManager(object):
    def __init__(self, constellation_api, job_watcher, is_constellation_portal_mode):
        # type: (ConstellationApi, UploadJobWatcher, bool) -> None

        self.__constellation_api = constellation_api
        self.__job_watcher = job_watcher
        self.__is_constellation_portal_mode = is_constellation_portal_mode

        self.__init_listeners()

    def start_watcher(self):
        self.__job_watcher.start()

    def _create_upload_job(self, seq_folder_name, sentinel):
        # type: (str, SentinelBase) -> None

        site_id = sentinel.get_properties().get(Property.SITE_ID, None)
        job_id = self.__constellation_api.start_upload_job(seq_folder_name, site_id)
        sentinel.add_property(Property.JOB_ID, job_id)

        self.__job_watcher.watch_job(seq_folder_name, job_id)

    def __init_listeners(self):
        @zope.event.classhandler.handler(SeqFolderUploadStart)
        def on_seq_folder_upload_start(event):
            # type: (SeqFolderUploadStart) -> None

            if not self.__is_constellation_portal_mode:
                # Wait 1 seconds, we need this for avoid problem with missing sentinel record
                time.sleep(1)
                self._create_upload_job(event.seq_folder.get_name(), event.sentinel)

        @zope.event.classhandler.handler(SeqFolderUploadComplete)
        def on_seq_folder_upload_complete(event):
            # type: (SeqFolderUploadComplete) -> None

            self.__job_watcher.wait_upload_job_completion(event.seq_folder.get_name())

        @zope.event.classhandler.handler(SeqFolderUploadTerminated)
        def on_seq_folder_upload_terminated(event):
            # type: (SeqFolderUploadTerminated) -> None

            self.__job_watcher.cleanup_seq_folder(event.seq_folder.get_name())
