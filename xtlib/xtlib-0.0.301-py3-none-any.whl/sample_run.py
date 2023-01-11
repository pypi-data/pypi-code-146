# sample_run.py: simulate train/valid metrics (loss, acc) for a single run
from random import randint, randrange
import numpy as np
import pandas as pd

def gen_loss_acc(name, start, increment, end, min_loss=0, max_acc=1):
    steps = np.arange(start, 1+end, increment)
    num_steps = len(steps)
    
    # loss should start around 3 and fall to 0
    loss = .35*np.random.normal(size=num_steps) + 1 - np.tanh((steps-num_steps/4)/15)
    loss = loss.clip(min_loss, 5)

    # acc should start at 0 and rise towards 1
    acc = .25*np.random.normal(size=num_steps) + np.tanh((steps-num_steps/4)/15)
    acc = np.clip(max_acc*acc, 0, max_acc)

    df = pd.DataFrame({'step': steps, name+'_loss': loss, name+'_acc': acc})
    return df

def get_sample_run(hparam1="orig_loss", hparam1_diff=0, hparam2="router32", hparam2_diff=0, detail=True, melt=False):
    # each split may have different frequencies
    train_steps = 100
    valid_steps = 20

    train_df = gen_loss_acc("train", 1, 1, 100)

    min_valid_loss = 0 + (hparam1_diff + hparam2_diff)
    max_valid_acc = 1 - (hparam1_diff + hparam2_diff)

    valid_df = gen_loss_acc("valid", 5, 5, 100, min_loss=min_valid_loss, max_acc=max_valid_acc)
    # print(valid_df.head())
    # print(valid_df.tail())

    df_metrics = pd.merge( train_df, valid_df, how="outer", on="step" )
    # print(df_metrics.head())
    # print(df_metrics.tail())

    # create df_run
    records = []
    job_id = "job42"
    for step in range(1, 101):
        run_id = "run42.{}".format(step-1)
        record = {'job_id': job_id, "run_name": run_id, "hparam1": hparam1, "hparam2": hparam2, "step": step}
        records.append(record)

    df_run = pd.DataFrame.from_records(records)

    # print(df_run.head())
    # print(df_run.tail())

    df_run = pd.merge(df_run, df_metrics, how="outer", on="step")

    if not detail:
        df_run = df_run.iloc[-1:]

    # print(df_run.head())
    # print(df_run.tail())

    if melt:
        df_run = pd.melt(df_run, "step")
        
    return df_run

def get_sample_job(detail=False, melt=False):
    # Setting a random seed for reproducibility
    np.random.seed(142)

    df_job = None
    #hparam1_diffs = [.02, .07, .15]
    hparam1_diffs = [.25, .17, .02]
    hparam1_names = ["orig_loss", "adj_loss", "adj_loss_400"]

    hparam2_diffs = [.15, .12]
    hparam2_names = ["router_32", "router_64"]

    for hparam1, hparam1_diff in zip(hparam1_names, hparam1_diffs):

        for hparam2, hparam2_diff in zip(hparam2_names, hparam2_diffs):
            for seed in range(5):

                df_run = get_sample_run(hparam1=hparam1, hparam1_diff=hparam1_diff, hparam2=hparam2, hparam2_diff=hparam2_diff, detail=detail, melt=melt)
                if df_job is None:
                    df_job = df_run
                else:
                    df_job = pd.concat( [df_job, df_run] )

    # print(df_job.head())
    # print(df_job.tail())

    return df_job

if __name__ == "__main__":
    get_job()
