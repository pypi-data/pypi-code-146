# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""Module defining extensions for Automation:
----------
Automation
----------
This class contains the helper methods extensions used to register, deploy, and test the created tasks. Additional helper
functions for retrieving details of existing tasks on the Switch Automation Platform are also included in this module.
"""
from .automation import deploy_as_upload_data_feed, deploy_on_timer
__all__ = ['deploy_as_upload_data_feed', 'deploy_on_timer']
