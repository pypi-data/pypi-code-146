import pandas as pd


def migrate(df: pd.DataFrame):
    # migrate data
    # migrate only if cycle.dataCompleteness is specified in upload
    if any(df.columns.str.startswith('cycle.dataCompleteness')):
        df['cycle.dataCompleteness.waste'] = 'false'
        df.loc[df['cycle.id'] == '-', 'cycle.dataCompleteness.waste'] = '-'

    # make sure to return the DataFrame so it can be uploaded
    return df
