import logging
from typing import Dict, List, Optional, Set

from katatachi.content import ContentStore

from .pipeline_mod_view import PipelineModView
from .pipeline_state import PipelineState
from .pipeline_worker import PipelineWorker


logger = logging.getLogger(__name__)


class Pipeline(object):
    def __init__(self, name: str):
        self.name = name
        self.states = []  # type: List[PipelineState]
        self.starting_state = None  # type: Optional[PipelineState]
        self.workers = []  # type: List[PipelineWorker]
        self.mod_views = []  # type: List[PipelineModView]
        self._graph_adj_list = {}  # type: Dict[str, List[str]]

    def add_state(self, state: PipelineState, is_starting: bool = False):
        if state in self._get_state_names():
            raise RuntimeError(
                f"For pipeline {self.name} state {state.name} already exists"
            )
        if is_starting:
            if self.starting_state:
                raise RuntimeError(
                    f"For pipeline {self.name} starting state is already set"
                )
            self.starting_state = state
        self.states.append(state)

    def _get_state_names(self) -> List[str]:
        return list(map(lambda s: s.name, self.states))

    def add_worker(self, worker: PipelineWorker):
        from_state = worker.from_state
        to_states = worker.to_states
        if from_state not in self._get_state_names():
            raise RuntimeError(
                f"For pipeline {self.name} {from_state} is not (yet) a valid state"
            )
        for to_state in to_states:
            if to_state not in self._get_state_names():
                raise RuntimeError(
                    f"For pipeline {self.name} {to_state} is not (yet) a valid state"
                )
        self.workers.append(worker)
        if from_state not in self._graph_adj_list:
            self._graph_adj_list[from_state] = []
        self._graph_adj_list[from_state] += list(to_states)

    def add_mod_view(self, mod_view: PipelineModView):
        from_state = mod_view.from_state
        to_states = mod_view.to_state_names()
        if from_state not in self._get_state_names():
            raise RuntimeError(
                f"For pipeline {self.name} {from_state} is not (yet) a valid state"
            )
        for to_state in to_states:
            if to_state not in self._get_state_names():
                raise RuntimeError(
                    f"For pipeline {self.name} {to_state} is not (yet) a valid state"
                )
        self.mod_views.append(mod_view)
        if from_state not in self._graph_adj_list:
            self._graph_adj_list[from_state] = []
        self._graph_adj_list[from_state] += list(to_states)

    def assert_pipeline_is_dag(self):
        discovered = set()  # type: Set[str]
        visiting = set()  # type: Set[str]

        def has_cycle(state_name: str) -> bool:
            discovered.add(state_name)
            visiting.add(state_name)
            for to_state in self._graph_adj_list.get(state_name, []):
                if to_state not in discovered:
                    if has_cycle(to_state):
                        return True
                elif to_state in visiting:
                    return True
            visiting.remove(state_name)
            return False

        if not self.starting_state:
            raise RuntimeError(f"Pipeline {self.name} does not have a starting state")
        if has_cycle(self.starting_state.name):
            raise RuntimeError(f"Pipeline {self.name} has a cycle")

        undiscovered = set(self._get_state_names()) - discovered
        if undiscovered:
            raise RuntimeError(f"States {', '.join(undiscovered)} are undiscovered")

    def to_dict(self, content_store: ContentStore):
        if not self.starting_state:
            raise RuntimeError(f"Pipeline {self.name} does not have a starting state")
        return {
            "states": list(map(lambda s: s.to_dict(content_store), self.states)),
            "starting_state": self.starting_state.to_dict(content_store),
            "workers": list(map(PipelineWorker.to_dict, self.workers)),
            "mod_views": list(map(PipelineModView.to_dict, self.mod_views)),
        }
