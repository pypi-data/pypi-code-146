# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from agconnect.common_server.src.config.config_service import ConfigService


class CloudGwUrlUtils:
    PROJECT_CLOUD_GW_URL = 'project_cloudgw_url'
    TEAM_CLOUD_GW_URL = 'team_cloudgw_url'
    TEAM_CLOUD_GW_BACK_URL = 'team_cloudgw_url_backup'

    @staticmethod
    def check_use_back_url(err, enable_back_url=None):
        if enable_back_url and err.message:
            return True
        else:
            return False

    @staticmethod
    def get_cloud_gw_url_by_region(region=None, use_back_up=False):
        if region:
            project_url = ConfigService.get_service("COMMON").get_config_value(
                CloudGwUrlUtils.PROJECT_CLOUD_GW_URL, [])
            for _, ele in enumerate(project_url):
                if ele.get('region') == region:
                    if use_back_up:
                        return ele.get('backupUrl')
                    else:
                        return ele.get('url')
            if use_back_up:
                return ConfigService.get_service("COMMON").get_config_value(
                    CloudGwUrlUtils.TEAM_CLOUD_GW_BACK_URL)
            return ConfigService.get_service("COMMON").get_config_value(
                CloudGwUrlUtils.TEAM_CLOUD_GW_URL)
        else:
            return None
