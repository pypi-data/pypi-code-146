import json
import ray
import logging

import txp.common.utils.bigquery_utils
from google.oauth2 import service_account
import google.cloud.firestore as firestore
import google.cloud.bigquery as bigquery
from txp.common.ml.annotation import AnnotationLabelPayload
from typing import List, Set, Dict
from google.cloud.exceptions import NotFound
from txp.ml.training_service.dataset_committer import DatasetCommitPayload
from txp.common.utils import firestore_utils, model_registry_utils
from txp.common.ml.models import ModelRegistry
import threading
import time


@ray.remote
class AnnotationManager:
    """This class is in charge of processing anything that arrives at the
    /annotation endpoint.

    The responbilitites for this class are:
        - Processing incoming request of annotations objects to store
            in the persistence layer.
        - Asynchronously write annotation objects from the persistence layer
            into the BigQuery tables.
        - Answer if there are pending annotations to be processed for a given
            task.
    """

    def __init__(self, credentials_str, models_registry_collection_name, log_level=logging.INFO):
        self._annotations_collection_name: str = "tasks_annotations"
        self._models_registry_collection_name = models_registry_collection_name
        self._tables_names: List[str] = [
            "time",
            "fft",
            "psd",
            "time_metrics",
            "fft_metrics",
            "psd_metrics",
        ]
        self._log_level = log_level
        logging.basicConfig(level=log_level)
        json_dict_service_account = json.loads(credentials_str, strict=False)
        credentials = service_account.Credentials.from_service_account_info(
            json_dict_service_account
        )
        self._credentials = credentials
        self._db_lock: threading.Lock = threading.Lock()
        self._annotations_rate: int = 50
        self._annotations_thread: threading.Thread = threading.Thread(
            daemon=True,
            name="annotations_processing_thread",
            target=self._process_background_annotations,
        )
        self._annotations_thread.start()
        self._current_pending_annotations: Set[str] = set()
        logging.info(f"{self.__class__.__name__} Created successfully.")

    def process_new_annotations(
            self, annotations: List[AnnotationLabelPayload]
    ) -> bool:
        logging.info("Processing new annotations received.")
        logging.info(f"Annotations to process {annotations.__len__()}")
        db: firestore.Client = firestore.Client(
            credentials=self._credentials, project=self._credentials.project_id
        )

        if not annotations:
            return True

        try:
            # Note: currently, we simplify code by the assumption that labelers are only
            #   labelling one edge at a time.
            self._db_lock.acquire()
            annotations_map = list(map(lambda ann: ann.dict(), annotations))

            doc_ref: firestore.DocumentReference = db.collection(
                self._annotations_collection_name
            ).document(annotations[0].tenant_id + "_" + annotations[0].edge_logical_id)

            doc: firestore.DocumentSnapshot = doc_ref.get()

            if doc.exists:
                doc.reference.update(
                    {"annotations": firestore.ArrayUnion(annotations_map)}
                )
            else:
                doc.reference.set({"annotations": annotations_map})

        except NotFound:
            logging.error(
                "Trying to add annotations to document, but the document was not found."
            )
            return False

        except Exception as e:
            logging.error(f"Unknown exception while writing firestore document: {e}")

        else:
            logging.info(
                f"Successfully updated the annotations for the document with new annotations"
            )
            return True

        finally:
            self._db_lock.release()
            db.close()

    def validate_commit(self, commit_payload: DatasetCommitPayload) -> bool:
        """Returns True if it's possible to perform a requested commit.

        The commit will be possible if all the pending annotations for the
        requested dataset commit has been written to the persistence layer.

        Returns:
            - False: the task specified in the DatasetCommitPayload was not found
                for the asset in firestore.

            - False: it's not possible to trigger the dataset commit generation
                because there are pending annotations to process.

            - True: The commit operation is valid an can be triggered
        """
        logging.info(f"Validating requested commit.")

        try:
            db: firestore.Client = firestore.Client(
                credentials=self._credentials, project=self._credentials.project_id
            )

            task = firestore_utils.get_task_from_firestore(
                db,
                commit_payload.tenant_id,
                commit_payload.machine_id,
                commit_payload.task_id,
            )
            if task is None:
                logging.error(
                    f"No task {commit_payload.task_id} was found for asset {commit_payload.machine_id} for"
                    f" tenant {commit_payload.tenant_id}"
                )
                return False
        except Exception as e:
            logging.error(f"Unexpected error while validating commit: {e}")
            return False

        # At this point, we need to validate that all the edges of the task don't have
        #   any pending annotation in the cache to be written in the persistence layer.
        for edge_id in task.edges:
            doc_ref: firestore.DocumentReference = db.collection(
                self._annotations_collection_name
            ).document(commit_payload.tenant_id + "_" + edge_id)
            annotations = doc_ref.get().get("annotations")
            if annotations:
                logging.warning(
                    "The commit isn't valid because there are pending "
                    f"annotations to process for edge {edge_id}"
                )
                return False

            if (
                    commit_payload.tenant_id + "_" + edge_id
                    in self._current_pending_annotations
            ):
                logging.warning(
                    "The commit isn't valid because there are annotations being"
                    f" processed for edge {edge_id}"
                )
                return False

        logging.info(f"The dataset commit is valid. There are not pending annotations.")

        return True

    def validate_pre_annotation_commit(self, commit_payload: DatasetCommitPayload) -> bool:
        """Returns True if it's possible to perform a requested commit for pre annotation.

        The commit will be possible if the current model is not pre annotating.

        Returns:
            - False: the task specified in the DatasetCommitPayload was not found
                for the asset in firestore.

            - False: it's not possible to trigger the dataset commit generation the model is pre-annotating.

            - True: The commit operation is valid an can be triggered
        """
        logging.info(f"Validating requested pre annotation commit.")
        db: firestore.Client = firestore.Client(
            credentials=self._credentials, project=self._credentials.project_id
        )

        try:
            task = firestore_utils.get_task_from_firestore(
                db,
                commit_payload.tenant_id,
                commit_payload.machine_id,
                commit_payload.task_id,
            )
            if task is None:
                logging.error(
                    f"No task {commit_payload.task_id} was found for asset {commit_payload.machine_id} for"
                    f" tenant {commit_payload.tenant_id}"
                )
                return False
        except Exception as e:
            logging.error(f"Unexpected error while validating commit: {e}")
            return False

        model_registry_doc_ref = model_registry_utils.get_active_ml_model_doc_ref(db,
                                                                                  commit_payload.tenant_id,
                                                                                  commit_payload.machine_id,
                                                                                  commit_payload.task_id,
                                                                                  self._models_registry_collection_name)
        if model_registry_doc_ref is None:
            logging.error(f"No such model registry found for {commit_payload}")
            return False
        try:
            model_registry = ModelRegistry(**model_registry_doc_ref.get().to_dict())
            if model_registry.state.is_pre_annotating:
                logging.warning(
                    "The commit isn't valid because there is a pre annotation process in "
                    "progress pending to finish annotations being")
                return False
        except Exception as e:
            logging.error(f"Error trying to create ModelRegistry instance for {commit_payload} based on dict: {e}")
            return False

        logging.info(f"The dataset commit is valid. There are not pending annotations.")
        return True

    def _process_background_annotations(self):
        """This infinite loop method code will pull annotations from the database
        and will update the BigQuery tables on a separated thread.

        TODO: we should handle errors in the interaction with the GCP services.
        """
        while True:
            time.sleep(60)

            logging.info(f"Pulling annotations from DB. Acquiring secure context...")
            self._db_lock.acquire()

            db: firestore.Client = firestore.Client(
                credentials=self._credentials, project=self._credentials.project_id
            )
            try:
                docs = db.collection(self._annotations_collection_name).stream()
            except Exception as e:
                logging.error(
                    f"Unexpected exception while pulling annotations from"
                    f" firestore: {e}"
                )
                continue

            finally:
                db.close()
                self._db_lock.release()

            bq_client: bigquery.Client = bigquery.Client(credentials=self._credentials)
            new_annotations: Dict[str, List[AnnotationLabelPayload]] = {}
            try:
                for doc in docs:
                    annotations = doc.get("annotations")
                    if not annotations:
                        logging.info(
                            f"Document {doc.id} doesn't have annotations. Removing"
                        )
                        doc.reference.delete()
                    else:
                        self._current_pending_annotations.add(doc.id)
                        temp_annotations = annotations[0: self._annotations_rate]
                        logging.info(f"Taking {temp_annotations.__len__()} to process")
                        # remove taken annotations
                        doc.reference.update(
                            {"annotations": firestore.ArrayRemove(temp_annotations)}
                        )

                        new_annotations[doc.id] = list(
                            map(
                                lambda ann: AnnotationLabelPayload(**ann),
                                temp_annotations,
                            )
                        )

                if not new_annotations:
                    logging.info(f"Not annotations found to write.")
                    continue

                logging.info(f"Writing annotations into BigQuery datasets")
                for doc_id, annotations_list in new_annotations.items():
                    logging.info(f"Processing a new annotation for collection {doc_id}")
                    for annotation in annotations_list:
                        for table in self._tables_names:
                            txp.common.utils.bigquery_utils.annotate_signal(
                                annotation.tenant_id,
                                f"{annotation.dataset_name}.{table}",
                                annotation.edge_logical_id,
                                annotation.observation_timestamp,
                                annotation.label.json(),
                                annotation.version,
                                bq_client,
                            )

                    self._current_pending_annotations.remove(doc_id)

            except Exception as ex:
                logging.error(
                    f"Unexpected exception while pulling annotations from"
                    f" firestore: {ex}"
                )
                continue

            finally:
                bq_client.close()
