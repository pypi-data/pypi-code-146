#!/usr/bin/env python

import sys
from xpycommon import ValNameDesc, ValNameDescs
from xpycommon.common import upgrade
from xpycommon.at_cmd import AtCode, AtCodes
from xpycommon.log import Logger, DEBUG
from xpycommon.ui import red
from xpycommon.bluetooth import oui_org_uap_to_naps


logger = Logger(__name__, DEBUG, filename='./log')


def main():
    """"""
    naps = oui_org_uap_to_naps('Huawei Device Co., Ltd.', 0xA0)
    print(naps)


if __name__ == '__main__':
    main()
