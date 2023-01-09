import pandas as pd
import numpy as np


def process_tech_df(final_ranks_dc, final_ranks_franchisee, volume_fraction):

    tech_input = pd.concat([final_ranks_dc, final_ranks_franchisee], axis=0)
    tech_input['volume_fraction'] = volume_fraction

    tech_input.rename(
        {"partial_dc_id": "dc_id", "distributor_rank_1": "final_dist_1",
         "distributor_rank_2": "final_dist_2", "distributor_rank_3": "final_dist_3"},
        axis=1, inplace=True)

    # combine volume fraction split for cases where total distributors < 3
    volume_fraction_split = tech_input['volume_fraction'].str.split(
        pat='-', expand=True).rename(
        columns={0: 'volume_fraction_1',
                 1: 'volume_fraction_2',
                 2: 'volume_fraction_3'})

    tech_input['volume_fraction_1'] = volume_fraction_split[
        'volume_fraction_1'].astype(float)
    tech_input['volume_fraction_2'] = volume_fraction_split[
        'volume_fraction_2'].astype(float)
    tech_input['volume_fraction_3'] = volume_fraction_split[
        'volume_fraction_3'].astype(float)

    tech_input['volume_fraction_2'] = np.where(
        tech_input['final_dist_3'].isna(),
        tech_input['volume_fraction_2'] +
        tech_input['volume_fraction_3'],
        tech_input['volume_fraction_2'])

    tech_input['volume_fraction_3'] = np.where(
        tech_input['final_dist_3'].isna(), 0,
        tech_input['volume_fraction_3'])

    tech_input['volume_fraction_1'] = np.where(
        tech_input['final_dist_2'].isna(),
        tech_input['volume_fraction_1'] +
        tech_input['volume_fraction_2'],
        tech_input['volume_fraction_1'])

    tech_input['volume_fraction_2'] = np.where(
        tech_input['final_dist_2'].isna(), 0,
        tech_input['volume_fraction_2'])

    tech_input['volume_fraction'] = tech_input['volume_fraction_1'].astype(
        'str') + '-' + tech_input['volume_fraction_2'].astype(
        'str') + '-' + tech_input['volume_fraction_3'].astype('str')

    tech_input = tech_input[
        ['dc_id', 'store_id', 'franchisee_id', 'drug_id',
         'drug_type', 'request_type', 'volume_fraction',
         'final_dist_1', 'final_dist_2', 'final_dist_3']]

    # adhoc changes by tech, table restructure
    tech_input = tech_input.reset_index(
        drop=True).reset_index().rename(columns={'index': 'id'})
    tech_input[['volume_fraction_1', 'volume_fraction_2',
                'volume_fraction_3']] = tech_input[
        'volume_fraction'].str.split('-', 3, expand=True)
    tech_input.loc[tech_input['request_type'] == 'AS/MS',
                   'request_type'] = 'manual-short/auto-short'
    tech_input.loc[tech_input['request_type'] ==
                   'PR', 'request_type'] = 'patient-request'
    tech_input.loc[tech_input['request_type'] ==
                   'ALL', 'request_type'] = 'all'

    volume_fraction_melt = pd.melt(tech_input, id_vars=['id'],
                                   value_vars=['volume_fraction_1',
                                               'volume_fraction_2',
                                               'volume_fraction_3']).sort_values(
        by='id')
    distributor_melt = pd.melt(tech_input, id_vars=['id'],
                               value_vars=['final_dist_1',
                                           'final_dist_2',
                                           'final_dist_3']).sort_values(
        by='id').rename(columns={'value': 'distributor_id'})
    distributor_ranking_rule_values = pd.merge(distributor_melt,
                                               volume_fraction_melt,
                                               left_index=True,
                                               right_index=True,
                                               suffixes=('', '_y'))
    distributor_ranking_rule_values = distributor_ranking_rule_values[
        ['id', 'distributor_id', 'value']].rename(
        columns={'id': 'distributor_ranking_rule_id'}).reset_index(
        drop=True)

    distributor_ranking_rule_values = distributor_ranking_rule_values.reset_index().rename(
        columns={'index': 'id'})

    # drop null values in distributor_id(for cases where historical distributors are < 3)
    distributor_ranking_rule_values = distributor_ranking_rule_values[
        ~distributor_ranking_rule_values['distributor_id'].isna()]
    # convert distributor_id in int format
    distributor_ranking_rule_values['distributor_id'] = \
        distributor_ranking_rule_values['distributor_id'].astype(int)

    distributor_ranking_rules = tech_input[['id', 'drug_id', 'dc_id',
                                            'franchisee_id', 'store_id',
                                            'drug_type', 'request_type']]

    return distributor_ranking_rules, distributor_ranking_rule_values
