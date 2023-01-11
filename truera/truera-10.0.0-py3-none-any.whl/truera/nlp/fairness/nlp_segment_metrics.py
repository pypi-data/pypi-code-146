from collections import defaultdict

import cloudpickle
import numpy as np
import pandas as pd
from scipy.stats import wasserstein_distance

from truera.nlp.general.aiq.aiq import NlpAIQ
from truera.nlp.general.utils.configs import QoIType
from truera.nlp.general.utils.configs import TokenType
from truera.nlp.general.utils.language_utils import remove_stop_words
from truera.rnn.general.container import ArtifactsContainer


class NLPSegmentMetrics():

    def __init__(
        self, aiq: NlpAIQ, artifacts_container: ArtifactsContainer,
        token_type: TokenType.WORD
    ):
        self.aiq = aiq
        self.num_records = self.aiq.model.get_default_num_records(
            artifacts_container
        )

        self.influences_df = self.aiq.model.get_artifacts_df(
            artifacts_container,
            num_records=self.num_records,
            token_type=token_type
        )

        self.segment_name_to_point_id = self.aiq.model.get_segment_name_to_point_id_dict(
            artifacts_container
        )
        self.segment_tokens = defaultdict(set)
        self.influences_dict = defaultdict(lambda: defaultdict(list))
        self.token_frequency = defaultdict(set)
        self.language = 'english'

    def compute_influences_dict(self, class_id: int, segment_name: str) -> None:
        """
        Store all the tokens and the influence values for a particular segment and class id
        Args:
            - class_id (int): Class ID
            - segment_name (str): Segment name for which we need influences
        Returns:
                None. Variables are stored in class
        """
        segment_ids = self.segment_name_to_point_id[segment_name]
        for i in segment_ids:
            len_of_sentence = self.influences_df.iloc[i]['lengths']
            for j in range(len_of_sentence):
                token = self.influences_df.iloc[i]['tokens'][j]
                self.token_frequency[token].add(i)
                self.segment_tokens[segment_name].add(token)
                self.influences_dict[class_id, segment_name][token].append(
                    self.influences_df.iloc[i]['influences'][class_id][j]
                )

    def get_segment_tokens_and_influences(
        self,
        class_id: int,
        segment_one_name: str,
        segment_two_name: str,
    ) -> tuple([dict, dict, dict]):
        '''
        Given 2 segments, get all the tokens present in all the examples in those 2 segments. 
        Also, get all the influence vector for each token in each segment.
        Args:
            - class_id (int): Class ID
            - segment_one_name (str): The first segment 
            - segment_two_name (str): The second segment
        Returns:
            - Segment tokens (Dict): A dictionary with the segment names as keys and all the tokens in that segment as values
            - Influences (Dict): A dictionary where token, class id and segment name as keys and the influence list as values
            - Token Frequency (Dict): A dictionary where the tokens are the keys and the no of reviews they are present are the values
        '''
        # To avoid re-appending to the initialized dicts in case they get created
        if not self.influences_dict[class_id, segment_one_name]:
            self.compute_influences_dict(class_id, segment_one_name)
        if not self.influences_dict[class_id, segment_two_name]:
            self.compute_influences_dict(class_id, segment_two_name)

        return (self.segment_tokens, self.influences_dict, self.token_frequency)

    def compute_token_wasserstein(
        self, class_id: int, token: str, segment_one_name: str,
        segment_two_name: str, token_cutoff_threshold: int,
        total_no_of_reviews: int
    ) -> tuple([float, int, int, int, float]):
        """
        Given a class_id, a particular token, calculate the token Wasserstein distance
        for that particular class id and token i.e the work taken to move that token
        from segment one to segment two.
        
        If the token is not present in either of the segments, initialise it to 0 
        (heuristic: There is one token) and calculate token wasserstein
        Args:
            - class_id (int): Class ID
            - token (str): Token 
            - segment_one_name (str): The first segment 
            - segment_two_name (str): The second segment
            - token_cutoff_threshold (int): The threshold used to decide whether a token is important or not
            - total_no_of_reviews (int): Total no of reviews present in both segments
              
        Returns:
            - Float : The token wasserstein distance
            - Int: The token weight computed using tf-idf (tf*idf)
            - Int: Tf term --> Token frequency
            - Int: Idf term
            - Float: Unnormalized token wasserstein distance
        """
        dist1 = self.influences_dict[class_id, segment_one_name][token]
        dist2 = self.influences_dict[class_id, segment_two_name][token]
        len_dist1, len_dist2 = len(dist1), len(dist2)

        # If the token is not present in either of the segment, we followed this heuristic:
        # Assume that token is present once in that segment, so the length of that distribution is 1
        # The influence of that token is 0 (neither +ve nor -ve). Also updating the influences dictionary as well.

        if len_dist1 == 0:
            len_dist1 = 1
            self.influences_dict[class_id, segment_one_name][token].append(0)
            dist1 = [0]

        elif len_dist2 == 0:
            len_dist2 = 1
            self.influences_dict[class_id, segment_two_name][token].append(0)
            dist2 = [0]

        token_total_len = len_dist1 + len_dist2
        if (token_total_len) < token_cutoff_threshold:
            '''
            If the number of combined tokens is less than token_cutoff_threshold, 
            we can assume it doesn't influence much and thus discard it
            '''
            return 0, 0, 0, 0, 0

        # Normalizing factor calculated using tf-idf algorithm. Logarithm is taken as it dampens when there are lots of reviews
        # IDF can be negative if denominator is larger. So, take only absolute value
        idf_term = abs(
            round(
                np.log(
                    total_no_of_reviews /
                    (1 + len(self.token_frequency[token]))
                ), 5
            )
        )
        token_weight = token_total_len * idf_term
        unnormalized_token_wasserstein_dist = round(
            wasserstein_distance(dist1, dist2), 5
        )
        token_wasserstein_dist = token_weight * unnormalized_token_wasserstein_dist

        return token_wasserstein_dist, token_weight, token_total_len, idf_term, unnormalized_token_wasserstein_dist

    def preprocess_remove_stop_words(
        self, segment_one_name, segment_two_name
    ) -> list:
        """
        Given the segment names, remove all the stop words present in both the segment tokens using NLTK remove_stop_words() function
        
        Args:
            - segment_one_name (str): The first segment 
            - segment_two_name (str): The second segment
              
        Returns:
            - List: A list with filtered tokens.
        """
        segment_tokens_filtered = self.segment_tokens[segment_one_name].union(
            self.segment_tokens[segment_two_name]
        )

        # Remove stop words using NLTK. Language is set to 'English' as it's the most common for reviews
        segment_tokens_filtered_sw_removed = remove_stop_words(
            self.language, segment_tokens_filtered
        )
        return segment_tokens_filtered_sw_removed

    def compute_total_wasserstein(
        self,
        class_id: int,
        segment_one_name: str,
        segment_two_name: str,
        save_to_pickle=False
    ) -> tuple([dict, dict, dict]):
        """
        Given a class_id, and the segments calculate the total Wasserstein distance
        for that particular class id i.e the work taken to move all the tokens
        from segment one to segment two.
        Args:
            - class_id (int): Class ID
            - segment_one_name (str): The first segment 
            - segment_two_name (str): The second segment
            - save_to_pickle (Boolean): Optional. Stores the dictionaries to pickle format if given True. Default is False
        Returns: The three dictionaries (Also stores them based on save_the_pickle flag)
            - Dict: The total Wasserstein
            - Dict: Token Wasserstein 
            - Dict: Token weights (tf*idf, tf, idf)
        """
        total_wasserstein = 0
        token_wasserstein_dict = defaultdict()
        total_wasserstein_dict = defaultdict()
        token_weight_dict = defaultdict()

        combined_sentences = self.segment_name_to_point_id[
            segment_one_name] + self.segment_name_to_point_id[segment_two_name]
        # Used for tf-idf calculation i.e this is similar to no of documents
        total_no_of_reviews = len(combined_sentences)

        # Note - We are not computing token wasserstein for stop words but are
        # including their occurances in the scaling factor as it's easier to compute.
        # Also, it's just a heuristic
        total_len = np.sum(self.influences_df['lengths'][combined_sentences])
        token_cutoff_threshold = int(total_len / 10000)

        segment_tokens_filtered_sw_removed = self.preprocess_remove_stop_words(
            segment_one_name, segment_two_name
        )

        for token in segment_tokens_filtered_sw_removed:
            token_wasserstein_dist, token_weight, tf, idf, unnormalized_token_wasserstein_dist = self.compute_token_wasserstein(
                class_id, token, segment_one_name, segment_two_name,
                token_cutoff_threshold, total_no_of_reviews
            )
            # Storing the tokens which has non zero Wasserstein distance
            # Keys are - token, class id, segment one and segment two names
            # Value is - Normalized token Wasserstein dist (based on tf-idf)
            if token_wasserstein_dist != 0:
                token_wasserstein_dict[token, class_id, segment_one_name,
                                       segment_two_name] = (
                                           token_wasserstein_dist,
                                           unnormalized_token_wasserstein_dist
                                       )
                total_wasserstein += token_wasserstein_dist
                token_weight_dict[token, class_id, segment_one_name,
                                  segment_two_name] = (token_weight, tf, idf)

        total_wasserstein = round(total_wasserstein / total_len, 5)
        total_wasserstein_dict[segment_one_name, segment_two_name,
                               class_id] = total_wasserstein
        token_wasserstein_dict = {
            k: (v[0] / total_len, v[1])
            for k, v in token_wasserstein_dict.items()
        }
        token_wasserstein_dict = dict(
            sorted(
                token_wasserstein_dict.items(),
                key=lambda item: item[1],
                reverse=True
            )
        )

        token_weight_dict = dict(
            sorted(
                token_weight_dict.items(),
                key=lambda item: item[1],
                reverse=True
            )
        )
        if save_to_pickle == True:
            with open(
                f'token_wasserstein_{segment_one_name}_{segment_two_name}_{class_id}.pkl',
                'wb'
            ) as handle:
                cloudpickle.dump(token_wasserstein_dict, handle)
            with open(
                f'total_wasserstein_{segment_one_name}_{segment_two_name}_{class_id}.pkl',
                'wb'
            ) as handle:
                cloudpickle.dump(total_wasserstein_dict, handle)
            with open(
                f'token_weight_{segment_one_name}_{segment_two_name}_{class_id}.pkl',
                'wb'
            ) as handle:
                cloudpickle.dump(token_weight_dict, handle)
        return total_wasserstein_dict, token_wasserstein_dict, token_weight_dict

    def difference_of_sums(
        self,
        class_id,
        segment_one_name,
        segment_two_name,
        save_to_pickle=False
    ) -> tuple([dict, dict, dict]):
        """
        Given a class_id, and the segments calculate the difference of sums 
        for that particular class id.
        Algorithm:
            1. Aggregate all the influence values of a segment (seg_one_all_infl_list, seg_two_all_infl_list)
            2. Get the min percentile from the absolute value of these two segment influence lists
            3. For every token influence, ignore the influence values which are less than this min percentile. 
            This produces a final list
            4. We have two variations of difference of sums
                4.1. Diff(Sum of absolute influence values of the final list/No of tokens in that segment)
                4.2. Diff(Sum of all the influences values of the final list/No of tokens in that segment)
            5. Based on the frequency of the token in both the segments, store it in a corresponding dictionary 
            (as it'll be easier for downstream analysis)
        Args:
            - class_id (int): Class ID
            - segment_one_name (str): The first segment 
            - segment_two_name (str): The second segment
            - save_to_pickle (Boolean): Optional. Stores the dictionaries to pickle format if given True. Default is False
        Returns: The three dictionaries (Also stores them based on save_the_pickle flag)
            - Dict: (diff_sum_both_seg_dict) Difference of sums dictionary for tokens that are prevalent in both segments
            - Dict: (diff_sum_seg_one_dict) Difference of sums dictionary for tokens that's prevalent in segment one
            - Dict: (diff_sum_seg_two_dict) Difference of sums dictionary for tokens that's prevalent in segment two
        """
        diff_sum_both_seg_dict, diff_sum_seg_one_dict, diff_sum_seg_two_dict = defaultdict(
        ), defaultdict(), defaultdict()
        seg_one_agg_infl_list, seg_two_agg_infl_list = [], []
        no_of_tokens_seg_one = len(self.segment_tokens[segment_one_name])
        no_of_tokens_seg_two = len(self.segment_tokens[segment_two_name])

        segment_tokens_filtered_sw_removed = self.preprocess_remove_stop_words(
            segment_one_name, segment_two_name
        )

        for token in segment_tokens_filtered_sw_removed:
            dist1 = self.influences_dict[class_id, segment_one_name][token]
            dist2 = self.influences_dict[class_id, segment_two_name][token]

            # Append all the influences to form an aggregated list
            seg_one_agg_infl_list = seg_one_agg_infl_list + dist1
            seg_two_agg_infl_list = seg_two_agg_infl_list + dist2

        # Take the 75th percentile on the aggregated list
        seg_one_agg_infl_list_abs = list(map(abs, seg_one_agg_infl_list))
        seg_two_agg_infl_list_abs = list(map(abs, seg_two_agg_infl_list))

        seg_one_percentile = np.percentile(seg_one_agg_infl_list_abs, 75)
        seg_two_percentile = np.percentile(seg_two_agg_infl_list_abs, 75)
        min_percentile = min(seg_one_percentile, seg_two_percentile)

        for token in segment_tokens_filtered_sw_removed:
            dist1 = self.influences_dict[class_id, segment_one_name][token]
            dist2 = self.influences_dict[class_id, segment_two_name][token]

            # Ignoring the low influences by taking only the tail values based on the min_percentile
            dist1 = [i for i in dist1 if abs(i) >= min_percentile]
            dist2 = [i for i in dist2 if abs(i) >= min_percentile]

            if len(dist1) == 0:
                dist1 = [0]
            if len(dist2) == 0:
                dist2 = [0]

            abs_dist1, abs_dist2 = list(map(abs, dist1)), list(map(abs, dist2))

            # Method 1 - Take the sum of ABSOLUTE values of the filtered influences
            # And normalize it with the no of tokens present in that segment
            diff_sum_abs = round(
                sum(abs_dist1) / no_of_tokens_seg_one -
                sum(abs_dist2) / no_of_tokens_seg_two, 7
            )
            # Method 2 - Take the sum of values of filtered influences
            diff_sum = round(
                sum(dist1) / no_of_tokens_seg_one -
                sum(dist2) / no_of_tokens_seg_two, 7
            )

            # If a token occurs more frequently in one segment over other, store it in a different dict (Easier for downstream tasks)
            # Default values set to - 5x times, 0.2x times
            dist_ratio = len(dist1) / len(dist2)
            MAJORITY_FACTOR = float(5)
            if dist_ratio >= MAJORITY_FACTOR:
                diff_sum_seg_one_dict[
                    token, class_id, segment_one_name,
                    segment_two_name] = (diff_sum_abs, diff_sum)
            elif dist_ratio <= 1 / MAJORITY_FACTOR:
                diff_sum_seg_two_dict[
                    token, class_id, segment_one_name,
                    segment_two_name] = (diff_sum_abs, diff_sum)
            else:
                diff_sum_both_seg_dict[
                    token, class_id, segment_one_name,
                    segment_two_name] = (diff_sum_abs, diff_sum)
        if save_to_pickle == True:
            with open(
                f'diff_sums_{segment_one_name}_{segment_two_name}_{class_id}.pkl',
                'wb'
            ) as handle:
                cloudpickle.dump(diff_sum_both_seg_dict, handle)
            with open(
                f'diff_sums_{segment_one_name}_{class_id}.pkl', 'wb'
            ) as handle:
                cloudpickle.dump(diff_sum_seg_one_dict, handle)
            with open(
                f'diff_sums_{segment_two_name}_{class_id}.pkl', 'wb'
            ) as handle:
                cloudpickle.dump(diff_sum_seg_two_dict, handle)
        return diff_sum_both_seg_dict, diff_sum_seg_one_dict, diff_sum_seg_two_dict
