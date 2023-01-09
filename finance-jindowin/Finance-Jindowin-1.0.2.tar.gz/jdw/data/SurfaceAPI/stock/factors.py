# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from jdw.data.SurfaceAPI.factors import Factors


class StkFactors(Factors):

    def __init__(self) -> None:
        super(StkFactors, self).__init__(name='stk_factor')
