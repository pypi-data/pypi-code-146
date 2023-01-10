import collections
import gc
import json
import os
import typing
from datetime import datetime

from remotemanager.storage.remotefunction import cached_functions
from remotemanager.connection.url import URL
from remotemanager.storage.database import Database
from remotemanager.storage.function import Function
from remotemanager.dataset.runner import Runner, localwinerror
import remotemanager.transport as tp
import remotemanager.serialisation as sr
from remotemanager.storage import SendableMixin, TrackedFile
from remotemanager.utils.uuid import generate_uuid
from remotemanager.utils import ensure_list, ensure_filetype
from remotemanager.logging.utils import format_iterable
from remotemanager.dataset.dependency import Dependency
from remotemanager.logging import LoggingMixin
from remotemanager.logging.verbosity import Verbosity


class Dataset(SendableMixin, LoggingMixin):
    """
    Bulk holder for remote runs. The Dataset class handles anything regarding
    the runs as a group. Running, retrieving results, sending to remote, etc.

    Args:
        function (Callable):
            function to run
        url (URL):
            connection to remote (optional)
        transport (tp.transport.Transport):
            transport system to use, if a specific is required. Defaults to
            transport.rsync
        serialiser (serial.serial):
            serialisation system to use, if a specific is required. Defaults
            to serial.serialjson
        script (str):
            callscript required to run the jobs in this dataset
        submitter (str):
            command to exec any scripts with. Defaults to "bash"
        name (str):
            optional name for this dataset. Will be used for runscripts
        extra_files_send(list, str):
            extra files to send with this run
        extra_files_recv(list, str):
            extra files to retrieve with this run
        global_run_args:
            any further (unchanging) arguments to be passed to the runner(s)
    """

    # DEV NOTE: arguments must be None for computer-url override to function
    def __init__(self,
                 function: typing.Callable,
                 url: URL = None,
                 dbfile: str = None,
                 transport: tp.transport.Transport = None,
                 serialiser: sr.serial = None,
                 script: str = None,
                 submitter: str = None,
                 name: str = None,
                 block_reinit: bool = False,
                 extra_files_send: list = None,
                 extra_files_recv: list = None,
                 verbose: int = None,
                 **global_run_args):
        self._verbose = Verbosity(verbose)

        self._logger.info('dataset initialised')

        self._function = Function(function)

        self._global_run_args = {'skip': True}
        if ' ' in global_run_args.get('remote_dir', ''):
            raise ValueError(f'Space character detected in remote_dir')
        if ' ' in global_run_args.get('run_dir', ''):
            raise ValueError(f'Space character detected in run_dir')
        if ' ' in os.path.abspath(global_run_args.get('local_dir', '')):
            raise ValueError(f'Space character detected in local_dir')
        self._global_run_args.update(global_run_args)

        # dataset uuid is equal to Function uuid for now
        self._name = name or 'dataset'
        self._uuid = generate_uuid(self._function.uuid + self.name)
        self._logger.info(f'shortened uuid is {self.short_uuid}')

        self._script = script or '#!/bin/bash'
        self._submitter = submitter or 'bash'
        self._extra_files = {'send': ensure_list(extra_files_send)
                             if extra_files_send is not None else [],
                             'recv': ensure_list(extra_files_recv)
                             if extra_files_recv is not None else []}

        self._url = None
        self._transport = None
        self._computer = False
        self._serialiser = None
        self._dbfile_override = dbfile
        self._dependency = None
        self._do_not_recurse = False

        self.url = url
        self.transport = transport
        self.serialiser = serialiser

        if block_reinit:
            try:
                os.remove(self.dbfile)
                self._logger.warning(f'deleted database file {self.dbfile}',
                                     silent=True)
            except FileNotFoundError:
                pass

        self._run_cmds = []
        if os.path.isfile(self.dbfile):
            self._logger.info(f'unpacking database from {self.dbfile}')

            # create a "temporary" database from the found file
            self._database = Database(self.dbfile)
            # update it with any new values
            self.database.update(self.pack())
            # unpack from here to retrieve
            payload = self.database._storage[self.uuid]
            self.inject_payload(payload)

        else:
            self._runs = collections.OrderedDict()
            self._uuids = []
            self._results = []

            # database property creates the database if it does not exist
            self.database.update(self.pack())

        self._logger.info(f'Dataset {self.name} init complete')

    def __hash__(self) -> int:
        return hash(self.uuid)

    def __getattribute__(self, item):
        """
        Redirect Dataset.attribute calls to _global_run_args if possible.
        Allows for run global_run_args to be kept seperate

        Args:
            item:
                attribute to fetch
        """
        # TODO: keep an eye on this, it's hacky and liable to break
        try:  # attempt to get item from self
            return object.__getattribute__(self, item)
        except AttributeError:  # if not found, check the run arguments
            # print('falling back on _global_run_args for', item)
            if item != '_global_run_args' and \
                    hasattr(self, '_global_run_args'):
                try:
                    return self._global_run_args[item]
                except:  # noqa E772
                    # if it's not in the run args anyway, go back
                    # to original behaviour for proper flow
                    return object.__getattribute__(self, item)

    def __delattr__(self, item):
        """
        As with __getattribute__, redirect del to global_run_args if possible.

        Args:
            item:
                attribute to delete
        """
        try:
            return object.__delattr__(self, item)
        except AttributeError:
            # print('falling back on _global_run_args for', item)
            if item != '_global_run_args' and \
                    hasattr(self, '_global_run_args'):
                del self._global_run_args[str(item)]

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.uuid == other.uuid

    def __repr__(self):
        return f'dataset-{self.name}-{self.short_uuid}'

    @classmethod
    def recreate(cls,
                 raise_if_not_found: bool = False,
                 *args,
                 **kwargs):
        """
        Attempts to extract a dataset matching the given args from the python
        garbage collection interface

        Args:
            raise_if_not_found (bool):
                raise ValueError if the Dataset was not found
            *args:
                args as passed to Dataset
            **kwargs:
                keyword args as passed to Dataset
        Returns:
            Dataset
        """

        for obj in gc.get_objects():
            if type(obj) == cls:

                tmp = cls(*args, **kwargs)
                if obj == tmp:
                    print('returning stored obj')
                    return obj

        if raise_if_not_found:
            raise ValueError('Dataset with args not found!')

        return cls(*args, **kwargs)

    @property
    def verbose(self):
        return self._verbose

    @property
    def database(self):
        """
        Access to the stored database object.
        Creates a connection if none exist.

        Returns (Database):
            Database
        """
        if self.is_missing('_database'):
            self._database = Database(file=self.dbfile)
        return self._database

    @property
    def dbfile(self) -> str:
        """
        Name of the database file
        """
        if self._dbfile_override is not None:
            return ensure_filetype(self._dbfile_override, 'yaml')
        if self.name == 'dataset':
            return ensure_filetype(f'{self.name}-{self.short_uuid}',
                                   'yaml')
        return ensure_filetype(f'dataset-{self.name}-{self.short_uuid}',
                               'yaml')

    @property
    def remote_dir(self) -> [str, bool]:
        """
        Accesses the remote_dir property from the run args. Tries to fall back
        on run_dir if not found, then returns default as a last resort.
        """
        remote = self.global_run_args.get('remote_dir', False)
        if not remote:
            return self.global_run_args.get('run_dir',
                                            Runner._default_remote_dir)
        return remote

    @property
    def local_dir(self):
        """
        Accesses the local_dir property from the run args. Returns default if
        not found.
        """
        return self.global_run_args.get('local_dir', Runner._default_local_dir)

    @property
    def repofile(self):
        return f'{self.name}-{self.short_uuid}-repo'

    @property
    def master_script(self):
        return f'{self.name}-{self.short_uuid}-master.sh'

    @property
    def argfile(self):
        return f'args-{self.name}-{self.short_uuid}'

    @property
    def do_not_recurse(self):
        self._do_not_recurse = False
        return True

    @property
    def dependency(self):
        return self._dependency

    @property
    def is_child(self):
        if self.dependency is None:
            return False
        return self.short_uuid in self.dependency._children

    @property
    def is_parent(self):
        if self.dependency is None:
            return False
        return self.short_uuid in self.dependency._parents

    def _mirror_dependency(self, dataset):

        self._logger.info(f'connecting with dataset {dataset}')
        if dataset.dependency is not None:
            self._logger.info('target has dependency, joining')
            self._dependency = dataset.dependency
        elif self.dependency is not None:
            self._logger.info('self has dependency, joining')
            dataset._dependency = self._dependency
        else:
            self._logger.info('creating a dependency and entering')
            self._dependency = Dependency()
            dataset._dependency = self.dependency

        self.database.update(self.pack())

    def set_downstream(self, dataset):
        self._mirror_dependency(dataset)

        self.dependency.add_edge(self, dataset)

        if not dataset.do_not_recurse:
            dataset._do_not_recurse = True
            dataset.set_upstream(self)

    def set_upstream(self, dataset):
        self._mirror_dependency(dataset)

        self.dependency.add_edge(dataset, self)

        if not dataset.do_not_recurse:
            dataset._do_not_recurse = True
            dataset.set_downstream(self)

    def pack(self, **kwargs):
        """
        Override for the SendableMixin.pack() method, ensuring the dataset is
        always below a uuid

        Args:
            **kwargs:
                Any arguments to be passed onwards to the SendableMixin.pack()

        Returns:
            None
        """
        if len(kwargs) == 0:
            self._logger.info('Dataset override pack called')
        else:
            self._logger.info('Data override pack called with kwargs')
            self._logger.info(f'{format_iterable(kwargs)}')
        return super().pack(uuid=self._uuid, **kwargs)

    def set_run_option(self, key, val):
        """
        Update a global run option `key` with value `val`

        Args:
            key (str):
                option to be updated
            val:
                value to set
        """
        self._global_run_args[key] = val

    def append_run(self,
                   args=None,
                   arguments=None,
                   name=None,
                   extra_files_send: list = None,
                   extra_files_recv: list = None,
                   dependency_call: bool = False,
                   verbose: int = None,
                   **run_args):
        """
        Serialise arguments for later runner construction

        Args:
            args (dict):
                dictionary of arguments to be unpacked
            arguments (dict):
                alias for args
            name (str):
                 append a runner under this name
            extra_files_send (list, str):
                extra files to send with this run
            extra_files_recv (list, str):
                extra files to retrieve with this run
            dependency_call (bool):
                True if called via the dependency handler
            verbose (int, Verbose, None):
                verbose level for this runner (defaults to Dataset level)
            run_args:
                any extra arguments to pass to runner
        """
        if args is None and arguments is not None:
            args = arguments

        if verbose is None:
            verbose = self.verbose.value

        if self.dependency is not None and not dependency_call:
            return self.dependency.append_run(self,
                                              args=args,
                                              name=name,
                                              extra_files_send=  # noqa: E251
                                              extra_files_send,
                                              extra_files_recv=  # noqa: E251
                                              extra_files_recv,
                                              verbose=verbose,
                                              **run_args)

        # first grab global arguments and update them with explicit args
        run_arguments = {k: v for k, v in self._global_run_args.items()}
        run_arguments.update(run_args)

        extra_files_send = ensure_list(extra_files_send) + \
            self._extra_files['send']

        extra_files_recv = ensure_list(extra_files_recv) + \
            self._extra_files['recv']

        # test if the object can be sent by base serialisation methods using
        # json.dumps
        # if not, attempt to use the stored serialiser
        rnum = len(self.runners)
        try:
            json.dumps(args)
        except TypeError:
            file = f'{self.argfile}-{rnum}{self.serialiser.extension}'
            lpath = os.path.join(self.local_dir, file)
            # rpath = os.path.join(self.remote_dir, file)

            if not os.path.isdir(self.local_dir):
                os.makedirs(self.local_dir)

            self.serialiser.dump(args, lpath)

            uuid_base = format_iterable(args)
            args = {file: Runner._args_replaced_key,
                    'uuid_base': uuid_base}

            extra_files_send.append(lpath)

        if name is not None:
            run_arguments['name'] = name
            r_id = name

            if name in self.runner_dict:
                self._logger.warning(f'{self} overwriting already '
                                     f'existing runner {r_id}')
        else:
            r_id = f'runner-{rnum}'

        tmp = Runner(arguments=args,
                     dbfile=self.dbfile,
                     parent=self,
                     self_id=r_id,
                     extra_files_send=extra_files_send,
                     extra_files_recv=extra_files_recv,
                     verbose=verbose,
                     **run_arguments)

        tmp.result_extension = self.serialiser.extension

        if tmp.uuid not in self._uuids:
            self._runs[r_id] = tmp
            self._uuids.append(tmp.uuid)
            self._logger.important(f'appended run {tmp.name}')
        else:
            self._logger.important(f'runner {tmp.name} already exists')

        self.database.update(self.pack())

    def remove_run(self,
                   id):
        """
        Remove a runner with the given identifier. Search methods are identical
        get_runner(id)

        Args:
            id:
                identifier

        Returns:
            (bool): True if succeeded
        """
        try:
            runner = self.get_runner(id)

            if runner is None:
                self._logger.info(f'could not find runner to remove')
                return False

            del self._runs[runner.id]
            self._uuids.remove(runner.uuid)

            self._logger.important(f'removed runner {runner}')

            # need to override attribute first, as updating can only add
            self.database._storage[self.uuid]['_runs'] = {}
            self.database.update(self.pack())

            return True

        except (KeyError, ValueError):
            self._logger.info(f'could not remove runner')

            return False

    def get_runner(self,
                   id):
        """
        Collect a runner with the given identifier. Depending on the type of
        arg passed, there are different search methods:

        - int: the runners[id] of the runner to remove
        - str: searches for a runner with the matching uuid
        - dict: attempts to find a runner with matching args

        Args:
            id:
                identifier

        Returns:
            (Runner): collected Runner, None if not available
        """

        def get_by_id(id):
            self._logger.info(f'getting runner by id {id}')
            try:
                key = list(self.runner_dict.keys())[id]
                return self.runner_dict[key]
            except IndexError:
                return

        def get_by_str(id):
            self._logger.info(f'getting runner by string "{id}"')

            if id.lower() in self.runner_dict:
                return self.runner_dict[id.lower()]

            for r_id, r in self.runner_dict.items():
                if len(id) == 64 and r.uuid == id:
                    self._logger.info(f'full uuid')
                    return r
                elif len(id) == 8 and r.short_uuid == id:
                    self._logger.info(f'short uuid')
                    return r

        def get_by_dict(id):
            self._logger.info(f'getting runner by args {id}')
            for r_id, r in self.runner_dict.items():
                if format_iterable(r.args) == format_iterable(id):
                    return r

        dispatch = {int: get_by_id,
                    str: get_by_str,
                    dict: get_by_dict}

        return dispatch.get(type(id))(id)

    def clear_runs(self):
        """
        Wipes all runners
        """
        self._logger.info('wiping all runners and updating the db')

        self._uuids = []
        self._runs = {}

        self.database._storage[self.uuid]['_runs'] = {}
        self.database.update(self.pack())

    @property
    def runner_dict(self):
        """
        Stored runners in dict form, where the keys are the append id
        """
        return dict(self._runs)

    @property
    def runners(self):
        """
        Stored runners as a list
        """
        return list(self.runner_dict.values())

    @property
    def function(self):
        """
        Currently stored Function wrapper
        """
        return self._function

    @property
    def global_run_args(self):
        """
        Global run args to be passed to runners by default.

        "Fakes" attributes added to dataset after init by adding anything that
        does not exist within the base Dataset (ignoring private vars)
        """
        out = {}
        for k, v in self.__dict__.items():
            if k not in Dataset.__dict__ and not k.startswith(('_', '~')):
                out[k] = v
        out.update(self._global_run_args)
        return out

    def _script_sub(self,
                    **sub_args):
        """
        Substitutes run argmuents into the computer script, if it exists

        Args:
            **sub_args:
                jobscript arguments

        Returns:
            (str):
            jobscript
        """
        if not self._computer:
            return self._script
        if 'name' not in sub_args:
            sub_args['name'] = self.name
        return self.url.script(**sub_args)

    @property
    def script(self,
               **sub_args):
        """
        Currently stored run script

        Args:
            sub_args:
                arguments to substitute into the script() method
        """
        sub_args.update(self.global_run_args)
        return self._script_sub(**sub_args)

    @script.setter
    def script(self, script: str) -> None:
        """
        Set the run script
        """
        self._script = script

    @property
    def submitter(self):
        """
        Currently stored submission command
        """
        return self._submitter

    @submitter.setter
    def submitter(self, submitter):
        """
        Set the submission command
        """
        self._submitter = submitter

    @property
    def url(self) -> URL:
        """
        Currently stored URL object
        """
        if not hasattr(self, '_url'):
            self.url = None
        return self._url

    @url.setter
    def url(self, url=None):
        """
        Verifies and sets the URL to be used.
        Will create an empty (local) url connection if url is None

        Args:
            url (URL):
                url to be verified
        """
        self._logger.info(f'new url is being set to {url}')
        if url is None:
            self._logger.info('no URL specified for this dataset, creating '
                              'localhost')
            self._url = URL(verbose=self.verbose)
        else:
            if not isinstance(url, URL):
                raise ValueError('URL is not a valid URL instance')
            self._url = url

        if not type(url) == URL and issubclass(type(url), URL):
            try:
                self.submitter = url.submitter
            except AttributeError:
                pass
            self._computer = True

        timeout = self._global_run_args.get('timeout', None)
        max_timeouts = self._global_run_args.get('max_timeouts', None)

        self._url.timeout = timeout
        self._url.max_timeouts = max_timeouts

    @property
    def transport(self):
        """
        Currently stored Transport system
        """
        if not hasattr(self, '_transport'):
            self.transport = None
        return self._transport

    @transport.setter
    def transport(self,
                  transport: tp.transport.Transport = None):
        """
        Verifies and sets the Transport to be used.
        Will use rsync if transport is None

        Args:
            transport (Transport):
                transport to be verified
        """
        if transport is None:
            self._logger.info('no transport specified for this dataset, '
                              'creating basic rsync')
            self._transport = tp.rsync(self.url)
        else:
            if not isinstance(transport, tp.transport.Transport):
                raise ValueError('transport is not a valid transport instance')
            self._transport = transport

        self._transport.set_remote(self.url)

    @property
    def serialiser(self):
        if not hasattr(self, '_serialiser'):
            self.serialiser = None
        return self._serialiser

    @serialiser.setter
    def serialiser(self, serialiser: sr.serial.serial = None):
        """
        Verifies and sets the serialiser to be used.
        Will use serialjson if serialiser is None

        Args:
            serialiser (serialiser):
                serialiser to be verified
        """
        if serialiser is None:
            self._logger.info('no serialiser specified,'
                              'creating basic json')
            self._serialiser = sr.serialjson()

        else:
            if not isinstance(serialiser, sr.serial.serial):
                raise ValueError('serialiser is not a valid serial instance')
            self._serialiser = serialiser

    @property
    def extra_files(self) -> dict:
        """
        Extra files to send and recieve
        """
        return self._extra_files

    def remove_database(self):
        """
        Deletes the database file
        """
        os.remove(self.dbfile)

    @property
    def name(self) -> str:
        """
        Name of this dataset
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """
        Sets the dataset name
        """
        if not isinstance(name, str):
            try:
                name = str(name)
            except TypeError:
                raise ValueError('name can only be str type')

        self._name = name

    @property
    def uuid(self) -> str:
        """
        This Dataset's full uuid (64 characcter)
        """
        return self._uuid

    @property
    def short_uuid(self) -> str:
        """
        This Dataset's short format (8 character) uuid
        """
        return self._uuid[:8]

    def set_runner_states(self, state: str, uuids: list = None):
        """
        Update runner states to `state`

        Args:
            (str) state:
                state to set
            (list) uuids:
                list of uuids to update, updates all if not passed
        """
        self._logger.info('updating runner states')
        if uuids is not None:
            self._logger.info(f'using uuid list: {uuids}')
            for runner in self.runners:
                if runner.uuid in uuids:
                    runner.state = state

            return

        for runner in self.runners:
            runner.state = state

    def get_all_runner_states(self) -> list:
        """
        Check all runner states, returning a list

        Returns (list):
            states
        """
        return [r.state for r in self.runners]

    def check_all_runner_states(self, state: str) -> bool:
        """
        Check all runner states against `state`, returning True if `all`
        runners have this state

        Args:
            state (str):
                state to check for

        Returns (bool):
            all(states)
        """
        return all([r == state for r in self.get_all_runner_states()])

    def run(self,
            force: bool = False,
            dry_run: bool = False,
            **run_args):
        """
        Run the functions

        Args:
            force (bool):
                force all runs to go through, ignoring checks
            dry_run (bool):
                create files, but do not run
            run_args:
                any arguments to pass to the runners during this run.
                will override any "global" arguments set at Dataset init
        """
        if os.name == 'nt' and self.url.is_local:
            raise RuntimeError(localwinerror)
        if self.is_parent:
            self._logger.warning(f'dataset {self} is a parent, '
                                 f'skipping run')
            return

        if self.dependency:
            self._logger.runtime(f'dataset {self} is a part of a dependency '
                                 f'chain, calling from there')
            self.dependency.run(force,
                                dry_run,
                                **run_args)
            return

        self._run(force,
                  dry_run,
                  **run_args)

    def _run(self,
             force: bool = False,
             dry_run: bool = False,
             **run_args):
        """
        Seperation of run and _run allows for dependency runs. Any
        functionality intended for run that does not interact with
        dependencies should be placed here
        """
        self._run_cmds = []
        # initial run args
        temp_args = {'force': force}
        temp_args.update(run_args)

        runners_to_update = []
        master_scripts = {}
        any_file_written = False
        asynchronous = None
        for runner in self.runners:
            if not runner._assess_run(**temp_args):
                continue

            runner.state = Runner._submit_status['initial']
            written = runner._write_runfile(self)
            if not written:
                # runner skipped, move onto the next one
                continue
            any_file_written = True

            self._logger.info('writing script with run args:')
            self._logger.info(format_iterable(runner.run_args))
            runner._write_script(self.url.python,
                                 self._script_sub(**runner.run_args))

            self.transport.queue_for_push([runner.jobscript.name,
                                           runner.runfile],
                                          runner.local_dir,
                                          runner.remote_dir)

            runline = f'{self.submitter} {runner.jobscript.name}'

            asynchronous = runner.run_option('asynchronous', True)
            if asynchronous and self.submitter == 'bash':
                self._logger.debug('appending "&" for async run')
                runline += ' &'

            if runner.remote_dir not in master_scripts:
                master_scripts[runner.remote_dir] = []
            master_scripts[runner.remote_dir].append(runline)

            for file in runner.extra_files["send"]:
                self.transport.queue_for_push(os.path.split(file)[1],
                                              os.path.split(file)[0],
                                              runner.remote_dir)

            runners_to_update.append(runner.uuid)

        if not any_file_written:
            self._run_finalise()

        cmds = []
        i = 0
        for remote, lines in master_scripts.items():
            scriptname = f'{i}-{self.master_script}'
            i += 1
            _scriptfile = os.path.join(runner.local_dir,
                                       scriptname)
            # newline='\n' is required to stop windows clients adding the \r\n
            with open(_scriptfile, 'w+', newline='\n') as o:
                o.write('\n'.join(lines))
            self.transport.queue_for_push(scriptname,
                                          self.local_dir,
                                          remote)
            cmd = f'cd {remote} && bash {scriptname}'
            cmds.append(cmd)

            # send a repo for each new remote dir
            # TODO this should ideally be reduced to just _one_
            self._write_to_repo(self.local_dir, remote)

        if not dry_run:
            self.transport.transfer()
            self.set_runner_states('files copied to remote',
                                   runners_to_update)
            for cmd in cmds:
                self._run_cmds.append(
                    self.url.cmd(cmd, asynchronous=asynchronous))
            self.set_runner_states(Runner._submit_status['final'],
                                   runners_to_update)
        else:
            self.transport.wipe_transfers()
            for cmd in cmds:
                self._logger.important(f'launch command: {cmd}')
            self.set_runner_states('dry run',
                                   runners_to_update)

        self._run_finalise()

    def _run_finalise(self):
        self.database.update(self.pack())

    def _write_to_repo(self,
                       local=None,
                       remote=None):
        """
        Writes the function to a "repo" file which can be imported from
        """
        if local is None:
            local = self.local_dir
        if remote is None:
            remote = self.remote_dir

        repo = TrackedFile(local, remote, self.repofile + '.py')

        if not os.path.isdir(repo.local_dir):
            os.makedirs(repo.local_dir)

        with open(repo.local, 'w+') as o:
            if len(cached_functions) > 0:
                o.write('### cached functions ###\n')

                for fname, f in cached_functions.items():
                    o.write(f.source + '\n')
                o.write('\n')

            if self.is_parent:
                o.write('### dependency functions ###\n')

                o.write("""
def submit_child(file):
    import subprocess
    subprocess.Popen(f"bash '{file}'",
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     shell=True,
                     universal_newlines=True)
\n""")

                o.write('\n')

            o.write('### primary function ###\n')
            o.write(self.function.source)

            o.write('\n### serialiser functions ###')
            o.write(self.serialiser.dumpfunc())
            o.write('\n')
            o.write(self.serialiser.loadfunc())

        self.transport.queue_for_push(repo.name,
                                      repo.local_dir,
                                      repo.remote_dir)

    @property
    def run_cmds(self) -> list:
        """
        Access to the storage of CMD objects used to run the scripts

        Returns:
            (list): List of CMD objects
        """
        return self._run_cmds

    def _check_for_resultfiles(self) -> dict:
        """
        Checks for the runfiles dictated by the runners
        """
        self._logger.important('checking remotely for finished runs')
        files_to_check = []
        for runner in self.runners:
            files_to_check.append(runner.resultpath())

        return self.url.utils.file_mtime(files_to_check)

    def fetch_results(self,
                      raise_if_not_finished: bool = False,
                      ignore_errors: bool = False) -> None:
        """
        Collect any scripted run resultfiles and insert them into their runners

        Args:
            raise_if_not_finished (bool):
                raise an error if all calculations not finished
            ignore_errors (bool):
                will ignore any raised errors if True

        Returns:
            None
        """
        if not ignore_errors:
            self._check_run_errors()

        present_runfiles = self._check_for_resultfiles()

        if not any(present_runfiles.values()):
            self._logger.info('no valid results found, exiting early')
            return

        self._logger.info('present result files:')
        self._logger.info(format_iterable(present_runfiles))
        for runner in self.runners:
            if present_runfiles[runner.resultpath()]:
                self.transport.queue_for_pull(os.path.split(
                                              runner.resultpath())[1],
                                              runner.local_dir,
                                              os.path.split(
                                                  runner.resultpath())[0])

                for file in runner.extra_files['recv']:
                    rmt = runner.run_dir if runner.run_dir is not None \
                        else runner.remote_dir
                    remote = os.path.join(rmt, os.path.split(file)[0])
                    self.transport.queue_for_pull(os.path.split(file)[1],
                                                  runner.local_dir,
                                                  remote)

        self._logger.info('pulling completed result files')
        self.transport.transfer()
        for runner in self.runners:
            if present_runfiles[runner.resultpath()]:
                pulled = runner.resultpath(local=True)

                result = self.serialiser.load(pulled)

                timestamp = int(os.path.getmtime(pulled))

                if timestamp < runner.last_updated \
                        and not runner.is_finished:
                    self._logger.warning(f'{runner}: '
                                         f'calculation not completed yet')
                    continue

                mtime = datetime.fromtimestamp(timestamp)
                runner.insert_history(mtime, 'resultfile created remotely')

                runner.result = result

        self.database.update(self.pack())

        if not all(self._is_finished(present_runfiles)) \
                and raise_if_not_finished:
            raise RuntimeError('Calculations not yet completed!')

    def _check_run_errors(self):
        errs = [c.stderr for c in self._run_cmds
                if c.stderr is not None and c.stderr != '']

        if len(errs) == 0:
            self._logger.info('no errors found at run')
            return

        print(f'There are {len(errs)} errors, printing:')
        for error in errs:
            self._logger.error(error)
            print(f'stderr from run call:\n{error}')

        from remotemanager import Logger
        raise RuntimeError('There was an issue during running. '
                           f'See printed info or logfile at {Logger.path}')

    @property
    def is_finished(self) -> list:
        return self._is_finished()

    def _is_finished(self,
                     files: dict = None) -> list:
        """
        Check if the runners have finished

        Args:
            files (dict):
                will use this dict of files instead of rechecking if passed

        Returns (list):
            boolean list corresponding to the Runner order
        """
        ret = {r.uuid: None for r in self.runners}
        if self.skip:
            self._logger.info('skip is true, checking runner first')
            for runner in self.runners:
                if runner.is_finished:
                    ret[runner.uuid] = True

        if files is None:
            self._logger.runtime('checking for files')
            # look for the resultfiles
            files = self._check_for_resultfiles()

        # create a list of the resultfiles that are available
        for runner in self.runners:
            if ret[runner.uuid] is not None:
                continue

            resultpath = runner.resultpath()
            last_submitted = runner.last_submitted
            mtime = files[resultpath]

            if mtime is None:
                ret[runner.uuid] = False
            elif mtime >= last_submitted:
                ret[runner.uuid] = True
            else:
                ret[runner.uuid] = False

            self._logger.debug(f'checking file {resultpath}. mtime '
                               f'{mtime} vs runner submit time '
                               f'{last_submitted} -> {ret[runner.uuid]}')

        return list(ret.values())

    @property
    def all_finished(self) -> bool:
        """
        Check if `all` runners have finished

        Returns (bool):
            True if all runners have completed their runs
        """
        return all(self.is_finished)

    @property
    def results(self) -> list:
        """
        Access the results of the runners

        Returns (list):
            runner.result for each runner
        """
        return [r.result for r in self.runners]

    def clear_results(self):
        """
        Remove any results from the stored runners and attempt to delete their
        result files.

        .. warning::
            This is a potentially destructive action, be careful with this
            method
        """
        for runner in self.runners:
            runner.clear_result()
