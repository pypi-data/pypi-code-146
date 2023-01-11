import apache_beam as beam
import logging


class ProcessPubsub(beam.DoFn):

    def to_runner_api_parameter(self, unused_context):
        return "beam:transforms:custom_parsing:custom_v0", None

    def process(self, pubsub_msg_bytes, time_table, fft_table, psd_table, time_metrics_table, fft_metrics_table,
                psd_metrics_table, events_table, states_table,
                timestamp=beam.DoFn.TimestampParam, window=beam.DoFn.WindowParam):
        from txp.common.reports.section import ReportSection
        from google.cloud import bigquery
        import txp.common.reports as common_reports
        import json
        pubsub_msg = json.loads(pubsub_msg_bytes.decode(encoding='utf-8', errors='strict'))
        logging.info(f"New section arrived: {pubsub_msg}")
        client = bigquery.Client()
        section_type = common_reports.SECTIONS_REGISTRY[pubsub_msg['type']]
        fetched_data = ReportSection.get_input_data(pubsub_msg, section_type.required_inputs(), client,
                                                    time_table, fft_table, psd_table, time_metrics_table,
                                                    fft_metrics_table, psd_metrics_table, events_table, states_table)
        yield fetched_data, pubsub_msg


class Plot2DSectionProcessing(beam.DoFn):

    def to_runner_api_parameter(self, unused_context):
        return "beam:transforms:custom_parsing:custom_v0", None

    def process(self, element, timestamp=beam.DoFn.TimestampParam, window=beam.DoFn.WindowParam):
        import txp.common.reports as common_reports

        input_data, pubsub_msg = element
        section_type = common_reports.SECTIONS_REGISTRY[pubsub_msg['type']]
        try:
            computed_data = section_type.compute(input_data, pubsub_msg)
        except Exception as e:
            logging.error(f"Error generating section {section_type.__name__}: "
                          f"{e}")
        else:
            if computed_data:
                yield computed_data


class WriteToBigQuery(beam.DoFn):

    def to_runner_api_parameter(self, unused_context):
        return "beam:transforms:custom_parsing:custom_v0", None

    def process(self, element, sections_table, timestamp=beam.DoFn.TimestampParam, window=beam.DoFn.WindowParam):
        from google.cloud import bigquery
        client = bigquery.Client()
        errors = client.insert_rows_json(sections_table, [element])
        message = f"""section stored: 
                        tenant_id: {element["tenant_id"]},
                        section_id: {element["section_id"]},
                        creation_timestamp: {element["creation_timestamp"]},
                        start_timestamp: {element['start_timestamp']},
                        end_timestamp: {element['end_timestamp']}
                  """
        if errors:
            logging.error(f"""Could not store in {sections_table}: {message}, ERROR: {errors} """)
        else:
            logging.info(message)
