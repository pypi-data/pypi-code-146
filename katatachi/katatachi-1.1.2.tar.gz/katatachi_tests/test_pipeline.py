from typing import Set

from katatachi.pipeline import Pipeline
from katatachi.pipeline import PipelineModView
from katatachi.pipeline import PipelineModViewToState
from katatachi.pipeline import PipelineState
from katatachi.pipeline import PipelineWorker

from .testcase_with_mongomock import TestCaseWithMongoMock


class TestPipeline(TestCaseWithMongoMock):
    @staticmethod
    def create_demo_worker_instance(from_state: str, to_states: Set[str]):
        return PipelineWorker(
            name="demo",
            process=lambda _: [],
            from_state=from_state,
            to_states=to_states,
        )


class TestPipelineAssertDag(TestPipeline):
    def test_assert_dag_straight_line_pipeline(self):
        pipeline = Pipeline("straight_line")
        pipeline.add_state(PipelineState("state1"), is_starting=True)
        pipeline.add_state(PipelineState("state2"))
        pipeline.add_state(PipelineState("state3"))
        pipeline.add_worker(self.create_demo_worker_instance("state1", {"state2"}))
        pipeline.add_mod_view(
            PipelineModView(
                "2to3", "state2", [PipelineModViewToState("state3", "state3")], [], ""
            )
        )
        pipeline.assert_pipeline_is_dag()

    def test_assert_dag_simple_pipeline(self):
        pipeline = Pipeline("simple")
        pipeline.add_state(PipelineState("state1"), is_starting=True)
        pipeline.add_state(PipelineState("state2"))
        pipeline.add_state(PipelineState("state3"))
        pipeline.add_state(PipelineState("state4"))
        pipeline.add_state(PipelineState("state5"))
        pipeline.add_worker(self.create_demo_worker_instance("state1", {"state2"}))
        pipeline.add_worker(self.create_demo_worker_instance("state2", {"state3"}))
        pipeline.add_worker(self.create_demo_worker_instance("state2", {"state4"}))
        pipeline.add_worker(self.create_demo_worker_instance("state3", {"state4"}))
        pipeline.add_worker(self.create_demo_worker_instance("state4", {"state5"}))
        pipeline.assert_pipeline_is_dag()

    def test_assert_not_dag(self):
        pipeline = Pipeline("not_dag")
        pipeline.add_state(PipelineState("state1"), is_starting=True)
        pipeline.add_state(PipelineState("state2"))
        pipeline.add_state(PipelineState("state3"))
        pipeline.add_state(PipelineState("state4"))
        pipeline.add_state(PipelineState("state5"))
        pipeline.add_worker(self.create_demo_worker_instance("state1", {"state2"}))
        pipeline.add_worker(self.create_demo_worker_instance("state3", {"state2"}))
        pipeline.add_worker(self.create_demo_worker_instance("state2", {"state4"}))
        pipeline.add_worker(self.create_demo_worker_instance("state4", {"state3"}))
        pipeline.add_worker(self.create_demo_worker_instance("state4", {"state5"}))
        self.assertRaisesRegex(
            RuntimeError, "has a cycle", pipeline.assert_pipeline_is_dag
        )

    def test_assert_missing_starting_state(self):
        pipeline = Pipeline("not_dag")
        pipeline.add_state(PipelineState("state1"))
        pipeline.add_state(PipelineState("state2"))
        pipeline.add_state(PipelineState("state3"))
        pipeline.add_worker(self.create_demo_worker_instance("state1", {"state2"}))
        pipeline.add_mod_view(
            PipelineModView(
                "2to3", "state2", [PipelineModViewToState("state3", "state3")], [], ""
            )
        )
        self.assertRaisesRegex(
            RuntimeError, "starting state", pipeline.assert_pipeline_is_dag
        )

    def test_assert_undiscovered_states(self):
        pipeline = Pipeline("not_dag")
        pipeline.add_state(PipelineState("state1"), is_starting=True)
        pipeline.add_state(PipelineState("state2"))
        pipeline.add_state(PipelineState("state3"))
        pipeline.add_state(PipelineState("state4"))
        pipeline.add_worker(self.create_demo_worker_instance("state1", {"state2"}))
        pipeline.add_mod_view(
            PipelineModView(
                "2to3", "state2", [PipelineModViewToState("state3", "state3")], [], ""
            )
        )
        self.assertRaisesRegex(
            RuntimeError, "undiscovered", pipeline.assert_pipeline_is_dag
        )
