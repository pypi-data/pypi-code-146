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
This class implements the Incident-Alert search pipeline following the Potential Outcome framework.
"""
import sys
sys.path.append('../')
import warnings
warnings.filterwarnings('ignore')
from runtime_windowed_ae_server import RuntimeWindowedAEServer
from runtime_static_ae_server import RuntimeStaticAEServer
from oculus_features_cli_runner import filter_alerts
import inspect
try:
  import mmd
except:
  raise RuntimeError("MMD Support code needs to be installed. Follow these steps:\n"
                     "* Go to: http://github.com/djsutherland/mmd and clone the repo.\n"
                     "* Install Cython: 'pip install Cython'\n"
                     "* edit 'setup.py' to remove all '-fopenmpi' occurrences if your machine has no fopenmpi ability\n"
                     "* Install MMD via 'python setup.py install'\n")
import numpy as np
from copy import deepcopy
from sklearn.decomposition import PCA
import pickle

EXP_ONE_HOT_ENCODINGS=1
EXP_STATIC_EMBEDDINGS=2

class SearchAndRankWindowedEmbeddings:
    def __init__(self, embedding_mdl_config, alertfn, verbose=True, mmd_alphas=[0.1, 0.5], query_constraints=None,
                 win_len_tol=0.3, staggered_filters=None, emb_database_output_cache_file=None,
                 emb_database_input_cache_file=None, timefield='updateTime',
                 pca_dim=None, encoder_version='v2', mmd_lib_version='v2',
                 experimental_operating_mode=None, experimental_static_emb_config=None):
        """
        Class for search and ranking of alerts windows in the RNN-embedding space
        :param embedding_mdl_config: dict with params to initialize RuntimeWindowedAEServer
        :param alertfn: json file containing all historical alerts
        :param verbose:
        :param mmd_alphas: list of floats to be passed into the mmd() distance function (see descr)
        :param query_constraints: Comma-separated list of fieldname:substring pairs, e.g., 'datacenter:dal05'
                             to be used to filter alerts for the Query. Multiple fields are logical AND connected.
        :param win_len_tol: maximum allowed discrepancy (fraction) in window length found to be passed
                        to _find_window() - see descr.
        :param staggered_filters: a comma-separated string with field constraints to be applied during generating
                    the alert embedding database. Each constraint will be applied individually
                      on the entire alert set, with subsequent constraints resulting in a repeated filtering and
                      concatenation. Example: ['datacenter:dal05', datacenter:dal12', ...]
        :param emb_database_output_cache_file: dump all database related variable into a pickle file
                    this file can be used to load later and skip lengthy computation of the db embeddings.
        :param emb_database_input_cache_file: pickle file with all database variables precomputed. will set all using this
        :param pca_dim: if not None, will create a PCA projection from embdim to pca_dim. Note that this param will
                    have no effect if emb_database_file is used!
        :param encoder_version: is passed to emb_server() to specify feature encoding version
        :param mmd_lib_version: either 'v1' - REMOVED (torch_two_sample lib), or 'v2' (github.com/djsutherland/mmd)
        :param experimental_operating_mode: None - deactivated
                                            EXP_ONE_HOT_ENCODINGS - (baseline purposes) oh encoding will be used everywhere instead of embeddings
                                            EXP_STATIC_EMBEDDINGS - (baseline purposes)
        :param experimental_static_emb_config: config file to instantiate static embedding server when
                    experimental_operating_mode==EXP_STATIC_EMBEDDINGS
        """
        if emb_database_output_cache_file is not None and emb_database_input_cache_file is not None:
            raise ValueError("ERROR: only one of the cache file options can be set at a time (input or output)")
        self.verbose = verbose
        self.mmd_alphas = mmd_alphas
        self.mmd_distance_routine = self._mmd_v1 if mmd_lib_version == 'v1' else self._mmd_v2
        auxcfg = self._filter_argdict(embedding_mdl_config, RuntimeWindowedAEServer)
        self.embsrv = RuntimeWindowedAEServer(**auxcfg, verbose=self.verbose)
        self.static_embsrv = None
        if experimental_static_emb_config is not None:
            auxcfg = self._filter_argdict(experimental_static_emb_config, RuntimeStaticAEServer)
            self.static_embsrv = RuntimeStaticAEServer(**auxcfg, verbose=self.verbose,
                                                       timefield=timefield)
        self.alerts_mastercopy = self._load_alerts(alertfn, self.verbose)
        self.alerts_for_query = deepcopy(self.alerts_mastercopy)
        self.alerts_for_db = deepcopy(self.alerts_mastercopy)
        self.win_len_tol = win_len_tol
        self.emb_db = None  # embeddings database
        self.db_time_array = []
        self.timefield = timefield
        self.db_alertid_array = []
        self.pca = None
        self.pca_dim = pca_dim
        self.info_db = None
        self.timeids_db = None
        self.encoder_version = encoder_version
        self._encoding_func = self._get_embeddings
        if experimental_operating_mode == EXP_ONE_HOT_ENCODINGS:
            self._encoding_func = self._get_oh_encodings
        elif experimental_operating_mode == EXP_STATIC_EMBEDDINGS:
            self._encoding_func = self._get_static_embeddings
        elif experimental_static_emb_config is not None:
            raise ValueError("ERROR: unknown experimental mode %s" % experimental_operating_mode)
        self.has_shown_warn = False
        # prepare query data
        assert (len(self.alerts_for_query) > 1)
        assert (self.timefield in self.alerts_for_query[0])
        assert ('epoch_time' in self.alerts_for_query[0][self.timefield])
        self._setup_query_constraints(query_constraints)

        # initialize embedding db from scratch
        if emb_database_input_cache_file is None:
            self._init_database(staggered_filters)
            if emb_database_output_cache_file is not None:  # and dump it
                self._dump_emb_db(emb_database_output_cache_file)
        else:  # load db from cache
            if staggered_filters is not None:
                if self.verbose: print("WARN: Option staggered_filters is ignored when loading from cache!")
            self._load_emb_db_fom_cache_file(emb_database_input_cache_file)

    @staticmethod
    def _filter_argdict(dict_to_filter, func_with_kwargs):
        # greps the required subset of key-value pairs from 'dict_to_filter' to pass into a function **kwargs
        s = inspect.signature(func_with_kwargs)
        keys = [param.name for param in s.parameters.values() if param.kind == param.POSITIONAL_OR_KEYWORD]
        return {key: dict_to_filter[key] for key in keys if key in dict_to_filter}

    def _init_database(self, staggered_filters):
        if self.verbose: print("INFO: Initializing embedding database")
        self.pca = None
        # prepare the embedding database
        assert(isinstance(self.alerts_for_db, list))
        assert (len(self.alerts_for_db) > 1)
        assert (self.timefield in self.alerts_for_db[0])
        assert ('epoch_time' in self.alerts_for_db[0][self.timefield])

        if staggered_filters is not None:  # perform staggering and embedding generation
            assert(isinstance(staggered_filters, str))
            if self.verbose: print("INFO: Staggered filters processing (for embedding db)...")
            self.alerts_for_db = self._filter_stack_embed_alerts(staggered_filters, self.alerts_for_db)
        else: # no staggering, just bulk embedding creation on the alert db as is
            if self.verbose: print("INFO: Generating embedding database")
            self.alerts_for_db = self._filter_stack_embed_alerts(None, self.alerts_for_db)
            # TODO remove the following soon: not needed
            # self.alerts_for_db are already set
            # self.emb_db, self.info_db, self.timeids_db = self._get_embeddings(self.alerts_for_db)
            # self.db_time_array = np.asarray([i[1]['epoch_time'] if isinstance(i[1], dict) else 0.0
            #                                  for i in self.info_db[self.timeids_db]])
            # self.db_alertid_array = np.asarray([i[0] if i[0] != '' else 0.0 for i in self.info_db[self.timeids_db]])
        if self.pca_dim is not None:
            orig_dim = next(iter(self.emb_db.items()))[1].shape[-1]
            if self.verbose: print("INFO: setting up PCA projection %d --> %d" % (orig_dim, self.pca_dim))
            assert(self.pca_dim <= orig_dim)
            assert(self.pca_dim > 0 and self.pca_dim < orig_dim)
            self.pca = PCA(n_components=orig_dim)
            self.pca.fit(np.vstack([i[1] for i in self.emb_db.items()]))
            for k in self.emb_db.keys():
                self.emb_db[k] = self.pca.transform(self.emb_db[k])[...,:self.pca_dim]
        if self.verbose: print("INFO: Database ready.")


    def _setup_query_constraints(self, query_constraints):
        if self.verbose:
            print("INFO: Setting up query database:")
        assert(self.alerts_mastercopy is not None)
        self.alerts_for_query = deepcopy(self.alerts_mastercopy)
        if query_constraints is not None:
            constraints_dict = {}
            for tok in query_constraints.split(','):
                fld, val = tok.strip().split(':')
                assert(len(fld) > 0 and len(val) > 0)
                constraints_dict[fld.strip()] = val.strip()
            if self.verbose:
                print("INFO: User-supplied Query constraints: %s" % str(query_constraints))
                print("INFO: Now filtering alert pool for queries...")
            self.alerts_for_query = filter_alerts(self.alerts_for_query, constraints_dict, verbose=self.verbose)
        if self.verbose: print("INFO: Sorting query alerts")
        self.alerts_for_query = sorted(self.alerts_for_query, key=lambda i: i[self.timefield]['epoch_time'])
        self.sorted_query_alert_times = np.asarray(
            [self.alerts_for_query[i][self.timefield]['epoch_time'] for i in range(len(self.alerts_for_query))])
        if len(self.alerts_for_query) < 1:
            raise ValueError("ERROR: no alerts left after filtering! Check constraints?")

    def _dump_emb_db(self, outfn):
        """
        Dumps all vars relevant to emb db
        :param outfn:
        :return:
        """
        D = {'emb_db': self.emb_db,
             'pca': self.pca,
             'db_alertid_array': self.db_alertid_array,
             'db_time_array': self.db_time_array,
             'alerts_for_db': self.alerts_for_db,
             'info_db': self.info_db,
             'timeids_db': self.timeids_db,
             'pca_dim': self.pca_dim
             }
        with open(outfn, 'wb') as of:
            pickle.dump(D, of)
            if self.verbose:
                print("INFO: Saved database file in %s. This file can be used with next instantiation" % outfn)


    def _load_emb_db_fom_cache_file(self, cachefn):
        """
        Loads all vars previously save via _dump_emb_db
        :param cachefn:
        :return:
        """
        with open(cachefn, 'rb') as f:
            D = pickle.load(f)
            assert('emb_db' in D and 'db_alertid_array' in D and 'db_time_array' in D)
            self.emb_db = D['emb_db']
            self.db_alertid_array = D['db_alertid_array']
            self.db_time_array = D['db_time_array']
            if 'pca' in D:
                self.pca = D['pca']
                self.pca_dim = D['pca_dim']
            if 'alerts_for_db' in D: self.alerts_for_db = D['alerts_for_db']
            if 'info_db' in D: self.info_db = D['info_db']
            if 'timeids_db' in D: self.timeids_db = D['timeids_db']
            if self.verbose: print("INFO: Loaded database cache from %s" % cachefn)


    def _filter_stack_embed_alerts(self, staggered_filters, alerts):
        """
        :param staggered_filters: comma-separated list of constraint strings
        :param alerts: json-formatted alerts
        :return: json-formatted alerts
        """
        new_alerts_count = 0
        new_alerts = {}
        filters_lst = []
        self.emb_db = {}
        self.db_time_array = {}
        self.db_alertid_array = {}
        if staggered_filters is not None:
            for tok in staggered_filters.split(','):
                fld, val = tok.strip().split(':')
                assert (len(fld) > 0 and len(val) > 0)
                filters_lst.append({fld: val})
        else:
            filters_lst = [{'__ALL__': None}]  # create bogus entry

        if self.verbose:
            print("INFO: User-supplied staggered filters: %s" % str(staggered_filters))
            print("INFO: Now filtering alerts...")
        for f in filters_lst:
            if list(f.keys())[0] != '__ALL__':
                if self.verbose: print("INFO: --> processing alerts with constraint %s" % (str(f)))
                partition = filter_alerts(alerts, f, verbose=self.verbose)
            else:
                if self.verbose: print("INFO: --> processing all alerts")
                partition = alerts
            if len(partition) < 5:
                if self.verbose: print("WARN: -- --> Partition size too small SKIPPING...")
                continue
            new_alerts[str(f)] = partition
            new_alerts_count += len(partition)
            if self.verbose: print("INFO: -- --> Generating embeddings for this partition (size = %d)" % len(partition))
            emb_db, info_db, timeids_db = self._encoding_func(partition) #self.embsrv.get_embeddings(partition)
            timeids_db = timeids_db.astype(int)
            self.emb_db[str(f)] = emb_db
            self.db_time_array[str(f)] = timeids_db
            self.db_alertid_array[str(f)] = info_db
            # self.db_time_array[str(f)] = np.asarray([i[1]['epoch_time'] if isinstance(i[1], dict) else 0.0
            #                                  for i in info_db[timeids_db]])
            # self.db_alertid_array[str(f)] = np.asarray([i[0] if i[0]!='' else 0.0 for i in info_db[timeids_db]])
        if self.verbose: print("INFO: Processed %d partitions, %d total db vectors." % (len(self.emb_db.keys()),
                                                 np.sum([self.emb_db[k].shape[0] for k in self.emb_db.keys()])))
        return new_alerts

    @staticmethod
    def _load_alerts(fn, verbose=False):
        """
        Loads alerts from a json formatted file.
        :param fn:
        :return:
        """
        with open(fn, 'rt') as f:
            alerts = json.load(f)
            if verbose:
                print("INFO: Loaded %d alerts from %s" % (len(alerts), fn))
        return alerts

    # @staticmethod
    # REMOVED
    # def _mmd_v1(x, y, alphas):
    #     tts = torch_two_sample.statistics_diff.MMDStatistic(x.shape[0], y.shape[0])
    #     return float(tts.__call__(torch.from_numpy(x), torch.from_numpy(y), alphas))

    @staticmethod
    def _mmd_v2(x, y, alphas):
        """
        Uses lib from https://github.com/djsutherland/mmd
        :param x: a list of numpys each [nsamp, dim]
        :param y: same as x
        :param alphas:
        :return: ndarray (xlistlen, ylistlen) of mmd distances
        """
        assert(isinstance(x, list) and isinstance(y, list))
        assert(len(x) and isinstance(x[0], np.ndarray) and len(x[0].shape)==2)
        assert(len(y) and isinstance(y[0], np.ndarray) and len(y[0].shape)==2)
        # summation is over gammas
        return(np.sum(mmd.rbf_mmd(X=x, Y=y, gammas=alphas, squared=True, n_jobs=40, ret_X_diag=False), axis=0))

    def _find_window_from_scratch(self, timearray, end_time, win_len_secs, win_len_tol=0.3):
        """
        :param timearray: sorted (ascending) ndarray of timestamps (seconds)
        :param end_time: time mark in seconds around which the window should end
        :param: win_len_secs: length of the window
        :param: win_len_tol: maximum allowed discrepancy (fraction) in window length found (shorter or longer)
                             (e.g., 0.3 == from 30% shorter up to 30% longer is OK).
                             If this check fails, the function returns None, None.
                             If win_len_tol == "None" this check will be disabled
        :return: start time index, end time index (or None, None)
        """
        assert (isinstance(timearray, np.ndarray))
        if len(timearray) < 2:
            print("you got a problem")
        assert (len(timearray) > 1)
        if timearray[1] < timearray[0] and (timearray[1] > 0. and timearray[0] > 0.):
            raise RuntimeError("ERROR: Alert ordering seems off. time1=%f time0=%f" % (timearray[1], timearray[0]))
        tei = np.argmin(np.abs(timearray - end_time))
        start_time = end_time - win_len_secs
        tsi = np.argmin(np.abs(timearray - start_time))
        if tsi >= tei:
            # print("WARN: Could not find a valid alert span for the requested time window.")
            return None, None
        if win_len_tol is not None:  # engage tolerance check
            ts = timearray[tsi]
            te = timearray[tei]
            rel_len = (te - ts) / win_len_secs
            if (rel_len > 1. + win_len_tol) or (rel_len < 1 - win_len_tol):
                if self.verbose and not self.has_shown_warn:
                    self.has_shown_warn = True
                    print("INFO: failed to find window within tolerance of %.1f%% ending at %d.. continuing"
                          " (will not show repeated warnings)."
                                       % (100*win_len_tol, end_time))
                return None, None
        return tsi, tei

    def _get_embeddings(self, query_alerts):
        """
        Helper routine that include any dim projections
        :param query_alerts:
        :return: embedding, info array, timeids
        """
        query, info_q, timeids_q = self.embsrv.get_embeddings(query_alerts)
        if self.pca is not None:
            query = self.pca.transform(query)[...,:self.pca_dim]
        return query, info_q, timeids_q

    def _get_oh_encodings(self, query_alerts):
        """
        Helper routine getting one-hot encodings (no embedding)
        :param query_alerts:
        :return: encoding, info array, timeids
        """
        return self.embsrv.get_oh_encodings(query_alerts)

    def _get_static_embeddings(self, query_alerts):
        """
        Helper routine getting static autoencoder embeddings
        :param query_alerts:
        :return: encoding, info array, timeids
        """
        return self.static_embsrv.get_embeddings(query_alerts)

    def search(self, time_of_interest, window_len, which_alert_to_drop, topk=0, subsample_search=1,
               adapt_window_len=True, alert_hit_list=None):
        """
        Returns ranked times based on similarity to a query. A query is a window of length
        window_len ending at time_of_interest with which_alert_to_drop deleted.
        The returned times are end times of best matching windows across the database.
        :param time_of_interest: time mark (in secs) delineating the end of the query window
        :param window_len: query window length (in secs)
        :param which_alert_to_drop: None or index of alert to drop from the query window (0-based index).
                        Example: 1 refers to the second oldest alert within the query window
        :param topk: truncate the result to this many (0 means return All)
        :param subsample_search: > 1 will speed up the search (experimental)
        :param adapt_window_len: True -> window_len will be adjusted based on the query length found
        :param gt_dict: if not None will be used as a look-up for an early bailout of search
        :return: list, dict. Ranked list of ending times (in seconds) representing best matching windows to the query
                 or None. Dict with keys holding info on which alert ids ended up in the query window + which dropped.
        """
        self.has_shown_warn = False # reset flag to shown one-time warnings
        info = {}
        win_len_tol = self.win_len_tol if not adapt_window_len else None # do not subject query to window tolerance if adaptation ON

        tsi, tei = self._find_window_from_scratch(self.sorted_query_alert_times, time_of_interest,
                                                  window_len, win_len_tol=win_len_tol)
        if tsi is None:
            return [], info
        if (which_alert_to_drop is not None and tei-tsi < 3) or (which_alert_to_drop is None and tei-tsi < 2):
            print("WARN: Insufficient number of alerts found within the requested window (%d)" % (tei-tsi))
            return [], info
        ts = self.sorted_query_alert_times[tsi]
        te = self.sorted_query_alert_times[tei]
        if adapt_window_len:
            window_len = te - ts
            if self.verbose:
                print("INFO: Adjusting window_len to %.1f (%.2f hrs), to match query length found, per user option."
                      % (window_len, window_len/3600))
        if self.verbose and subsample_search != 1:
            print("WARN: running search with subsampling factor %d" % subsample_search)

        # bookkeeping of alerts before and after dropping
        info['all_window_alerts'] = [self.alerts_for_query[i]['id'] for i in range(tsi, tei+1)]

        # let's see if we should bail out due to the fact that none of these alerts are appearing in the
        # ground truth table
        if alert_hit_list is not None:
            hits = [a in alert_hit_list for a in info['all_window_alerts']]
            if not any(hits):
                print("WARNING: none of the window alerts are hits...BAILING OUT as per option.")
                return [], info
            else:
                if self.verbose: print("INFO: There are %d hits within the window of %d alerts. Proceeding."
                      %(int(np.sum(hits)), len(hits)))


        if which_alert_to_drop is not None:
            if self.verbose: print("INFO: removing alert %d (index %d) from query"
                                % (which_alert_to_drop, tsi + which_alert_to_drop))
            l = list(range(tsi, tei+1))
            l.remove(tsi + which_alert_to_drop)
            query_alerts = [self.alerts_for_query[i] for i in l]
            info['dropped_alert'] = self.alerts_for_query[tsi + which_alert_to_drop]['id']
        else:
            query_alerts = self.alerts_for_query[tsi:tei+1]
            info['dropped_alert'] = None
        # Generate embedding query
        query, info_q, timeids_q = self._encoding_func(query_alerts)  #self.embsrv.get_embeddings(query_alerts)
        if self.verbose: print("INFO: Query created with size %s" % str(query.shape))
        if query.shape[0] < 2:
            print("ERROR: Query window size insufficient (< 2 vectors). No search performed.")
            return [], info

        # Search in the database
        mmd_query_distance = []
        if self.verbose: print("INFO: Searching")
        for k in self.emb_db.keys():
            if self.verbose: print("DEBUG: Searching partition %s ..." % k)
            t1i = t2i = -1
            this_subsample_search = subsample_search if (self.db_time_array[k].shape[0] / subsample_search) >= 10 else 1
            for ti in range(0, self.db_time_array[k].shape[0], this_subsample_search):
                t = self.db_time_array[k][ti]
                if t == 0.:  # no alert here
                    continue
                if t - window_len < self.db_time_array[k][0]:  # window exceeds limits
                    continue
                if (t - window_len >= ts and t - window_len <= te) or (t >= ts and t <= te):  # overlaps w/query
                    continue
                if t1i is not None and t1i < 0: # first time
                    t1i, t2i = self._find_window_from_scratch(self.db_time_array[k], t, window_len,
                                                              win_len_tol=self.win_len_tol)
                    if t1i is None or t2i is None:
                        t1i=t2i=-1
                elif t1i is not None and t2i is not None and t1i >= 0 and t2i >= 0: # use previous values
                    # run search on the previous window expanded by one future step in index
                    # this is to speed things up
                    newt1i, newt2i = self._find_window_from_scratch(self.db_time_array[k][t1i:ti+1],
                                                              t, window_len, win_len_tol=self.win_len_tol)
                    if newt1i is None or newt2i is None:
                        continue
                    # print("JIRIDEBUG: Before window search, span=%d:%d --> after span:%d:%d" %(t1i, ti, newt1i, newt2i))
                    # transform to global indexing
                    newt1i += t1i
                    newt2i += t1i
                    if t1i is not None and t2i is not None and newt1i == t1i and newt2i == t2i:
                        continue
                        # no change in window
                    t1i = newt1i
                    t2i = newt2i

                if t1i is None or t2i is None:
                    continue
                if t2i - t1i < 2:
                    # print("WARN: Found db window with < 2 vectors. SKIPPING.")
                    continue
                # print("JIRIDEBUG: partition=%s, Window t1i=%d (%f), t2i=%d (%f), dur = %.1f secs" %
                #       (k, t1i, self.db_time_array[k][t1i], t2i, self.db_time_array[k][t2i],
                #        (self.db_time_array[k][t2i]-self.db_time_array[k][t1i])))
                # if self.mmd_distance_routine == self._mmd_v1:
                #     if torch_two_sample is None:
                #         raise ImportError("torch_two_sample is not installed.")
                #     mmd_distance = self._mmd_v1(query, self.emb_db[k][t1i:t2i + 1], self.mmd_alphas)
                if self.mmd_distance_routine == self._mmd_v2:
                    mmd_distance = np.squeeze(self._mmd_v2(x=[query], y=[self.emb_db[k][t1i:t2i + 1]],
                                                           alphas=self.mmd_alphas)[0][0])
                else:
                    raise RuntimeError("ERROR: unknown mmd routine")
                mmd_query_distance.append((mmd_distance,
                                           k,
                                           self.db_time_array[k][t1i],
                                           self.db_time_array[k][t2i]))
        mmd_query_distance = sorted(mmd_query_distance, key=lambda i: i[0])
        if self.verbose: print("INFO: Done.")
        if topk > 0:
            return mmd_query_distance[:topk], info
        else:
            return mmd_query_distance, info


    def search_drop_each(self, time_of_interest, window_len, subsample_search=1,
               adapt_window_len=True, alert_hit_list=None):
        """
        Returns ranked times based on similarity to a query. A query is a window of length
        window_len ending at time_of_interest. All alerts will be dropped individually one by one.
        The returned times are end times of best matching windows across the database.
        :param time_of_interest: time mark (in secs) delineating the end of the query window
        :param window_len: query window length (in secs)
        :param topk: truncate the result to this many (0 means return All)
        :param subsample_search: > 1 will speed up the search (experimental)
        :param adapt_window_len: True -> window_len will be adjusted based on the query length found
        :param gt_dict: if not None will be used as a look-up for an early bailout of search
        :return: Dict. Contains: Ranked scores along with info structure on which alert ids
                    ended up in the query window + which dropped.
        """
        self.has_shown_warn = False # reset flag to shown one-time warnings
        info = {}
        win_len_tol = self.win_len_tol if adapt_window_len else None # do not subject query to window tolerance if adaptation ON

        tsi, tei = self._find_window_from_scratch(self.sorted_query_alert_times, time_of_interest,
                                                  window_len, win_len_tol=win_len_tol)
        if tsi is None:
            return info
        if tei-tsi < 3:
            print("WARN: Insufficient number of alerts found within the requested window (%d)" % (tei-tsi))
            return info
        ts = self.sorted_query_alert_times[tsi]
        te = self.sorted_query_alert_times[tei]
        if adapt_window_len:
            window_len = te - ts
            if self.verbose:
                print("INFO: Adjusting window_len to %.1f (%.2f hrs), to match query length found, per user option."
                      % (window_len, window_len/3600))
        if self.verbose and subsample_search != 1:
            print("WARN: running search with subsampling factor %d" % subsample_search)

        # bookkeeping of alerts before and after dropping
        info['all_window_alerts'] = [self.alerts_for_query[i]['id'] for i in range(tsi, tei+1)]

        # let's see if we should bail out due to the fact that none of these alerts are appearing in the
        # ground truth table
        if alert_hit_list is not None:
            hits = [a in alert_hit_list for a in info['all_window_alerts']]
            if not any(hits):
                print("WARNING: none of the window alerts are hits...BAILING OUT as per option.")
                return info
            else:
                if self.verbose: print("INFO: There are %d hits within the window of %d alerts. Proceeding."
                      %(int(np.sum(hits)), len(hits)))

        total_num_alerts = len(info['all_window_alerts'])
        if self.verbose: print("INFO: Generating embedded queries for all drops...")
        for which_alert_to_drop in range(total_num_alerts):
            if self.verbose: print("INFO: removing alert %d (index %d) of total %d from query"
                                % (which_alert_to_drop+1, tsi + which_alert_to_drop, total_num_alerts))
            l = list(range(tsi, tei+1))
            l.remove(tsi + which_alert_to_drop)
            # "this query" refers to the query with 'this' alert removed
            this_query_alerts = [self.alerts_for_query[i] for i in l]
            this_query_dict = {'id': self.alerts_for_query[tsi + which_alert_to_drop]['id']}
            info['dropped_alert_%d' % which_alert_to_drop] = this_query_dict  # we will be updating this_query_dict later on
            # Generate embedding query
            try:
                this_query, info_q, timeids_q = self._encoding_func(this_query_alerts)  #self.embsrv.get_embeddings(query_alerts)
            except ValueError as e:
                print(e)
                this_query = None
            if this_query is None or this_query.shape[0] < 2:
                print("ERROR: Query window size insufficient (< 2 vectors). Ignoring this drop.")
                this_query_dict['query_embedding'] = this_query_dict['query_info'] = this_query_dict['query_timeids'] = None
                continue
            if self.verbose: print("INFO: Query created with size %s" % str(this_query.shape))
            this_query_dict['query_embedding'] = this_query
            this_query_dict['query_info'] = info_q
            this_query_dict['query_timeids'] = timeids_q
        # at this point we have all leave-one-out queries processed and stored

        # Search in the database
        mmd_query_distance = [[] for _ in range(total_num_alerts)]   # indexing [alert_dropped][score]
        # collect queries for mmd calc
        queries = []
        dropped_ids = []
        for dropped_alert_id in range(total_num_alerts):
            emb_q = info['dropped_alert_%d' % dropped_alert_id]['query_embedding']
            if emb_q is not None:
                queries.append(emb_q)
                dropped_ids.append(dropped_alert_id)
        if len(queries) < 1: # wow, there were no valid queries found
            print("WARN: No queries found for this task - nothing to do!")
            return {}

        if self.emb_db[next(iter(self.emb_db.keys()))].shape[-1] != queries[0].shape[-1]:
            raise RuntimeError("ERROR: Query vs. DB encoding dimensions (%d vs. %d) differ! (wrong cache?)"
                               % (queries[0].shape[-1], self.emb_db[next(iter(self.emb_db.keys()))].shape[-1]))
        if self.verbose: print("INFO: Searching")
        for k in self.emb_db.keys():
            if self.verbose: print("DEBUG: Searching partition %s ..." % k)
            t1i = t2i = -1
            this_subsample_search = subsample_search if (self.db_time_array[k].shape[0] / subsample_search) >= 10 else 1
            seq_range = range(0, self.db_time_array[k].shape[0], this_subsample_search)
            disp_N = len(seq_range)
            disp_chunk = np.floor(disp_N/10)
            for c, ti in enumerate(seq_range):
                if self.verbose and (disp_chunk > 0 and c % disp_chunk == 0):
                    print("\r%d%%" % int(100*c/disp_N), end="", flush=True)

                t = self.db_time_array[k][ti]
                if t == 0.:  # no alert here
                    continue
                if t - window_len < self.db_time_array[k][0]:  # window exceeds limits
                    continue
                if (t - window_len >= ts and t - window_len <= te) or (t >= ts and t <= te):  # overlaps w/query
                    continue
                if t1i is not None and t1i < 0: # first time
                    t1i, t2i = self._find_window_from_scratch(self.db_time_array[k], t, window_len,
                                                              win_len_tol=self.win_len_tol)
                    if t1i is None or t2i is None:
                        t1i=t2i=-1
                elif t1i is not None and t2i is not None and t1i >= 0 and t2i >= 0: # use previous values
                    # run search on the previous window expanded by one future step in index
                    # this is to speed things up
                    newt1i, newt2i = self._find_window_from_scratch(self.db_time_array[k][t1i:ti+1],
                                                              t, window_len, win_len_tol=self.win_len_tol)
                    if newt1i is None or newt2i is None:
                        continue
                    # print("JIRIDEBUG: Before window search, span=%d:%d --> after span:%d:%d" %(t1i, ti, newt1i, newt2i))
                    # transform to global indexing
                    newt1i += t1i
                    newt2i += t1i
                    if t1i is not None and t2i is not None and newt1i == t1i and newt2i == t2i:
                        continue
                        # no change in window
                    t1i = newt1i
                    t2i = newt2i

                if t1i is None or t2i is None:
                    continue
                if t2i - t1i < 2:
                    # print("WARN: Found db window with < 2 vectors. SKIPPING.")
                    continue

                # print("JIRIDEBUG: partition=%s, Window t1i=%d (%f), t2i=%d (%f), dur = %.1f secs" %
                #       (k, t1i, self.db_time_array[k][t1i], t2i, self.db_time_array[k][t2i],
                #        (self.db_time_array[k][t2i]-self.db_time_array[k][t1i])))

                # if self.mmd_distance_routine == self._mmd_v1:
                #     if torch_two_sample is None:
                #         raise ImportError("torch_two_sample is not installed.")
                #     print('Progress', end=': ')
                #     for dropped_alert_id in range(total_num_alerts):
                #         emb_q = info['dropped_alert_%d' % dropped_alert_id]['query_embedding']
                #         if emb_q is not None:
                #             mmd_query_distance[dropped_alert_id].append((self._mmd_v1(emb_q, self.emb_db[k][t1i:t2i + 1], self.mmd_alphas),
                #                                k,
                #                                self.db_time_array[k][t1i],
                #                                self.db_time_array[k][t2i]))
                #             print('.', end='', flush=True)
                #         else:
                #             continue
                #     print('', flush=True)
                if self.mmd_distance_routine == self._mmd_v2:
                    # mmd_v2
                    # this version does all mmd calculations in one shot, so first collect all the queries in a list
                    # and now calc the mmds
                    mmd_res = np.squeeze(self._mmd_v2(queries, [self.emb_db[k][t1i:t2i + 1]], self.mmd_alphas))
                    assert(len(mmd_res)==len(dropped_ids))
                    # mmd_res is now [numqueries,] --> distribute
                    for di, r in zip(dropped_ids, mmd_res):
                        mmd_query_distance[di].append((r, k, self.db_time_array[k][t1i], self.db_time_array[k][t2i]))
                else:
                    raise RuntimeError("ERROR: Unknown mmd_distance_routine")
            if self.verbose: print("")
        for dropped_alert_id in range(total_num_alerts):
            info['dropped_alert_%d' % dropped_alert_id]['scores'] = sorted(mmd_query_distance[dropped_alert_id], key=lambda i: i[0])
        if self.verbose: print("INFO: Done.")
        return info

if __name__ == "__main__":
    import json
    import numpy as np
    import argparse

    parser = argparse.ArgumentParser(description="Generate an alert cache file for IA search & rank runtime.")
    parser.add_argument('-i', '--inFile', dest='alertfn', required=True, metavar='<json>', default=None,
                        help="json file with alerts")
    parser.add_argument('-o', '--outFile', dest='cachefn', required=True, metavar='<outfn>',
                        help="Cache file to be generated. Can be used with runtime for fast loading.")
    parser.add_argument('-config', '--config', dest='configfn', required=True, metavar='<json>',
                        help="Package config file. ")
    parser.add_argument('-filters', '--filters', dest='staggered_filters', required=True, metavar='<str>',
                        help="Comma-separated filters to stagger alerts by partition (usually by datacenter). "
                             "Filter format: <key>:<value>. Ex.: 'datacenter:ams01,datacenter:ams02'. "
                             "The value can be '' (will do no filtering)")
    parser.add_argument('-tfield', '--tfield', dest='timefield', required=False, metavar='<str>',
                        help="Key within an alert carrying timestamp", default='updateTime')
    parser.add_argument('-mmd_alphas', '--mmd_alphas', dest='mmd_alphas', required=False, default="0.1,0.5",
                        metavar='<str>', help="Comma-separated alpha values for the MMD")
    parser.add_argument('-pca_dim', '--pca_dim', dest='pca_dim', required=False, default=None,
                        metavar='<int>', help="Activates projection PCA.")
    parser.add_argument('-s', '--silent', dest='silent', required=False, action='store_true',
                        help="Turn off verbosity.")
    args = parser.parse_args()

    verbose = True if not args.silent else False
    with open(args.configfn) as f:
        config = json.load(f)

    mmd_alphas = [float(s.strip()) for s in args.mmd_alphas.split(',')]
    S = SearchAndRankWindowedEmbeddings(embedding_mdl_config=config, alertfn=args.alertfn,
                                        verbose=verbose, mmd_alphas=mmd_alphas,
                                        staggered_filters=args.staggered_filters,
                                        emb_database_output_cache_file=args.cachefn,
                                        pca_dim=int(args.pca_dim) if args.pca_dim is not None else None,
                                        timefield=args.timefield)

    if verbose:
        print("INFO: Completed.")
