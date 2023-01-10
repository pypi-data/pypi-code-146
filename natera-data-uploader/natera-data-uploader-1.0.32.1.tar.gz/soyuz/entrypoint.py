#!/usr/bin/env python

import logging

from soyuz.configuration import Parameters
from soyuz.configuration import Settings
from soyuz.constellation.api import ConstellationApi
from soyuz.constellation.job_manager import UploadJobManager, UploadJobWatcher
from soyuz.data.daemons import Daemon
from soyuz.data.folders import WesSignateraSeqFolder, BgiSeqFolder, RawSeqFolder, PersonalisSeqFolder, WatchDirectory, \
    SangerSeqFolder, NgsSeqFolder
from soyuz.dx.context import Context
from soyuz.dx.uploaders import WesSignateraDxUploader, BgiDxUploader, RawDxUploader, PersonalisDxUploader, \
    WatchUploader, SangerDxUploader, NgsDxUploader
from soyuz.utils import UploaderException


def main():
    try:
        params = Parameters()
        settings = Settings(full_path_to_settings_file=params.get_setting_file_path())
        settings.logging.initialize()

        if params.get_action() in [Parameters.UPLOAD_ACTION, Parameters.WATCH_ACTION]:
            folder = None
            uploader = None

            context = Context(params, settings)
            context.initialize()

            if params.is_with_upload_job() or params.is_constellation_portal_mode():
                constellation_api = ConstellationApi(settings.get_token(), settings.get_constellation_url())

                UploadJobManager(constellation_api,
                                 UploadJobWatcher(context, constellation_api),
                                 params.is_constellation_portal_mode()).start_watcher()

            if params.get_action() == Parameters.UPLOAD_ACTION:
                if params.get_upload_type() == Parameters.WES_SIGNATERA_UPLOAD:
                    uploader = WesSignateraDxUploader(context)
                    folder = WesSignateraSeqFolder(params.get_folder())
                elif params.get_upload_type() == Parameters.BGI_UPLOAD:
                    uploader = BgiDxUploader(context)
                    folder = BgiSeqFolder(params.get_folder())
                elif params.get_upload_type() == Parameters.RAW_UPLOAD:
                    uploader = RawDxUploader(context)
                    folder = RawSeqFolder(params.get_folder())
                elif params.get_upload_type() == Parameters.PERSONALIS_UPLOAD:
                    uploader = PersonalisDxUploader(context)
                    folder = PersonalisSeqFolder(params.get_folder())
                elif params.get_upload_type() == Parameters.SANGER_UPLOAD:
                    uploader = SangerDxUploader(context)
                    folder = SangerSeqFolder(params.get_folder(), params.get_sanger_check_interval())
                elif params.get_upload_type() == Parameters.NGS_UPLOAD:
                    uploader = NgsDxUploader(context)
                    folder = NgsSeqFolder(params.get_folder(),
                                          params.get_ngs_completion_marker(),
                                          params.get_ngs_check_interval(),
                                          params.get_ngs_file_age_time(),
                                          params.get_ngs_archive_temp_folder())

                if not folder or not uploader:
                    raise UploaderException("Incorrect upload type")

                if not folder.is_valid:
                    raise UploaderException("Data folder is not in a valid state")

                uploader.upload(folder)

            elif params.get_action() == Parameters.WATCH_ACTION:

                settings.set_interval(params.get_interval() or settings.get_interval())

                uploader = WatchUploader(context)

                if params.get_watch_type() == Parameters.START_WATCH:
                    if params.foreground():
                        uploader.watch(WatchDirectory(context))
                    else:
                        Daemon(uploader.watch, WatchDirectory(context)).start()
                elif params.get_watch_type() == Parameters.STOP_WATCH:
                    Daemon().stop()
                elif params.get_watch_type() == Parameters.STATUS_WATCH:
                    Daemon().status()

        elif params.get_action() == Parameters.CONFIG_ACTION:

            if params.get_config_action() == Parameters.GET_CONFIG:
                if params.get_config_parameter_key() == "storage":
                    logging.info(settings.get_storage())
                elif params.get_config_parameter_key() == "token":
                    logging.info(settings.get_token())
                elif params.get_config_parameter_key() == "stella_url":
                    logging.info(settings.get_exodus_url())
                elif params.get_config_parameter_key() == "constellation_url":
                    logging.info(settings.get_constellation_url())
                elif params.get_config_parameter_key() == "basedir":
                    logging.info(settings.get_base_dir())
                elif params.get_config_parameter_key() == "interval":
                    logging.info(settings.get_interval())
                elif params.get_config_parameter_key() == "ua_path":
                    logging.info(settings.get_ua_path())
                elif params.get_config_parameter_key() == "ua_parameters":
                    logging.info(settings.get_ua_parameters())
                elif params.get_config_parameter_key() == "process_count":
                    logging.info(settings.get_process_count())
                elif params.get_config_parameter_key() == "chunk_size":
                    logging.info(settings.get_chunk_size())
                elif params.get_config_parameter_key() == "jwt_token":
                    logging.info(settings.get_jwt_token())
                elif params.get_config_parameter_key() == "jwt_token_public_key_path":
                    logging.info(settings.get_jwt_token_public_key_path())
                elif params.get_config_parameter_key() == "constellation_url":
                    logging.info(settings.get_constellation_url())

            elif params.get_config_action() == Parameters.SET_CONFIG:
                if params.get_config_parameter_key() == "storage":
                    settings.set_storage(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "token":
                    settings.set_token(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "stella_url":
                    settings.set_exodus_url(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "stella_username":
                    settings.set_exodus_username(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "stella_password":
                    settings.set_exodus_password(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "stella_aws_access_key_id":
                    settings.set_exodus_aws_access_key_id(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "stella_aws_secret_access_key":
                    settings.set_exodus_aws_secret_access_key(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "stella_s3_bucket_name":
                    settings.set_exodus_s3_bucket_name(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "stella_aws_region":
                    settings.set_exodus_aws_region(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "stella_sample_source":
                    settings.set_exodus_sample_source(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "constellation_url":
                    settings.set_constellation_url(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "basedir":
                    settings.set_basedir(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "interval":
                    settings.set_interval(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "ua_path":
                    settings.set_ua_path(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "ua_parameters":
                    settings.set_ua_parameters(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "process_count":
                    settings.set_process_count(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "chunk_size":
                    settings.set_chunk_size(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "jwt_token":
                    settings.set_jwt_token(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "jwt_token_public_key_path":
                    settings.set_jwt_token_public_key_path(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "constellation_url":
                    settings.set_constellation_url(params.get_config_parameter_value())
                else:
                    raise UploaderException("There is no parameter '{}'".format(params.get_config_parameter_key()))
                settings.dump()
                logging.info("Set {} to {}".format(params.get_config_parameter_key(), params.get_config_parameter_value()))

    except Exception as e:
        logging.error(e, exc_info=True)
        quit(1)


if __name__ == "__main__":
    main()
