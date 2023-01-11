##
# File:  SiteGeneratorExec.py
# Date: 29-Dec-2020  jdw
#
#  Execution wrapper  --  PDBx/mmCIF site generator
#
#  Updates:
#
##
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import argparse
import logging
import os
import sys

from mmcif.sitegen.wf.HtmlGeneratorWf import HtmlGeneratorWf
from mmcif.sitegen.wf.NeighborFiguresWf import NeighborFiguresWf


HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()


def main():
    parser = argparse.ArgumentParser()
    #
    parser.add_argument("--web_gen_path", default=None, help="Top path to website generated content")
    parser.add_argument("--web_file_assets_path", default=None, help="Top path for website source file assests")
    parser.add_argument("--html", default=False, action="store_true", help="Generate HTML content")
    parser.add_argument("--images", default=False, action="store_true", help="Generate image content")
    parser.add_argument("--test_mode_flag", default=False, action="store_true", help="Test mode flag (default=False)")
    #
    args = parser.parse_args()
    #
    try:
        websiteGenPath = args.web_gen_path
        websiteFileAssetsPath = args.web_file_assets_path
        testModeFlag = args.test_mode_flag
        doHtml = args.html
        doImages = args.images
    except Exception as e:
        logger.exception("Argument processing problem %s", str(e))
        parser.print_help(sys.stderr)
        exit(1)
    #
    if not websiteGenPath or not websiteFileAssetsPath:
        parser.print_help(sys.stderr)
        exit(1)
    # ----------------------- - ----------------------- - ----------------------- - ----------------------- - ----------------------- -
    if doHtml:
        hgWf = HtmlGeneratorWf(websiteGenPath=websiteGenPath, websiteFileAssetsPath=websiteFileAssetsPath, testMode=testModeFlag)
        ok = hgWf.run()
        logger.info("Completed HTML generation actions with status %r", ok)

    if doImages:
        nfWf = NeighborFiguresWf(websiteGenPath=websiteGenPath, websiteFileAssetsPath=websiteFileAssetsPath, testMode=testModeFlag)
        ok = nfWf.run()
        logger.info("Completed image generation actions with status %r", ok)


if __name__ == "__main__":
    main()
