"""nlp related module to help the analysis"""

from fuzzywuzzy import fuzz
import pandas as pd

def fuzzy_word_matching(word1_def, word2_def):
    """produce fuzz score for word matching"""
    fuzz_ratio = fuzz.token_set_ratio(word1_def, word2_def)
    return fuzz_ratio

def fuzzy_word_list_matching(word1_def, word2_in_list_def):
    """produce fuzz score and closest word match from a list"""
    fuzzscore = [fuzz.token_set_ratio(word1_def, match) for match in word2_in_list_def]
    max_index = fuzzscore.index(max(fuzzscore))
    fuzzscore_max = fuzzscore[max_index]
    email_domain_max = word2_in_list_def[max_index]
    return fuzzscore_max, email_domain_max

def fuzzy_word_pandas_matching(pandas_df_def, column_df_def, word2_in_list_def):
    """produce fuzz score and closest word match from pandas data frame"""
    subset_column = [column_df_def]
    pandas_df_def['fuzz'] = pandas_df_def.apply(lambda x: fuzzy_word_list_matching(x[subset_column].squeeze(), word2_in_list_def), axis=1)
    pandas_df_def[['fuzz_score', 'fuzz_name']] = pd.DataFrame(pandas_df_def['fuzz'].tolist(), index = pandas_df_def.index)
    return pandas_df_def[['fuzz_score', 'fuzz_name']]
