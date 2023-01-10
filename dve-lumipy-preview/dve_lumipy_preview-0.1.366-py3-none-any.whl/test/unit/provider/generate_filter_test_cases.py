import datetime as dt
import json
import os

import lumipy as lm
import lumipy.provider as lp
from lumipy.test.provider.int_test_providers import PandasFilteringTestProvider
from lumipy.test.test_infra import load_secrets_into_env_if_local_run

"""This is a script for generating python provider filter translation test cases

To run you'll need to have your fbn-ci secrets file path as an env var (LOCAL_INT_TEST_SECRETS_PATH) and have python 
providers set up. This will output two JSON files: one for the normal filter test cases and one for partial application 
(i.e. for missing functions and columns)

"""


def build_filter_test_defs(p):
    return {
        'Not': ~p.col_e,
        'And': p.col_e & (p.col_a > 10),
        'Or': (p.col_a > 10) or (p.col_a < 5),
        'Gt': p.col_a > 10,
        'Lt': p.col_a < 10,
        'Gte': p.col_a >= 10,
        'Lte': p.col_a <= 10,
        'In': p.col_a.is_in(list(range(10, 20, 1))),
        'NotIn': p.col_a.not_in(list(range(10, 20, 1))),
        'Eq': p.col_a == 20,
        'Neq': p.col_a != 20,
        'Add': (p.col_a + p.col_f) < 50,
        'Subtract': (p.col_a - p.col_f) < 0,
        'Multiply': (p.col_a * p.col_b) < 50,
        'Between': p.col_b.between(5, 10),
        'NotBetween': p.col_b.not_between(5, 10),
        'DateValue': p.col_d > dt.datetime(2022, 1, 1),
        'BoolValue': p.col_e == False,
        'StrValue': p.col_c == "8ZV,aGyup`T5\t}#lpU<:d\\wG]a29>gT$#1Tr(_NM:;8wC8VzRN",
        'Mod': p.col_a % 10 == 0,
        'Concatenate1': (p.col_c.str.concat(p.col_h)).str.like('%ab%cd%'),
        'Concatenate2': (p.col_c.str.concat('--TESTLITERAL')).str.like('%ab%'),
        'Like1': p.col_c.str.like('B%'),
        'Like2': p.col_c.str.like('%B'),
        'Like3': p.col_c.str.like('d%u'),
        'Like4': p.col_c.str.like('d_e%'),
        'Like5': p.col_c.str.like('%px%'),
        'Glob1': p.col_c.str.glob('B*'),
        'Glob2': p.col_c.str.glob('*B'),
        'Glob3': p.col_c.str.glob('d*u'),
        'Glob4': p.col_c.str.glob('f?d*'),
        'Glob5': p.col_c.glob('J?h4ui0A*64.(X{\tJ96;XWl*'),
        'Regexp1': p.col_c.str.regexp('^V.*7.*'),
        'Regexp2': p.col_c.str.regexp('^V.*7.*'),
        "Round": round(p.col_b, 1) == 1.1,
    }


def build_partial_test_defs(p):

    mfn = lambda x: x.log()

    return {
        'lt_left': (mfn(p.col_a) < 3, None),
        'lt_right': (3 < mfn(p.col_a), None),
        'gt_left': (mfn(p.col_a) > 3, None),
        'gt_right': (3 > mfn(p.col_a), None),
        'lte_left': (mfn(p.col_a) <= 3, None),
        'lte_right': (3 <= mfn(p.col_a), None),
        'gte_left': (mfn(p.col_a) >= 3, None),
        'gte_right': (3 >= mfn(p.col_a), None),
        'eq_left': (round(mfn(p.col_b)) == 2, None),
        'eq_right': (2 == round(mfn(p.col_b)), None),
        'neq_left': (round(mfn(p.col_b)) != 2, None),
        'neq_right': (2 != round(mfn(p.col_b)), None),
        'DivCast': ((3.0 / p.col_b) >= 1, None),
        'IsIn': (round(mfn(p.col_a)).is_in(list(range(3, 6))), None),
        'NotIsIn': (round(mfn(p.col_a)).not_in(list(range(3, 6))), None),
        'Between': (mfn(p.col_b).between(1, 2), None),
        'NotBetween': (mfn(p.col_b).not_between(1, 2), None),
        'MissingCol': (p.col_h.str.contains('abc'), None),
        'Like': (p.col_h.str.like('a%'), None),
        'Glob': (p.col_h.str.glob('n*'), None),
        'Regexp': (p.col_h.str.regexp('^n.*'), None),
        'NotLike': (p.col_h.str.not_like('a%'), None),
        'NotGlob': (p.col_h.str.not_glob('n*'), None),
        'NotRegexp': (p.col_h.str.not_regexp('^n.*'), None),
        'And': (p.col_c.str.contains('ab') & (mfn(p.col_a) < 3), p.col_c.str.contains('ab')),
        'Or': (p.col_c.str.contains('ab') | (mfn(p.col_a) < 3), None),
    }


def build_filter_tests_json(p, directory):

    test_defs = build_filter_test_defs(p)

    test_cases = {}
    for tlabel, condition in test_defs.items():

        df = p.select('*').where(condition).limit(25).go()
        if df.shape[0] == 0:
            raise ValueError(f'{tlabel} result is empty')

        test_cases[tlabel] = {
            'result': df.iloc[:, :-1].to_csv(index=False),
            'filter': df.iloc[0].FilterString
        }

    fpath = f'{directory}/filter_test_cases.json'
    with open(fpath, 'w') as f:
        f.write(json.dumps(test_cases, indent=4))


def build_partial_filter_tests_json(p, directory):

    test_defs = build_partial_test_defs(p)
    test_cases = {}

    for tlabel, (c1, c2) in test_defs.items():

        q1 = p.select('*').where(c1).limit(25)
        df1 = q1.go()
        if df1.shape[0] == 0:
            raise ValueError(f'{tlabel} result is empty')

        q2 = p.select('*').where(c2).limit(25) if c2 is not None else p.select('*').limit(25)
        df2 = q2.go()
        if df2.shape[0] == 0:
            raise ValueError(f'{tlabel} result is empty')

        test_cases[tlabel] = {
            'filter1': df1.iloc[0].FilterString,
            'filter2': df2.iloc[0].FilterString,
        }

    fpath = f'/{directory}/partial_filter_test_cases.json'
    with open(fpath, 'w') as f:
        f.write(json.dumps(test_cases, indent=4))


if __name__ == '__main__':

    # Spin up the test provider
    with lp.ProviderManager(PandasFilteringTestProvider(1989), domain='fbn-ci'):

        # Load secrets and get the atlas
        load_secrets_into_env_if_local_run()
        atlas = lm.get_atlas()

        # Make provider table object where pandas-side filtering is switched off. We want to compare against
        # luminesce-side filtering
        test_provider = atlas.pandas_test_filtering(use_pandas_filter=False)

        # Find the test data dir...
        file_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = file_dir + '/../../data/'

        # Build the test case jsons
        build_filter_tests_json(test_provider, data_dir)
        build_partial_filter_tests_json(test_provider, data_dir)
