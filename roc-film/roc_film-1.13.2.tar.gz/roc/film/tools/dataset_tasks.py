
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import methods to extract data from RPW packets
# IMPORTANT: Make sure the name/alias of the imported function is the same
# than the name/alias of the output dataset in the descriptor
from roc.rap.tasks.lfr.normal_burst import bp1 as l1_surv_bp1
from roc.rap.tasks.lfr.normal_burst import bp2 as l1_surv_bp2
from roc.rap.tasks.lfr.normal_burst import cwf as l1_surv_cwf
from roc.rap.tasks.lfr.normal_burst import swf as l1_surv_swf
from roc.rap.tasks.lfr.normal_burst import asm as l1_surv_asm
from roc.rap.tasks.tds.normal_rswf import set_rswf as l1_surv_rswf
from roc.rap.tasks.tds.normal_tswf import set_tswf as l1_surv_tswf
from roc.rap.tasks.tds.normal_mamp import set_mamp as l1_surv_mamp
from roc.rap.tasks.tds.normal_stat import set_stat as l1_surv_stat
from roc.rap.tasks.tds.normal_hist1d import set_hist1d as l1_surv_hist1d
from roc.rap.tasks.tds.normal_hist2d import set_hist2d as l1_surv_hist2d
from roc.rap.tasks.tds.lfm_rswf import set_rswf as l1_lfm_rswf
from roc.rap.tasks.tds.lfm_cwf import set_cwf as l1_lfm_cwf
from roc.rap.tasks.tds.lfm_psd import set_psd as l1_lfm_psd
from roc.rap.tasks.tds.lfm_sm import set_sm as l1_lfm_sm
from roc.rap.tasks.thr import extract_tnr_data as l1_surv_tnr
from roc.rap.tasks.thr import extract_hfr_data as l1_surv_hfr
from roc.rap.tasks.bia import extract_bia_sweep as l1_bia_sweep
from roc.rap.tasks.bia import extract_bia_current as l1_bia_current

from roc.rap.tasks.tds.sbm import rswf as l1_sbm1_rswf
from roc.rap.tasks.tds.sbm import tswf as l1_sbm2_tswf
from roc.rap.tasks.lfr.sbm1 import bp1 as l1_sbm1_bp1
from roc.rap.tasks.lfr.sbm1 import bp2 as l1_sbm1_bp2
from roc.rap.tasks.lfr.sbm1 import cwf as l1_sbm1_cwf
from roc.rap.tasks.lfr.sbm2 import bp1 as l1_sbm2_bp1
from roc.rap.tasks.lfr.sbm2 import bp2 as l1_sbm2_bp2
from roc.rap.tasks.lfr.sbm2 import cwf as l1_sbm2_cwf
