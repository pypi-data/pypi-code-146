from beginai.utils.date import parse_date_to_format
from . import ParseAndExecute
from ...orchapi.api import OrchAPI
from tqdm import tqdm
import pandas as pd
import datetime
from beginai.exec.embeddings.instructions.utils import sort_instructions


class AlgorithmsApplier(object):

    host = "https://sdk.begin.ai"

    INTERACTIONS = 'interactions'
    CREATED_AT = 'beginai_created_at'
    LABELS = 'labels'
    BATCH_SIZE = 20000

    def __init__(self, app_id, license_key, host=None):
        self.orchapi = OrchAPI()
        self.orchapi.configure_orch_connection(host or self.host)
        self.orchapi.set_app_id_and_license_key(
            app_id=app_id, license_key=license_key)
        self._submission_in_progress = False

        self.embeddings = {}
        self.files = {}

    def load_user_data(self, filename, unique_identifier_column, label_column=None, created_at_column=None, file_separator=","):
        if unique_identifier_column == '' or unique_identifier_column is None:
            raise ValueError('The unique indentifier column must be provided')

        self._add_data_to_files_dictionary(
            filename, 'user', unique_identifier_column, label_column=label_column, created_at_column=created_at_column, file_separator=file_separator)

    def load_object_data(self, filename, object_name, unique_identifier_column, label_column=None, created_at_column=None, file_separator=","):
        if object_name == '' or object_name is None:
            raise ValueError(
                'The object name must be provied before the file is loaded')

        if unique_identifier_column == '' or unique_identifier_column is None:
            raise ValueError('The unique indentifier column must be provided')

        self._add_data_to_files_dictionary(
            filename, object_name, unique_identifier_column, label_column=label_column, created_at_column=created_at_column, file_separator=file_separator)

    def load_interactions(self, filename, unique_identifier_column, target_object_name,
                          target_unique_identifier_column, interaction_column_name, created_at_column=None, file_separator=","):
        if unique_identifier_column == '' or unique_identifier_column is None:
            raise ValueError('The unique indentifier column must be provided')
        if target_object_name == '' or target_object_name is None:
            raise ValueError(
                'The target object when registering an interaction must be provided')
        if target_unique_identifier_column == '' or target_unique_identifier_column is None:
            raise ValueError(
                'The target unique indentifer column when registering an interaction must be provided')
        if interaction_column_name == '' or interaction_column_name is None:
            raise ValueError(
                'The interaction column when registering an interaction must be provided')

        target_object = {
            'name': target_object_name.lower(),
            'uuid_column': target_unique_identifier_column.lower(),
            'interaction_column': interaction_column_name.lower()
        }

        self._add_data_to_files_dictionary(
            filename, self.INTERACTIONS, unique_identifier_column, target_object, created_at_column=created_at_column, file_separator=file_separator)

    def _add_data_to_files_dictionary(self, filename, object_name, uuid_column, target_object={}, label_column=None, created_at_column=None, file_separator=","):
        self.files[object_name] = {
            'data': self._read_file(filename, file_separator),
            'uuid_column': uuid_column.lower(),
            'target_object': target_object,
            'label_column': label_column,
            'created_at_column': created_at_column,
        }

    def _read_file(self, filename, file_separator):
        if filename == '' or filename is None:
            raise ValueError('File must be provided')

        df = pd.read_csv(filename, dtype=str, sep=file_separator)
        df = df.rename(columns=str.lower)
        return df

    def _get_instructions(self):
        return self.orchapi.fetch_instructions()

    def learn_from_data(self, update=False):
        if len(self.files) == 0:
            return

        print("Start time: ", datetime.datetime.now())

        instructions_id, current_embeddings_version, instructions = \
            self._get_instructions()

        self._generate_signatures(instructions)

        self._submit(instructions_id, current_embeddings_version, update)

        print("End time: ", datetime.datetime.now())
        self.flush_memory()

    def flush_memory(self):
        self.embeddings = {}
        self.files = {}

    def _generate_signatures(self, instructions):
        parser = ParseAndExecute(instructions)

        for object in self.files.keys():
            object_config = self.files[object]

            df: pd.DataFrame = object_config['data']
            uuid_column = object_config['uuid_column']

            df = self._preparing_dataframe(df, object_config, object)

            dictionary = df.to_dict(orient='records')

            object_data = []

            if object == self.INTERACTIONS:
                target_object = object_config['target_object']
                target_object_name = target_object['name']
                user_interactions = self._parse_interactions(
                    df, uuid_column, target_object)

                grouped_interactions = {
                    'interactions': [],
                    'raw_interactions': []
                }

                for user_id in user_interactions.keys():
                    value = user_interactions[user_id]
                    parser.feed(value)
                    results = parser.parse(object)
                    if len(results) > 0:
                        grouped_interactions['interactions'].append(
                            [str(user_id), target_object_name, results[self.INTERACTIONS]])
                        grouped_interactions['raw_interactions'].append(
                            [str(user_id), target_object_name, results['raw_interactions']])

                if len(grouped_interactions['interactions']) > 0 or len(grouped_interactions['raw_interactions']) > 0:
                    if object not in self.embeddings:
                        self.embeddings[object] = []
                    self.embeddings[object] = grouped_interactions

            else:
                for index, row in tqdm(enumerate(dictionary)):
                    parser.feed(row)
                    results = parser.parse(object)
                    if len(results) > 0:
                        key = row[uuid_column]
                        object_data.append([key, results])

                if len(object_data) > 0:
                    if object not in self.embeddings:
                        self.embeddings[object] = []

                    self.embeddings[object] = object_data

    def _preparing_dataframe(self, df: pd.DataFrame, object_config: dict, object: str) -> pd.DataFrame:
        label_column = object_config['label_column']
        created_at_column = object_config['created_at_column']

        # Rename columns representing begin constructs as identified by the user
        if object != self.INTERACTIONS and label_column is not None:
            try:
                df = df.rename(
                    columns={label_column: self.LABELS}, errors="raise")
            except:
                raise ValueError(
                    f"The [labels] column provided [{label_column}] was not found in the csv.")

        if created_at_column is not None:
            try:
                df = df.rename(
                    columns={created_at_column: self.CREATED_AT}, errors="raise")
            except:
                raise ValueError(
                    f"The [created_at] column provided [{created_at_column}] was not found in the csv.")

            df[self.CREATED_AT] = pd.to_datetime(df[self.CREATED_AT], infer_datetime_format=True).view(int) // 10 ** 9
        else:
            df[self.CREATED_AT] = datetime.datetime.now(datetime.timezone.utc).timestamp()

        return df

    def _parse_interactions(self, df, uuid_column, target_object):
        target_object_name = target_object['name']
        interaction_column = target_object['interaction_column']
        df = df.dropna().groupby(
            [uuid_column, target_object['uuid_column']], as_index=False)

        user_interactions = {}
        for key, group in tqdm(df):
            uuid = key[0]
            target_uuid = key[1]

            if uuid not in user_interactions:
                user_interactions[uuid] = {}

            if target_object_name not in user_interactions[uuid]:
                user_interactions[uuid][target_object_name] = {}

            if target_uuid not in user_interactions[uuid][target_object_name]:
                user_interactions[uuid][target_object_name][target_uuid] = []
    
            for action_value in group.apply(lambda row: [{'value': row[interaction_column], 'created_at': row[self.CREATED_AT]}], axis=1):
                user_interactions[uuid][target_object_name][target_uuid].append(action_value[0])

        return user_interactions

    def _submit(self, instructions_id, current_version, update):
        if self._submission_in_progress or len(self.embeddings) == 0:
            return

        print("Working on submitting existing set. please wait.")

        self._submission_in_progress = True

        self._update_interactions_structure_before_batch()

        for key in self.embeddings.keys():
            print(f"Submitting embeddings associated with {key}")
            if key == self.INTERACTIONS:
                self._submit_interactions(
                    self.embeddings[key], instructions_id, current_version)
            else:
                self._submit_objects(
                    self.embeddings[key], key, instructions_id, current_version, None, update)

        self._submission_in_progress = False

    def _update_interactions_structure_before_batch(self):
        if len(self.embeddings) == 0 or self.INTERACTIONS not in self.embeddings:
            return

        def _remap_object_based_on_type(person_id: str, interactions_dictionary: dict) -> list:
            remapped_list = []
            for object_id in interactions_dictionary.keys():
                remapped_list.append({
                    'person_id': person_id,
                    'object_id': str(object_id),
                    'interaction': interactions_dictionary[object_id],
                })
            return remapped_list

        grouped_interactions = self.embeddings[self.INTERACTIONS]
        interactions = {}

        for key in grouped_interactions:
            grouped_by_target_object = {}
            for data in grouped_interactions[key]:
                person_id = data[0]
                target_object = data[1]
                interactions_dictionary = data[2]

                if target_object not in grouped_by_target_object:
                    grouped_by_target_object[target_object] = []

                if len(interactions_dictionary) > 0:
                    grouped_by_target_object[target_object].extend(
                        _remap_object_based_on_type(person_id, interactions_dictionary[target_object]))
            interactions[key] = grouped_by_target_object

        self.embeddings[self.INTERACTIONS] = interactions

    def _submit_interactions(self, interactions_dictionary, instructions_id, current_version):
        for key in interactions_dictionary:
            for target_object in interactions_dictionary[key]:
                self._submit_objects(
                    interactions_dictionary[key][target_object], key, instructions_id, current_version, target_object, update=False)

    def _submit_objects(self, data, key, instructions_id, current_version, target_object=None, update=False):
        end_counter = self.BATCH_SIZE
        start_counter = 0
        all_ = len(data)
        while(start_counter < all_):
            slice = data[start_counter:end_counter]            
            self.orchapi.submit_embeddings_batch(
                slice, instructions_id, current_version, key, target_object, update)
            print(f"Submitted {len(slice)} at index {start_counter} out of {all_} {key}")
            start_counter += self.BATCH_SIZE
            end_counter += self.BATCH_SIZE

    def recommend(self, project_id, user_id, limit=None, page=None):
        return self.orchapi.recommend(project_id, user_id, limit, page)

    def predict_engagement(self, project_id, user_id, object_id):
        return self.orchapi.predict_engagement(project_id, user_id, object_id)

    def fake_detect(self, project_id, target_id):
        return self.orchapi.fake_detect(project_id, target_id)

    def classify(self, project_id, target_id):
        return self.orchapi.classify(project_id, target_id)

    def get_training_performance(self, project_id):
        return self.orchapi.training_results(project_id)

    def engagement_score(self, project_id, target_id, start_date, end_date):
        start_date = parse_date_to_format(start_date)
        end_date = parse_date_to_format(end_date)

        return self.orchapi.engagement_score(project_id, target_id, start_date, end_date)

    # maintenance end points

    def learn_from_data_dry_run(self):
        """
        does not submit embeddings, only generates them.
        """
        if len(self.files) == 0:
            return

        print("Start time: ", datetime.datetime.now())

        instructions_id, current_embeddings_version, instructions = self._get_instructions()

        self._generate_signatures(instructions)
        return self.embeddings

    def get_embedding_position_label(self, object_type):
        instructions_id, current_embeddings_version, data = self._get_instructions()

        position_label = []

        if len(data) == 0:
            return position_label

        sorted_dictionary = sort_instructions(data)

        if object_type not in sorted_dictionary:
            return position_label

        instructions_for_object = sorted_dictionary[object_type]
        for instruction in instructions_for_object:
            position_label.append(instruction['f_id'])

        return position_label
