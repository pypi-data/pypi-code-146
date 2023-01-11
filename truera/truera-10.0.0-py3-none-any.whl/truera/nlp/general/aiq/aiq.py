from typing import Any, Dict, Iterable, Sequence, Tuple, TypeVar

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import binarize
from tqdm import tqdm

from truera.nlp.general.container.model import NLPModelProxy
from truera.nlp.general.model_runner_proxy.nlp_counterfactuals import \
    match_counterfactual_artifacts
from truera.nlp.general.utils.configs import QoIType
from truera.nlp.general.utils.configs import TokenType
from truera.rnn.general.aiq import AIQ
from truera.rnn.general.aiq.clustering import SpectralHierarchicalClusterer
from truera.rnn.general.container import artifacts
from truera.rnn.general.container import ArtifactsContainer

# sentence_idx -> (sentence_info_df, words)
SentenceInfo = TypeVar(
    'SentenceInfo', bound=Dict[int, Tuple[pd.DataFrame, Iterable[str]]]
)


class NlpAIQ(AIQ):

    def __init__(self, model: NLPModelProxy):
        super().__init__(model)
        self.model = model

    def feature_interaction_dendrogram_info(
        self,
        artifacts_container: ArtifactsContainer,
        num_records: int,
        token_type: TokenType,
        class_idx: int = -1,
        offset: int = 0,
        filter_top_n: int = -1
    ) -> SentenceInfo:
        '''
        Takes sentences in the given artifact container from index offset to offset + num_records.
        Build a spectral coclustering-based binary tree of each sentence, and return a dataframe that contains
        (1) tree structure (parent, ancestors of each node)
        (2) link to original sentence (token indexes in the original sentence)
        '''
        corrs, corr_idx_mapping = self.model.get_correlation_matrices(
            artifacts_container,
            num_records,
            class_idx=class_idx,
            token_type=token_type,
            offset=offset,
            filter_top_n=filter_top_n
        )
        if token_type == TokenType.TOKEN:
            tokens = self.model.get_tokens(
                artifacts_container, num_records, offset=offset
            )
            lengths = self.model.get_lengths(
                artifacts_container, num_records, offset=offset
            )[0].astype(int)

        elif token_type == TokenType.WORD:
            tokens, lengths = self.model.get_words(
                artifacts_container, num_records, offset
            )
        return SpectralHierarchicalClusterer.interaction_dendrogram_info(
            corrs,
            corr_idx_mapping,
            tokens,
            num_records=num_records,
            offset=offset
        )

    def gradient_landscape_info(
        self,
        artifacts_container: ArtifactsContainer,
        num_records,
        token_type: TokenType,
        class_idx=-1,
        offset=0,
    ) -> SentenceInfo:
        '''
        Takes sentences in the given artifact container from index offset to offset + num_records.
        Returns the gradient landscape for each sentence, building a dataframe where
        - each column corresponds to a token index
        - each row corresponds to a specific step number
        in the gradient attribution interpolation
        '''

        grad_path_influences = self.model.get_grad_path_influences(
            artifacts_container,
            num_records=num_records,
            class_idx=class_idx,
            offset=offset,
            token_type=token_type
        )

        if token_type == TokenType.TOKEN:
            tokens = self.model.get_tokens(
                artifacts_container, num_records, offset=offset
            )
            lengths = self.model.get_lengths(
                artifacts_container, num_records, offset=offset
            )[0].astype(int)

        elif token_type == TokenType.WORD:
            tokens, lengths = self.model.get_words(
                artifacts_container, num_records, offset
            )

        return_dfs = {}
        for idx, length, sent, grad_path in zip(
            range(offset, offset + num_records), lengths, tokens,
            grad_path_influences
        ):

            idx_sent = [
                f'{idx}: {word}' for idx, word in enumerate(sent[:length])
            ]
            return_dfs[idx] = pd.DataFrame(
                data=grad_path[:length].T, columns=idx_sent
            ), sent[:length]
        return return_dfs

    def segment_output_metrics_info(
        self,
        artifacts_container: ArtifactsContainer,
    ) -> Dict[str, Any]:
        """ 
        get a output metrics for each segment group in a dictionary
        """
        multi_class_segments_dict = self.model.get_segment_ind_dict(
            artifacts_container=artifacts_container, binarize_data=False
        )
        return multi_class_segments_dict

    def get_influences_df(
        self,
        artifacts_container: ArtifactsContainer,
        token_type: TokenType,
        num_records: int,
        offset=0
    ) -> pd.DataFrame:
        return self.model.get_artifacts_df(
            artifacts_container,
            token_type=token_type,
            num_records=num_records,
            offset=offset
        )

    def global_explanations_error_driver_info(
        self,
        artifacts_container_val: ArtifactsContainer,
        num_records: int,
        max_words_to_track: int,
        offset=0,
        token_type=TokenType.TOKEN,
        ranking='influence'
    ):
        """
        get token df of each accuracy-based groups and 
        (1) filter error driver tokens, 
        (2) rank tokens according to their influence or occurrences, 
        """
        group_ind_dict = self.model.get_group_ind_dict(
            artifacts_container_val, num_records, offset
        )

        def get_filter_func(group_name: str):
            if group_name != 'All':
                return lambda df: df.influences_comparative < 0
            else:
                return lambda df: np.ones(len(df), dtype=bool)

        token_influence_df = self.model.get_token_influences_df(
            artifacts_container_val, token_type, num_records, offset
        )
        token_influences_group_dict = {}

        if ranking == 'occurrence':
            ranking_col_name = 'occurrences'
            two_tailed = False
            ascending = False
        elif ranking == 'frequency':
            ranking_col_name = 'frequencies'
            two_tailed = False
            ascending = False
        elif ranking == 'influence':
            ranking_col_name = 'influences_comparative_mean'
            ascending = True
        for group_name, group_inds in group_ind_dict.items():
            if group_name == 'all' and ranking == 'influence':
                two_tailed = True
            elif group_name != 'All' and ranking == 'influence':
                two_tailed = False
            token_influences_group_dict[
                group_name] = self.model.filter_token_influences_df(
                    token_influence_df,
                    group_inds,
                    filter_func=get_filter_func(group_name),
                    two_tailed=two_tailed,
                    max_words_to_track=max_words_to_track,
                    ranking_col_name=ranking_col_name,
                    ascending=ascending
                )
        return token_influences_group_dict

    def model_robustness_info(
        self,
        artifacts_container: ArtifactsContainer,
        artifacts_container_cf: ArtifactsContainer,
        *,
        num_records: int,
        num_records_cf: int,
        offset=0,
        mask_token='[MASK]',
        token_type=TokenType.TOKEN
    ):
        """
        extract 3 dfs combining original data artifacts and counterfactual perturbation (1-gram) artifacts
        (1) the df containing the text and swapping metadata
        (2) the local influence df of original data
        (3) the local influence df of counterfactual data 
        all 3 dfs matches in indices.
        """
        df_dict = {
            'Text':
                self.model.get_original_text(artifacts_container, num_records),
        }

        df_original = pd.DataFrame(df_dict)

        df_joined = self.model.get_joined_df(
            artifacts_container,
            token_type=token_type,
            num_records=num_records,
            offset=offset,
            df=df_original
        )
        df_joined_cf = self.model.get_joined_df(
            artifacts_container_cf,
            token_type=token_type,
            num_records=num_records_cf,
            offset=offset
        )

        text_df = df_joined_cf[[
            'MaskedText', 'word_from', 'word_to', 'coherence_score', 'preds',
            'original_index', 'tokens', 'influences', 'lengths', 'labels'
        ]].join(
            df_joined[[
                'Text', 'preds', 'labels', 'data_index', 'tokens', 'influences',
                'lengths'
            ]],
            on='original_index',
            lsuffix='_cf'
        )[[
            'data_index', 'original_index', 'MaskedText', 'Text', 'word_from',
            'word_to', 'coherence_score', 'preds', 'preds_cf', 'labels',
            'labels_cf', 'tokens', 'tokens_cf', 'influences', 'influences_cf',
            'lengths', 'lengths_cf'
        ]]

        text_df = text_df[text_df['Text'].notna()]
        if len(text_df) == 0:
            print("No good coherence counterfactuals found in current set.")
            return None, None, None

        text_df['mask_pos'] = text_df.MaskedText.apply(
            lambda s: s.split().index(mask_token)
        )
        text_df = match_counterfactual_artifacts(text_df)

        return text_df
