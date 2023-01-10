#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Contains task to create the RPW L1 Bias current CDF files."""

import os

from poppy.core.logger import logger
from poppy.core.target import FileTarget
from poppy.core.task import Task
from roc.rpl import Time

from roc.film.tools.file_helpers import get_l0_files, get_output_dir, is_output_dir, l0_to_trange_cdf

__all__ = ['L0ToL1BiaCurrent']

@FileTarget.input(identifier='l0_file', many=True, filepath=get_l0_files)
@FileTarget.output(identifier='l1_bia_current')
@Task.as_task(plugin_name='roc.film', name='l0_to_l1_bia_current')
def L0ToL1BiaCurrent(task):
    """
    Task to generate l1 bias current CDF from l0 file(s)

    :param task:
    :return:
    """

    # Get list of input l0 file(s)
    l0_file_list = task.inputs['l0_file'].filepath

    # Get --monthly keyword
    monthly = task.pipeline.get('monthly', default=False, args=True)

    # Get overwrite argument
    overwrite = task.pipeline.get('overwrite', default=False, args=True)

    # Get cdag keyword
    is_cdag = task.pipeline.get('cdag', default=False, args=True)

    # Get (optional) arguments for SPICE
    predictive = task.pipeline.get('predictive', default=False, args=True)
    kernel_date = task.pipeline.get('kernel_date', default=None, args=True)
    no_spice = task.pipeline.get('no_spice', default=False, args=True)

    # Get/create Time singleton
    Time(predictive=predictive,
         kernel_date=kernel_date,
         no_spice=no_spice)

    # Get products directory (folder where final output files will be moved)
    products_dir = task.pipeline.get('products_dir',
                                     default=[None], args=True)[0]

    # Get output dir
    output_dir = get_output_dir(task.pipeline)
    if not is_output_dir(output_dir,
                         products_dir=products_dir):
        logger.info(f'Making {output_dir}')
        os.makedirs(output_dir)
    else:
        logger.debug(f'Output files will be '
                    f'saved into folder {output_dir}')

    try:
        l0_to_trange_cdf(task, 'l0_to_l1_bia_current',
                         l0_file_list, output_dir,
                         monthly=monthly,
                         unique=True,
                         is_cdag=is_cdag,
                         overwrite=overwrite)
    except:
        logger.exception('L1 Bias current CDF production has failed!')
