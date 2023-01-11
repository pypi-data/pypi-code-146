from collections import defaultdict
import itertools
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
from scipy.special import logit

from truera.nlp.fairness.output_metrics import OutputMetrics
from truera.nlp.fairness.utils import get_segment_metrics_dict
from truera.nlp.fairness.utils import segment_all_data
from truera.nlp.general.aiq.filtering_utils import get_accuracy_group_name_dict
from truera.nlp.general.utils.configs import QoIType
from truera.nlp.general.utils.configs import TokenType
from truera.nlp.general.utils.general_utils import multirange
from truera.nlp.general.utils.mem import MemUtil
from truera.rnn.general.aiq.clustering import SpectralHierarchicalClusterer
from truera.rnn.general.container.artifacts import ArtifactsContainer
from truera.rnn.general.container.model import ModelProxy


def cache_results(cached_name):

    def cache_with_name(getter_function):

        def wrapper(self, artifacts_container, *args, **kwargs):
            artifacts_path = artifacts_container.get_path()

            if artifacts_path not in self._cache:
                self._cache[artifacts_path] = {}
            if (cached_name, args, tuple(kwargs.values()
                                        )) not in self._cache[artifacts_path]:
                self._cache[artifacts_path][
                    (cached_name, args, tuple(kwargs.values()))
                ] = getter_function(self, artifacts_container, *args, **kwargs)

            return self._cache[artifacts_path][
                (cached_name, args, tuple(kwargs.values()))]

        return wrapper

    return cache_with_name


class NLPModelProxy(ModelProxy):

    def __init__(self):
        self._cache = {}

    @cache_results('data_dtype')
    def get_data_dtype(self, artifacts_container: ArtifactsContainer):
        return MemUtil.get_data_dtype(artifacts_container)

    def get_original_text(
        self, artifacts_container: ArtifactsContainer, num_records, offset=0
    ):
        name = 'original_text'
        return MemUtil.get_text(artifacts_container, name, num_records, offset)

    def get_num_classes(self, artifacts_container: ArtifactsContainer):
        token_occurrences_dict = self.get_token_occurrences_dict(
            artifacts_container
        )
        return len(list(token_occurrences_dict.values())[0])

    def get_default_num_records(
        self,
        artifacts_container: ArtifactsContainer,
        influences: bool = False
    ) -> int:
        """Get the total number of records generated. This will be based off the number of records for metrics.
        If influences is True, this will be based off the number of records for influences.

        Args:
            artifacts_container (ArtifactsContainer): The artifact metadata.
            influences (bool, optional): Whether to use metrics or influences counts. Defaults to False.

        Returns:
            int: The number of records.
        """
        return MemUtil._get_total_records(
            artifacts_container, influences=influences
        )

    def get_data(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset=0
    ):
        name = 'token_ids'
        dtype = MemUtil.get_data_dtype(artifacts_container)
        return MemUtil.get(
            artifacts_container, name, num_records, offset=offset, dtype=dtype
        )

    def get_ids(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset=0
    ):
        name = 'original_ids'
        return MemUtil.get(
            artifacts_container, name, num_records, offset=offset, dtype=int
        )

    def get_ids_reverse_dict(
        self, artifacts_container: ArtifactsContainer, num_records: int
    ):
        """
        get the dictionary of original data id : actual data index
        """

        ids = np.rint(
            np.concatenate(self.get_ids(artifacts_container, num_records), 0)
        ).astype(int)
        return {k: v for k, v in zip(ids, np.arange(len(ids)))}

    def get_tokens(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset=0
    ):
        name = 'id_to_token'
        id_to_token = MemUtil.get_pickle(artifacts_container, name)

        data = np.concatenate(
            self.get_data(artifacts_container, num_records, offset=offset), 0
        )
        tokens = []
        for d in data:
            tokens.append([id_to_token[int(di)] for di in d])
        return tokens

    def has_words(self, artifacts_container: ArtifactsContainer):
        """ Returns whether words were ingested. Ingestion of words is determined on if spans were provided.

        Args:
            artifacts_container (ArtifactsContainer): The artifact metadata.

        Returns:
            bool: True if words were ingested, False otherwise.
        """
        name = 'index_mappings'
        word_mappings = MemUtil.get_pickle(artifacts_container, name)
        if len(word_mappings) > 0:
            return True
        else:
            return False

    def get_words(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset=0
    ) -> Tuple[List[List[str]], List[int]]:
        """ Returns the words in each sentence, and the number of words in each sentence.

        Args:
            artifacts_container (ArtifactsContainer): The artifact metadata.
            num_records (int): The number of records to use.
            offset (int, optional): The offset of the records to use. Defaults to 0.

        Returns:
            Tuple[List[List[str]], List[int]]: For each record, return the words and the lengths
        """
        name = 'words'
        try:  #### TODO: for now there is a difference in the format between the covid artifact and the yelp artifact in the azure,
            ###will convert everything to pickle once the renewed artifacts for covid are uploaded
            words = MemUtil.get_pickle(
                artifacts_container, name, num_records, offset=offset
            )
        except:
            word_list = MemUtil.get_text(
                artifacts_container, name, num_records, offset=offset
            )
            # unsure if this is still needed
            words = [s.split() for s in word_list]
            # words = word_list

        sentence_lengths_words = np.array(list(map(len, words)))
        return words, sentence_lengths_words

    def get_probits_or_regression(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset=0
    ):
        name = 'preds'
        return MemUtil.get(
            artifacts_container, name, num_records, offset=offset
        )

    def get_logits(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset=0
    ):
        probits = self.get_probits_or_regression(
            artifacts_container, num_records, offset
        )
        return logit(probits)

    def get_predictions(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset=0
    ):
        return [
            np.argmax(x, -1).astype('int32')
            for x in self.get_logits(artifacts_container, num_records, offset)
        ]

    def get_lengths(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset=0
    ):
        name = 'sentence_length_tokens'
        return MemUtil.get(
            artifacts_container, name, num_records, offset=offset
        )

    def get_ground_truth(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset=0
    ):
        name = 'targets'
        return [
            x.astype('int32') for x in
            MemUtil.get(artifacts_container, name, num_records, offset=offset)
        ]

    def get_segments(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset=0
    ):
        name = 'segments'
        return [
            x.astype('int32') for x in
            MemUtil.get(artifacts_container, name, num_records, offset=offset)
        ]

    @cache_results('occurrences')
    def get_occurrences(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset=0
    ):
        num_tokens = self.get_num_tokens(artifacts_container)
        occurrences = np.zeros(num_tokens)

        data = self.get_data(artifacts_container, num_records,
                             offset=offset)[0].astype(int)

        # weight each datapoint by a unique imaginary value
        # the same word in within a datapoint will have the same value but the same words between different data points will have different values
        weighted_data = data + (1j * np.arange(len(data)))[:, np.newaxis]
        # find unique values to isolate unique words in each datapoint
        unique_words = np.real(np.unique(weighted_data)).astype(int)

        np.add.at(occurrences, unique_words, 1)

        return occurrences

    def get_frequencies(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset=0
    ):
        frequencies = self.get_occurrences(
            artifacts_container, num_records, offset=offset
        ) / num_records

        return frequencies

    @cache_results('token_occurrences_dict')
    def get_token_occurrences_dict(
        self, artifacts_container: ArtifactsContainer
    ):
        name = 'token_occurrence'
        return MemUtil.get_pickle(artifacts_container, name)

    @cache_results('word_occurrences_dict')
    def get_word_occurrences_dict(
        self, artifacts_container: ArtifactsContainer
    ):
        name = 'word_occurrence'
        return MemUtil.get_pickle(artifacts_container, name)

    def get_vocab(self, artifacts_container: ArtifactsContainer):
        name = 'token_to_id'
        token_to_id = MemUtil.get_pickle(artifacts_container, name)
        return [
            entry[0]
            for entry in sorted(token_to_id.items(), key=lambda item: item[1])
        ]

    @cache_results('num_tokens')
    def get_num_tokens(self, artifacts_container: ArtifactsContainer):
        return len(self.get_vocab(artifacts_container))

    def get_influences(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset=0,
    ):
        name = QoIType.CLASS_WISE.get_attr_artifact_save_name()
        return MemUtil.get(
            artifacts_container, name, num_records, offset=offset
        )

    def get_activations(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset=0,
    ):
        name = 'activations'
        return MemUtil.get(
            artifacts_container, name, num_records, offset=offset
        )

    def get_baseline_activations(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset=0,
    ):
        name = 'baseline_activations'
        return MemUtil.get(
            artifacts_container, name, num_records, offset=offset
        )

    def get_grad_path_influences(
        self,
        artifacts_container: ArtifactsContainer,
        *,
        num_records: int,
        token_type: TokenType,
        offset: int = 0,
        class_idx: int = -1,
    ) -> Sequence[np.ndarray]:
        """
        Get the gradients per DoI per sentence.

        Args:
            artifacts_container (ArtifactsContainer): The artifact metadata.
            num_records (int): The number of records to take
            token_type (TokenType): Whether to get gradient paths per word or token
            offset (int): The starting point of records to take
            class_idx (int): the index of the class

        Returns:
            list[np.ndarray]: The list holds gradient paths per record. The gradient paths are np.ndarray of size timestep x resolution
        """
        if token_type == TokenType.TOKEN:
            name = QoIType.CLASS_WISE.get_attr_artifact_save_name(
            ) + '_grad_path'
            lengths = self.get_lengths(
                artifacts_container, num_records, offset=offset
            )[0].astype(int)
        elif token_type == TokenType.WORD:
            name = QoIType.CLASS_WISE.get_attr_artifact_save_name(
            ) + '_grad_path_original_word'
            _, lengths = self.get_words(
                artifacts_container, num_records, offset
            )
        # num_records x (num_classes x) num_steps x num_words
        grad_path_influences = MemUtil.get(
            artifacts_container, name, num_records, offset=offset
        )[0]

        # take selected class if multiple classes are given
        # num_records x num_words x resolution
        # TODO: check if class_idx = -1 has maybe unintended meaning here?
        grad_path_influences = grad_path_influences[:, class_idx]

        length_adjusted_grad_paths = []
        for length, grad_path in zip(lengths, grad_path_influences):
            grad_path = grad_path[:length, :]
            length_adjusted_grad_paths.append(grad_path)
        return length_adjusted_grad_paths

    def get_correlation_matrices(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        token_type: TokenType,
        offset=0,
        class_idx=-1,
        filter_top_n: int = -1
    ):
        '''
        Gets the correlation matrices of token to token, using the pearson correlation on the token grad paths

        =========
        returns:
            corrcoef - the correlation matrix
            idx_mapping - a mapping of the correlation matrix indices to a token index.
                          usually 1:1 unless a top_n filter was applied or a token has no influence change.
        '''
        grad_path_influences = self.get_grad_path_influences(
            artifacts_container,
            num_records=num_records,
            token_type=token_type,
            offset=offset,
            class_idx=class_idx
        )

        return SpectralHierarchicalClusterer._get_correlation_matrices(
            grad_path_influences, filter_top_n=filter_top_n
        )

    def get_influences_word_combined(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset=0,
    ):
        name = QoIType.CLASS_WISE.get_attr_artifact_save_name()
        return MemUtil.get(
            artifacts_container,
            name + '_original_word',
            num_records,
            offset=offset
        )

    def get_segment_ind_dict(
        self,
        artifacts_container: ArtifactsContainer,
        binarize_data: bool = False,
        positive_group: Sequence[int] = None,
    ) -> Dict[str, Any]:
        """
        get a dictionary of output metrics indices divided into each segment group
        """
        segment_id_to_name = self.get_segment_id_to_name(artifacts_container)

        metrics = [
            OutputMetrics.CONFUSION_MATRIX,
            OutputMetrics.CONFUSION_MATRIX_METRICS, OutputMetrics.ACCURACY,
            OutputMetrics.F1_SCORE
        ]

        num_records = self.get_default_num_records(artifacts_container)

        # MULTI-CLASS DATA
        targets = list(
            self.get_ground_truth(artifacts_container, num_records)[0]
        )
        preds = list(self.get_predictions(artifacts_container, num_records)[0])
        segments = list(self.get_segments(artifacts_container, num_records)[0])

        if not binarize_data:
            multi_class_segmented_data = segment_all_data(
                targets, preds, segments
            )

            num_classes = np.max(targets) + 1

            multi_class_segment_metrics_dict = get_segment_metrics_dict(
                multi_class_segmented_data, segment_id_to_name, metrics,
                num_classes
            )
            segment_metrics_dict = multi_class_segment_metrics_dict

        # BINARY DATA
        else:
            if positive_group is None:
                return

            binary_targets = np.array(
                [int(x in positive_group) for x in targets]
            ).astype(np.int32)
            binary_preds = np.array([int(x in positive_group) for x in preds]
                                   ).astype(np.int32)

            binary_segmented_data = segment_all_data(
                binary_targets, binary_preds, segments
            )

            num_classes = 2

            binary_segment_metrics_dict = get_segment_metrics_dict(
                binary_segmented_data, segment_id_to_name, metrics, num_classes
            )

            segment_metrics_dict = binary_segment_metrics_dict

        return segment_metrics_dict

    def get_segment_id_to_name(
        self,
        artifacts_container: ArtifactsContainer,
    ) -> Sequence[str]:
        segment_map = MemUtil.get_pickle(
            artifacts_container, "segment_keywords"
        )
        segment_id_to_name = sorted(list(segment_map.keys()))
        return segment_id_to_name

    def get_segment_name_to_point_id_dict(
        self,
        artifacts_container: ArtifactsContainer,
    ) -> Dict[str, Any]:
        """
        get a dictionary of output metrics indices divided into each segment group
        """
        segment_id_to_name = self.get_segment_id_to_name(artifacts_container)
        num_records = self.get_default_num_records(artifacts_container)
        segments = list(self.get_segments(artifacts_container, num_records)[0])
        segment_name_to_point_id = defaultdict(list)
        for point_id, segment_id in enumerate(segments):
            segment_name = segment_id_to_name[int(segment_id)]
            segment_name_to_point_id[segment_name].append(point_id)
        return segment_name_to_point_id

    @cache_results('group_inds')
    def get_group_ind_dict(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        offset=0
    ):
        """
        get a dictionary of data indices divided into each accuracy-based group
        """
        targets = np.concatenate(
            self.get_ground_truth(artifacts_container, num_records, offset), 0
        )
        preds = np.concatenate(
            self.get_predictions(artifacts_container, num_records, offset), 0
        )
        num_classes = self.get_num_classes(artifacts_container)
        # Typically we treat binary as a single class. But for confusion matrix, we need to break it out
        num_classes = max(num_classes, 2)

        accuracy_group_name_dict = get_accuracy_group_name_dict(num_classes)
        group_ind_dict = {}

        for target in range(num_classes):
            for pred in range(num_classes):
                group_ind_dict[
                    accuracy_group_name_dict[(target, pred)]
                ] = np.where((preds == pred) & (targets == target))[0]
        group_ind_dict['All'] = np.arange(len(preds))
        return group_ind_dict

    def get_artifacts_metadata(
        self,
        artifacts_container: ArtifactsContainer,
        *,
        token_type: TokenType,
        num_records: int,
        offset: int = 0
    ) -> Tuple[np.ndarray]:
        """
        Gets the numpy arrays of various information from the artifacts. Each array's first dimension correspond to records.

        Args:
            artifacts_container (ArtifactsContainer): The artifact metadata.
            token_type (TokenType): Whether to get gradient paths per word or token
            num_records (int): The number of records to take
            offset (int): The starting point of records to take

        Returns:
            Tuple[np.ndarray]: Returns tokens, influences, influences_comparative, lengths, preds, labels, ids, data_ids
        """
        num_classes = self.get_num_classes(artifacts_container)
        labels = np.concatenate(
            self.get_ground_truth(artifacts_container, num_records, offset), 0
        ).astype(np.int32)

        preds = np.concatenate(
            self.get_predictions(artifacts_container, num_records, offset), 0
        ).astype(np.int32)

        if token_type == TokenType.TOKEN:
            tokens = self.get_tokens(artifacts_container, num_records, offset)
            influences = np.concatenate(
                self.get_influences(
                    artifacts_container, num_records, offset=offset
                ), 0
            )
            lengths = np.concatenate(
                self.get_lengths(
                    artifacts_container, num_records, offset=offset
                ), 0
            ).astype(np.int32)

        elif token_type == TokenType.WORD:
            tokens, lengths = self.get_words(
                artifacts_container, num_records, offset
            )
            influences = np.concatenate(
                self.get_influences_word_combined(
                    artifacts_container, num_records, offset=offset
                ), 0
            )

        ids = np.rint(
            np.concatenate(
                self.get_ids(artifacts_container, num_records, offset), 0
            )
        ).astype(np.int32)

        data_ids = np.arange(offset, offset + num_records)

        # Standardize label/preds records to match with influences
        labels = labels[:len(influences)]
        preds = preds[:len(influences)]
        tokens = tokens[:len(influences)]
        lengths = lengths[:len(influences)]
        ids = ids[:len(influences)]
        data_ids = data_ids[:len(influences)]

        if labels.max() > num_classes:
            raise RuntimeError(
                f"Received more labels ({labels.max()+1}) than there are classes ({num_classes})."
            )
        if num_classes == 1:
            influences_comparative = np.squeeze(influences, axis=1)
        else:
            all_labels = np.arange(num_classes)[None, :].repeat(len(labels), 0)

            non_labels = all_labels[(all_labels - labels[:, None]) != 0
                                   ].reshape(len(labels), -1)

            # influences_comparative is the influence of the label class minues the nonlabel classes
            # It is used for sorting in some downstream cases.
            influences_comparative = influences[
                np.arange(len(influences)),
                labels] - influences[np.arange(len(influences))[:, None].
                                     repeat(num_classes - 1, -1),
                                     non_labels].mean(1)

        return tokens, influences, influences_comparative, lengths, preds, labels, ids, data_ids

    def get_artifacts_df(
        self,
        artifacts_container: ArtifactsContainer,
        *,
        token_type: TokenType,
        num_records: int,
        offset=0
    ):
        """
        local influences df, each row representing one instance
        """
        tokens, influences, influences_comparative, lengths, preds, labels, ids, data_ids = self.get_artifacts_metadata(
            artifacts_container,
            token_type=token_type,
            num_records=num_records,
            offset=offset
        )
        df = {}
        # Add unparsed text here?
        df['tokens'] = list(tokens)
        df['influences'] = list(influences)
        df['influences_comparative'] = list(influences_comparative)
        df['lengths'] = lengths
        df['preds'] = preds
        df['labels'] = labels
        df['original_index'] = ids
        df['data_index'] = data_ids
        return pd.DataFrame(df)

    def is_counterfactual(self, artifacts_container):
        # naive check to see if an artifacts container is a counterfactual split
        return '_counterfactual' in artifacts_container.get_path()

    def get_joined_df(
        self,
        artifacts_container: ArtifactsContainer,
        *,
        token_type: TokenType,
        num_records: int,
        offset: int = 0,
        df: Optional[pd.DataFrame] = None
    ) -> pd.DataFrame:
        """
        Joins the generated counterfactual dataset.csv or a dataframe with Text and Labels
        with the artifacts (preds, labels, influences...)

        Args:
            artifacts_container (ArtifactsContainer): The artifact metadata.
            token_type (TokenType): The tokenization unit. Either TokenType.TOKEN or TokenType.WORD
            num_records (int): The number of records to return.
            offset (int): A record id to offset the start of the data.
            df (pd.DataFrame): If this is supplied, it is the non-counterfactual dataframe with Text and Labels.
                Otherwise, read the generated counterfactual data.


        Returns:
            pd.DataFrame: A DataFrame joined on the record ids containing Text, Labels, Influences
        """
        df_cf = self.get_artifacts_df(
            artifacts_container,
            token_type=token_type,
            num_records=num_records,
            offset=offset
        ).rename(columns={
            "original_index": "aug_index"
        }).set_index('aug_index')

        # The CF methods generate a new a data split in CF folder and call it dataset.csv.
        if df is None:
            df_name = 'dataset'

            df_cf_metadata = MemUtil.get_df_from_csv(
                artifacts_container, df_name
            )
        else:
            df_cf_metadata = df
        df_cf_joined = df_cf.join(df_cf_metadata)
        df_cf_joined.Text = df_cf_joined.tokens.apply(lambda x: ' '.join(x))
        return df_cf_joined

    def _aggregate_by_token(
        self, tokens: list, influences: np.ndarray,
        influences_comparative: np.ndarray, lengths: np.ndarray,
        preds: np.ndarray, labels: np.ndarray, data_ids: np.ndarray
    ):
        df = {}
        df['data_index'] = np.repeat(data_ids, lengths)
        df['token_pos'] = multirange(lengths)
        df['lengths'] = np.repeat(lengths, lengths)
        df['preds'] = np.repeat(preds, lengths)
        df['labels'] = np.repeat(labels, lengths)
        df['tokens'] = np.array(
            list(itertools.zip_longest(*tokens, fillvalue=''))
        )[df['token_pos'], df['data_index']]
        df['influences_comparative'] = influences_comparative[df['data_index'],
                                                              df['token_pos']]

        classwise_influences = influences[df['data_index'], :,
                                          df['token_pos']].T
        num_class = classwise_influences.shape[0]
        for cl_name, cw_influence in zip(
            QoIType.CLASS_WISE.get_qoi_type_widget_options(num_class),
            classwise_influences
        ):
            df['influences_{}'.format(cl_name)] = cw_influence

        return pd.DataFrame(df)

    def get_token_influences_df(
        self,
        artifacts_container: ArtifactsContainer,
        token_type: TokenType,
        num_records: int,
        offset=0
    ):
        tokens, influences, influences_comparative, lengths, preds, labels, _, data_ids = self.get_artifacts_metadata(
            artifacts_container,
            token_type=token_type,
            num_records=num_records,
            offset=offset
        )
        return self._aggregate_by_token(
            tokens, influences, influences_comparative, lengths, preds, labels,
            data_ids
        )

    def filter_token_influences_df(
        self,
        token_influence_df: pd.DataFrame,
        group_inds: np.ndarray,
        max_words_to_track: int,
        two_tailed=False,
        filter_func=lambda x: np.ones(len(x), dtype=bool),
        ranking_col_name='occurrences',
        ascending=False
    ):
        """
        filter and rank token_influence df based on influence and
        append other metadata such as average influence and occurrences.
        two_tailed: how to select top max_words_to_track in the ranked df. if True,
        select evenly from both ends
        """
        token_influence_filtered_df = token_influence_df[
            token_influence_df.data_index.isin(group_inds)]
        token_influence_filtered_df = token_influence_filtered_df[
            filter_func(token_influence_filtered_df)]
        influence_cols = [
            cn for cn in token_influence_filtered_df.columns
            if 'influence' in cn
        ]
        token_influence_filtered_df = token_influence_filtered_df.groupby(
            ['tokens']
        ).agg(lambda x: list(x)).reset_index()
        for c in influence_cols:
            token_influence_filtered_df[
                c + '_mean'] = token_influence_filtered_df[c].apply(np.mean)
            token_influence_filtered_df[
                c + '_std'] = token_influence_filtered_df[c].apply(np.std)
        token_influence_filtered_df[
            'word_occurrences'] = token_influence_filtered_df.data_index.apply(
                len
            )
        token_influence_filtered_df[
            'word_frequencies'] = token_influence_filtered_df[
                'word_occurrences'] / len(token_influence_df)
        token_influence_filtered_df[
            'occurrences'] = token_influence_filtered_df.data_index.apply(
                lambda x: len(set(x))
            )
        if (len(token_influence_filtered_df) == 0):
            token_influence_filtered_df[
                'frequencies'] = token_influence_filtered_df['occurrences']
        else:
            token_influence_filtered_df[
                'frequencies'
            ] = token_influence_filtered_df['occurrences'] / len(
                np.unique(
                    np.concatenate(token_influence_filtered_df.data_index)
                )
            )
        token_influence_filtered_df = token_influence_filtered_df.sort_values(
            by=ranking_col_name, ascending=ascending
        )
        num_vocab = len(token_influence_filtered_df)
        max_words_to_track = min(max_words_to_track, num_vocab)
        if two_tailed:
            return pd.concat(
                [
                    token_influence_filtered_df.
                    iloc[:int(max_words_to_track / 2)],
                    token_influence_filtered_df.
                    iloc[-int(max_words_to_track / 2):]
                ],
                axis=0
            )
        else:
            return token_influence_filtered_df.iloc[:int(max_words_to_track)]

    def get_text_examples_df(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        tokens: list,
        max_num_examples_per_token: int,
        token_type: TokenType,
        offset=0
    ):
        """
        extract a df of training examples (as well as number of such examples) for a list of tokens [tokens] for both classes.
        max_num_examples_per_token specifies the max number of examples per token
        """
        if token_type == TokenType.TOKEN:
            token_occurrences_dict = self.get_token_occurrences_dict(
                artifacts_container
            )
        elif token_type == TokenType.WORD:
            token_occurrences_dict = self.get_word_occurrences_dict(
                artifacts_container
            )
        ids_reverse_dict = self.get_ids_reverse_dict(
            artifacts_container, num_records
        )
        num_classes = self.get_num_classes(artifacts_container)
        token_occurrences_dict = defaultdict(
            lambda: [[] for _ in range(num_classes)], token_occurrences_dict
        )

        text = self.get_original_text(
            artifacts_container, num_records, offset=offset
        )
        text_examples_dfs = []
        for c in range(num_classes):
            text_examples_df = defaultdict(list)
            for t in tokens:
                tinds = token_occurrences_dict[t]
                for i in range(min(len(tinds[c]), max_num_examples_per_token)):
                    text_examples_df['tokens'].append(t)
                    text_examples_df['occurrences'].append(len(tinds[c]))
                    text_examples_df['examples'].append(
                        text[ids_reverse_dict[tinds[c][i]]]
                    )
            text_examples_dfs.append(pd.DataFrame(dict(text_examples_df)))
        return text_examples_dfs
