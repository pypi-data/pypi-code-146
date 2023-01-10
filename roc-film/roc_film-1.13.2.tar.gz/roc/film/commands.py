#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Commands for FILM plugin.
"""

import os.path as osp

from poppy.core.command import Command
from poppy.core.tools.exceptions import MissingArgument
from poppy.core.logger import logger

from roc.film.tools.file_helpers import get_output_dir, get_products_dir, is_output_dir
from roc.film.tools import IDBToExcel
from roc.film.tools import paths, \
    valid_time, \
    valid_single_file, \
    setup_lock, valid_date

from roc.film.tasks import L0ToHk
from roc.film.tasks import L0ToL1Surv
from roc.film.tasks import L0ToL1Sbm
from roc.film.tasks.l0_to_anc_bia_sweep_table import L0ToAncBiaSweepTable
from roc.film.tasks.l0_to_l1_bia_current import L0ToL1BiaCurrent
from roc.film.tasks import L0ToL1BiaSweep
from roc.film.tasks import MoveFailedFiles, MoveToProdDir
from roc.film.tasks import CopyProcessedDds, CopyFailedDds
from roc.film.tasks.dds_to_l0 import DdsToL0
from roc.film.tasks.set_l0_utc import SetL0Utc
from roc.film.tasks.cdf_postpro import CdfPostPro
from roc.film.tasks.check_dds import CheckDds
from roc.film.tasks.cat_solo_hk import CatSoloHk
from roc.film.tasks.make_daily_tm import MakeDailyTm
from roc.film.tasks.merge_tcreport import MergeTcReport
from roc.film.tasks.merge_tmraw import MergeTmRaw
from roc.film.tasks.parse_dds_xml import ParseDdsXml
from roc.film.constants import SCOS_HEADER_BYTES, TEMP_DIR, CDFEXPORT_PATH, CDF_POST_PRO_OPTS_ARGS


class FilmCommands(Command):
    """
    Manage the commands relative to the FILM plugin.
    """
    __command__ = 'film'
    __command_name__ = 'film'
    __parent__ = 'master'
    __parent_arguments__ = ['base']
    __help__ = """
        Commands relative to the FILM plugin, responsible for generating and
        storing data products files from the ROC pipeline.
    """

    def add_arguments(self, parser):
        """
        Add input arguments common to all the FILM plugin.

        :param parser: high-level pipeline parser
        :return:
        """

        # If passed as an argument, then generate a temporary file
        # in the output folder
        # To indicate that output file production is in progress
        # lock file is automatically deleted at the end.
        parser.add_argument(
            '--lock-file',
            help='Name of the lock temporary file.',
            default=None,
            nargs=1,
        )

        # Final target output file directory
        # Output files will be moved into this directory at the end of the run
        # (If not passed, output files will stay in the output directory)
        parser.add_argument(
            '--products-dir',
            type=str,
            help='Path of the directory where output file(s) folder'
                 ' must be moved at the end of the process',
            default=None,
            nargs=1,
        )

        # specify the IDB version to use
        parser.add_argument(
            '--idb-version',
            help='IDB version to use.',
            default=None,
            nargs=1,
        )

        # specify the IDB source to use
        parser.add_argument(
            '--idb-source',
            help='IDB source to use (MIB, SRDB or PALISADE).',
            default=None,
            nargs=1,
        )

        # Get path of the master binary CDF directory
        parser.add_argument(
            '-m',
            '--master-cdf-dir',
            help="""
            The absolute path to the directory where the master binary CDF are stored.
            If not provided, try to check the value of
            $RPW_CDF_MASTER_PATH variable in the config.json file
            (otherwise try to load the $RPW_CDF_MASTER_PATH env. variable).
            """,
            type=str,
            default=None,
            nargs=1,
        )

        # Specify the value of the Data_version attribute (and filename)
        parser.add_argument(
            '-v',
            '--data-version',
            help='Define the Data_version attribute value for output CDF.',
            default=None,
            nargs=1
        )

        parser.add_argument(
            '-s',
            '--start-time',
            help='Data file production start time. '
            "Expected datetime format is 'YYYY-MM-DDThh:mm:ss'.",
            type=valid_time,
            default=None,
            nargs=1,
        )

        parser.add_argument(
            '-e',
            '--end-time',
            help='Data file production end time. '
                 "Expected datetime format is 'YYYY-MM-DDThh:mm:ss'.",
            type=valid_time,
            default=None,
            nargs=1,
        )

        # Give the month to process (will replace start_time/end_time values)
        parser.add_argument(
            '--monthly',
            action='store_true',
            default=False,
            help='Generate output monthly files'
        )

        # Remove SCOS2000 header in the binary packet
        parser.add_argument(
            '--scos-header',
            nargs=1,
            type=int,
            default=[SCOS_HEADER_BYTES],
            help='Length (in bytes) of SCOS2000 header to be removed'
                 ' from the TM packet in the DDS file.'
                 f' (Default value is {SCOS_HEADER_BYTES} bytes.)',
        )

        # Do no process/write invalid packet(s)
        parser.add_argument(
            '--no-invalid-packet',
            action='store_true',
            help='Do not keep invalid packet(s).',
        )

        # If True, tag any output file with "-cdag" suffix in the descriptor field
        # of the L1 CDF filename.
        # Indicating that it is a preliminary files to be distributed to the
        # Calibration Data Access Group (CDAG) only
        parser.add_argument(
            '--cdag',
            action='store_true',
            help='If True, add the "cdag" suffix to the descriptor field of L1 CDF filename.',
            default=False,
        )

        # Do not use NAIF SPICE toolkit to compute time/ancillary data
        parser.add_argument(
            '--no-spice',
            action='store_true',
            help='Do not use NAIF SPICE toolkit to compute time/ancillary data.',
        )

        # Force data file creation
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force data file creation.',
        )


class ClassifyTmRawCommand(Command):
    """
    Command to classify input set of SolO DDS TmRaw file(s) into daily files.
    TmRaw data is sorted using CCSDS CUC time in packet data field header.

    If output files already found for a given date in the local archive,
    by default new version of the daily file is created and
    only new DDS packets have been inserted.
    """
    __command__ = 'film_classify_tmraw'
    __command_name__ = 'classify_tmraw'
    __parent__ = 'film'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to classify input SolO DDS TmRaw files as daily file(s).
    """

    def add_arguments(self, parser):

        # path of input DDS TmRaw response file(s)
        parser.add_argument(
            '--dds-files',
            help="""
             List of input SolO DDS TmRaw response XML file(s) to classify.
             """,
            type=str,
            nargs='+',
            required=True,
        )

        parser.add_argument(
            '--processed-dds-dir',
            help=f"""
             Directory where processed DDS file(s) must be moved at the end.
             """,
            type=str,
            default=None,
            nargs=1,
        )

        parser.add_argument(
            '--failed-dds-dir',
            help=f"""
             Directory where failed DDS file(s) must be moved at the end.
             """,
            type=str,
            default=None,
            nargs=1,
        )

        parser.add_argument(
            '--archive-path',
            type=str,
            default=None,
            help='Root path of the archive local directory.'
                 'If defined, the pipeline first check if daily file(s) already exist(s) in the archive',
            nargs=1,
        )

        # Clear input DDS files
        parser.add_argument(
            '--clear-dds',
            action='store_true',
            help='If passed, then remove input list of processed/failed Dds.',
            default=False,
        )

        parser.add_argument(
            '--filter-date',
            type=valid_date,
            default=[],
            help='List of date(s) to process (format is YYYYMMDD)',
            nargs='+',
        )

    def setup_tasks(self, pipeline):
        """
        Execute the generation of the RPW daily file(s) with TmRaw data.
        """

        # Define start task
        start = CheckDds()
        end = CopyProcessedDds()
        loop_start = ParseDdsXml()
        loop_end = MergeTmRaw()

        # create the tasks and their dependencies :
        # load an input DDS TmRaw, then extract time,
        # then generate or update daily files
        pipeline | start | loop_start | loop_end | MakeDailyTm() | \
            MoveFailedFiles() | \
            CopyFailedDds() | end

        # define the start points of the pipeline
        pipeline.start = start

        # Loop over each chunk of packets in the DDS files
        pipeline.loop(loop_start, loop_end, start.loop_generator)

        # Set no_tcreport to True to retrieve only TmRaw
        pipeline.properties.no_tcreport = True


class ClassifyTcReportCommand(Command):
    """
    Command to classify input set of SolO DDS TcReport file(s) into daily files.
    TcReport data is sorted using CCSDS CUC time in packet data field header.

    If output files already found for a given date in the local archive,
    by default new version of the daily file is created and
    only new DDS packets have been inserted.
    """
    __command__ = 'film_classify_tcreport'
    __command_name__ = 'classify_tcreport'
    __parent__ = 'film'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to classify input SolO DDS TcReport files as daily file(s).
    """

    def add_arguments(self, parser):

        # List of input DDS TcReport response files
        parser.add_argument(
            '--dds-files',
            help="""
             List of SolO DDS TcReport response XML file(s) to classify.
             """,
            type=str,
            nargs='+',
            required=True,
        )

        parser.add_argument(
            '--processed-dds-dir',
            help=f"""
             Directory where processed DDS file(s) must be moved at the end.
             """,
            type=str,
            default=None,
            nargs=1,
        )

        parser.add_argument(
            '--failed-dds-dir',
            help=f"""
             Directory where failed DDS file(s) must be moved at the end.
             """,
            type=str,
            default=None,
            nargs=1,
        )

        parser.add_argument(
            '--archive-path',
            type=str,
            default=None,
            nargs=1,
            help='Root path of the archive local directory.'
                 'If defined, the pipeline first check if daily file(s) already exist(s) in the archive',
        )

        # Clear input DDS files
        parser.add_argument(
            '--clear-dds',
            action='store_true',
            help='If passed, then remove input list of processed/failed Dds.',
            default=False,
        )

        parser.add_argument(
            '--filter-date',
            type=valid_date,
            default=[],
            help='List of date(s) to process (format is YYYYMMDD)',
            nargs='+',
        )

    def setup_tasks(self, pipeline):
        """
        Execute the generation of the RPW daily file(s) with TcReport data.
        """

        # Define start task
        start = CheckDds()
        loop_start = ParseDdsXml()
        loop_end = CopyFailedDds()

        # create the tasks and their dependencies :
        # load an input DDS TcReport, then extract time,
        # then generate or update daily files
        pipeline | start | loop_start | MergeTcReport() \
            | CopyProcessedDds() | loop_end | \
            MoveFailedFiles()

        # define the start points of the pipeline
        pipeline.start = start

        # Loop over each chunk of packets in the DDS files
        pipeline.loop(loop_start, loop_end, start.loop_generator)

        # Set no_tmraw to True to retrieve only TcReport
        pipeline.properties.no_tmraw = True


class ProcessSoloHkCommand(Command):
    """
    Command to process input set of SolO DDS Param file(s) containing
    Solar Orbiter HK data.
    Input data are save into daily XML files when parameters are sorted
    by ascending times

    If output files already found for a given date in the local archive,
    by default new version of the daily file is created and
    only new Param elements have been inserted.
    """
    __command__ = 'film_process_solohk'
    __command_name__ = 'process_solohk'
    __parent__ = 'film'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to make daily XML file(s) from an
        input set of SolO DDS Solo HK param files
    """

    def add_arguments(self, parser):

        # path of input DDS TmRaw response file(s)
        parser.add_argument(
            '--dds-files',
            help="""
             List of input SolO DDS Param response XML file(s) to process.
             """,
            type=str,
            nargs='+',
            required=True,
        )

        parser.add_argument(
            '--processed-dds-dir',
            help=f"""
             Directory where processed DDS file(s) must be moved at the end.
             """,
            type=str,
            default=None,
            nargs=1,
        )

        parser.add_argument(
            '--failed-dds-dir',
            help=f"""
             Directory where failed DDS file(s) must be moved at the end.
             """,
            type=str,
            default=None,
            nargs=1,
        )

        parser.add_argument(
            '--archive-path',
            type=str,
            default=None,
            help='Root path of the archive local directory.'
                 'If defined, the pipeline first check if daily file(s) already exist(s) in the archive',
            nargs=1,
        )

        # Clear input DDS files
        parser.add_argument(
            '--clear-dds',
            action='store_true',
            help='If passed, then remove input list of processed/failed Dds.',
            default=False,
        )

        parser.add_argument(
            '--filter-date',
            type=valid_date,
            default=[],
            help='List of date(s) to process (format is YYYYMMDD)',
            nargs='+',
        )

    def setup_tasks(self, pipeline):
        """
        Execute the generation of the RPW daily file(s) with SOLO HK data.
        """

        # Define start task
        start = CatSoloHk()
        end = MoveFailedFiles()

        # create the tasks and their dependencies :
        # load an input DDS SOLO HK Param, then extract time,
        # then generate or update daily files
        pipeline | start | CopyProcessedDds() \
                 | CopyFailedDds() \
                 | end

        # define the start points of the pipeline
        pipeline.start = start
        pipeline.end = end


class DdsToLOCommand(Command):
    """
    Command to produce a RPW L0 file for a given day
    from an input set of MOC DDS response XML file(s).
    """
    __command__ = 'film_dds_to_l0'
    __command_name__ = 'dds_to_l0'
    __parent__ = 'film'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to generate a RPW L0 XML daily file
        from an input set of MOC DDS response XML files.
    """

    def add_arguments(self, parser):

        # add lstable argument
        #        LSTableMixin.add_arguments(parser)

        #
        parser.add_argument(
            'datetime',
            help="""
             Date for which L0 file must produced.
             """,
            type=valid_date,
        )

        # path to input DDS TmRaw response file(s)
        parser.add_argument(
            '--dds-tmraw-xml',
            help="""
             Input DDS TmRaw response XML file(s) to convert.
             """,
            nargs='*',
            type=str,
            default=[],
        )

        # path to input DDS TcReport XML response file(s)
        parser.add_argument(
            '--dds-tcreport-xml',
            help="""
             Input DDS TcReport response XML file(s) (to add TC in the output file).
             """,
            nargs='*',
            type=str,
            default=[],
        )

        parser.add_argument(
            '--chunk',
            help=f"""
             Number of DDS packets to write in the L0 in one shot.
             """,
            type=int,
            default=None,
        )

    def setup_tasks(self, pipeline):
        """
        Execute the generation of the RPW L0 daily file from DDS files.
        """

        # Check if output dir already exists
        force = pipeline.get('force', default=False)
        output_dir = get_output_dir(pipeline)
        products_dir = get_products_dir(pipeline)
        if (is_output_dir(output_dir, products_dir=products_dir) and
                not force):
            # if yes exit
            logger.info(f'Input request has been already processed. (Use --force keyword to force execution)')
            pipeline.exit()

        start = DdsToL0()
        pipeline | start | MoveFailedFiles() | MoveToProdDir()

        # define the start point of the pipeline
        pipeline.start = start

        # Check mandatory arguments
        for arg in ['idb_source', 'idb_version']:
            if not pipeline.get(arg, default=None, args=True):
                raise MissingArgument(f'{arg} input argument not defined, aborting!')

        # Setup the lock file
        setup_lock(pipeline)

        # Force setting of start_time/end_time value for the input datetime
        if pipeline.get('datetime', args=True):
            pipeline.properties.start_time = None
            pipeline.properties.end_time = None


class SetL0UtcCommand(Command):
    """
    Command to set the UTC times of the input L0 file using SPICE kernels.
    """
    __command__ = 'film_set_l0_utc'
    __command_name__ = 'set_l0_utc'
    __parent__ = 'film'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to set the packet UTC times of
        the input L0 file using SPICE kernels.
        A copy of the input L0 file will be saved to store new UTC time values.
    """

    def add_arguments(self, parser):

        parser.add_argument(
            'l0_file',
            help="""
             L0 file to update.
             """,
            type=str,
            nargs=1,
        )

        parser.add_argument(
            '--kernel-date',
            help="""
             Date of the SPICE kernels to use.
             """,
            type=str,
            nargs=1,
        )

    def setup_tasks(self, pipeline):

        start = SetL0Utc()
        pipeline | start | \
            MoveFailedFiles() | MoveToProdDir()

        # define the start points of the pipeline
        pipeline.start = start

        # Setup the lock file
        setup_lock(pipeline)


class L0ToHkCommand(Command):
    """
    Command to generate RPW HK "digest" CDF files from a given L0 file.
    """
    __command__ = 'film_l0_to_hk'
    __command_name__ = 'l0_to_hk'
    __parent__ = 'film'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to generate RPW HK CDF files from
        a given L0 file.
    """

    def add_arguments(self, parser):
        # path to XML file of the IDB
        parser.add_argument(
            'l0_file',
            help="""
            The L0 file to parse.
            """,
            type=valid_single_file,
            nargs=1,
        )

        # Specify the list of dataset for which files must be generated
        parser.add_argument(
            '-d',
            '--dataset',
            help='List of RPW HK dataset(s) for which files must be produced.'
            'If not defined, then produce all file(s).',
            type=str,
            nargs='+',
            default=[None],
        )

    def setup_tasks(self, pipeline):
        """
        Execute the generation of the RPW HK CDF files.
        """

        # Check if output dir already exists
        force = pipeline.get('force', default=False)
        output_dir = get_output_dir(pipeline)
        products_dir = get_products_dir(pipeline)
        if (is_output_dir(output_dir, products_dir=products_dir) and
                not force):
            # if yes exit
            logger.info(f'Input request has been already processed. (Use --force keyword to force execution)')
            pipeline.exit()

        # the task
        task = L0ToHk()

        # set the workflow with the tasks
        pipeline | task | MoveFailedFiles() | MoveToProdDir()
        pipeline.start = task

        # Setup the lock file
        setup_lock(pipeline)


class L0ToL1SurvCommand(Command):
    """
    Command to generate RPW L1 survey data CDF files from a given L0 file.
    """
    __command__ = 'film_l0_to_l1_surv'
    __command_name__ = 'l0_to_l1_surv'
    __parent__ = 'film'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to generate RPW L1 survey data files from
        a given L0 file.
    """

    def add_arguments(self, parser):
        # path to XML file of the IDB
        parser.add_argument(
            'l0_file',
            help="""
            The L0 file to parse.
            """,
            type=valid_single_file,
            nargs=1
        )

        # Specify the list of dataset for which files must be generated
        parser.add_argument(
            '-d',
            '--dataset',
            help='List of RPW L1 dataset(s) for which files must be produced.'
            'If not defined, then produce all file(s).',
            type=str,
            nargs='+',
            default=[None],
        )

    def setup_tasks(self, pipeline):
        """
        Execute the generation of the RPW L1 survey CDF files.
        """

        # Check if output dir already exists
        force = pipeline.get('force', default=False)
        output_dir = get_output_dir(pipeline)
        products_dir = get_products_dir(pipeline)
        if (is_output_dir(output_dir, products_dir=products_dir) and
                not force):
            # if yes exit
            logger.info(f'Input request has been already processed. (Use --force keyword to force execution)')
            pipeline.exit()

        # the task
        task = L0ToL1Surv()

        # set the workflow with the tasks
        pipeline | task | MoveFailedFiles() | MoveToProdDir()
        pipeline.start = task

        # Setup the lock file
        setup_lock(pipeline)


class L0ToL1SbmCommand(Command):
    """
    Command to generate RPW L1 SBM1/SBM2 data CDF files from a given set of L0 files.
    """
    __command__ = 'film_l0_to_l1_sbm'
    __command_name__ = 'l0_to_l1_sbm'
    __parent__ = 'film'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to generate RPW L1 SBM1/SBM2 data files from
        a given set of L0 file(s).
    """

    def add_arguments(self, parser):
        # path to RPW L0 file(s) to process
        parser.add_argument(
            'l0_files',
            help="""
            The L0 file(s) to process.
            """,
            type=str,
            nargs='+',
        )

        # Specify the list of dataset for which files must be generated
        parser.add_argument(
            '-d',
            '--dataset',
            help='List of RPW dataset(s) for which files must be produced.'
            'If not defined, then produce all file(s).',
            type=str,
            nargs='+',
            default=[None],
        )

        # No process SBM1
        parser.add_argument(
            '--no-sbm1',
            action='store_true',
            help='If passed, then do no process SBM1 data.',
            default=False,
        )

        # No process SBM2
        parser.add_argument(
            '--no-sbm2',
            action='store_true',
            help='If passed, then do no process SBM2 data.',
            default=False,
        )

        # Process any SBM TM packets found in input L0 files, without using
        # TM_DPU_EVENT_PR_DPU_SBM1 or TM_DPU_EVENT_PR_DPU_SBM1 packets information
        parser.add_argument(
            '--manual',
            action='store_true',
            help='Process any SBM TM packets found in input L0 files '
                 '(i.e., without using TM_DPU_EVENT_PR_DPU_SBM1 or TM_DPU_EVENT_PR_DPU_SBM1 packets). '
                 'Use this option with --start-time, --end-time and --sbm-type keywords to process SBM science packets'
                 ' dumped by TC.',
            default=False,
        )

        #
        parser.add_argument(
            '--sbm-type',
            nargs=1,
            type=int,
            default=[None],
            help='Indicate the type of SBM event (1=SBM1 or 2=SBM2) processed when --manual option is passed.',
        )

    def setup_tasks(self, pipeline):
        """
        Execute the generation of the RPW L1 SBM CDF files.
        """

        # Check if output dir already exists
        force = pipeline.get('force', default=False)
        output_dir = get_output_dir(pipeline)
        products_dir = get_products_dir(pipeline)
        if (is_output_dir(output_dir, products_dir=products_dir) and
                not force):
            # if yes exit
            logger.info(f'Input request has been already processed. (Use --force keyword to force execution)')
            pipeline.exit()

        # the task
        task = L0ToL1Sbm()

        # set the pipeline workflow with the task
        pipeline | task | MoveFailedFiles() | MoveToProdDir()
        pipeline.start = task

        # Setup the lock file
        setup_lock(pipeline)


class L0ToAncBiaSweepTableCommand(Command):
    """
    Command to run the pipeline to generate ancillary Bias Sweep table file
    """
    __command__ = 'film_l0_to_anc_bia_sweep_table'
    __command_name__ = 'l0_to_anc_bia_sweep_table'
    __parent__ = 'film'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to generate ancillary Bias sweep table report file.
    """

    def add_arguments(self, parser):
        # path to input L0 files
        parser.add_argument(
            '--l0-files',
            help="""
            List of input l0 files used to make output ANC Bias sweep table file.
            """,
            type=str,
            nargs='+',
            required=True,
        )

        # Existing anc_bia_sweep_table csv file containing previous sweep table data
        # (can be used to ensure the continuity of sweep table mapping)
        parser.add_argument(
            '--sweep-tables',
            help="""
            Existing anc_bia_sweep_table file containing previous sweep table data.
            (can be used to ensure the continuity of sweep table mapping
            or check if new data must be saved)
            """,
            type=str,
            nargs=1
        )

    def setup_tasks(self, pipeline):

        # Check if output dir already exists
        force = pipeline.get('force', default=False)
        output_dir = get_output_dir(pipeline)
        products_dir = get_products_dir(pipeline)
        if (is_output_dir(output_dir, products_dir=products_dir) and
                not force):
            # if yes exit
            logger.info(f'Input request has been already processed. (Use --force keyword to force execution)')
            pipeline.exit()

        # starting task
        start = L0ToAncBiaSweepTable()

        # create the tasks and their dependencies
        pipeline | start | MoveFailedFiles() | MoveToProdDir()

        # define the start points of the pipeline
        pipeline.start = start

        # Setup the lock file
        setup_lock(pipeline)


class L0ToL1BiaSweepCommand(Command):
    """
    Command to run the pipeline to generate Bias Sweep L1 CDF.
    """
    __command__ = 'film_l0_to_l1_bia_sweep'
    __command_name__ = 'l0_to_l1_bia_sweep'
    __parent__ = 'film'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to generate Bias sweep L1 CDF.
    """

    def add_arguments(self, parser):

        parser.add_argument(
            '--sweep-tables',
            help="""
            List of CSV file(s) containing Bias sweep table data.
            """,
            type=str,
            nargs='+',
            required=True,
        )

        # path to input L0 files
        parser.add_argument(
            '--l0-files',
            help="""
            List of input l0 files used to make output L1 Bias sweep CDF.
            """,
            type=str,
            nargs='+',
            required=True,
        )

    def setup_tasks(self, pipeline):

        # Check if output dir already exists
        force = pipeline.get('force', default=False)
        output_dir = get_output_dir(pipeline)
        products_dir = get_products_dir(pipeline)
        if (is_output_dir(output_dir, products_dir=products_dir) and
                not force):
            # if yes exit
            logger.info(f'Input request has been already processed. (Use --force keyword to force execution)')
            pipeline.exit()

        # starting task
        start = L0ToL1BiaSweep()

        # create the tasks workflow and their dependencies
        pipeline | start | MoveFailedFiles() | MoveToProdDir()

        # define the start points of the pipeline
        pipeline.start = start

        # Setup the lock file
        setup_lock(pipeline)


class L0ToL1BiaCurrentCommand(Command):
    """
    Command to run the pipeline to generate L1 Bias current CDF file
    """
    __command__ = 'film_l0_to_l1_bia_current'
    __command_name__ = 'l0_to_l1_bia_current'
    __parent__ = 'film'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to generate L1 Bias current CDF file.
    """

    def add_arguments(self, parser):
        # path to input L0 files
        parser.add_argument(
            '--l0-files',
            help="""
            List of input l0 files used to make output L1 Bias current CDF.
            """,
            type=str,
            nargs='+',
            required=True,
        )

    def setup_tasks(self, pipeline):

        # Check if output dir already exists
        force = pipeline.get('force', default=False)
        output_dir = get_output_dir(pipeline)
        products_dir = get_products_dir(pipeline)
        if (is_output_dir(output_dir, products_dir=products_dir) and
                not force):
            # if yes exit
            logger.info(f'Input request has been already processed. (Use --force keyword to force execution)')
            pipeline.exit()

        # starting task
        start = L0ToL1BiaCurrent()

        # create the tasks workflow and their dependencies
        pipeline | start | MoveFailedFiles() | MoveToProdDir()

        # define the start points of the pipeline
        pipeline.start = start

        # Setup the lock file
        setup_lock(pipeline)


class HkSktToXlsxCommand(Command):
    """
    Command to generate the skeleton files for HK parameters from the IDB.
    """
    __command__ = 'hk_skt_to_xlsx'
    __command_name__ = 'hk_skt_to_xlsx'
    __parent__ = 'film'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to generate the Excel files used to generate CDF skeleton for
        HK parameters.
    """

    def add_arguments(self, parser):
        # to read the path to the directory where to store the HK CDF skeletons
        # in Excel format
        parser.add_argument(
            '-d',
            '--directory',
            help="""
            The absolute path to the directory where to
            save the HK CDF skeletons in Excel format.
            """,
            type=str,
            default=osp.join(TEMP_DIR, 'hk_xls')
        )

        # path to XML file of the IDB
        parser.add_argument(
            '-i',
            '--idb',
            help="""
            Path to the RPW IDB main directory.
            """,
            type=str,
        )

        # path to the mapping of parameters and packets to the SRDB
        parser.add_argument(
            '-m',
            '--mapping',
            help="""
            Path to the XML file containing the mapping of parameters and
            packets to the SRDB.
            """,
            type=str,
        )

        # path to the configuration file for the generation
        parser.add_argument(
            '-s',
            '--skeleton-configuration',
            help="""
            Path to the JSON configuration file of the skeleton command, for
            packets selection and structure.
            """,
            type=str,
            default=paths.from_config('hk_metadef.json'),
        )

        # path to the HK CDF Excel template file
        parser.add_argument(
            'hk_template_file',
            help="""
            Path to the HK CDF Excel template file.
            """,
            type=str,
        )

    def setup_tasks(self, pipeline):
        """
        Execute the generation of the excel files allowing the creation of the
        skeleton for CDF files of ROC data products.
        """
        # create the class managing the conversion
        converter = IDBToExcel(pipeline.args)

        # convert the IDB
        converter()


class CdfPostProCommand(Command):
    """
    Command to run the pipeline to generate ancillary Bias Sweep table file
    """
    __command__ = 'film_cdf_post_pro'
    __command_name__ = 'cdf_post_pro'
    __parent__ = 'film'
    __parent_arguments__ = ['base']
    __help__ = """
        Command to perform post-processing in the set of input RPW CDF files.
    """

    def add_arguments(self, parser):

        parser.add_argument(
            '--cdf-files',
            help="""
            List of input RPW CDF files to post-process.
            """,
            type=str,
            nargs='+',
            required=True,
        )

        parser.add_argument(
            '--rpw-obs-json',
            help="""
            List of RPW SoopKitchen export JSON files.
            """,
            type=str,
            nargs='+',
        )

        parser.add_argument(
            '--rpw-ior-xml',
            help="""
            List of RPW IOR XML files (ZIP archive can be also passed).
            """,
            type=str,
            nargs='+',
        )

        parser.add_argument(
            '--options',
            help=f"""
            List of post-processing jobs to run.
            Available options are: {CDF_POST_PRO_OPTS_ARGS} .
            """,
            type=str,
            nargs='+',
            required=True,
        )

        parser.add_argument(
            '--update-json',
            help='JSON file containing updates to be performed '
                 'on input CDF files. '
                 '(Only works with "update_cdf" option)',
            type=str,
            nargs=1,
            default=[None],
        )

        parser.add_argument(
            '--cdfexport',
            help="""
            Path to the cdfexport executable.
            """,
            type=str,
            nargs=1,
            default=[CDFEXPORT_PATH],
        )

    def setup_tasks(self, pipeline):
        """
        Execute the RPW CDF post-processing.
        """

        # Check if output dir already exists
        force = pipeline.get('force', default=False)
        output_dir = get_output_dir(pipeline)
        products_dir = get_products_dir(pipeline)
        if (is_output_dir(output_dir, products_dir=products_dir) and
                not force):
            # if yes exit
            logger.info(f'Input request has been already processed. (Use --force keyword to force execution)')
            pipeline.exit()

        # starting task
        start = CdfPostPro()

        # create the tasks workflow and their dependencies
        pipeline | start | MoveFailedFiles() | MoveToProdDir()

        # define the start points of the pipeline
        pipeline.start = start

        # Setup the lock file
        setup_lock(pipeline)
