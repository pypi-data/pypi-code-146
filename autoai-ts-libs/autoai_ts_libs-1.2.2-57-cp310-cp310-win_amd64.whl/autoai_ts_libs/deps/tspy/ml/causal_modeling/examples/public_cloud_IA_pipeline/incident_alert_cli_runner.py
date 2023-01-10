#  /************** Begin Copyright - Do not add comments here **************
#   * Licensed Materials - Property of IBM
#   *
#   *   OCO Source Materials
#   *
#   *   (C) Copyright IBM Corp. 2020, All Rights Reserved
#   *
#   * The source code for this program is not published or other-
#   * wise divested of its trade secrets, irrespective of what has
#   * been deposited with the U.S. Copyright Office.
#   ***************************** End Copyright ****************************/
"""
Cmdline runnable Incident-Alert pipeline, includes search and ranking.
User provides the embedding model (trained separately).
"""
import os
import pandas as pd
import argparse
import time as tm
from search_and_rank_windowed_embeddings import SearchAndRankWindowedEmbeddings
from search_and_rank_windowed_embeddings import EXP_STATIC_EMBEDDINGS, EXP_ONE_HOT_ENCODINGS
import json
import numpy as np
import time as tm
import datetime as dt
import nltk
from nltk.translate.bleu_score import sentence_bleu
from nltk.stem import WordNetLemmatizer, PorterStemmer
import re
import pickle
import warnings

warnings.filterwarnings('ignore')

import cProfile
import pstats


def sub_select(string, dataseries):
    index_list = []
    for count, i in enumerate(dataseries.tolist()):
        if str(i) != "NaT":
            index_list.append(count)
    return index_list


def incident_desconly_pairwise_bleu(index1_list, index2, list_description):
    lemmatizer = PorterStemmer()
    desc_1_list = []
    for index1 in index1_list:
        desc_1 = nltk.word_tokenize(list_description[index1])
        desc_1 = [lemmatizer.stem(word.lower()) for word in desc_1 if word.isalpha()]
        desc_1_list.append(desc_1)
    desc_2 = nltk.word_tokenize(list_description[index2])
    desc_2 = [lemmatizer.stem(word.lower()) for word in desc_2 if word.isalpha()]
    print(desc_1)
    print(desc_2)
    return sentence_bleu(desc_1_list, desc_2, weights=(1, 0, 0, 0))


# Parse the list of hostnames into list of segments that have semantic meaning
# fcs45.sr01.dal03 will be ['fcs','45','sr','01','dal','03'] - there is a fcs type device in server room 01 in the Dallas datacenter 3.
def listify_hostname(index, hostnames_list):
    hlist = hostnames_list[index]
    str_list = []
    for x in hlist:
        a = x.split(".")
        form = re.compile("[a-zA-Z]{3}[0-9]{2}")
        for y in a:
            if len(form.findall(y)) != 0:
                str_list.append(form.findall(y)[0][0:3])
                str_list.append(form.findall(y)[0][3:])
            if len(y) == 4:
                str_list.append(y[0:2])
                str_list.append(y[2:])
    return str_list


def distance_hostnames(index_1, index_2, hostnames_list):
    str_list1 = listify_hostname(index_1, hostnames_list)
    str_list2 = listify_hostname(index_2, hostnames_list)
    print(str_list1)
    print(str_list2)
    return len(set(str_list1).intersection(set(str_list2))) / len(set(str_list1).union(set(str_list2)))


def incident_descandhostnames_pairwise_bleu(index1_list, index2, list_description, hostnames_list, verbose=True):
    lemmatizer = PorterStemmer()
    desc_1_list = []
    for index1 in index1_list:
        desc_1 = nltk.word_tokenize(list_description[index1])
        desc_1 = [lemmatizer.stem(word.lower()) for word in desc_1 if word.isalpha()]
        desc_1_h = listify_hostname(index1, hostnames_list)
        desc_1 = desc_1 + desc_1_h
        desc_1_list.append(desc_1)
    desc_2 = nltk.word_tokenize(list_description[index2])
    desc_2 = [lemmatizer.stem(word.lower()) for word in desc_2 if word.isalpha()]
    desc_2_h = listify_hostname(index2, hostnames_list)
    desc_2 = desc_2 + desc_2_h
    if verbose == True:
        print(desc_1_list)
        print(desc_2)
    if not desc_1_list:
        return 0
    else:
        return sentence_bleu(desc_1_list, desc_2, weights=(1, 0, 0, 0))


def find_incident_indices(outage_start_pd_series, interval_start, interval_end):
    indices_list = []
    timestamp_list = outage_start_pd_series.tolist()
    for i in range(outage_start_pd_series.size):
        timestamp = timestamp_list[i]
        time_secs = tm.mktime(timestamp.to_pydatetime().timetuple()) - 5 * 3600
        # mktime gives time in EST - subtracting 5 hours to get to UTC
        if (interval_start <= time_secs) & (interval_end >= time_secs):
            indices_list.append(i)
    return indices_list


def return_similarity_scores(index_of_interest, list_end_times, interval_before, interval_after, outage_start_pd_series,
                             hostname_series, description_series, verbose=True):
    outage_start_list = outage_start_pd_series.tolist()
    hostname_list = hostname_series.tolist()
    desc_list = description_series.tolist()

    scores = []
    for t in list_end_times:
        indx_list = find_incident_indices(outage_start_pd_series, t - interval_before, t + interval_after)
        indx_list = [i for i in indx_list if i != index_of_interest]
        s = incident_descandhostnames_pairwise_bleu(indx_list, index_of_interest, desc_list, hostname_list, verbose)
        if verbose == True:
            print(s)
        scores.append(s)
    return scores


def obtain_datacenter(incident_index_of_interest, df_select, verbose=True):
    unique_datacenters = []
    list_h = df_select['hostnames'].tolist()[incident_index_of_interest]
    print(list_h)
    for l in list_h:
        a = l.split(".")
        if (len(a) >= 2):
            if (a[-1] not in unique_datacenters):
                unique_datacenters.append(a[-1])
    import re
    form = re.compile("[a-zA-Z]{3}[0-9]{2}")
    unique_datacenters_formatted = []
    for i in range(len(unique_datacenters)):
        if len(form.findall(unique_datacenters[i])) != 0:
            unique_datacenters_formatted.append(form.findall(unique_datacenters[i])[0])
    if verbose == True:
        print(unique_datacenters_formatted)
    return unique_datacenters_formatted


def compute_dropped_score(r, incident_index_of_interest, interval_before, interval_after, df_select, verbose=True):
    list_endtimes = [j[2] for j in r]
    similarities = [1 - abs(j[0]) for j in r]
    scores = return_similarity_scores(incident_index_of_interest, list_endtimes, interval_before, interval_after,
                                      df_select['Outage Start'], df_select['hostnames'],
                                      df_select['Description w/o hostnames'], verbose=verbose)
    weighted_score = 0
    for i in range(len(similarities)):
        weighted_score = weighted_score + similarities[i] * scores[i]
    weighted_score = weighted_score / sum(similarities)

    if verbose == True:
        print("Scores of various intervals")
        print(scores)
        print("Distances of corresponding intervals in the embedding space")
        print(similarities)
        print("Weighted Similarity score after dropping")
        print(weighted_score)

    return weighted_score


def read_task_file(fn):
    """
    fn has format: <incident id> <datacenter>\n
    :param fn:
    :return: list of lists with content
    """
    tasks = []
    with open(fn, 'rt') as f:
        for c, l in enumerate(f.readlines()):
            aux = [s.strip() for s in l.strip().split()]
            if len(aux) == 0:
                continue
            if len(aux) != 2:
                raise RuntimeError("ERROR: expecting 2 entries on line %d of file %s (but found %d)" %
                                   (c + 1, fn, len(aux)))
            tasks.append(aux)
    print("INFO: Read %d tasks from file %s" % (len(tasks), fn))
    return tasks


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Runner of Incident-Ticket Search'n'Rank (SPEEDY version).")
    parser.add_argument('-taskfn', '--taskfn', dest='taskfn', required=True, metavar='<fn>',
                        help="Task file. Format: <incid> <datacenter>\\n")
    parser.add_argument('-outdir', '--outdir', dest='outdir', required=True, metavar='<dir>',
                        help="Results will be dumped in this dir.")
    parser.add_argument('-incfn', '--incfn', dest='incfn', required=True, metavar='<fn>',
                        help="xlsx file with incidents")
    parser.add_argument('-alertfn', '--alertfn', dest='alertfn', required=True, metavar='<fn>',
                        help="JSON modified alert file (json after unrolling)")
    parser.add_argument('-cachefn', '--cachefn', dest='cachefn', required=True, metavar='<fn>',
                        help="full name of the cachefile")
    parser.add_argument('-packdir', '--packdir', dest='packdir', required=True, metavar='<dir>',
                        help="package directory. ")
    parser.add_argument('-alert_winlen', '--alert-winlen', dest='awinlen', required=True, metavar='<float>',
                        help="Length of search window for alerts (in hours)")
    parser.add_argument('-gt_file', '--gt_file', dest='gt_fn', required=False, metavar='<fn>', default=None,
                        help="Load ground truth and activate early bail-out mechanism:"
                             "i.e., if no alerts within window are a hit, do not rank anything.")
    parser.add_argument('-incident_hr_before', '--incident-hr-before', dest='ihrbefore', required=False,
                        metavar='<float>', default=1.0,
                        help="Number of hours before to look at in the incidents database.")
    parser.add_argument('-subsample_search', '--subsample-search', dest='subsample_search', required=False,
                        metavar='<int>', default=1,
                        help="Speed up by looking at every nth window in the db (1 = no subsampling).")
    parser.add_argument('-pca_dim', '--pca_dim', dest='pca_dim', required=False,
                        metavar='<int>', default=None,
                        help="None or an integer. Latter will activate PCA projection of the embeddings. ")
    parser.add_argument('-incident_hr_after', '--incident-hr-after', dest='ihrafter', required=False,
                        metavar='<float>', default=8.0,
                        help="Number of hours before to look at in the incidents database.")
    parser.add_argument('-profile', '--profile', dest='profilefn', required=False,
                        metavar='<fn>', default=None,
                        help="Will activate performance profiling and dump stats in <fn> (cProfile, pstats)")
    parser.add_argument('-mmdlibv', '--mmdlibv', dest='mmdlibv', required=False,
                        metavar='<str>', default='v2',
                        help="Which library version for mmd calculation: currently supporting only \"v2\" (cython)")
    parser.add_argument('-experimental_baseline_mode', '--experimental_baseline_mode',
                        dest='experimental_baseline_mode',
                        default=None,
                        required=False, help="Experimental: 1=One-hot Encodings, 2=Static Embeddings")
    parser.add_argument('-experimental_static_emb_config', '--experimental_static_emb_config',
                        dest='experimental_static_emb_config',
                        default=None,
                        required=False,
                        help="When using experimental_baseline_mode==2, this option allows you to specify"
                             "the config to instantiate the static embeddings server")
    parser.add_argument('-mmd_alphas', '--mmd_alphas', dest='mmd_alphas', required=False, default="0.1,0.5",
                        metavar='<str>', help="Comma-separated alpha values for the MMD")


    args = parser.parse_args()

    profiler = None
    profiler_dumpfn = None
    if args.profilefn is not None:
        profiler = cProfile.Profile()
        profiler_dumpfn = args.profilefn
        print("INFO: Profiling ACTIVE. Will dump stats in %s" % profiler_dumpfn)
    if args.mmdlibv == 'v2':
        print("INFO: Using speedy version of mmd (cython)...")
    elif args.mmdlibv == 'v1':
        raise NotImplementedError("ERROR: torch-two-sample not supported in this version.")
    else:
        raise ValueError("Unknown mmd version requested. Use \"-v2\" (MMD).")
    incidents_fn = args.incfn  ## "/Users/jirinavratil/ws/github/causality-for-aiops/data/Incidents-Jan-Dec-1-2020.xlsx"
    packdir = args.packdir  ## "./packaged_runtime_golerta_JulToOct2020_hipr_top7dcs.sec6win20.allDCisolated_feav4_fC87100Up_lr0.0100_LS128x1noL2UsePrevB100/"
    packfn = packdir + '/' + 'config.json'
    cachefn = args.cachefn  ## 'cachefile_staggeredDCs_PCA10_12072020.dbfrom10012020.5DCsOnly.pkl'
    alertfn = args.alertfn  ##"./packaged/alerts.unrolled_from10012020_v2.json"
    alert_winlen_hours = float(args.awinlen)
    incident_hours_before = float(args.ihrbefore)
    incident_hours_after = float(args.ihrafter)
    tasks = read_task_file(args.taskfn)
    subsample_search = int(args.subsample_search)
    outdir = args.outdir
    if not os.path.exists(outdir):
        print("INFO: Creating folder \"%s\"" % outdir)
        os.makedirs(outdir)
    print("INFO: All results will be dumped in directory \"%s\"" % outdir)
    gt_dict = None
    pca_dim = int(args.pca_dim) if args.pca_dim is not None else None
    experimental_baseline_mode = None
    if args.experimental_baseline_mode is not None:
        pca_dim = None
        print("INFO: Switching to experimental mode!")
        experimental_baseline_mode = int(args.experimental_baseline_mode)
        if experimental_baseline_mode == EXP_ONE_HOT_ENCODINGS:
            print("INFO: --> Will use one-hot encodings.")
        elif experimental_baseline_mode == EXP_STATIC_EMBEDDINGS:
            print("INFO: --> Will use static embeddings.")
            assert (
                        args.experimental_static_emb_config is not None), "Static embedder config must be provided via option."
    if pca_dim is not None:
        print("INFO: PCA dimension to project embeddings is %d" % pca_dim)
    if args.gt_fn is not None:
        # ground truth table
        # format: list of tuples (incident id, orig. alert id, event id, float)
        with open(args.gt_fn, 'rb') as f:
            gt_list = pickle.load(f)
            print("INFO: Loaded %d entries from ground-truth file %s" % (len(gt_list), args.gt_fn))
            print("INFO: Early-stopping due to no hits ACTIVE!")
            # convert to a lookup by INCID --> dict key INCID, value EVENTID
            gt_dict = {}
            for i in set([ii[0] for ii in gt_list]):
                gt_dict[i] = [a[2] for a in gt_list if a[0] == i]
    mmd_alphas = [float(s.strip()) for s in args.mmd_alphas.split(',')]
    print("INFO: Using MMD alphas = %s" % str(mmd_alphas))

    # read incidents file
    print("INFO: Reading incident file %s" % incidents_fn)
    df = pd.read_excel(incidents_fn, engine='openpyxl')
    df_select = df[
        ['Outage Start', 'Opened Date', 'Configuration Item (CI)', 'Incident Tribe', 'Incident Status',
         'Incident Short Description', 'Incident Number']]
    index_list_1 = sub_select("NaT", df_select['Opened Date'])
    # index_list_2=sub_select("NaT",df_select['Outage End'])
    # index_list_3=sub_select("NaT",df_select['Opened Date'])
    index_list_1 = list(set(index_list_1))  # .intersection(set(index_list_2),set(index_list_3)))
    df_select = df_select.iloc[index_list_1]
    # Processing Incident Description to get hostnames out
    a = df_select['Incident Short Description'].tolist()
    b = []
    hostnames = []
    for i in a:
        h_list = []
        str_list = i.split(" ")
        for j in str_list:
            if (len(j.split(".")) == 3) | (len(j.split(".")) == 2):
                h_list.append(j)
                str_list.remove(j)
        hostnames.append(h_list)
        b.append(" ".join(str_list))
    print(len(hostnames))
    print(len(b))
    # print(np.hstack((np.array(b[0:10]).reshape(-1,1),np.array(hostnames[0:10]).reshape(-1,1))))
    df_select['Description w/o hostnames'] = b
    df_select['hostnames'] = hostnames

    alert_search_window_len = alert_winlen_hours * 3600
    interval_before = 3600 * incident_hours_before
    interval_after = 3600 * incident_hours_after
    interval_before_alerts = alert_search_window_len

    # initialize search class
    secondary_config = None
    with open(packfn) as f:
        config = json.load(f)
    if args.experimental_static_emb_config is not None:
        with open(args.experimental_static_emb_config) as f:
            secondary_config = json.load(f)

    S = SearchAndRankWindowedEmbeddings(embedding_mdl_config=config, alertfn=alertfn, verbose=True,
                                        mmd_alphas=mmd_alphas, query_constraints=None,
                                        emb_database_input_cache_file=cachefn, pca_dim=pca_dim,
                                        mmd_lib_version=args.mmdlibv,
                                        experimental_operating_mode=experimental_baseline_mode,
                                        experimental_static_emb_config=secondary_config)

    for taskid, (incident_of_interest, datacenter_of_incident) in enumerate(tasks):
        print("INFO: ================================================")
        print("INFO: Task number %d: INCID=%s, DC=%s" % (taskid, incident_of_interest, datacenter_of_incident))
        if np.sum((df_select['Incident Number'] == incident_of_interest)) < 1:
            raise RuntimeError("ERROR: Incident id  %s not found in %s." % (incident_of_interest, incidents_fn))
        incident_index_of_interest = np.where([i for i in df_select['Incident Number'] == incident_of_interest])[0][0]
        outage_start_times = df_select['Opened Date'].tolist()[incident_index_of_interest]
        outage_time_secs = outage_start_times.timestamp()
        # print(outage_time_secs)
        unique_datacenters_formatted = obtain_datacenter(incident_index_of_interest, df_select, verbose=False)
        # print(unique_datacenters_formatted)

        try:
            query_constraints = 'datacenter:' + datacenter_of_incident
            S._setup_query_constraints(query_constraints)
            # print(query_constraints)

            time_of_interest = outage_time_secs
            results_dict = {}
            alert_hit_list = None
            if gt_dict is not None and incident_of_interest in gt_dict:
                alert_hit_list = gt_dict[incident_of_interest]
            print("INFO: Incident %s time = %s (%.1fs)"
                  % (incident_of_interest, outage_start_times.to_pydatetime().timetuple(), time_of_interest))
            if profiler is not None:
                profiler.enable()
            info = S.search_drop_each(time_of_interest, window_len=interval_before_alerts,
                                      subsample_search=subsample_search, adapt_window_len=True,
                                      alert_hit_list=alert_hit_list)
            if profiler is not None:
                profiler.disable()
            # print(info)
            # print("# of Alerts found:",len(info['all_window_alerts']))
        except ValueError as e:
            print('Exception=%s' % e)
            print("INFO: No alerts found for incident %s within a %d hrs window. Skipping this task." % (
                incident_of_interest, alert_winlen_hours))
            if profiler is not None:
                profiler.disable()
            continue
        if info is None or len(info) < 1 or 'all_window_alerts' not in info or 'dropped_alert_0' not in info:
            print("INFO: Problem finding alerts. Skipping this task...")
            continue

        tot_win_alerts = len(info['all_window_alerts'])

        for j in range(tot_win_alerts):
            info_key = 'dropped_alert_%s' % j
            if info[info_key]['scores'] is None or len(info[info_key]['scores']) < 1:
                print("WARN: ignoring alert drop (index %d)" % j)
                results_dict[info[info_key]['id']] = 1.0
                continue
            r = info[info_key]['scores']
            if profiler is not None:
                profiler.enable()
            if len(r) > 0:
                if len(r) >= 10:
                    weighted_score = compute_dropped_score(r[:10], incident_index_of_interest, interval_before,
                                                           interval_after,
                                                           df_select, verbose=False)
                else:
                    print("Less than 10 entries")
                    weighted_score = compute_dropped_score(r, incident_index_of_interest, interval_before,
                                                           interval_after,
                                                           df_select, verbose=False)
                results_dict[info[info_key]['id']] = weighted_score
            if profiler is not None:
                profiler.disable()

        R = {'alert_scores': results_dict, 'incident_id': incident_of_interest,
             'alert_window_hours': alert_winlen_hours,
             'inc_before_hours': incident_hours_before, 'inc_after_hours': incident_hours_after,
             'time_of_incident': time_of_interest, 'datacenter': datacenter_of_incident, 'cachefile': cachefn,
             'configfn': packfn, 'alertfn': alertfn}
        resfn = "%s/results_%s_%s.json" % (outdir, incident_of_interest, datacenter_of_incident)
        print("INFO: Saving results in %s" % resfn)
        with open(resfn, 'wt') as of:
            json.dump(R, of, indent=5)

    if profiler is not None:
        profiler.disable()
        # stats = pstats.Stats(profiler).sort_stats('cumtime')
        stats = pstats.Stats(profiler)
        stats.dump_stats(profiler_dumpfn)
        print("INFO: Profile stats dumped in %s" % profiler_dumpfn)
