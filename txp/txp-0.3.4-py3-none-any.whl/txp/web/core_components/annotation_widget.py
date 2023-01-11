import streamlit as st
import pandas as pd
import logging
import requests
import pytz
import datetime
import json
from fastapi import status
from txp.common.config import settings
from txp.common.ml.annotation import AnnotationLabelPayload, AnnotationLabel
from txp.common.ml.tasks import ClassificationLabelDefinition

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class AnnotationWidget:
    def __init__(self, asset_labels: ClassificationLabelDefinition,
                 machine_devices, data, dataset, client):
        self.machine_devices = machine_devices
        self.data = data
        self.dataset = dataset
        self.client = client

        self._label_obj: ClassificationLabelDefinition = asset_labels
        self._num_categories: int = len(self._label_obj.categories())
        self.url = st.secrets['service_url']
        self._timestamps = []
        for sample in self.data:
            self._timestamps.append(self._change_utc_timezone(sample['observation_timestamp']))

    def tables_for_edge_type(self, logical_id):
        for device in self.machine_devices:
            if device['logical_id'] == logical_id:
                if device["device_kind"] == "Icomox":
                    return ['.time', '.fft', '.psd', '.time_metrics', '.fft_metrics', '.psd_metrics']
                else:
                    return ['.time']

    def _change_utc_timezone(self, timestamp):
        utc = pytz.timezone('UTC')
        timezone = pytz.timezone("America/Mexico_City")
        date_time = pd.to_datetime(timestamp)
        localized_timestamp = utc.localize(date_time)
        new_timezone = localized_timestamp.astimezone(timezone)
        strtime = new_timezone.strftime("%d/%m/%Y, %H:%M:%S,%f")
        return strtime

    def _render(self):
        """ Render visual components of annotation widget. """
        with st.form("annotation_form"):
            st.number_input(
                    'Número de versión:',
                    min_value=1,
                    step=1,
                    value=1,
                    key=f"{self.__class__.__name__}_actual_annotation_version"
            )

            st.markdown("Seleccione un rango de tiempo que desee adjudicarle una etiqueta.")
            st.selectbox(
                label="Desde:",
                options=['<Seleccionar>'] + sorted(set(self._timestamps)),
                key=f"{self.__class__.__name__}_annotation_since",
                index=0

            )
            st.selectbox(
                label="Hasta:",
                options=['<Seleccionar>'] + sorted(set(self._timestamps)),
                key=f"{self.__class__.__name__}_annotation_until",
                index=0
            )

            for idx, category in enumerate(self._label_obj.categories()):
               st.selectbox(
                    label=f"{category}",
                    options=['<Seleccionar>'] + list(self._label_obj.get_labels_in_category(category)),
                    key=f"{self.__class__.__name__}_{category}_{idx}_label",
                    index=0
                )
            st.form_submit_button("Anotar", on_click=self._annotate)

    def _annotate(self) -> None:
        """ Get annotation records. """
        if not st.session_state[f"{self.__class__.__name__}_annotation_since"] == '<Seleccionar>':
            version, samples, labels = self._get_labeled_traces()

            # TODO: We should centralize the label handling in the core contacts
            json_label = {
                'label_value': labels,
                'parameters': {},
                'label_type': ClassificationLabelDefinition.__name__
            }

            log.info(f"Collected multicategory: {labels}")
            log.info(f"Label: {json_label}")

            annotation_records = []
            for sample in samples:
                annotation = AnnotationLabelPayload(
                    tenant_id=sample['tenant_id'],
                    dataset_name=f'{self.dataset}',
                    edge_logical_id=sample['edge_logical_id'],
                    observation_timestamp=sample['observation_timestamp'],
                    label=AnnotationLabel(**json_label),
                    version=version,
                )
                log.info(f"Generating annotation: {annotation.json()}")
                annotation_records.append(annotation.dict())
            try:
                headers = {"Authorization": f"Bearer {st.secrets['service_auth_token']}"}
                response = requests.post(f"{self.url}/annotation", json=annotation_records, headers=headers)
            except (ConnectionError, ConnectionRefusedError, Exception) as ce:
                st.error("No se pudo establecer con el servidor de anotación. "
                         "Contacte a soporte.")
            else:
                if response.status_code == status.HTTP_201_CREATED:
                    st.caption(f'{len(annotation_records)} muestras fueron etiquetadas como {labels}')
                    print(response.json())
                else:
                    st.caption(f'{len(annotation_records)} no pudieron ser etiquetadas como {labels}')
                    log.error(f"Could not create labels. Response: {response.json()}")
                    return None

    def _get_labeled_traces(self):
        """ selects the traces of figure that are within interval to annotate them. """

        version = st.session_state[f"{self.__class__.__name__}_actual_annotation_version"]

        since_timestamp = datetime.datetime.strptime(st.session_state[
            f"{self.__class__.__name__}_annotation_since"
        ], "%d/%m/%Y, %H:%M:%S,%f")
        until_timestamp = datetime.datetime.strptime(st.session_state[
            f"{self.__class__.__name__}_annotation_until"
        ], "%d/%m/%Y, %H:%M:%S,%f")

        # Get the multi category labels from form
        labels = []
        for idx, category in enumerate(self._label_obj.categories()):
            labels.append(st.session_state[f"{self.__class__.__name__}_{category}_{idx}_label"])

        labeled_samples = []
        for sample in self.data:
            mex_timestamp = self._change_utc_timezone(sample['observation_timestamp'])
            sample_timestamp = datetime.datetime.strptime(mex_timestamp, "%d/%m/%Y, %H:%M:%S,%f")
            if since_timestamp <= sample_timestamp <= until_timestamp:
                labeled_samples.append(sample)

        return version, labeled_samples, labels
