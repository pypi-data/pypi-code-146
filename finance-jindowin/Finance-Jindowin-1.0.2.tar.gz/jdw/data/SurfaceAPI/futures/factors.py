# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from jdw.data.SurfaceAPI.factors import Factors


class FutFactors(Factors):

    def __init__(self) -> None:
        super(FutFactors, self).__init__(name='fut_factor')
