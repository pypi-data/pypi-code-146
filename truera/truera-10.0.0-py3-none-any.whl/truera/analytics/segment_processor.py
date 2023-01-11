from dataclasses import dataclass
import logging
import os
from typing import Mapping, Optional, Sequence, Tuple
import uuid

import numpy as np
import pandas as pd

from truera.authn.usercontext import RequestContext
from truera.caching import util as caching_util
from truera.client.private.metarepo import ModelTestDao
from truera.client.private.metarepo import Segmentation as SegmentationDao
from truera.client.private.metarepo import \
    SegmentationCache as SegmentationCacheDao
from truera.protobuf.public.data.segment_pb2 import \
    InterestingSegmentInfo  # pylint: disable=no-name-in-module
from truera.protobuf.public.data.segment_pb2 import \
    Segmentation  # pylint: disable=no-name-in-module
from truera.protobuf.public.data.segment_pb2 import \
    SegmentationCacheMetadata  # pylint: disable=no-name-in-module
from truera.utils.filter_utils import FilterProcessor
from truera.utils.truera_status import TruEraAlreadyExistsError
from truera.utils.truera_status import TruEraInvalidArgumentError


@dataclass(frozen=True)
class SegmentationMetadata:
    project_id: str
    split_id: str
    segmentation_id: str
    model_id: Optional[str] = None


class SegmentLoader(object):

    def __init__(self, server_config, metarepo_client):
        self.logger = logging.getLogger(__name__)
        self.server_config = server_config
        self.metarepo_client = metarepo_client
        self.segmentation_dao = SegmentationDao(self.metarepo_client)
        self.segmentation_cache_dao = SegmentationCacheDao(self.metarepo_client)

    def load_segment_definitions_from_name(
        self,
        request_ctx: RequestContext,
        project_id: str,
        segmentation_name: str,
    ) -> Segmentation:
        params = {"name": segmentation_name}
        return self.segmentation_dao.get_by_params(
            request_ctx=request_ctx, project_id=project_id, params=params
        )

    def load_segment_definition_from_id(
        self,
        request_ctx: RequestContext,
        project_id: str,
        segmentation_id: str,
    ) -> Segmentation:
        ret = self.segmentation_dao.get_by_id(
            obj_id=segmentation_id, request_ctx=request_ctx
        )
        if ret and ret.project_id != project_id:
            raise TruEraInvalidArgumentError(
                f"Segmentation {segmentation_id} does not belong to project {project_id}, but instead to {ret.project_id}"
            )
        return ret

    def load_segment_definitions(
        self,
        request_ctx: RequestContext,
        project_id: str,
        segmentation_id: Optional[str],
        include_unaccepted_interesting_segments: bool,
    ) -> Sequence[Segmentation]:
        params = {}
        if segmentation_id:
            params["id"] = segmentation_id
        all_segmentations = self.segmentation_dao.get_all(
            request_ctx=request_ctx, project_id=project_id, params=params
        )
        if include_unaccepted_interesting_segments:
            return all_segmentations
        ret = []
        for curr in all_segmentations:
            if not curr.HasField(
                "interesting_segment_info"
            ) or curr.interesting_segment_info.acceptance_state == InterestingSegmentInfo.AcceptanceState.Type.ACCEPTED:
                ret.append(curr)
        return ret

    def save_segment_definition(
        self,
        request_ctx: RequestContext,
        segmentation: Segmentation,
    ) -> Segmentation:
        return self.segmentation_dao.add(
            object=segmentation, request_ctx=request_ctx
        )

    def delete_segment_definition(
        self, request_ctx: RequestContext, segmentation_id: str
    ):
        self.segmentation_dao.delete(
            obj_id=segmentation_id, request_ctx=request_ctx
        )

    def _find_segment_result(
        self, request_ctx: RequestContext,
        segmentation_metadata: SegmentationMetadata
    ) -> Optional[SegmentationCacheMetadata]:
        params = {
            "split_id": segmentation_metadata.split_id,
            "segmentation_id": segmentation_metadata.segmentation_id
        }
        if segmentation_metadata.model_id:
            params["model_id"] = segmentation_metadata.model_id
        return self.segmentation_cache_dao.get_by_params(
            request_ctx=request_ctx,
            project_id=segmentation_metadata.project_id,
            params=params,
        )

    def load_segment_result(
        self,
        request_ctx: RequestContext,
        segmentation_metadata: SegmentationMetadata,
    ) -> np.ndarray:
        segmentation_cache_metadata = self._find_segment_result(
            request_ctx, segmentation_metadata
        )
        if segmentation_cache_metadata is None:
            return None
        self.logger.debug("Loaded cache %s", segmentation_cache_metadata)
        return np.loadtxt(segmentation_cache_metadata.location, delimiter=",")

    def delete_segment_result(
        self, request_ctx: RequestContext,
        segmentation_metadata: SegmentationMetadata
    ):
        segmentation_cache_metadata = self._find_segment_result(
            request_ctx, segmentation_metadata
        )
        if segmentation_cache_metadata is None:
            return
        self.segmentation_cache_dao.delete(
            obj_id=segmentation_cache_metadata.id, request_ctx=request_ctx
        )
        os.remove(segmentation_cache_metadata.location)

    def save_segment_result(
        self,
        request_ctx: RequestContext,
        segmentation_metadata: SegmentationMetadata,
        segments: np.ndarray,
    ):
        folder = os.path.join(
            caching_util.get_v2_cache_file_directory(
                self.server_config, segmentation_metadata.project_id
            ), "segmentations"
        )
        os.makedirs(folder, exist_ok=True)
        segmentation_metadata_id = str(uuid.uuid4())
        path = os.path.join(folder, f"{segmentation_metadata_id}.csv")
        np.savetxt(path, segments, delimiter=",")
        segment_cache_metadata = SegmentationCacheMetadata()
        segment_cache_metadata.id = segmentation_metadata_id
        segment_cache_metadata.segmentation_id = segmentation_metadata.segmentation_id
        segment_cache_metadata.split_id = segmentation_metadata.split_id
        segment_cache_metadata.project_id = segmentation_metadata.project_id
        if segmentation_metadata.model_id is not None:
            segment_cache_metadata.model_id = segmentation_metadata.model_id
        segment_cache_metadata.location = path
        self.logger.debug(
            "Adding segmentation cache entry: %s", segment_cache_metadata
        )
        self.segmentation_cache_dao.add(
            object=segment_cache_metadata, request_ctx=request_ctx
        )


class SegmentProcessor(object):

    def __init__(self, server_config, metarepo_client):
        self.segment_loader = SegmentLoader(server_config, metarepo_client)
        self._modeltest_dao = ModelTestDao(metarepo_client)
        self.loaded_result_caches: Mapping[SegmentationMetadata,
                                           np.ndarray] = {}
        self.loaded_definition_caches: Mapping[Tuple[str, str],
                                               Segmentation] = {}
        self.logger = logging.getLogger(__name__)

    # TODO(AB#1195) Segment results will also depend on model_id for segments which look at
    # model output, model_id should be added to segmentation_metadata.
    def segment_result(
        self, request_ctx: RequestContext, data: pd.DataFrame,
        segmentation_metadata: SegmentationMetadata
    ) -> np.ndarray:
        self.logger.debug("Processing segment: %s", segmentation_metadata)
        segment_result = self.processed_segment_result(
            request_ctx, segmentation_metadata
        )
        if segment_result is not None:
            if segment_result.shape[0] >= data.shape[0]:
                return segment_result[0:data.shape[0]]
        segment_definition = self.segment_definition(
            request_ctx, segmentation_metadata.project_id,
            segmentation_metadata.segmentation_id
        )
        return_val = np.full(data.shape[0], -1)
        for index, segment in enumerate(segment_definition.segments):
            filter_exp = segment.filter_expression
            filter_result = FilterProcessor.filter(data, filter_exp)
            return_val = np.where(
                filter_result, np.full_like(return_val, index), return_val
            )
        is_not_exhaustive = np.any(return_val < 0)
        if is_not_exhaustive:
            # Applicable if the defined segments are not exhaustive over the input space.
            # TODO(apoorv) Maybe assert if segmentation.has_other_segment = false
            return_val = np.where(
                return_val < 0,
                np.full_like(return_val, len(segment_definition.segments)),
                return_val
            )
        self.segment_loader.save_segment_result(
            request_ctx, segmentation_metadata, return_val
        )
        self.loaded_result_caches[segmentation_metadata] = return_val
        return return_val

    def processed_segment_result(
        self,
        request_ctx: RequestContext,
        segmentation_metadata: SegmentationMetadata,
        length: int = 0
    ) -> np.ndarray:
        # TODO(apoorv) We can optimise the caching by dropping model id from
        # the cache key when the segment results dont depend on model output,
        # but only the data.
        if segmentation_metadata in self.loaded_result_caches:
            cache = self.loaded_result_caches[segmentation_metadata]
            if cache.shape[0] >= length:
                return cache
        segment_result = self.segment_loader.load_segment_result(
            request_ctx, segmentation_metadata
        )
        if segment_result is not None:
            self.loaded_result_caches[segmentation_metadata] = segment_result
            if segment_result.shape[0] >= length:
                return segment_result

    def segment_definition(
        self, request_ctx: RequestContext, project_id: str, segmentation_id: str
    ) -> Optional[Segmentation]:
        key = (project_id, segmentation_id)
        if key in self.loaded_definition_caches:
            return self.loaded_definition_caches[key]
        segmentation = self.segment_loader.load_segment_definition_from_id(
            request_ctx, project_id, segmentation_id
        )
        if segmentation:
            self.loaded_definition_caches[key] = segmentation
        return segmentation

    def save_segment_definition(
        self, request_ctx: RequestContext, segmentation: Segmentation
    ) -> Segmentation:
        project_id = segmentation.project_id
        if segmentation.name:
            existing_segmentation = self.segment_loader.load_segment_definitions_from_name(
                request_ctx, project_id, segmentation.name
            )
            if existing_segmentation:
                if existing_segmentation.id == segmentation.id:
                    self.logger.info(
                        f"Deleting segmentation with id=\"{segmentation.id}\" and name=\"{segmentation.name}\""
                    )
                    self.delete_segment(
                        request_ctx, project_id, segmentation.id
                    )
                else:
                    raise TruEraAlreadyExistsError(
                        f"Segmentation {segmentation.name} already exists in project {segmentation.project_id}."
                    )
        updated_segmentation = self.segment_loader.save_segment_definition(
            request_ctx, segmentation
        )
        segmentation_id = updated_segmentation.id
        key = (project_id, segmentation_id)
        self.loaded_definition_caches[key] = updated_segmentation
        return updated_segmentation

    def delete_segment(
        self, request_ctx: RequestContext, project_id: str, segmentation_id: str
    ):
        self.segment_loader.delete_segment_definition(
            request_ctx, segmentation_id
        )
        key = (project_id, segmentation_id)
        if key in self.loaded_definition_caches:
            del self.loaded_definition_caches[key]
        self._remove_result_caches(request_ctx, segmentation_id)
        affected_test_ids = self._get_associated_model_test_ids_from_segmentation_id(
            request_ctx, segmentation_id
        )
        for test_id in affected_test_ids:
            self.logger.info(
                f"Segmentation to be deleted ({segmentation_id}) is associated with test {test_id}. Deleting the associated test."
            )
            self._modeltest_dao.delete(obj_id=test_id, request_ctx=request_ctx)

    def load_segments(
        self,
        request_ctx: RequestContext,
        project_id: str,
        segmentation_id: Optional[str],
        include_unaccepted_interesting_segments: bool,
    ) -> Sequence[Segmentation]:
        ret = self.segment_loader.load_segment_definitions(
            request_ctx, project_id, segmentation_id,
            include_unaccepted_interesting_segments
        )
        for segmentation in ret:
            key = (segmentation.project_id, segmentation.id)
            self.loaded_definition_caches[key] = segmentation
        return ret

    def _remove_result_caches(
        self, request_ctx: RequestContext, segmentation_id: str
    ):
        keys_to_delete = []
        for segmentation_metadata in self.loaded_result_caches:
            if segmentation_id != segmentation_metadata.segmentation_id:
                continue
            keys_to_delete.append(segmentation_metadata)
        for key in keys_to_delete:
            del self.loaded_result_caches[key]
            self.segment_loader.delete_segment_result(request_ctx, key)

    def _get_associated_model_test_ids_from_segmentation_id(
        self, request_ctx: RequestContext, segmentation_id: str
    ) -> Sequence[str]:
        test_ids = [
            i.id for i in self._modeltest_dao.get_all(
                request_ctx=request_ctx,
                params={"segment_id.segmentation_id": segmentation_id},
                as_proto=True
            )
        ]
        test_ids += [
            i.id for i in self._modeltest_dao.get_all(
                request_ctx=request_ctx,
                params={
                    "stability_test.base_segment_id.segmentation_id":
                        segmentation_id
                },
                as_proto=True
            )
        ]
        test_ids += [
            i.id for i in self._modeltest_dao.get_all(
                request_ctx=request_ctx,
                params={
                    "fairness_test.segment_id_protected.segmentation_id":
                        segmentation_id
                },
                as_proto=True
            )
        ]
        test_ids += [
            i.id for i in self._modeltest_dao.get_all(
                request_ctx=request_ctx,
                params={
                    "fairness_test.segment_id_comparison.segmentation_id":
                        segmentation_id
                },
                as_proto=True
            )
        ]
        return list(set(test_ids))
