from functools import lru_cache
import os
import shutil
import time
from typing import Iterable

import dash
from dash.exceptions import PreventUpdate
from dash.long_callback import DiskcacheLongCallbackManager
import dash_bootstrap_components as dbc
import diskcache

from truera.rnn.general.container import ArtifactsContainer
from truera.rnn.general.service.container import Locator
from truera.rnn.general.utils import log
from truera.rnn.general.utils.types import to_iterable
from truera.rnn.general.utils.types import to_list

from .component import Component

FONT_AWESOME_CSS = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css'


class App(dash.Dash):

    def __init__(
        self,
        project="toy_project",
        figures=None,
        sync_client=None,
        setup_path="/rnn/",
        callback_cache_path="./callback_cache_path"
    ):

        dash.Dash.__init__(
            self,
            __name__,
            external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_AWESOME_CSS],
            url_base_pathname=setup_path
        )

        log.info(f"Dash version = {dash.__version__}")

        self.config['suppress_callback_exceptions'] = True
        self.viz = figures
        self.viz.set_href_path(setup_path)
        self.sync_client = sync_client
        self.default_project = project

        # Note: Production grade systems should use Celery/Redis, or move to React.
        if os.path.exists(callback_cache_path):
            shutil.rmtree(callback_cache_path)
        os.makedirs(callback_cache_path, exist_ok=True)
        callback_cache = diskcache.Cache(callback_cache_path)
        self.long_callback_manager = DiskcacheLongCallbackManager(
            callback_cache
        )

    def get_artifacts_container(
        self,
        project: str,
        model: str,
        data_collection: str,
        split: str,
        debug=False
    ) -> ArtifactsContainer:

        def get_ttl_hash(seconds=30):
            """Return the same value within `seconds` time period"""
            return round(time.time() / seconds)

        return self.get_artifacts_container_with_ttl_cache(
            project,
            model,
            data_collection,
            split,
            debug,
            ttl_hash=get_ttl_hash()
        )

    @lru_cache(maxsize=128)
    def get_artifacts_container_with_ttl_cache(
        self,
        project: str,
        model: str,
        data_collection: str,
        split: str,
        debug: bool = False,
        ttl_hash: int = None
    ) -> ArtifactsContainer:

        try:
            artifacts_container = ArtifactsContainer(
                self.sync_client.sync_service,
                Locator.Artifact(project, model, data_collection, split)
            )
            if debug:
                log.debug(f"container = {artifacts_container}")

            if os.path.isdir(artifacts_container.get_path()):
                return artifacts_container

            else:
                if debug:
                    log.debug(
                        f"could not get artifact: {artifacts_container.get_path()} is not a directory"
                    )
                raise PreventUpdate

        except Exception as e:
            if debug:
                log.debug(f"could not get artifact\n{str(e)}")
            raise PreventUpdate

    def component_callback(
        self,
        output=[],
        inputs=[],
        state=[],
        debug=False,
        long_callback=False,
        running=[],
        cancel=[]
    ):
        '''
        A callback that can process Component types as valid operable elements. 
        Components are structured dash elements that can be customly designed.
        '''
        multiple = isinstance(output, (list, tuple))

        output = to_list(output)

        parts_expanded = Component.expand_callback(inputs, output, state)

        if debug:
            log.debug(f"inputs expanded")
            for i in parts_expanded['inputs']:
                log.debug("\t" + str(i))

        def wrap_func(method):
            if debug:
                log.debug(f"registering {method}")
                log.debug(f"inputs")
                for i in inputs:
                    log.debug("\t" + str(i))
                log.debug(f"output:")
                for i in output:
                    log.debug("\t" + str(i))
                log.debug(f"state:")
                for i in state:
                    log.debug("\t" + str(i))

            def add_context(*args, **kwargs):
                if debug:
                    log.debug("args:")
                    for a in args:
                        log.debug("\t" + str(a))

                args_collapsed = Component.collapse_args(inputs + state, args)

                if debug:
                    log.debug(f"args collapsed:")
                    for i in args_collapsed:
                        log.debug("\t" + str(i))

                outs = method(*args_collapsed, **kwargs)

                if debug:
                    log.debug(f"outs:")
                    for i in outs:
                        log.debug("\t" + str(i))

                outs_expanded = Component.expand_outputs(
                    outs, multiple=multiple
                )

                if debug:
                    log.debug(f"outs expanded:")
                    for i in outs_expanded:
                        log.debug("\t" + str(i))

                return outs_expanded

            if long_callback:
                parts_expanded['manager'] = self.long_callback_manager
                parts_expanded['running'] = running
                parts_expanded['cancel'] = cancel
                dash.Dash.long_callback(self, **parts_expanded)(add_context)
            else:
                dash.Dash.callback(self, **parts_expanded)(add_context)

            return add_context

        return wrap_func

    @classmethod
    def update_selection_of_updated_options(
        cls, options, selection, default=None
    ):
        available = [entry_dict['value'] for entry_dict in options]

        if selection in available:
            raise PreventUpdate

        if default is not None and default in available:
            return [default]

        selection = sorted(available)[0] if len(available) > 0 else None

        return [selection]
