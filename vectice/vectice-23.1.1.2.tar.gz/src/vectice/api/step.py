from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from gql import gql

if TYPE_CHECKING:
    from vectice.api.json import IterationOutput, IterationStepArtifactInput
    from vectice.api.json import StepOutput
    from vectice.api.json.step import StepUpdateInput

from gql.transport.exceptions import TransportQueryError

from vectice.api.gql_api import GqlApi, Parser

_logger = logging.getLogger(__name__)

_RETURNS_WITH_STEPS = """
                steps {
                    id
                    index
                    name
                    completed
                    description
                    artifacts {
                                entityFileId
                                modelVersionId
                                datasetVersionId
                                type
                    }
                    __typename
                }
                phase {
                    name
                }
              __typename
            """

_RETURNS = """
                id
                index
                name
                completed
                description
                artifacts {
                                entityFileId
                                modelVersionId
                                datasetVersionId
                                type
                    }
                __typename
            """


class StepApi(GqlApi):
    def list_steps(self, phase_id: int, phase_name: str | None) -> list[StepOutput]:
        gql_query = "getActiveIterationOrCreateOne"
        variable_types = "$phaseId:Float!"
        variables = {"phaseId": phase_id}
        kw = "phaseId:$phaseId"
        query = GqlApi.build_query(
            gql_query=gql_query,
            variable_types=variable_types,
            returns=_RETURNS_WITH_STEPS,
            keyword_arguments=kw,
            query=True,
        )
        query_built = gql(query)
        try:
            response = self.execute(query_built, variables)
            iteration_output: IterationOutput = Parser().parse_item(response[gql_query])
            step_output: list[StepOutput] = iteration_output.steps
            return step_output
        except TransportQueryError as e:
            phase_ref: int | str = phase_name if phase_name else phase_id
            raise self._error_handler.handle_post_gql_error(e, "steps", phase_ref)

    def list_steps_for_iteration(
        self, phase_id: int, iteration_index: int, phase_name: str | None = None
    ) -> list[StepOutput]:
        gql_query = "getIterationByIndex"
        variable_types = "$index:Float!,$phaseId:Float!"
        variables = {"index": iteration_index, "phaseId": phase_id}
        kw = "index:$index,phaseId:$phaseId"
        query = GqlApi.build_query(
            gql_query=gql_query,
            variable_types=variable_types,
            returns=_RETURNS_WITH_STEPS,
            keyword_arguments=kw,
            query=True,
        )
        query_built = gql(query)
        try:
            response = self.execute(query_built, variables)
            iteration_output: IterationOutput = Parser().parse_item(response[gql_query])
            step_output: list[StepOutput] = iteration_output.steps
            return step_output
        except TransportQueryError as e:
            phase_ref: int | str = phase_name if phase_name else phase_id
            raise self._error_handler.handle_post_gql_error(e, "steps", phase_ref)

    def close_step(self, step_id: int, step_update: StepUpdateInput) -> StepOutput:
        gql_query = "completeIterationStep"
        variable_types = "$id:Float!,$data:IterationStepUpdateInput"
        variables = {"id": step_id, "data": step_update}
        kw = "id:$id, data:$data"
        query = GqlApi.build_query(
            gql_query=gql_query,
            variable_types=variable_types,
            returns=_RETURNS,
            keyword_arguments=kw,
            query=False,
        )
        query_built = gql(query)
        try:
            response = self.execute(query_built, variables)
            step_output: StepOutput = Parser().parse_item(response[gql_query])
            return step_output
        except TransportQueryError as e:
            raise self._error_handler.handle_post_gql_error(e, "step", step_id)

    def add_iteration_step_artifact(self, data: IterationStepArtifactInput, step_id: int) -> StepOutput:
        gql_query = "addIterationStepArtifact"
        variable_types = "$id:Float!,$data:IterationStepArtifactInput!"
        variables = {"id": step_id, "data": data}
        kw = "id:$id, data:$data"
        query = GqlApi.build_query(
            gql_query=gql_query,
            variable_types=variable_types,
            returns=_RETURNS,
            keyword_arguments=kw,
            query=False,
        )
        query_built = gql(query)
        try:
            response = self.execute(query_built, variables)
            step_output: StepOutput = Parser().parse_item(response[gql_query])
            return step_output
        except TransportQueryError as e:
            raise self._error_handler.handle_post_gql_error(e, "step", step_id)

    def get_step(self, step: str, iteration_id: int) -> StepOutput:
        """
        parent_id is the project id
        """
        if isinstance(step, str) and iteration_id:
            gql_query = "getStepByName"
            variable_types = "$name:String!,$parentId:Float!"
            variables = {"name": step, "parentId": iteration_id}
            kw = "name:$name,parentId:$parentId"
        else:
            raise ValueError("string and parent id required.")
        query = GqlApi.build_query(
            gql_query=gql_query, variable_types=variable_types, returns=_RETURNS, keyword_arguments=kw, query=True
        )
        query_built = gql(query)
        try:
            response = self.execute(query_built, variables)
            step_output: StepOutput = Parser().parse_item(response[gql_query])
            return step_output
        except TransportQueryError as e:
            raise self._error_handler.handle_post_gql_error(e, "step", step)
