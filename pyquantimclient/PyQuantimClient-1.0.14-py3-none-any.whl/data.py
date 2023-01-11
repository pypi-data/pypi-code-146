# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime as dt
from .api import quantim

class time_series(quantim):
    def __init__(self, username, password, secretpool, env="qa"):
        super().__init__(username, password, secretpool, env)

    def get_series(self, tks, ref_curr='Origen', join='outer'):
        '''
        Get series
        '''
        data = {'tks':list(tks), 'ref_curr':ref_curr, 'join':join}
        resp = self.api_call('get_series', method="post", data=data, verify=False)
        ref_curr, ts, summ = resp['ref_curr'], pd.DataFrame(resp['ts']).set_index("Date"), pd.DataFrame(resp['summ'])
        return ref_curr, ts, summ
