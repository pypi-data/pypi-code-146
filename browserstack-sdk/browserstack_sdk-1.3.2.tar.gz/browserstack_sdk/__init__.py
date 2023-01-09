# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack1ll_opy_ = 2048
bstack1l1l_opy_ = 7
def bstack11_opy_ (bstack11l_opy_):
    global bstack1ll1_opy_
    stringNr = ord (bstack11l_opy_ [-1])
    bstackl_opy_ = bstack11l_opy_ [:-1]
    bstack1l1_opy_ = stringNr % len (bstackl_opy_)
    bstack1l_opy_ = bstackl_opy_ [:bstack1l1_opy_] + bstackl_opy_ [bstack1l1_opy_:]
    if bstack1_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll_opy_ - (bstack111_opy_ + stringNr) % bstack1l1l_opy_) for bstack111_opy_, char in enumerate (bstack1l_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1ll_opy_ - (bstack111_opy_ + stringNr) % bstack1l1l_opy_) for bstack111_opy_, char in enumerate (bstack1l_opy_)])
    return eval (bstack1lll_opy_)
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
from packaging import version
from browserstack.local import Local
bstack1ll1l_opy_ = {
	bstack11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪৄ"): bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷ࠭৅"),
  bstack11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭৆"): bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡯ࡪࡿࠧে"),
  bstack11_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨৈ"): bstack11_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ৉"),
  bstack11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ৊"): bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨো"),
  bstack11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧৌ"): bstack11_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷ্ࠫ"),
  bstack11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧৎ"): bstack11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࠫ৏"),
  bstack11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ৐"): bstack11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ৑"),
  bstack11_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧ৒"): bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭ࠧ৓"),
  bstack11_opy_ (u"ࠪࡧࡴࡴࡳࡰ࡮ࡨࡐࡴ࡭ࡳࠨ৔"): bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡳࡰ࡮ࡨࠫ৕"),
  bstack11_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࠪ৖"): bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࠪৗ"),
  bstack11_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫ৘"): bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫ৙"),
  bstack11_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨ৚"): bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡹ࡭ࡩ࡫࡯ࠨ৛"),
  bstack11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡒ࡯ࡨࡵࠪড়"): bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡒ࡯ࡨࡵࠪঢ়"),
  bstack11_opy_ (u"࠭ࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࡎࡲ࡫ࡸ࠭৞"): bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࡎࡲ࡫ࡸ࠭য়"),
  bstack11_opy_ (u"ࠨࡩࡨࡳࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭ৠ"): bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡩࡨࡳࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭ৡ"),
  bstack11_opy_ (u"ࠪࡸ࡮ࡳࡥࡻࡱࡱࡩࠬৢ"): bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸ࡮ࡳࡥࡻࡱࡱࡩࠬৣ"),
  bstack11_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ৤"): bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ৥"),
  bstack11_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡈࡵ࡭࡮ࡣࡱࡨࡸ࠭০"): bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡮ࡣࡶ࡯ࡈࡵ࡭࡮ࡣࡱࡨࡸ࠭১"),
  bstack11_opy_ (u"ࠩ࡬ࡨࡱ࡫ࡔࡪ࡯ࡨࡳࡺࡺࠧ২"): bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡬ࡨࡱ࡫ࡔࡪ࡯ࡨࡳࡺࡺࠧ৩"),
  bstack11_opy_ (u"ࠫࡲࡧࡳ࡬ࡄࡤࡷ࡮ࡩࡁࡶࡶ࡫ࠫ৪"): bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡄࡤࡷ࡮ࡩࡁࡶࡶ࡫ࠫ৫"),
  bstack11_opy_ (u"࠭ࡳࡦࡰࡧࡏࡪࡿࡳࠨ৬"): bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦࡰࡧࡏࡪࡿࡳࠨ৭"),
  bstack11_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡡࡪࡶࠪ৮"): bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡸࡸࡴ࡝ࡡࡪࡶࠪ৯"),
  bstack11_opy_ (u"ࠪ࡬ࡴࡹࡴࡴࠩৰ"): bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡬ࡴࡹࡴࡴࠩৱ"),
  bstack11_opy_ (u"ࠬࡨࡦࡤࡣࡦ࡬ࡪ࠭৲"): bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡦࡤࡣࡦ࡬ࡪ࠭৳"),
  bstack11_opy_ (u"ࠧࡸࡵࡏࡳࡨࡧ࡬ࡔࡷࡳࡴࡴࡸࡴࠨ৴"): bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡸࡵࡏࡳࡨࡧ࡬ࡔࡷࡳࡴࡴࡸࡴࠨ৵"),
  bstack11_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡆࡳࡷࡹࡒࡦࡵࡷࡶ࡮ࡩࡴࡪࡱࡱࡷࠬ৶"): bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧ࡭ࡸࡧࡢ࡭ࡧࡆࡳࡷࡹࡒࡦࡵࡷࡶ࡮ࡩࡴࡪࡱࡱࡷࠬ৷"),
  bstack11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ৸"): bstack11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ৹"),
  bstack11_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪ৺"): bstack11_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬ৻"),
  bstack11_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨৼ"): bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ৽"),
  bstack11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡑࡩࡹࡽ࡯ࡳ࡭ࠪ৾"): bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡺࡹࡴࡰ࡯ࡑࡩࡹࡽ࡯ࡳ࡭ࠪ৿"),
  bstack11_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡖࡲࡰࡨ࡬ࡰࡪ࠭਀"): bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡴࡥࡵࡹࡲࡶࡰࡖࡲࡰࡨ࡬ࡰࡪ࠭ਁ"),
  bstack11_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭ਂ"): bstack11_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡔࡵ࡯ࡇࡪࡸࡴࡴࠩਃ"),
  bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ਄"): bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫਅ"),
  bstack11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫਆ"): bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸࡵࡵࡳࡥࡨࠫਇ"),
  bstack11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨਈ"): bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨਉ"),
  bstack11_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࠪਊ"): bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡪࡲࡷࡹࡔࡡ࡮ࡧࠪ਋"),
}
bstack11l1l_opy_ = [
  bstack11_opy_ (u"ࠪࡳࡸ࠭਌"),
  bstack11_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧ਍"),
  bstack11_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ਎"),
  bstack11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫਏ"),
  bstack11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫਐ"),
  bstack11_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬ਑"),
  bstack11_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ਒"),
]
bstack1llll_opy_ = {
  bstack11_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ਓ"): bstack11_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨਔ"),
  bstack11_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧਕ"): [bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨਖ"), bstack11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪਗ")],
  bstack11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ਘ"): bstack11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧਙ"),
  bstack11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧਚ"): bstack11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫਛ"),
  bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪਜ"): [bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧਝ"), bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭ਞ")],
  bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩਟ"): bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫਠ"),
  bstack11_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧਡ"): bstack11_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩਢ"),
  bstack11_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬਣ"): [bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ਤ"), bstack11_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨਥ")],
  bstack11_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧਦ"): [bstack11_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡕࡶࡰࡈ࡫ࡲࡵࡵࠪਧ"), bstack11_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࠪਨ")]
}
bstack111l_opy_ = [
  bstack11_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ਩"),
  bstack11_opy_ (u"ࠬࡶࡡࡨࡧࡏࡳࡦࡪࡓࡵࡴࡤࡸࡪ࡭ࡹࠨਪ"),
  bstack11_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬਫ"),
  bstack11_opy_ (u"ࠧࡴࡧࡷ࡛࡮ࡴࡤࡰࡹࡕࡩࡨࡺࠧਬ"),
  bstack11_opy_ (u"ࠨࡶ࡬ࡱࡪࡵࡵࡵࡵࠪਭ"),
  bstack11_opy_ (u"ࠩࡶࡸࡷ࡯ࡣࡵࡈ࡬ࡰࡪࡏ࡮ࡵࡧࡵࡥࡨࡺࡡࡣ࡫࡯࡭ࡹࡿࠧਮ"),
  bstack11_opy_ (u"ࠪࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡖࡲࡰ࡯ࡳࡸࡇ࡫ࡨࡢࡸ࡬ࡳࡷ࠭ਯ"),
  bstack11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩਰ"),
  bstack11_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪ਱"),
  bstack11_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧਲ"),
  bstack11_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ਲ਼"),
  bstack11_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ਴"),
]
bstack1l1ll_opy_ = [
  bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ਵ"),
  bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧਸ਼"),
  bstack11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ਷"),
  bstack11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬਸ"),
  bstack11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਹ"),
  bstack11_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ਺"),
  bstack11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ਻"),
  bstack11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ਼࠭"),
  bstack11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭਽"),
]
bstack11l11_opy_ = [
  bstack11_opy_ (u"ࠫࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩਾ"),
  bstack11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧਿ"),
  bstack11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩੀ"),
  bstack11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬੁ"),
  bstack11_opy_ (u"ࠨࡶࡨࡷࡹࡖࡲࡪࡱࡵ࡭ࡹࡿࠧੂ"),
  bstack11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ੃"),
  bstack11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡖࡤ࡫ࠬ੄"),
  bstack11_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ੅"),
  bstack11_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ੆"),
  bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫੇ"),
  bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨੈ"),
  bstack11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ੉"),
  bstack11_opy_ (u"ࠩࡲࡷࠬ੊"),
  bstack11_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ੋ"),
  bstack11_opy_ (u"ࠫ࡭ࡵࡳࡵࡵࠪੌ"),
  bstack11_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺ੍ࠧ"),
  bstack11_opy_ (u"࠭ࡲࡦࡩ࡬ࡳࡳ࠭੎"),
  bstack11_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩ੏"),
  bstack11_opy_ (u"ࠨ࡯ࡤࡧ࡭࡯࡮ࡦࠩ੐"),
  bstack11_opy_ (u"ࠩࡵࡩࡸࡵ࡬ࡶࡶ࡬ࡳࡳ࠭ੑ"),
  bstack11_opy_ (u"ࠪ࡭ࡩࡲࡥࡕ࡫ࡰࡩࡴࡻࡴࠨ੒"),
  bstack11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡓࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨ੓"),
  bstack11_opy_ (u"ࠬࡼࡩࡥࡧࡲࠫ੔"),
  bstack11_opy_ (u"࠭࡮ࡰࡒࡤ࡫ࡪࡒ࡯ࡢࡦࡗ࡭ࡲ࡫࡯ࡶࡶࠪ੕"),
  bstack11_opy_ (u"ࠧࡣࡨࡦࡥࡨ࡮ࡥࠨ੖"),
  bstack11_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧ੗"),
  bstack11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭੘"),
  bstack11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡩࡳࡪࡋࡦࡻࡶࠫਖ਼"),
  bstack11_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨਗ਼"),
  bstack11_opy_ (u"ࠬࡴ࡯ࡑ࡫ࡳࡩࡱ࡯࡮ࡦࠩਜ਼"),
  bstack11_opy_ (u"࠭ࡣࡩࡧࡦ࡯࡚ࡘࡌࠨੜ"),
  bstack11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ੝"),
  bstack11_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡄࡱࡲ࡯࡮࡫ࡳࠨਫ਼"),
  bstack11_opy_ (u"ࠩࡦࡥࡵࡺࡵࡳࡧࡆࡶࡦࡹࡨࠨ੟"),
  bstack11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ੠"),
  bstack11_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ੡"),
  bstack11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡘࡨࡶࡸ࡯࡯࡯ࠩ੢"),
  bstack11_opy_ (u"࠭࡮ࡰࡄ࡯ࡥࡳࡱࡐࡰ࡮࡯࡭ࡳ࡭ࠧ੣"),
  bstack11_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡘ࡫࡮ࡥࡍࡨࡽࡸ࠭੤"),
  bstack11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡍࡱࡪࡷࠬ੥"),
  bstack11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡋࡧࠫ੦"),
  bstack11_opy_ (u"ࠪࡨࡪࡪࡩࡤࡣࡷࡩࡩࡊࡥࡷ࡫ࡦࡩࠬ੧"),
  bstack11_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡔࡦࡸࡡ࡮ࡵࠪ੨"),
  bstack11_opy_ (u"ࠬࡶࡨࡰࡰࡨࡒࡺࡳࡢࡦࡴࠪ੩"),
  bstack11_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࠫ੪"),
  bstack11_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡔࡶࡴࡪࡱࡱࡷࠬ੫"),
  bstack11_opy_ (u"ࠨࡥࡲࡲࡸࡵ࡬ࡦࡎࡲ࡫ࡸ࠭੬"),
  bstack11_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ੭"),
  bstack11_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧ੮"),
  bstack11_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡆ࡮ࡵ࡭ࡦࡶࡵ࡭ࡨ࠭੯"),
  bstack11_opy_ (u"ࠬࡼࡩࡥࡧࡲ࡚࠷࠭ੰ"),
  bstack11_opy_ (u"࠭࡭ࡪࡦࡖࡩࡸࡹࡩࡰࡰࡌࡲࡸࡺࡡ࡭࡮ࡄࡴࡵࡹࠧੱ"),
  bstack11_opy_ (u"ࠧࡦࡵࡳࡶࡪࡹࡳࡰࡕࡨࡶࡻ࡫ࡲࠨੲ"),
  bstack11_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧੳ"),
  bstack11_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡇࡩࡶࠧੴ"),
  bstack11_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪੵ"),
  bstack11_opy_ (u"ࠫࡸࡿ࡮ࡤࡖ࡬ࡱࡪ࡝ࡩࡵࡪࡑࡘࡕ࠭੶"),
  bstack11_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪ੷"),
  bstack11_opy_ (u"࠭ࡧࡱࡵࡏࡳࡨࡧࡴࡪࡱࡱࠫ੸"),
  bstack11_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡑࡴࡲࡪ࡮ࡲࡥࠨ੹"),
  bstack11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡏࡧࡷࡻࡴࡸ࡫ࠨ੺"),
  bstack11_opy_ (u"ࠩࡩࡳࡷࡩࡥࡄࡪࡤࡲ࡬࡫ࡊࡢࡴࠪ੻"),
  bstack11_opy_ (u"ࠪࡼࡲࡹࡊࡢࡴࠪ੼"),
  bstack11_opy_ (u"ࠫࡽࡳࡸࡋࡣࡵࠫ੽"),
  bstack11_opy_ (u"ࠬࡳࡡࡴ࡭ࡆࡳࡲࡳࡡ࡯ࡦࡶࠫ੾"),
  bstack11_opy_ (u"࠭࡭ࡢࡵ࡮ࡆࡦࡹࡩࡤࡃࡸࡸ࡭࠭੿"),
  bstack11_opy_ (u"ࠧࡸࡵࡏࡳࡨࡧ࡬ࡔࡷࡳࡴࡴࡸࡴࠨ઀"),
  bstack11_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡅࡲࡶࡸࡘࡥࡴࡶࡵ࡭ࡨࡺࡩࡰࡰࡶࠫઁ"),
  bstack11_opy_ (u"ࠩࡤࡴࡵ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ં"),
  bstack11_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩઃ"),
  bstack11_opy_ (u"ࠫࡷ࡫ࡳࡪࡩࡱࡅࡵࡶࠧ઄"),
  bstack11_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇ࡮ࡪ࡯ࡤࡸ࡮ࡵ࡮ࡴࠩઅ"),
  bstack11_opy_ (u"࠭ࡣࡢࡰࡤࡶࡾ࠭આ"),
  bstack11_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨઇ"),
  bstack11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨઈ"),
  bstack11_opy_ (u"ࠩ࡬ࡩࠬઉ"),
  bstack11_opy_ (u"ࠪࡩࡩ࡭ࡥࠨઊ"),
  bstack11_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫઋ"),
  bstack11_opy_ (u"ࠬࡷࡵࡦࡷࡨࠫઌ"),
  bstack11_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨઍ"),
  bstack11_opy_ (u"ࠧࡢࡲࡳࡗࡹࡵࡲࡦࡅࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠨ઎"),
  bstack11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡄࡣࡰࡩࡷࡧࡉ࡮ࡣࡪࡩࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧએ"),
  bstack11_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࡅࡹࡥ࡯ࡹࡩ࡫ࡈࡰࡵࡷࡷࠬઐ"),
  bstack11_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࡊࡰࡦࡰࡺࡪࡥࡉࡱࡶࡸࡸ࠭ઑ"),
  bstack11_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡅࡵࡶࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨ઒"),
  bstack11_opy_ (u"ࠬࡸࡥࡴࡧࡵࡺࡪࡊࡥࡷ࡫ࡦࡩࠬઓ"),
  bstack11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ઔ"),
  bstack11_opy_ (u"ࠧࡴࡧࡱࡨࡐ࡫ࡹࡴࠩક"),
  bstack11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡑࡣࡶࡷࡨࡵࡤࡦࠩખ"),
  bstack11_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡃࡸࡨ࡮ࡵࡉ࡯࡬ࡨࡧࡹ࡯࡯࡯ࠩગ"),
  bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫઘ"),
  bstack11_opy_ (u"ࠫࡼࡪࡩࡰࡕࡨࡶࡻ࡯ࡣࡦࠩઙ"),
  bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧચ"),
  bstack11_opy_ (u"࠭ࡰࡳࡧࡹࡩࡳࡺࡃࡳࡱࡶࡷࡘ࡯ࡴࡦࡖࡵࡥࡨࡱࡩ࡯ࡩࠪછ"),
  bstack11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡐࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࡶࠫજ"),
  bstack11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫઝ"),
  bstack11_opy_ (u"ࠩࡵࡩࡲࡵࡶࡦࡋࡒࡗࡆࡶࡰࡔࡧࡷࡸ࡮ࡴࡧࡴࡎࡲࡧࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠧઞ"),
  bstack11_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬટ"),
  bstack11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ઠ")
]
bstack1111l_opy_ = {
  bstack11_opy_ (u"ࠬࡼࠧડ"): bstack11_opy_ (u"࠭ࡶࠨઢ"),
  bstack11_opy_ (u"ࠧࡧࠩણ"): bstack11_opy_ (u"ࠨࡨࠪત"),
  bstack11_opy_ (u"ࠩࡩࡳࡷࡩࡥࠨથ"): bstack11_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩદ"),
  bstack11_opy_ (u"ࠫࡴࡴ࡬ࡺࡣࡸࡸࡴࡳࡡࡵࡧࠪધ"): bstack11_opy_ (u"ࠬࡵ࡮࡭ࡻࡄࡹࡹࡵ࡭ࡢࡶࡨࠫન"),
  bstack11_opy_ (u"࠭ࡦࡰࡴࡦࡩࡱࡵࡣࡢ࡮ࠪ઩"): bstack11_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫપ"),
  bstack11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫફ"): bstack11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡉࡱࡶࡸࠬબ"),
  bstack11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭ભ"): bstack11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧમ"),
  bstack11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨય"): bstack11_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩર"),
  bstack11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡶࡡࡴࡵࠪ઱"): bstack11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫલ"),
  bstack11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾ࡮࡯ࡴࡶࠪળ"): bstack11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡈࡰࡵࡷࠫ઴"),
  bstack11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡱࡵࡸࠬવ"): bstack11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡲࡶࡹ࠭શ"),
  bstack11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡸࡷࡪࡸࠧષ"): bstack11_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽ࡚ࡹࡥࡳࠩસ"),
  bstack11_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪહ"): bstack11_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫ઺"),
  bstack11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫ઻"): bstack11_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ઼࠭"),
  bstack11_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡥࡸࡹࠧઽ"): bstack11_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡦࡹࡳࠨા"),
  bstack11_opy_ (u"ࠧࡣ࡫ࡱࡥࡷࡿࡰࡢࡶ࡫ࠫિ"): bstack11_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬી"),
  bstack11_opy_ (u"ࠩࡳࡥࡨ࡬ࡩ࡭ࡧࠪુ"): bstack11_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ૂ"),
  bstack11_opy_ (u"ࠫࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ૃ"): bstack11_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨૄ"),
  bstack11_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩૅ"): bstack11_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪ૆"),
  bstack11_opy_ (u"ࠨ࡮ࡲ࡫࡫࡯࡬ࡦࠩે"): bstack11_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪૈ"),
  bstack11_opy_ (u"ࠪࡰࡴࡩࡡ࡭࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬૉ"): bstack11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૊"),
}
bstack1llll1_opy_ = bstack11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ો")
bstack11ll1_opy_ = bstack11_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠩૌ")
bstack1lll1_opy_ = {
  bstack11_opy_ (u"ࠧࡤࡴ࡬ࡸ࡮ࡩࡡ࡭્ࠩ"): 50,
  bstack11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ૎"): 40,
  bstack11_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪ૏"): 30,
  bstack11_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨૐ"): 20,
  bstack11_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪ૑"): 10
}
DEFAULT_LOG_LEVEL = bstack1lll1_opy_[bstack11_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ૒")]
bstack1l111_opy_ = bstack11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬ૓")
bstack11ll_opy_ = bstack11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬ૔")
bstack111l1_opy_ = bstack11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧ૕")
bstack11lll_opy_ = bstack11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨ૖")
bstack1lll1l_opy_ = [bstack11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫ૗"), bstack11_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫ૘")]
bstack11l1_opy_ = [bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ૙"), bstack11_opy_ (u"࡙࠭ࡐࡗࡕࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ૚")]
bstack111ll_opy_ = [
  bstack11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡒࡦࡳࡥࠨ૛"),
  bstack11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ૜"),
  bstack11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭૝"),
  bstack11_opy_ (u"ࠪࡲࡪࡽࡃࡰ࡯ࡰࡥࡳࡪࡔࡪ࡯ࡨࡳࡺࡺࠧ૞"),
  bstack11_opy_ (u"ࠫࡦࡶࡰࠨ૟"),
  bstack11_opy_ (u"ࠬࡻࡤࡪࡦࠪૠ"),
  bstack11_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨૡ"),
  bstack11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡫ࠧૢ"),
  bstack11_opy_ (u"ࠨࡱࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭ૣ"),
  bstack11_opy_ (u"ࠩࡤࡹࡹࡵࡗࡦࡤࡹ࡭ࡪࡽࠧ૤"),
  bstack11_opy_ (u"ࠪࡲࡴࡘࡥࡴࡧࡷࠫ૥"), bstack11_opy_ (u"ࠫ࡫ࡻ࡬࡭ࡔࡨࡷࡪࡺࠧ૦"),
  bstack11_opy_ (u"ࠬࡩ࡬ࡦࡣࡵࡗࡾࡹࡴࡦ࡯ࡉ࡭ࡱ࡫ࡳࠨ૧"),
  bstack11_opy_ (u"࠭ࡥࡷࡧࡱࡸ࡙࡯࡭ࡪࡰࡪࡷࠬ૨"),
  bstack11_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡐࡦࡴࡩࡳࡷࡳࡡ࡯ࡥࡨࡐࡴ࡭ࡧࡪࡰࡪࠫ૩"),
  bstack11_opy_ (u"ࠨࡱࡷ࡬ࡪࡸࡁࡱࡲࡶࠫ૪"),
  bstack11_opy_ (u"ࠩࡳࡶ࡮ࡴࡴࡑࡣࡪࡩࡘࡵࡵࡳࡥࡨࡓࡳࡌࡩ࡯ࡦࡉࡥ࡮ࡲࡵࡳࡧࠪ૫"),
  bstack11_opy_ (u"ࠪࡥࡵࡶࡁࡤࡶ࡬ࡺ࡮ࡺࡹࠨ૬"), bstack11_opy_ (u"ࠫࡦࡶࡰࡑࡣࡦ࡯ࡦ࡭ࡥࠨ૭"), bstack11_opy_ (u"ࠬࡧࡰࡱ࡙ࡤ࡭ࡹࡇࡣࡵ࡫ࡹ࡭ࡹࡿࠧ૮"), bstack11_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡐࡢࡥ࡮ࡥ࡬࡫ࠧ૯"), bstack11_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡅࡷࡵࡥࡹ࡯࡯࡯ࠩ૰"),
  bstack11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭૱"),
  bstack11_opy_ (u"ࠩࡤࡰࡱࡵࡷࡕࡧࡶࡸࡕࡧࡣ࡬ࡣࡪࡩࡸ࠭૲"),
  bstack11_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡇࡴࡼࡥࡳࡣࡪࡩࠬ૳"), bstack11_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡈࡵࡶࡦࡴࡤ࡫ࡪࡋ࡮ࡥࡋࡱࡸࡪࡴࡴࠨ૴"),
  bstack11_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡊࡥࡷ࡫ࡦࡩࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪ૵"),
  bstack11_opy_ (u"࠭ࡡࡥࡤࡓࡳࡷࡺࠧ૶"),
  bstack11_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡓࡰࡥ࡮ࡩࡹ࠭૷"),
  bstack11_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡋࡱࡷࡹࡧ࡬࡭ࡖ࡬ࡱࡪࡵࡵࡵࠩ૸"),
  bstack11_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡌࡲࡸࡺࡡ࡭࡮ࡓࡥࡹ࡮ࠧૹ"),
  bstack11_opy_ (u"ࠪࡥࡻࡪࠧૺ"), bstack11_opy_ (u"ࠫࡦࡼࡤࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧૻ"), bstack11_opy_ (u"ࠬࡧࡶࡥࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧૼ"), bstack11_opy_ (u"࠭ࡡࡷࡦࡄࡶ࡬ࡹࠧ૽"),
  bstack11_opy_ (u"ࠧࡶࡵࡨࡏࡪࡿࡳࡵࡱࡵࡩࠬ૾"), bstack11_opy_ (u"ࠨ࡭ࡨࡽࡸࡺ࡯ࡳࡧࡓࡥࡹ࡮ࠧ૿"), bstack11_opy_ (u"ࠩ࡮ࡩࡾࡹࡴࡰࡴࡨࡔࡦࡹࡳࡸࡱࡵࡨࠬ଀"),
  bstack11_opy_ (u"ࠪ࡯ࡪࡿࡁ࡭࡫ࡤࡷࠬଁ"), bstack11_opy_ (u"ࠫࡰ࡫ࡹࡑࡣࡶࡷࡼࡵࡲࡥࠩଂ"),
  bstack11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡉࡽ࡫ࡣࡶࡶࡤࡦࡱ࡫ࠧଃ"), bstack11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡆࡸࡧࡴࠩ଄"), bstack11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࡆ࡬ࡶࠬଅ"), bstack11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡃࡩࡴࡲࡱࡪࡓࡡࡱࡲ࡬ࡲ࡬ࡌࡩ࡭ࡧࠪଆ"), bstack11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡖࡵࡨࡗࡾࡹࡴࡦ࡯ࡈࡼࡪࡩࡵࡵࡣࡥࡰࡪ࠭ଇ"),
  bstack11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡒࡲࡶࡹ࠭ଈ"), bstack11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡓࡳࡷࡺࡳࠨଉ"),
  bstack11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡈ࡮ࡹࡡࡣ࡮ࡨࡆࡺ࡯࡬ࡥࡅ࡫ࡩࡨࡱࠧଊ"),
  bstack11_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡪࡨࡶࡪࡧࡺࡘ࡮ࡳࡥࡰࡷࡷࠫଋ"),
  bstack11_opy_ (u"ࠧࡪࡰࡷࡩࡳࡺࡁࡤࡶ࡬ࡳࡳ࠭ଌ"), bstack11_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡄࡣࡷࡩ࡬ࡵࡲࡺࠩ଍"), bstack11_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡈ࡯ࡥ࡬ࡹࠧ଎"), bstack11_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡤࡰࡎࡴࡴࡦࡰࡷࡅࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ଏ"),
  bstack11_opy_ (u"ࠫࡩࡵ࡮ࡵࡕࡷࡳࡵࡇࡰࡱࡑࡱࡖࡪࡹࡥࡵࠩଐ"),
  bstack11_opy_ (u"ࠬࡻ࡮ࡪࡥࡲࡨࡪࡑࡥࡺࡤࡲࡥࡷࡪࠧ଑"), bstack11_opy_ (u"࠭ࡲࡦࡵࡨࡸࡐ࡫ࡹࡣࡱࡤࡶࡩ࠭଒"),
  bstack11_opy_ (u"ࠧ࡯ࡱࡖ࡭࡬ࡴࠧଓ"),
  bstack11_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࡖࡰ࡬ࡱࡵࡵࡲࡵࡣࡱࡸ࡛࡯ࡥࡸࡵࠪଔ"),
  bstack11_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲࡩࡸ࡯ࡪࡦ࡚ࡥࡹࡩࡨࡦࡴࡶࠫକ"),
  bstack11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪଖ"),
  bstack11_opy_ (u"ࠫࡷ࡫ࡣࡳࡧࡤࡸࡪࡉࡨࡳࡱࡰࡩࡉࡸࡩࡷࡧࡵࡗࡪࡹࡳࡪࡱࡱࡷࠬଗ"),
  bstack11_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫଘ"),
  bstack11_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࡓࡥࡹ࡮ࠧଙ"),
  bstack11_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡔࡲࡨࡩࡩ࠭ଚ"),
  bstack11_opy_ (u"ࠨࡩࡳࡷࡊࡴࡡࡣ࡮ࡨࡨࠬଛ"),
  bstack11_opy_ (u"ࠩ࡬ࡷࡍ࡫ࡡࡥ࡮ࡨࡷࡸ࠭ଜ"),
  bstack11_opy_ (u"ࠪࡥࡩࡨࡅࡹࡧࡦࡘ࡮ࡳࡥࡰࡷࡷࠫଝ"),
  bstack11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡨࡗࡨࡸࡩࡱࡶࠪଞ"),
  bstack11_opy_ (u"ࠬࡹ࡫ࡪࡲࡇࡩࡻ࡯ࡣࡦࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩଟ"),
  bstack11_opy_ (u"࠭ࡡࡶࡶࡲࡋࡷࡧ࡮ࡵࡒࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸ࠭ଠ"),
  bstack11_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡏࡣࡷࡹࡷࡧ࡬ࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬଡ"),
  bstack11_opy_ (u"ࠨࡵࡼࡷࡹ࡫࡭ࡑࡱࡵࡸࠬଢ"),
  bstack11_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡃࡧࡦࡍࡵࡳࡵࠩଣ"),
  bstack11_opy_ (u"ࠪࡷࡰ࡯ࡰࡖࡰ࡯ࡳࡨࡱࠧତ"), bstack11_opy_ (u"ࠫࡺࡴ࡬ࡰࡥ࡮ࡘࡾࡶࡥࠨଥ"), bstack11_opy_ (u"ࠬࡻ࡮࡭ࡱࡦ࡯ࡐ࡫ࡹࠨଦ"),
  bstack11_opy_ (u"࠭ࡡࡶࡶࡲࡐࡦࡻ࡮ࡤࡪࠪଧ"),
  bstack11_opy_ (u"ࠧࡴ࡭࡬ࡴࡑࡵࡧࡤࡣࡷࡇࡦࡶࡴࡶࡴࡨࠫନ"),
  bstack11_opy_ (u"ࠨࡷࡱ࡭ࡳࡹࡴࡢ࡮࡯ࡓࡹ࡮ࡥࡳࡒࡤࡧࡰࡧࡧࡦࡵࠪ଩"),
  bstack11_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧ࡚࡭ࡳࡪ࡯ࡸࡃࡱ࡭ࡲࡧࡴࡪࡱࡱࠫପ"),
  bstack11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡖࡲࡳࡱࡹࡖࡦࡴࡶ࡭ࡴࡴࠧଫ"),
  bstack11_opy_ (u"ࠫࡪࡴࡦࡰࡴࡦࡩࡆࡶࡰࡊࡰࡶࡸࡦࡲ࡬ࠨବ"),
  bstack11_opy_ (u"ࠬ࡫࡮ࡴࡷࡵࡩ࡜࡫ࡢࡷ࡫ࡨࡻࡸࡎࡡࡷࡧࡓࡥ࡬࡫ࡳࠨଭ"), bstack11_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࡄࡦࡸࡷࡳࡴࡲࡳࡑࡱࡵࡸࠬମ"), bstack11_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡄࡦࡶࡤ࡭ࡱࡹࡃࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠪଯ"),
  bstack11_opy_ (u"ࠨࡴࡨࡱࡴࡺࡥࡂࡲࡳࡷࡈࡧࡣࡩࡧࡏ࡭ࡲ࡯ࡴࠨର"),
  bstack11_opy_ (u"ࠩࡦࡥࡱ࡫࡮ࡥࡣࡵࡊࡴࡸ࡭ࡢࡶࠪ଱"),
  bstack11_opy_ (u"ࠪࡦࡺࡴࡤ࡭ࡧࡌࡨࠬଲ"),
  bstack11_opy_ (u"ࠫࡱࡧࡵ࡯ࡥ࡫ࡘ࡮ࡳࡥࡰࡷࡷࠫଳ"),
  bstack11_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࡓࡦࡴࡹ࡭ࡨ࡫ࡳࡆࡰࡤࡦࡱ࡫ࡤࠨ଴"), bstack11_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࡔࡧࡵࡺ࡮ࡩࡥࡴࡃࡸࡸ࡭ࡵࡲࡪࡼࡨࡨࠬଵ"),
  bstack11_opy_ (u"ࠧࡢࡷࡷࡳࡆࡩࡣࡦࡲࡷࡅࡱ࡫ࡲࡵࡵࠪଶ"), bstack11_opy_ (u"ࠨࡣࡸࡸࡴࡊࡩࡴ࡯࡬ࡷࡸࡇ࡬ࡦࡴࡷࡷࠬଷ"),
  bstack11_opy_ (u"ࠩࡱࡥࡹ࡯ࡶࡦࡋࡱࡷࡹࡸࡵ࡮ࡧࡱࡸࡸࡒࡩࡣࠩସ"),
  bstack11_opy_ (u"ࠪࡲࡦࡺࡩࡷࡧ࡚ࡩࡧ࡚ࡡࡱࠩହ"),
  bstack11_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡍࡳ࡯ࡴࡪࡣ࡯࡙ࡷࡲࠧ଺"), bstack11_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡆࡲ࡬ࡰࡹࡓࡳࡵࡻࡰࡴࠩ଻"), bstack11_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏࡧ࡯ࡱࡵࡩࡋࡸࡡࡶࡦ࡚ࡥࡷࡴࡩ࡯ࡩ଼ࠪ"), bstack11_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡏࡱࡧࡱࡐ࡮ࡴ࡫ࡴࡋࡱࡆࡦࡩ࡫ࡨࡴࡲࡹࡳࡪࠧଽ"),
  bstack11_opy_ (u"ࠨ࡭ࡨࡩࡵࡑࡥࡺࡅ࡫ࡥ࡮ࡴࡳࠨା"),
  bstack11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡪࡼࡤࡦࡱ࡫ࡓࡵࡴ࡬ࡲ࡬ࡹࡄࡪࡴࠪି"),
  bstack11_opy_ (u"ࠪࡴࡷࡵࡣࡦࡵࡶࡅࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ୀ"),
  bstack11_opy_ (u"ࠫ࡮ࡴࡴࡦࡴࡎࡩࡾࡊࡥ࡭ࡣࡼࠫୁ"),
  bstack11_opy_ (u"ࠬࡹࡨࡰࡹࡌࡓࡘࡒ࡯ࡨࠩୂ"),
  bstack11_opy_ (u"࠭ࡳࡦࡰࡧࡏࡪࡿࡓࡵࡴࡤࡸࡪ࡭ࡹࠨୃ"),
  bstack11_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡒࡦࡵࡳࡳࡳࡹࡥࡕ࡫ࡰࡩࡴࡻࡴࠨୄ"), bstack11_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸ࡜ࡧࡩࡵࡖ࡬ࡱࡪࡵࡵࡵࠩ୅"),
  bstack11_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡆࡨࡦࡺ࡭ࡐࡳࡱࡻࡽࠬ୆"),
  bstack11_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡄࡷࡾࡴࡣࡆࡺࡨࡧࡺࡺࡥࡇࡴࡲࡱࡍࡺࡴࡱࡵࠪେ"),
  bstack11_opy_ (u"ࠫࡸࡱࡩࡱࡎࡲ࡫ࡈࡧࡰࡵࡷࡵࡩࠬୈ"),
  bstack11_opy_ (u"ࠬࡽࡥࡣ࡭࡬ࡸࡉ࡫ࡢࡶࡩࡓࡶࡴࡾࡹࡑࡱࡵࡸࠬ୉"),
  bstack11_opy_ (u"࠭ࡦࡶ࡮࡯ࡇࡴࡴࡴࡦࡺࡷࡐ࡮ࡹࡴࠨ୊"),
  bstack11_opy_ (u"ࠧࡸࡣ࡬ࡸࡋࡵࡲࡂࡲࡳࡗࡨࡸࡩࡱࡶࠪୋ"),
  bstack11_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡅࡲࡲࡳ࡫ࡣࡵࡔࡨࡸࡷ࡯ࡥࡴࠩୌ"),
  bstack11_opy_ (u"ࠩࡤࡴࡵࡔࡡ࡮ࡧ୍ࠪ"),
  bstack11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡗࡑࡉࡥࡳࡶࠪ୎"),
  bstack11_opy_ (u"ࠫࡹࡧࡰࡘ࡫ࡷ࡬ࡘ࡮࡯ࡳࡶࡓࡶࡪࡹࡳࡅࡷࡵࡥࡹ࡯࡯࡯ࠩ୏"),
  bstack11_opy_ (u"ࠬࡹࡣࡢ࡮ࡨࡊࡦࡩࡴࡰࡴࠪ୐"),
  bstack11_opy_ (u"࠭ࡷࡥࡣࡏࡳࡨࡧ࡬ࡑࡱࡵࡸࠬ୑"),
  bstack11_opy_ (u"ࠧࡴࡪࡲࡻ࡝ࡩ࡯ࡥࡧࡏࡳ࡬࠭୒"),
  bstack11_opy_ (u"ࠨ࡫ࡲࡷࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡵࡴࡧࠪ୓"),
  bstack11_opy_ (u"ࠩࡻࡧࡴࡪࡥࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠫ୔"),
  bstack11_opy_ (u"ࠪ࡯ࡪࡿࡣࡩࡣ࡬ࡲࡕࡧࡳࡴࡹࡲࡶࡩ࠭୕"),
  bstack11_opy_ (u"ࠫࡺࡹࡥࡑࡴࡨࡦࡺ࡯࡬ࡵ࡙ࡇࡅࠬୖ"),
  bstack11_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹ࡝ࡄࡂࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠭ୗ"),
  bstack11_opy_ (u"࠭ࡷࡦࡤࡇࡶ࡮ࡼࡥࡳࡃࡪࡩࡳࡺࡕࡳ࡮ࠪ୘"),
  bstack11_opy_ (u"ࠧ࡬ࡧࡼࡧ࡭ࡧࡩ࡯ࡒࡤࡸ࡭࠭୙"),
  bstack11_opy_ (u"ࠨࡷࡶࡩࡓ࡫ࡷࡘࡆࡄࠫ୚"),
  bstack11_opy_ (u"ࠩࡺࡨࡦࡒࡡࡶࡰࡦ࡬࡙࡯࡭ࡦࡱࡸࡸࠬ୛"), bstack11_opy_ (u"ࠪࡻࡩࡧࡃࡰࡰࡱࡩࡨࡺࡩࡰࡰࡗ࡭ࡲ࡫࡯ࡶࡶࠪଡ଼"),
  bstack11_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡒࡶ࡬ࡏࡤࠨଢ଼"), bstack11_opy_ (u"ࠬࡾࡣࡰࡦࡨࡗ࡮࡭࡮ࡪࡰࡪࡍࡩ࠭୞"),
  bstack11_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡪࡗࡅࡃࡅࡹࡳࡪ࡬ࡦࡋࡧࠫୟ"),
  bstack11_opy_ (u"ࠧࡳࡧࡶࡩࡹࡕ࡮ࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡶࡹࡕ࡮࡭ࡻࠪୠ"),
  bstack11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࡵࠪୡ"),
  bstack11_opy_ (u"ࠩࡺࡨࡦ࡙ࡴࡢࡴࡷࡹࡵࡘࡥࡵࡴ࡬ࡩࡸ࠭ୢ"), bstack11_opy_ (u"ࠪࡻࡩࡧࡓࡵࡣࡵࡸࡺࡶࡒࡦࡶࡵࡽࡎࡴࡴࡦࡴࡹࡥࡱ࠭ୣ"),
  bstack11_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࡍࡧࡲࡥࡹࡤࡶࡪࡑࡥࡺࡤࡲࡥࡷࡪࠧ୤"),
  bstack11_opy_ (u"ࠬࡳࡡࡹࡖࡼࡴ࡮ࡴࡧࡇࡴࡨࡵࡺ࡫࡮ࡤࡻࠪ୥"),
  bstack11_opy_ (u"࠭ࡳࡪ࡯ࡳࡰࡪࡏࡳࡗ࡫ࡶ࡭ࡧࡲࡥࡄࡪࡨࡧࡰ࠭୦"),
  bstack11_opy_ (u"ࠧࡶࡵࡨࡇࡦࡸࡴࡩࡣࡪࡩࡘࡹ࡬ࠨ୧"),
  bstack11_opy_ (u"ࠨࡵ࡫ࡳࡺࡲࡤࡖࡵࡨࡗ࡮ࡴࡧ࡭ࡧࡷࡳࡳ࡚ࡥࡴࡶࡐࡥࡳࡧࡧࡦࡴࠪ୨"),
  bstack11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡊ࡙ࡇࡔࠬ୩"),
  bstack11_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡖࡲࡹࡨ࡮ࡉࡥࡇࡱࡶࡴࡲ࡬ࠨ୪"),
  bstack11_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࡌ࡮ࡪࡤࡦࡰࡄࡴ࡮ࡖ࡯࡭࡫ࡦࡽࡊࡸࡲࡰࡴࠪ୫"),
  bstack11_opy_ (u"ࠬࡳ࡯ࡤ࡭ࡏࡳࡨࡧࡴࡪࡱࡱࡅࡵࡶࠧ୬"),
  bstack11_opy_ (u"࠭࡬ࡰࡩࡦࡥࡹࡌ࡯ࡳ࡯ࡤࡸࠬ୭"), bstack11_opy_ (u"ࠧ࡭ࡱࡪࡧࡦࡺࡆࡪ࡮ࡷࡩࡷ࡙ࡰࡦࡥࡶࠫ୮"),
  bstack11_opy_ (u"ࠨࡣ࡯ࡰࡴࡽࡄࡦ࡮ࡤࡽࡆࡪࡢࠨ୯")
]
bstack1l1l1_opy_ = bstack11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡷࡳࡰࡴࡧࡤࠨ୰")
bstack1l11l_opy_ = [bstack11_opy_ (u"ࠪ࠲ࡦࡶ࡫ࠨୱ"), bstack11_opy_ (u"ࠫ࠳ࡧࡡࡣࠩ୲"), bstack11_opy_ (u"ࠬ࠴ࡩࡱࡣࠪ୳")]
bstack1111_opy_ = [bstack11_opy_ (u"࠭ࡩࡥࠩ୴"), bstack11_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ୵"), bstack11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫ୶"), bstack11_opy_ (u"ࠩࡶ࡬ࡦࡸࡥࡢࡤ࡯ࡩࡤ࡯ࡤࠨ୷")]
bstack1l11_opy_ = {
  bstack11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ୸"): bstack11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ୹"),
  bstack11_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭୺"): bstack11_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫ୻"),
  bstack11_opy_ (u"ࠧࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬ୼"): bstack11_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ୽"),
  bstack11_opy_ (u"ࠩ࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬ୾"): bstack11_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ୿"),
  bstack11_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡓࡵࡺࡩࡰࡰࡶࠫ஀"): bstack11_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭஁")
}
bstack11111_opy_ = [
  bstack11_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫஂ"),
  bstack11_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬஃ"),
  bstack11_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ஄"),
  bstack11_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨஅ"),
  bstack11_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫஆ"),
]
bstack1lllll_opy_ = bstack1l1ll_opy_ + bstack11l11_opy_ + bstack111ll_opy_
bstack11ll11l_opy_ = bstack11_opy_ (u"ࠫࡘ࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡰࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠰ࠥࡻࡳࡪࡰࡪࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠺ࠡࡽࢀࠫஇ")
bstack1lll11l11_opy_ = bstack11_opy_ (u"ࠬࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡࡵࡨࡸࡺࡶࠡࠨஈ")
bstack1111llll_opy_ = bstack11_opy_ (u"࠭ࡐࡢࡴࡶࡩࡩࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠨஉ")
bstack1l1l1lll_opy_ = bstack11_opy_ (u"ࠧࡔࡣࡱ࡭ࡹ࡯ࡺࡦࡦࠣࡧࡴࡴࡦࡪࡩࠣࡪ࡮ࡲࡥ࠻ࠢࡾࢁࠬஊ")
bstack1lll1ll11_opy_ = bstack11_opy_ (u"ࠨࡗࡶ࡭ࡳ࡭ࠠࡩࡷࡥࠤࡺࡸ࡬࠻ࠢࡾࢁࠬ஋")
bstack111111_opy_ = bstack11_opy_ (u"ࠩࡖࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡲࡵࡧࡧࠤࡼ࡯ࡴࡩࠢ࡬ࡨ࠿ࠦࡻࡾࠩ஌")
bstack1llllll_opy_ = bstack11_opy_ (u"ࠪࡖࡪࡩࡥࡪࡸࡨࡨࠥ࡯࡮ࡵࡧࡵࡶࡺࡶࡴ࠭ࠢࡨࡼ࡮ࡺࡩ࡯ࡩࠪ஍")
bstack1ll1111_opy_ = bstack11_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡡࠩஎ")
bstack1lll11l_opy_ = bstack11_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹࠦࡡ࡯ࡦࠣࡴࡾࡺࡥࡴࡶ࠰ࡷࡪࡲࡥ࡯࡫ࡸࡱࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺࠠࡱࡻࡷࡩࡸࡺ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡢࠪஏ")
bstack111ll111_opy_ = bstack11_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡳࡱࡥࡳࡹ࠲ࠠࡱࡣࡥࡳࡹࠦࡡ࡯ࡦࠣࡷࡪࡲࡥ࡯࡫ࡸࡱࡱ࡯ࡢࡳࡣࡵࡽࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡹࠠࡵࡱࠣࡶࡺࡴࠠࡳࡱࡥࡳࡹࠦࡴࡦࡵࡷࡷࠥ࡯࡮ࠡࡲࡤࡶࡦࡲ࡬ࡦ࡮࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡶࡴࡨ࡯ࡵࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡷࡵࡢࡰࡶࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠲ࡶࡡࡣࡱࡷࠤࡷࡵࡢࡰࡶࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡬ࡪࡤࡵࡥࡷࡿࡠࠨஐ")
bstack1llll11l1_opy_ = bstack11_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡤࡨ࡬ࡦࡼࡥࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡣࡧ࡫ࡥࡻ࡫ࡠࠨ஑")
bstack11lllll_opy_ = bstack11_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡤࡴࡵ࡯ࡵ࡮࠯ࡦࡰ࡮࡫࡮ࡵࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡃࡳࡴ࡮ࡻ࡭࠮ࡒࡼࡸ࡭ࡵ࡮࠮ࡅ࡯࡭ࡪࡴࡴࡡࠩஒ")
bstack1ll1ll1l_opy_ = bstack11_opy_ (u"ࠩࡋࡥࡳࡪ࡬ࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡬ࡰࡵࡨࠫஓ")
bstack11l1111l_opy_ = bstack11_opy_ (u"ࠪࡅࡱࡲࠠࡥࡱࡱࡩࠦ࠭ஔ")
bstack1llllll1l_opy_ = bstack11_opy_ (u"ࠫࡈࡵ࡮ࡧ࡫ࡪࠤ࡫࡯࡬ࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶࠣࡥࡹࠦࠢࡼࡿࠥ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡤ࡮ࡸࡨࡪࠦࡡࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤ࡫࡯࡬ࡦࠢࡦࡳࡳࡺࡡࡪࡰ࡬࡫ࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࡳ࠯ࠩக")
bstack1ll11lll_opy_ = bstack11_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡸࡥࡥࡧࡱࡸ࡮ࡧ࡬ࡴࠢࡱࡳࡹࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤ࠯ࠢࡓࡰࡪࡧࡳࡦࠢࡤࡨࡩࠦࡴࡩࡧࡰࠤ࡮ࡴࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠣࡧࡴࡴࡦࡪࡩࠣࡪ࡮ࡲࡥࠡࡣࡶࠤࠧࡻࡳࡦࡴࡑࡥࡲ࡫ࠢࠡࡣࡱࡨࠥࠨࡡࡤࡥࡨࡷࡸࡑࡥࡺࠤࠣࡳࡷࠦࡳࡦࡶࠣࡸ࡭࡫࡭ࠡࡣࡶࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࡷ࠿ࠦࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣࠢࡤࡲࡩࠦࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠥࠫ஖")
bstack1ll1ll1_opy_ = bstack11_opy_ (u"࠭ࡍࡢ࡮ࡩࡳࡷࡳࡥࡥࠢࡦࡳࡳ࡬ࡩࡨࠢࡩ࡭ࡱ࡫࠺ࠣࡽࢀࠦࠬ஗")
bstack1ll1111l_opy_ = bstack11_opy_ (u"ࠧࡆࡰࡦࡳࡺࡴࡴࡦࡴࡨࡨࠥ࡫ࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡺࡶࠠ࠮ࠢࡾࢁࠬ஘")
bstack1l1lll1l_opy_ = bstack11_opy_ (u"ࠨࡕࡷࡥࡷࡺࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡏࡳࡨࡧ࡬ࠨங")
bstack1l1l111_opy_ = bstack11_opy_ (u"ࠩࡖࡸࡴࡶࡰࡪࡰࡪࠤࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡐࡴࡩࡡ࡭ࠩச")
bstack1ll1l1_opy_ = bstack11_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡏࡳࡨࡧ࡬ࠡ࡫ࡶࠤࡳࡵࡷࠡࡴࡸࡲࡳ࡯࡮ࡨࠣࠪ஛")
bstack11l111_opy_ = bstack11_opy_ (u"ࠫࡈࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡴࡶࡤࡶࡹࠦࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡒ࡯ࡤࡣ࡯࠾ࠥࢁࡽࠨஜ")
bstack1ll11ll_opy_ = bstack11_opy_ (u"࡙ࠬࡴࡢࡴࡷ࡭ࡳ࡭ࠠ࡭ࡱࡦࡥࡱࠦࡢࡪࡰࡤࡶࡾࠦࡷࡪࡶ࡫ࠤࡴࡶࡴࡪࡱࡱࡷ࠿ࠦࡻࡾࠩ஝")
bstack111111l_opy_ = bstack11_opy_ (u"࠭ࡕࡱࡦࡤࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡧࡩࡹࡧࡩ࡭ࡵ࠽ࠤࢀࢃࠧஞ")
bstack1lll11ll_opy_ = bstack11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡹࡵࡪࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵࠣࡿࢂ࠭ட")
bstack1111l1ll_opy_ = bstack11_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡࡲࡵࡳࡻ࡯ࡤࡦࠢࡤࡲࠥࡧࡰࡱࡴࡲࡴࡷ࡯ࡡࡵࡧࠣࡊ࡜ࠦࠨࡳࡱࡥࡳࡹ࠵ࡰࡢࡤࡲࡸ࠮ࠦࡩ࡯ࠢࡦࡳࡳ࡬ࡩࡨࠢࡩ࡭ࡱ࡫ࠬࠡࡵ࡮࡭ࡵࠦࡴࡩࡧࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦ࡫ࡦࡻࠣ࡭ࡳࠦࡣࡰࡰࡩ࡭࡬ࠦࡩࡧࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡷ࡮ࡳࡰ࡭ࡧࠣࡴࡾࡺࡨࡰࡰࠣࡷࡨࡸࡩࡱࡶࠣࡻ࡮ࡺࡨࡰࡷࡷࠤࡦࡴࡹࠡࡈ࡚࠲ࠬ஠")
bstack1l1l11_opy_ = bstack11_opy_ (u"ࠩࡖࡩࡹࡺࡩ࡯ࡩࠣ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠵ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦ࡯࡯ࠢࡦࡹࡷࡸࡥ࡯ࡶ࡯ࡽࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡲࡪࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࠩࡽࢀ࠭࠱ࠦࡰ࡭ࡧࡤࡷࡪࠦࡵࡱࡩࡵࡥࡩ࡫ࠠࡵࡱࠣࡗࡪࡲࡥ࡯࡫ࡸࡱࡃࡃ࠴࠯࠲࠱࠴ࠥࡵࡲࠡࡴࡨࡪࡪࡸࠠࡵࡱࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡼࡽࡷ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡩࡵࡣࡴ࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠵ࡲࡶࡰ࠰ࡸࡪࡹࡴࡴ࠯ࡥࡩ࡭࡯࡮ࡥ࠯ࡳࡶࡴࡾࡹࠤࡲࡼࡸ࡭ࡵ࡮ࠡࡨࡲࡶࠥࡧࠠࡸࡱࡵ࡯ࡦࡸ࡯ࡶࡰࡧ࠲ࠬ஡")
bstack1lll11lll_opy_ = bstack11_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡹ࡮࡮ࠣࡪ࡮ࡲࡥ࠯࠰ࠪ஢")
bstack111l1111_opy_ = bstack11_opy_ (u"ࠫࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࡩࠦࡴࡩࡧࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪ࡮ࡲࡥࠢࠩண")
bstack1l111111_opy_ = bstack11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣࡸ࡭࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡦࡪ࡮ࡨ࠲ࠥࢁࡽࠨத")
bstack1lll1llll_opy_ = bstack11_opy_ (u"࠭ࡅࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡷࠤࡱ࡫ࡡࡴࡶࠣ࠵ࠥ࡯࡮ࡱࡷࡷ࠰ࠥࡸࡥࡤࡧ࡬ࡺࡪࡪࠠ࠱ࠩ஥")
bstack1ll1l1l1_opy_ = bstack11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡁࡱࡲࠣࡹࡵࡲ࡯ࡢࡦ࠱ࠤࢀࢃࠧ஦")
bstack1l1ll1l_opy_ = bstack11_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡺࡶ࡬ࡰࡣࡧࠤࡆࡶࡰ࠯ࠢࡌࡲࡻࡧ࡬ࡪࡦࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡽࢀ࠲ࠬ஧")
bstack111l11l_opy_ = bstack11_opy_ (u"ࠩࡎࡩࡾࡹࠠࡤࡣࡱࡲࡴࡺࠠࡤࡱ࠰ࡩࡽ࡯ࡳࡵࠢࡤࡷࠥࡧࡰࡱࠢࡹࡥࡱࡻࡥࡴ࠮ࠣࡹࡸ࡫ࠠࡢࡰࡼࠤࡴࡴࡥࠡࡲࡵࡳࡵ࡫ࡲࡵࡻࠣࡪࡷࡵ࡭ࠡࡽ࡬ࡨࡁࡹࡴࡳ࡫ࡱ࡫ࡃ࠲ࠠࡱࡣࡷ࡬ࡁࡹࡴࡳ࡫ࡱ࡫ࡃ࠲ࠠࡤࡷࡶࡸࡴࡳ࡟ࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡹࡨࡢࡴࡨࡥࡧࡲࡥࡠ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂࢂ࠲ࠠࡰࡰ࡯ࡽࠥࠨࡰࡢࡶ࡫ࠦࠥࡧ࡮ࡥࠢࠥࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩࠨࠠࡤࡣࡱࠤࡨࡵ࠭ࡦࡺ࡬ࡷࡹࠦࡴࡰࡩࡨࡸ࡭࡫ࡲ࠯ࠩந")
bstack1ll111_opy_ = bstack11_opy_ (u"ࠪ࡟ࡎࡴࡶࡢ࡮࡬ࡨࠥࡧࡰࡱࠢࡳࡶࡴࡶࡥࡳࡶࡼࡡࠥࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠥࡧࡲࡦࠢࡾ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡲࡤࡸ࡭ࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡳࡩࡣࡵࡩࡦࡨ࡬ࡦࡡ࡬ࡨࡁࡹࡴࡳ࡫ࡱ࡫ࡃࢃ࠮ࠡࡈࡲࡶࠥࡳ࡯ࡳࡧࠣࡨࡪࡺࡡࡪ࡮ࡶࠤࡵࡲࡥࡢࡵࡨࠤࡻ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡼࡽࡷ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡩࡵࡣࡴ࠱ࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡣࡳࡴ࡮ࡻ࡭࠰ࡵࡨࡸ࠲ࡻࡰ࠮ࡶࡨࡷࡹࡹ࠯ࡴࡲࡨࡧ࡮࡬ࡹ࠮ࡣࡳࡴࠬன")
bstack1lllll1ll_opy_ = bstack11_opy_ (u"ࠫࡠࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡡࡱࡲࠣࡴࡷࡵࡰࡦࡴࡷࡽࡢࠦࡓࡶࡲࡳࡳࡷࡺࡥࡥࠢࡹࡥࡱࡻࡥࡴࠢࡲࡪࠥࡧࡰࡱࠢࡤࡶࡪࠦ࡯ࡧࠢࡾ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡲࡤࡸ࡭ࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡳࡩࡣࡵࡩࡦࡨ࡬ࡦࡡ࡬ࡨࡁࡹࡴࡳ࡫ࡱ࡫ࡃࢃ࠮ࠡࡈࡲࡶࠥࡳ࡯ࡳࡧࠣࡨࡪࡺࡡࡪ࡮ࡶࠤࡵࡲࡥࡢࡵࡨࠤࡻ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡼࡽࡷ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡩࡵࡣࡴ࠱ࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡣࡳࡴ࡮ࡻ࡭࠰ࡵࡨࡸ࠲ࡻࡰ࠮ࡶࡨࡷࡹࡹ࠯ࡴࡲࡨࡧ࡮࡬ࡹ࠮ࡣࡳࡴࠬப")
bstack1111ll1l_opy_ = bstack11_opy_ (u"࡛ࠬࡳࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦࡡࡱࡲࠣ࡭ࡩࠦࡻࡾࠢࡩࡳࡷࠦࡨࡢࡵ࡫ࠤ࠿ࠦࡻࡾ࠰ࠪ஫")
bstack1lll1l11l_opy_ = bstack11_opy_ (u"࠭ࡁࡱࡲ࡙ࠣࡵࡲ࡯ࡢࡦࡨࡨ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼ࠲ࠥࡏࡄࠡ࠼ࠣࡿࢂ࠭஬")
bstack1lll1ll_opy_ = bstack11_opy_ (u"ࠧࡖࡵ࡬ࡲ࡬ࠦࡁࡱࡲࠣ࠾ࠥࢁࡽ࠯ࠩ஭")
bstack11ll1l1_opy_ = bstack11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠡ࡫ࡶࠤࡳࡵࡴࠡࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤ࡫ࡵࡲࠡࡸࡤࡲ࡮ࡲ࡬ࡢࠢࡳࡽࡹ࡮࡯࡯ࠢࡷࡩࡸࡺࡳ࠭ࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡻ࡮ࡺࡨࠡࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠠ࠾ࠢ࠴ࠫம")
bstack11l1ll11_opy_ = bstack11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲ࠻ࠢࡾࢁࠬய")
bstack11lll11_opy_ = bstack11_opy_ (u"ࠪࡇࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡣ࡭ࡱࡶࡩࠥࡨࡲࡰࡹࡶࡩࡷࡀࠠࡼࡿࠪர")
bstack1llll1l1_opy_ = bstack11_opy_ (u"ࠫࡈࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡨࡧࡷࠤࡷ࡫ࡡࡴࡱࡱࠤ࡫ࡵࡲࠡࡤࡨ࡬ࡦࡼࡥࠡࡨࡨࡥࡹࡻࡲࡦࠢࡩࡥ࡮ࡲࡵࡳࡧ࠱ࠤࢀࢃࠧற")
from ._version import __version__
bstack1l111l_opy_ = None
CONFIG = {}
bstack111l1ll_opy_ = None
bstack1ll1l111_opy_ = None
bstack1l111l1_opy_ = None
bstack111lllll_opy_ = -1
bstack1lll11l1_opy_ = DEFAULT_LOG_LEVEL
bstack1l1l1l_opy_ = 1
bstack1lllll1l1_opy_ = False
bstack11ll111l_opy_ = bstack11_opy_ (u"ࠬ࠭ல")
bstack1llllll1_opy_ = bstack11_opy_ (u"࠭ࠧள")
bstack1llll1ll_opy_ = False
bstack11ll1lll_opy_ = None
bstack11111l11_opy_ = None
bstack1l1l1l1_opy_ = None
bstack1l1l1l1l_opy_ = None
bstack1l11l11l_opy_ = None
bstack11111l1l_opy_ = None
bstack11111l1_opy_ = None
bstack1111ll11_opy_ = None
bstack11l11lll_opy_ = None
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1lll11l1_opy_,
                    format=bstack11_opy_ (u"ࠧ࡝ࡰࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬழ"),
                    datefmt=bstack11_opy_ (u"ࠨࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪவ"))
def bstack1ll1ll11_opy_():
  global CONFIG
  global bstack1lll11l1_opy_
  if bstack11_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫஶ") in CONFIG:
    bstack1lll11l1_opy_ = bstack1lll1_opy_[CONFIG[bstack11_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬஷ")]]
    logging.getLogger().setLevel(bstack1lll11l1_opy_)
def bstack11l1ll_opy_():
  from bstack1l1l11ll_opy_.version import version as bstack1ll11l11_opy_
  return version.parse(bstack1ll11l11_opy_)
def bstack11l1lll1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1ll1l1_opy_():
  fileName = bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧஸ")
  bstack1111ll1_opy_ = os.path.abspath(fileName)
  if not os.path.exists(bstack1111ll1_opy_):
    fileName = bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡧ࡭࡭ࠩஹ")
    bstack1111ll1_opy_ = os.path.abspath(fileName)
    if not os.path.exists(bstack1111ll1_opy_):
      bstack11l111ll_opy_(
        bstack1llllll1l_opy_.format(os.getcwd()))
  with open(bstack1111ll1_opy_, bstack11_opy_ (u"࠭ࡲࠨ஺")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack11l111ll_opy_(bstack1ll1ll1_opy_.format(str(exc)))
def bstack11l1111_opy_(config):
  bstack1llll11ll_opy_ = bstack1ll1lll1_opy_(config)
  for option in list(bstack1llll11ll_opy_):
    if option.lower() in bstack1111l_opy_ and option != bstack1111l_opy_[option.lower()]:
      bstack1llll11ll_opy_[bstack1111l_opy_[option.lower()]] = bstack1llll11ll_opy_[option]
      del bstack1llll11ll_opy_[option]
  return config
def bstack1lll11ll1_opy_(config):
  bstack1l111ll_opy_ = config.keys()
  for bstack11ll11l1_opy_, bstack111llll1_opy_ in bstack1ll1l_opy_.items():
    if bstack111llll1_opy_ in bstack1l111ll_opy_:
      config[bstack11ll11l1_opy_] = config[bstack111llll1_opy_]
      del config[bstack111llll1_opy_]
  for bstack11ll11l1_opy_, bstack111llll1_opy_ in bstack1llll_opy_.items():
    if isinstance(bstack111llll1_opy_, list):
      for bstack11l1ll1l_opy_ in bstack111llll1_opy_:
        if bstack11l1ll1l_opy_ in bstack1l111ll_opy_:
          config[bstack11ll11l1_opy_] = config[bstack11l1ll1l_opy_]
          del config[bstack11l1ll1l_opy_]
          break
    elif bstack111llll1_opy_ in bstack1l111ll_opy_:
        config[bstack11ll11l1_opy_] = config[bstack111llll1_opy_]
        del config[bstack111llll1_opy_]
  for bstack11l1ll1l_opy_ in list(config):
    for bstack1ll11l1l_opy_ in bstack1lllll_opy_:
      if bstack11l1ll1l_opy_.lower() == bstack1ll11l1l_opy_.lower() and bstack11l1ll1l_opy_ != bstack1ll11l1l_opy_:
        config[bstack1ll11l1l_opy_] = config[bstack11l1ll1l_opy_]
        del config[bstack11l1ll1l_opy_]
  bstack1l1lllll_opy_ = []
  if bstack11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ஻") in config:
    bstack1l1lllll_opy_ = config[bstack11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ஼")]
  for platform in bstack1l1lllll_opy_:
    for bstack11l1ll1l_opy_ in list(platform):
      for bstack1ll11l1l_opy_ in bstack1lllll_opy_:
        if bstack11l1ll1l_opy_.lower() == bstack1ll11l1l_opy_.lower() and bstack11l1ll1l_opy_ != bstack1ll11l1l_opy_:
          platform[bstack1ll11l1l_opy_] = platform[bstack11l1ll1l_opy_]
          del platform[bstack11l1ll1l_opy_]
  for bstack11ll11l1_opy_, bstack111llll1_opy_ in bstack1llll_opy_.items():
    for platform in bstack1l1lllll_opy_:
      if isinstance(bstack111llll1_opy_, list):
        for bstack11l1ll1l_opy_ in bstack111llll1_opy_:
          if bstack11l1ll1l_opy_ in platform:
            platform[bstack11ll11l1_opy_] = platform[bstack11l1ll1l_opy_]
            del platform[bstack11l1ll1l_opy_]
            break
      elif bstack111llll1_opy_ in platform:
        platform[bstack11ll11l1_opy_] = platform[bstack111llll1_opy_]
        del platform[bstack111llll1_opy_]
  for bstack11ll1111_opy_ in bstack1l11_opy_:
    if bstack11ll1111_opy_ in config:
      if not bstack1l11_opy_[bstack11ll1111_opy_] in config:
        config[bstack1l11_opy_[bstack11ll1111_opy_]] = {}
      config[bstack1l11_opy_[bstack11ll1111_opy_]].update(config[bstack11ll1111_opy_])
      del config[bstack11ll1111_opy_]
  for platform in bstack1l1lllll_opy_:
    for bstack11ll1111_opy_ in bstack1l11_opy_:
      if bstack11ll1111_opy_ in list(platform):
        if not bstack1l11_opy_[bstack11ll1111_opy_] in platform:
          platform[bstack1l11_opy_[bstack11ll1111_opy_]] = {}
        platform[bstack1l11_opy_[bstack11ll1111_opy_]].update(platform[bstack11ll1111_opy_])
        del platform[bstack11ll1111_opy_]
  config = bstack11l1111_opy_(config)
  return config
def bstack1l11l1l_opy_(config):
  global bstack1llllll1_opy_
  if bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭஽") in config and str(config[bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧா")]).lower() != bstack11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪி"):
    if not bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩீ") in config:
      config[bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪு")] = {}
    if not bstack11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩூ") in config[bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ௃")]:
      if bstack11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ௄") in os.environ:
        config[bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ௅")][bstack11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ெ")] = os.environ[bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧே")]
      else:
        current_time = datetime.datetime.now()
        bstack1ll1lll_opy_ = current_time.strftime(bstack11_opy_ (u"࠭ࠥࡥࡡࠨࡦࡤࠫࡈࠦࡏࠪை"))
        hostname = socket.gethostname()
        bstack1l11l1_opy_ = bstack11_opy_ (u"ࠧࠨ௉").join(random.choices(string.ascii_lowercase + string.digits, k=4))
        identifier = bstack11_opy_ (u"ࠨࡽࢀࡣࢀࢃ࡟ࡼࡿࠪொ").format(bstack1ll1lll_opy_, hostname, bstack1l11l1_opy_)
        config[bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ோ")][bstack11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬௌ")] = identifier
    bstack1llllll1_opy_ = config[bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ்")][bstack11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ௎")]
  return config
def bstack1lll111_opy_(config):
  if bstack11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ௏") in config and config[bstack11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪௐ")] not in bstack11l1_opy_:
    return config[bstack11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ௑")]
  elif bstack11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬ௒") in os.environ:
    return os.environ[bstack11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭௓")]
  else:
    return None
def bstack111l11_opy_(config):
  if bstack11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡑࡅࡒࡋࠧ௔") in os.environ:
    return os.environ[bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠨ௕")]
  elif bstack11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ௖") in config:
    return config[bstack11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪௗ")]
  else:
    return None
def bstack1lll1ll1l_opy_():
  if (
    isinstance(os.getenv(bstack11_opy_ (u"ࠨࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑ࠭௘")), str) and len(os.getenv(bstack11_opy_ (u"ࠩࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠧ௙"))) > 0
  ) or (
    isinstance(os.getenv(bstack11_opy_ (u"ࠪࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠩ௚")), str) and len(os.getenv(bstack11_opy_ (u"ࠫࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠪ௛"))) > 0
  ):
    return os.getenv(bstack11_opy_ (u"ࠬࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠫ௜"), 0)
  if str(os.getenv(bstack11_opy_ (u"࠭ࡃࡊࠩ௝"))).lower() == bstack11_opy_ (u"ࠧࡵࡴࡸࡩࠬ௞") and str(os.getenv(bstack11_opy_ (u"ࠨࡅࡌࡖࡈࡒࡅࡄࡋࠪ௟"))).lower() == bstack11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ௠"):
    return os.getenv(bstack11_opy_ (u"ࠪࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒ࠭௡"), 0)
  if str(os.getenv(bstack11_opy_ (u"ࠫࡈࡏࠧ௢"))).lower() == bstack11_opy_ (u"ࠬࡺࡲࡶࡧࠪ௣") and str(os.getenv(bstack11_opy_ (u"࠭ࡔࡓࡃ࡙ࡍࡘ࠭௤"))).lower() == bstack11_opy_ (u"ࠧࡵࡴࡸࡩࠬ௥"):
    return os.getenv(bstack11_opy_ (u"ࠨࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠧ௦"), 0)
  if str(os.getenv(bstack11_opy_ (u"ࠩࡆࡍࠬ௧"))).lower() == bstack11_opy_ (u"ࠪࡸࡷࡻࡥࠨ௨") and str(os.getenv(bstack11_opy_ (u"ࠫࡈࡏ࡟ࡏࡃࡐࡉࠬ௩"))).lower() == bstack11_opy_ (u"ࠬࡩ࡯ࡥࡧࡶ࡬࡮ࡶࠧ௪"):
    return 0 # bstack1l111l11_opy_ bstack1l1ll11_opy_ not set build number env
  if os.getenv(bstack11_opy_ (u"࠭ࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅࡖࡆࡔࡃࡉࠩ௫")) and os.getenv(bstack11_opy_ (u"ࠧࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡇࡔࡓࡍࡊࡖࠪ௬")):
    return os.getenv(bstack11_opy_ (u"ࠨࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠪ௭"), 0)
  if str(os.getenv(bstack11_opy_ (u"ࠩࡆࡍࠬ௮"))).lower() == bstack11_opy_ (u"ࠪࡸࡷࡻࡥࠨ௯") and str(os.getenv(bstack11_opy_ (u"ࠫࡉࡘࡏࡏࡇࠪ௰"))).lower() == bstack11_opy_ (u"ࠬࡺࡲࡶࡧࠪ௱"):
    return os.getenv(bstack11_opy_ (u"࠭ࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠫ௲"), 0)
  if str(os.getenv(bstack11_opy_ (u"ࠧࡄࡋࠪ௳"))).lower() == bstack11_opy_ (u"ࠨࡶࡵࡹࡪ࠭௴") and str(os.getenv(bstack11_opy_ (u"ࠩࡖࡉࡒࡇࡐࡉࡑࡕࡉࠬ௵"))).lower() == bstack11_opy_ (u"ࠪࡸࡷࡻࡥࠨ௶"):
    return os.getenv(bstack11_opy_ (u"ࠫࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡎࡊࠧ௷"), 0)
  if str(os.getenv(bstack11_opy_ (u"ࠬࡉࡉࠨ௸"))).lower() == bstack11_opy_ (u"࠭ࡴࡳࡷࡨࠫ௹") and str(os.getenv(bstack11_opy_ (u"ࠧࡈࡋࡗࡐࡆࡈ࡟ࡄࡋࠪ௺"))).lower() == bstack11_opy_ (u"ࠨࡶࡵࡹࡪ࠭௻"):
    return os.getenv(bstack11_opy_ (u"ࠩࡆࡍࡤࡐࡏࡃࡡࡌࡈࠬ௼"), 0)
  if str(os.getenv(bstack11_opy_ (u"ࠪࡇࡎ࠭௽"))).lower() == bstack11_opy_ (u"ࠫࡹࡸࡵࡦࠩ௾") and str(os.getenv(bstack11_opy_ (u"ࠬࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࠨ௿"))).lower() == bstack11_opy_ (u"࠭ࡴࡳࡷࡨࠫఀ"):
    return os.getenv(bstack11_opy_ (u"ࠧࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠩఁ"), 0)
  if str(os.getenv(bstack11_opy_ (u"ࠨࡖࡉࡣࡇ࡛ࡉࡍࡆࠪం"))).lower() == bstack11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧః"):
    return os.getenv(bstack11_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠪఄ"), 0)
  return -1
def bstack11ll1l_opy_(bstack111l1l1l_opy_):
  global CONFIG
  if not bstack11_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭అ") in CONFIG[bstack11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧఆ")]:
    return
  CONFIG[bstack11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨఇ")] = CONFIG[bstack11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩఈ")].replace(
    bstack11_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪఉ"),
    str(bstack111l1l1l_opy_)
  )
def bstack111l1ll1_opy_():
  global CONFIG
  if not bstack11_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨఊ") in CONFIG[bstack11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬఋ")]:
    return
  current_time = datetime.datetime.now()
  bstack1ll1lll_opy_ = current_time.strftime(bstack11_opy_ (u"ࠫࠪࡪ࠭ࠦࡤ࠰ࠩࡍࡀࠥࡎࠩఌ"))
  CONFIG[bstack11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ఍")] = CONFIG[bstack11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨఎ")].replace(
    bstack11_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭ఏ"),
    bstack1ll1lll_opy_
  )
def bstack11llll11_opy_():
  global CONFIG
  if bstack11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪఐ") in CONFIG and not bool(CONFIG[bstack11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ఑")]):
    del CONFIG[bstack11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬఒ")]
    return
  if not bstack11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ఓ") in CONFIG:
    CONFIG[bstack11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧఔ")] = bstack11_opy_ (u"࠭ࠣࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩక")
  if bstack11_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭ఖ") in CONFIG[bstack11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪగ")]:
    bstack111l1ll1_opy_()
    os.environ[bstack11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ఘ")] = CONFIG[bstack11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬఙ")]
  if not bstack11_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭చ") in CONFIG[bstack11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧఛ")]:
    return
  bstack111l1l1l_opy_ = bstack11_opy_ (u"࠭ࠧజ")
  bstack11lll111_opy_ = bstack1lll1ll1l_opy_()
  if bstack11lll111_opy_ != -1:
    bstack111l1l1l_opy_ = bstack11_opy_ (u"ࠧࡄࡋࠣࠫఝ") + str(bstack11lll111_opy_)
  if bstack111l1l1l_opy_ == bstack11_opy_ (u"ࠨࠩఞ"):
    bstack1l1llll_opy_ = bstack1111lll1_opy_(CONFIG[bstack11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬట")])
    if bstack1l1llll_opy_ != -1:
      bstack111l1l1l_opy_ = str(bstack1l1llll_opy_)
  if bstack111l1l1l_opy_:
    bstack11ll1l_opy_(bstack111l1l1l_opy_)
    os.environ[bstack11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧఠ")] = CONFIG[bstack11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭డ")]
def bstack1llll1l_opy_(bstack1ll1l11l_opy_, bstack1l11111_opy_, path):
  bstack1ll11ll1_opy_ = {
    bstack11_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩఢ"): bstack1l11111_opy_
  }
  if os.path.exists(path):
    bstack11lllll1_opy_ = json.load(open(path, bstack11_opy_ (u"࠭ࡲࡣࠩణ")))
  else:
    bstack11lllll1_opy_ = {}
  bstack11lllll1_opy_[bstack1ll1l11l_opy_] = bstack1ll11ll1_opy_
  with open(path, bstack11_opy_ (u"ࠢࡸ࠭ࠥత")) as outfile:
    json.dump(bstack11lllll1_opy_, outfile)
def bstack1111lll1_opy_(bstack1ll1l11l_opy_):
  bstack1ll1l11l_opy_ = str(bstack1ll1l11l_opy_)
  bstack1lll111ll_opy_ = os.path.join(os.path.expanduser(bstack11_opy_ (u"ࠨࢀࠪథ")), bstack11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩద"))
  try:
    if not os.path.exists(bstack1lll111ll_opy_):
      os.makedirs(bstack1lll111ll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11_opy_ (u"ࠪࢂࠬధ")), bstack11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫన"), bstack11_opy_ (u"ࠬ࠴ࡢࡶ࡫࡯ࡨ࠲ࡴࡡ࡮ࡧ࠰ࡧࡦࡩࡨࡦ࠰࡭ࡷࡴࡴࠧ఩"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11_opy_ (u"࠭ࡷࠨప")):
        pass
      with open(file_path, bstack11_opy_ (u"ࠢࡸ࠭ࠥఫ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11_opy_ (u"ࠨࡴࠪబ")) as bstack1l1ll111_opy_:
      bstack1ll1l11_opy_ = json.load(bstack1l1ll111_opy_)
    if bstack1ll1l11l_opy_ in bstack1ll1l11_opy_:
      bstack1lll1lll1_opy_ = bstack1ll1l11_opy_[bstack1ll1l11l_opy_][bstack11_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭భ")]
      bstack1l1111_opy_ = int(bstack1lll1lll1_opy_) + 1
      bstack1llll1l_opy_(bstack1ll1l11l_opy_, bstack1l1111_opy_, file_path)
      return bstack1l1111_opy_
    else:
      bstack1llll1l_opy_(bstack1ll1l11l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack11l1ll11_opy_.format(str(e)))
    return -1
def bstack1lllll11_opy_(config):
  if bstack11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬమ") in config and config[bstack11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭య")] not in bstack1lll1l_opy_:
    return config[bstack11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧర")]
  elif bstack11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧఱ") in os.environ:
    return os.environ[bstack11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨల")]
  else:
    return None
def bstack1lllll111_opy_(config):
  if not bstack1lllll11_opy_(config) or not bstack1lll111_opy_(config):
    return True
  else:
    return False
def bstack1ll11l_opy_(config):
  if bstack11l1lll1_opy_() < version.parse(bstack11_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧళ")):
    return False
  if bstack11l1lll1_opy_() >= version.parse(bstack11_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨఴ")):
    return True
  if bstack11_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪవ") in config and config[bstack11_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫశ")] == False:
    return False
  else:
    return True
def bstack1111l11l_opy_(config, index = 0):
  global bstack1llll1ll_opy_
  bstack111l1l11_opy_ = {}
  caps = bstack1l1ll_opy_ + bstack111l_opy_
  if bstack1llll1ll_opy_:
    caps += bstack111ll_opy_
  for key in config:
    if key in caps + [bstack11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨష")]:
      continue
    bstack111l1l11_opy_[key] = config[key]
  if bstack11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩస") in config:
    for bstack1l111l1l_opy_ in config[bstack11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪహ")][index]:
      if bstack1l111l1l_opy_ in caps + [bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭఺"), bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ఻")]:
        continue
      bstack111l1l11_opy_[bstack1l111l1l_opy_] = config[bstack11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ఼࠭")][index][bstack1l111l1l_opy_]
  bstack111l1l11_opy_[bstack11_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ఽ")] = socket.gethostname()
  return bstack111l1l11_opy_
def bstack11lll1ll_opy_(config):
  global bstack1llll1ll_opy_
  bstack111lll1l_opy_ = {}
  caps = bstack111l_opy_
  if bstack1llll1ll_opy_:
    caps+= bstack111ll_opy_
  for key in caps:
    if key in config:
      bstack111lll1l_opy_[key] = config[key]
  return bstack111lll1l_opy_
def bstack111111l1_opy_(bstack111l1l11_opy_, bstack111lll1l_opy_):
  bstack11111111_opy_ = {}
  for key in bstack111l1l11_opy_.keys():
    if key in bstack1ll1l_opy_:
      bstack11111111_opy_[bstack1ll1l_opy_[key]] = bstack111l1l11_opy_[key]
    else:
      bstack11111111_opy_[key] = bstack111l1l11_opy_[key]
  for key in bstack111lll1l_opy_:
    if key in bstack1ll1l_opy_:
      bstack11111111_opy_[bstack1ll1l_opy_[key]] = bstack111lll1l_opy_[key]
    else:
      bstack11111111_opy_[key] = bstack111lll1l_opy_[key]
  return bstack11111111_opy_
def bstack1lll1l1_opy_(config, index = 0):
  global bstack1llll1ll_opy_
  caps = {}
  bstack111lll1l_opy_ = bstack11lll1ll_opy_(config)
  bstack1lll1ll1_opy_ = bstack111l_opy_
  bstack1lll1ll1_opy_ += bstack11111_opy_
  if bstack1llll1ll_opy_:
    bstack1lll1ll1_opy_ += bstack111ll_opy_
  if bstack11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨా") in config:
    if bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫి") in config[bstack11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪీ")][index]:
      caps[bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ు")] = config[bstack11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬూ")][index][bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨృ")]
    if bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬౄ") in config[bstack11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ౅")][index]:
      caps[bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧె")] = str(config[bstack11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪే")][index][bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩై")])
    bstack111lll1_opy_ = {}
    for bstack111llll_opy_ in bstack1lll1ll1_opy_:
      if bstack111llll_opy_ in config[bstack11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౉")][index]:
        if bstack111llll_opy_ == bstack11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬొ"):
          bstack111lll1_opy_[bstack111llll_opy_] = str(config[bstack11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧో")][index][bstack111llll_opy_] * 1.0)
        else:
          bstack111lll1_opy_[bstack111llll_opy_] = config[bstack11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨౌ")][index][bstack111llll_opy_]
        del(config[bstack11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ్ࠩ")][index][bstack111llll_opy_])
    bstack111lll1l_opy_ = update(bstack111lll1l_opy_, bstack111lll1_opy_)
  bstack111l1l11_opy_ = bstack1111l11l_opy_(config, index)
  for bstack11l1ll1l_opy_ in bstack111l_opy_ + [bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ౎"), bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ౏")]:
    if bstack11l1ll1l_opy_ in bstack111l1l11_opy_:
      bstack111lll1l_opy_[bstack11l1ll1l_opy_] = bstack111l1l11_opy_[bstack11l1ll1l_opy_]
      del(bstack111l1l11_opy_[bstack11l1ll1l_opy_])
  if bstack1ll11l_opy_(config):
    bstack111l1l11_opy_[bstack11_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ౐")] = True
    caps.update(bstack111lll1l_opy_)
    caps[bstack11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ౑")] = bstack111l1l11_opy_
  else:
    bstack111l1l11_opy_[bstack11_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ౒")] = False
    caps.update(bstack111111l1_opy_(bstack111l1l11_opy_, bstack111lll1l_opy_))
    if bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ౓") in caps:
      caps[bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ౔")] = caps[bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩౕࠬ")]
      del(caps[bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪౖ࠭")])
    if bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ౗") in caps:
      caps[bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬౘ")] = caps[bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬౙ")]
      del(caps[bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ౚ")])
  return caps
def bstack111l11l1_opy_():
  if bstack11l1lll1_opy_() <= version.parse(bstack11_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭౛")):
    return bstack11ll1_opy_
  return bstack1llll1_opy_
def bstack1l11l111_opy_(options):
  return hasattr(options, bstack11_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨ౜"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack111l111_opy_(options, bstack1l11ll1l_opy_):
  for bstack1llll1ll1_opy_ in bstack1l11ll1l_opy_:
    if bstack1llll1ll1_opy_ in [bstack11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ౝ"), bstack11_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭౞")]:
      next
    if bstack1llll1ll1_opy_ in options._experimental_options:
      options._experimental_options[bstack1llll1ll1_opy_]= update(options._experimental_options[bstack1llll1ll1_opy_], bstack1l11ll1l_opy_[bstack1llll1ll1_opy_])
    else:
      options.add_experimental_option(bstack1llll1ll1_opy_, bstack1l11ll1l_opy_[bstack1llll1ll1_opy_])
  if bstack11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ౟") in bstack1l11ll1l_opy_:
    for arg in bstack1l11ll1l_opy_[bstack11_opy_ (u"ࠫࡦࡸࡧࡴࠩౠ")]:
      options.add_argument(arg)
    del(bstack1l11ll1l_opy_[bstack11_opy_ (u"ࠬࡧࡲࡨࡵࠪౡ")])
  if bstack11_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪౢ") in bstack1l11ll1l_opy_:
    for ext in bstack1l11ll1l_opy_[bstack11_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫౣ")]:
      options.add_extension(ext)
    del(bstack1l11ll1l_opy_[bstack11_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ౤")])
def bstack1111111_opy_(options, bstack1llll111_opy_):
  if bstack11_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ౥") in bstack1llll111_opy_:
    for bstack11ll11ll_opy_ in bstack1llll111_opy_[bstack11_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ౦")]:
      if bstack11ll11ll_opy_ in options._preferences:
        options._preferences[bstack11ll11ll_opy_] = update(options._preferences[bstack11ll11ll_opy_], bstack1llll111_opy_[bstack11_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ౧")][bstack11ll11ll_opy_])
      else:
        options.set_preference(bstack11ll11ll_opy_, bstack1llll111_opy_[bstack11_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ౨")][bstack11ll11ll_opy_])
  if bstack11_opy_ (u"࠭ࡡࡳࡩࡶࠫ౩") in bstack1llll111_opy_:
    for arg in bstack1llll111_opy_[bstack11_opy_ (u"ࠧࡢࡴࡪࡷࠬ౪")]:
      options.add_argument(arg)
def bstack1ll111ll_opy_(options, bstack11l1l1l_opy_):
  if bstack11_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࠩ౫") in bstack11l1l1l_opy_:
    options.use_webview(bool(bstack11l1l1l_opy_[bstack11_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪ౬")]))
  bstack111l111_opy_(options, bstack11l1l1l_opy_)
def bstack1llll11l_opy_(options, bstack111ll1l_opy_):
  for bstack1l1lll_opy_ in bstack111ll1l_opy_:
    if bstack1l1lll_opy_ in [bstack11_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧ౭"), bstack11_opy_ (u"ࠫࡦࡸࡧࡴࠩ౮")]:
      next
    options.set_capability(bstack1l1lll_opy_, bstack111ll1l_opy_[bstack1l1lll_opy_])
  if bstack11_opy_ (u"ࠬࡧࡲࡨࡵࠪ౯") in bstack111ll1l_opy_:
    for arg in bstack111ll1l_opy_[bstack11_opy_ (u"࠭ࡡࡳࡩࡶࠫ౰")]:
      options.add_argument(arg)
  if bstack11_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫ౱") in bstack111ll1l_opy_:
    options.use_technology_preview(bool(bstack111ll1l_opy_[bstack11_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬ౲")]))
def bstack1llll1l1l_opy_(options, bstack11ll111_opy_):
  for bstack1llll1l11_opy_ in bstack11ll111_opy_:
    if bstack1llll1l11_opy_ in [bstack11_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭౳"), bstack11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ౴")]:
      next
    options._options[bstack1llll1l11_opy_] = bstack11ll111_opy_[bstack1llll1l11_opy_]
  if bstack11_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ౵") in bstack11ll111_opy_:
    for bstack1ll1ll_opy_ in bstack11ll111_opy_[bstack11_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ౶")]:
      options.add_additional_option(
          bstack1ll1ll_opy_, bstack11ll111_opy_[bstack11_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ౷")][bstack1ll1ll_opy_])
  if bstack11_opy_ (u"ࠧࡢࡴࡪࡷࠬ౸") in bstack11ll111_opy_:
    for arg in bstack11ll111_opy_[bstack11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭౹")]:
      options.add_argument(arg)
def bstack1lll1l111_opy_(options, caps):
  if not hasattr(options, bstack11_opy_ (u"ࠩࡎࡉ࡞࠭౺")):
    return
  if options.KEY == bstack11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ౻") and options.KEY in caps:
    bstack111l111_opy_(options, caps[bstack11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ౼")])
  elif options.KEY == bstack11_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪ౽") and options.KEY in caps:
    bstack1111111_opy_(options, caps[bstack11_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫ౾")])
  elif options.KEY == bstack11_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ౿") and options.KEY in caps:
    bstack1llll11l_opy_(options, caps[bstack11_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩಀ")])
  elif options.KEY == bstack11_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪಁ") and options.KEY in caps:
    bstack1ll111ll_opy_(options, caps[bstack11_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫಂ")])
  elif options.KEY == bstack11_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪಃ") and options.KEY in caps:
    bstack1llll1l1l_opy_(options, caps[bstack11_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ಄")])
def bstack11lll1l1_opy_(caps):
  global bstack1llll1ll_opy_
  if bstack1llll1ll_opy_:
    if bstack11l1ll_opy_() < version.parse(bstack11_opy_ (u"࠭࠲࠯࠵࠱࠴ࠬಅ")):
      return None
    else:
      from bstack1l1l11ll_opy_.options.common.base import bstack1lll1l1l_opy_
      options = bstack1lll1l1l_opy_().bstack1l11llll_opy_(caps)
      return options
  else:
    browser = bstack11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧಆ")
    if bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ಇ") in caps:
      browser = caps[bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧಈ")]
    elif bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫಉ") in caps:
      browser = caps[bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬಊ")]
    browser = str(browser).lower()
    if browser == bstack11_opy_ (u"ࠬ࡯ࡰࡩࡱࡱࡩࠬಋ") or browser == bstack11_opy_ (u"࠭ࡩࡱࡣࡧࠫಌ"):
      browser = bstack11_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧ಍")
    if browser == bstack11_opy_ (u"ࠨࡵࡤࡱࡸࡻ࡮ࡨࠩಎ"):
      browser = bstack11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩಏ")
    if browser not in [bstack11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪಐ"), bstack11_opy_ (u"ࠫࡪࡪࡧࡦࠩ಑"), bstack11_opy_ (u"ࠬ࡯ࡥࠨಒ"), bstack11_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ಓ"), bstack11_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨಔ")]:
      return None
    try:
      package = bstack11_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡻࡾ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪಕ").format(browser)
      name = bstack11_opy_ (u"ࠩࡒࡴࡹ࡯࡯࡯ࡵࠪಖ")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l11l111_opy_(options):
        return None
      for bstack11l1ll1l_opy_ in caps.keys():
        options.set_capability(bstack11l1ll1l_opy_, caps[bstack11l1ll1l_opy_])
      bstack1lll1l111_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack11lll1_opy_(options, bstack1l111lll_opy_):
  if not bstack1l11l111_opy_(options):
    return
  for bstack11l1ll1l_opy_ in bstack1l111lll_opy_.keys():
    if bstack11l1ll1l_opy_ in bstack11111_opy_:
      next
    if bstack11l1ll1l_opy_ in options._caps and type(options._caps[bstack11l1ll1l_opy_]) in [dict, list]:
      options._caps[bstack11l1ll1l_opy_] = update(options._caps[bstack11l1ll1l_opy_], bstack1l111lll_opy_[bstack11l1ll1l_opy_])
    else:
      options.set_capability(bstack11l1ll1l_opy_, bstack1l111lll_opy_[bstack11l1ll1l_opy_])
  bstack1lll1l111_opy_(options, bstack1l111lll_opy_)
  if bstack11_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩಗ") in options._caps:
    if options._caps[bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩಘ")] and options._caps[bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪಙ")].lower() != bstack11_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧಚ"):
      del options._caps[bstack11_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ಛ")]
def bstack11l11l_opy_(proxy_config):
  if bstack11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬಜ") in proxy_config:
    proxy_config[bstack11_opy_ (u"ࠩࡶࡷࡱࡖࡲࡰࡺࡼࠫಝ")] = proxy_config[bstack11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧಞ")]
    del(proxy_config[bstack11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨಟ")])
  if bstack11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨಠ") in proxy_config and proxy_config[bstack11_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩಡ")].lower() != bstack11_opy_ (u"ࠧࡥ࡫ࡵࡩࡨࡺࠧಢ"):
    proxy_config[bstack11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫಣ")] = bstack11_opy_ (u"ࠩࡰࡥࡳࡻࡡ࡭ࠩತ")
  if bstack11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡃࡸࡸࡴࡩ࡯࡯ࡨ࡬࡫࡚ࡸ࡬ࠨಥ") in proxy_config:
    proxy_config[bstack11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧದ")] = bstack11_opy_ (u"ࠬࡶࡡࡤࠩಧ")
  return proxy_config
def bstack11ll11_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬನ") in config:
    return proxy
  config[bstack11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭಩")] = bstack11l11l_opy_(config[bstack11_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧಪ")])
  if proxy == None:
    proxy = Proxy(config[bstack11_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨಫ")])
  return proxy
def bstack1lll1l1ll_opy_(self):
  global CONFIG
  global bstack1111ll11_opy_
  if bstack11_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ಬ") in CONFIG and bstack111l11l1_opy_().startswith(bstack11_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࠬಭ")):
    return CONFIG[bstack11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨಮ")]
  elif bstack11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪಯ") in CONFIG and bstack111l11l1_opy_().startswith(bstack11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࠩರ")):
    return CONFIG[bstack11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬಱ")]
  else:
    return bstack1111ll11_opy_(self)
def bstack1111l1_opy_():
  if bstack11l1lll1_opy_() < version.parse(bstack11_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࠨಲ")):
    logger.warning(bstack1l1l11_opy_.format(bstack11l1lll1_opy_()))
    return
  global bstack1111ll11_opy_
  from selenium.webdriver.remote.remote_connection import RemoteConnection
  bstack1111ll11_opy_ = RemoteConnection._get_proxy_url
  RemoteConnection._get_proxy_url = bstack1lll1l1ll_opy_
def bstack11111lll_opy_(config):
  if bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧಳ") in config:
    if str(config[bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ಴")]).lower() == bstack11_opy_ (u"ࠬࡺࡲࡶࡧࠪವ"):
      return True
    else:
      return False
  elif bstack11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࠫಶ") in os.environ:
    if str(os.environ[bstack11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࠬಷ")]).lower() == bstack11_opy_ (u"ࠨࡶࡵࡹࡪ࠭ಸ"):
      return True
    else:
      return False
  else:
    return False
def bstack1ll1lll1_opy_(config):
  if bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ಹ") in config:
    return config[bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ಺")]
  if bstack11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ಻") in config:
    return config[bstack11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶ಼ࠫ")]
  return {}
def bstack11l1l11l_opy_(caps):
  global bstack1llllll1_opy_
  if bstack11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧಽ") in caps:
    caps[bstack11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨಾ")][bstack11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧಿ")] = True
    if bstack1llllll1_opy_:
      caps[bstack11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪೀ")][bstack11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬು")] = bstack1llllll1_opy_
  else:
    caps[bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩೂ")] = True
    if bstack1llllll1_opy_:
      caps[bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ೃ")] = bstack1llllll1_opy_
def bstack1111l11_opy_():
  global CONFIG
  if bstack11111lll_opy_(CONFIG):
    bstack1llll11ll_opy_ = bstack1ll1lll1_opy_(CONFIG)
    bstack1l1111l_opy_(bstack1lll111_opy_(CONFIG), bstack1llll11ll_opy_)
def bstack1l1111l_opy_(key, bstack1llll11ll_opy_):
  global bstack1l111l_opy_
  logger.info(bstack1l1lll1l_opy_)
  try:
    bstack1l111l_opy_ = Local()
    bstack111ll1ll_opy_ = {bstack11_opy_ (u"࠭࡫ࡦࡻࠪೄ"): key}
    bstack111ll1ll_opy_.update(bstack1llll11ll_opy_)
    logger.debug(bstack1ll11ll_opy_.format(str(bstack111ll1ll_opy_)))
    bstack1l111l_opy_.start(**bstack111ll1ll_opy_)
    if bstack1l111l_opy_.isRunning():
      logger.info(bstack1ll1l1_opy_)
  except Exception as e:
    bstack11l111ll_opy_(bstack11l111_opy_.format(str(e)))
def bstack11ll1ll_opy_():
  global bstack1l111l_opy_
  if bstack1l111l_opy_.isRunning():
    logger.info(bstack1l1l111_opy_)
    bstack1l111l_opy_.stop()
  bstack1l111l_opy_ = None
def bstack11l11l1_opy_():
  logger.info(bstack1ll1ll1l_opy_)
  global bstack1l111l_opy_
  if bstack1l111l_opy_:
    bstack11ll1ll_opy_()
  logger.info(bstack11l1111l_opy_)
def bstack11ll1ll1_opy_(self, *args):
  logger.error(bstack1llllll_opy_)
  bstack11l11l1_opy_()
  sys.exit(1)
def bstack11l111ll_opy_(err):
  logger.critical(bstack1ll1111l_opy_.format(str(err)))
  atexit.unregister(bstack11l11l1_opy_)
  sys.exit(1)
def bstack1l11l1ll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  atexit.unregister(bstack11l11l1_opy_)
  sys.exit(1)
def bstack1lllll1l_opy_():
  global CONFIG
  CONFIG = bstack1l1ll1l1_opy_()
  CONFIG = bstack1lll11ll1_opy_(CONFIG)
  CONFIG = bstack1l11l1l_opy_(CONFIG)
  if bstack1lllll111_opy_(CONFIG):
    bstack11l111ll_opy_(bstack1ll11lll_opy_)
  CONFIG[bstack11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ೅")] = bstack1lllll11_opy_(CONFIG)
  CONFIG[bstack11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫೆ")] = bstack1lll111_opy_(CONFIG)
  if bstack111l11_opy_(CONFIG):
    CONFIG[bstack11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬೇ")] = bstack111l11_opy_(CONFIG)
    if not os.getenv(bstack11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡐࡄࡑࡊ࠭ೈ")):
      if os.getenv(bstack11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨ೉")):
        CONFIG[bstack11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧೊ")] = os.getenv(bstack11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪೋ"))
      else:
        bstack11llll11_opy_()
    else:
      if bstack11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩೌ") in CONFIG:
        del(CONFIG[bstack11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ್ࠪ")])
  bstack1ll11l1_opy_()
  bstack1lllllll_opy_()
  if bstack1llll1ll_opy_:
    CONFIG[bstack11_opy_ (u"ࠩࡤࡴࡵ࠭೎")] = bstack1l11111l_opy_(CONFIG)
    logger.info(bstack1lll1ll_opy_.format(CONFIG[bstack11_opy_ (u"ࠪࡥࡵࡶࠧ೏")]))
def bstack1lllllll_opy_():
  global CONFIG
  global bstack1llll1ll_opy_
  if bstack11_opy_ (u"ࠫࡦࡶࡰࠨ೐") in CONFIG:
    try:
      from bstack1l1l11ll_opy_ import version
    except Exception as e:
      bstack1l11l1ll_opy_(e, bstack11lllll_opy_)
    bstack1llll1ll_opy_ = True
def bstack1l11111l_opy_(config):
  bstack11111l_opy_ = bstack11_opy_ (u"ࠬ࠭೑")
  app = config[bstack11_opy_ (u"࠭ࡡࡱࡲࠪ೒")]
  if isinstance(config[bstack11_opy_ (u"ࠧࡢࡲࡳࠫ೓")], str):
    if os.path.splitext(app)[1] in bstack1l11l_opy_:
      if os.path.exists(app):
        bstack11111l_opy_ = bstack1lll1111_opy_(config, app)
      elif bstack1111l1l1_opy_(app):
        bstack11111l_opy_ = app
      else:
        bstack11l111ll_opy_(bstack1l1ll1l_opy_.format(app))
    else:
      if bstack1111l1l1_opy_(app):
        bstack11111l_opy_ = app
      elif os.path.exists(app):
        bstack11111l_opy_ = bstack1lll1111_opy_(app)
      else:
        bstack11l111ll_opy_(bstack1lllll1ll_opy_)
  else:
    if len(app) > 2:
      bstack11l111ll_opy_(bstack111l11l_opy_)
    elif len(app) == 2:
      if bstack11_opy_ (u"ࠨࡲࡤࡸ࡭࠭೔") in app and bstack11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬೕ") in app:
        if os.path.exists(app[bstack11_opy_ (u"ࠪࡴࡦࡺࡨࠨೖ")]):
          bstack11111l_opy_ = bstack1lll1111_opy_(config, app[bstack11_opy_ (u"ࠫࡵࡧࡴࡩࠩ೗")], app[bstack11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ೘")])
        else:
          bstack11l111ll_opy_(bstack1l1ll1l_opy_.format(app))
      else:
        bstack11l111ll_opy_(bstack111l11l_opy_)
    else:
      for key in app:
        if key in bstack1111_opy_:
          if key == bstack11_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ೙"):
            if os.path.exists(app[key]):
              bstack11111l_opy_ = bstack1lll1111_opy_(config, app[key])
            else:
              bstack11l111ll_opy_(bstack1l1ll1l_opy_.format(app))
          else:
            bstack11111l_opy_ = app[key]
        else:
          bstack11l111ll_opy_(bstack1ll111_opy_)
  return bstack11111l_opy_
def bstack1111l1l1_opy_(bstack11111l_opy_):
  import re
  bstack1l1l1111_opy_ = re.compile(bstack11_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢ೚"))
  bstack111l111l_opy_ = re.compile(bstack11_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧ೛"))
  if bstack11_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨ೜") in bstack11111l_opy_ or re.fullmatch(bstack1l1l1111_opy_, bstack11111l_opy_) or re.fullmatch(bstack111l111l_opy_, bstack11111l_opy_):
    return True
  else:
    return False
def bstack1lll1111_opy_(config, path, bstack11l1lll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11_opy_ (u"ࠪࡶࡧ࠭ೝ")).read()).hexdigest()
  bstack1lll1l1l1_opy_ = bstack1llllll11_opy_(md5_hash)
  bstack11111l_opy_ = None
  if bstack1lll1l1l1_opy_:
    logger.info(bstack1111ll1l_opy_.format(bstack1lll1l1l1_opy_, md5_hash))
    return bstack1lll1l1l1_opy_
  bstack11l111l_opy_ = MultipartEncoder(
    fields={
        bstack11_opy_ (u"ࠫ࡫࡯࡬ࡦࠩೞ"): (os.path.basename(path), open(os.path.abspath(path), bstack11_opy_ (u"ࠬࡸࡢࠨ೟")), bstack11_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪೠ")),
        bstack11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪೡ"): bstack11l1lll_opy_
    }
  )
  response = requests.post(bstack1l1l1_opy_, data=bstack11l111l_opy_,
                         headers={bstack11_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧೢ"): bstack11l111l_opy_.content_type}, auth=(bstack1lllll11_opy_(config), bstack1lll111_opy_(config)))
  try:
    res = json.loads(response.text)
    bstack11111l_opy_ = res[bstack11_opy_ (u"ࠩࡤࡴࡵࡥࡵࡳ࡮ࠪೣ")]
    logger.info(bstack1lll1l11l_opy_.format(bstack11111l_opy_))
    bstack1llll111l_opy_(md5_hash, bstack11111l_opy_)
  except ValueError as err:
    bstack11l111ll_opy_(bstack1ll1l1l1_opy_.format(str(err)))
  return bstack11111l_opy_
def bstack1ll11l1_opy_():
  global CONFIG
  global bstack1l1l1l_opy_
  bstack1lllll11l_opy_ = 1
  if bstack11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ೤") in CONFIG:
    bstack1lllll11l_opy_ = CONFIG[bstack11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ೥")]
  bstack1111l111_opy_ = 0
  if bstack11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ೦") in CONFIG:
    bstack1111l111_opy_ = len(CONFIG[bstack11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ೧")])
  bstack1l1l1l_opy_ = int(bstack1lllll11l_opy_) * int(bstack1111l111_opy_)
def bstack1llllll11_opy_(md5_hash):
  bstack1l11l11_opy_ = os.path.join(os.path.expanduser(bstack11_opy_ (u"ࠧࡿࠩ೨")), bstack11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ೩"), bstack11_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪ೪"))
  if os.path.exists(bstack1l11l11_opy_):
    bstack1l1lll11_opy_ = json.load(open(bstack1l11l11_opy_,bstack11_opy_ (u"ࠪࡶࡧ࠭೫")))
    if md5_hash in bstack1l1lll11_opy_:
      bstack1l1111ll_opy_ = bstack1l1lll11_opy_[md5_hash]
      bstack11l1ll1_opy_ = datetime.datetime.now()
      bstack1ll111l_opy_ = datetime.datetime.strptime(bstack1l1111ll_opy_[bstack11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ೬")], bstack11_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ೭"))
      if (bstack11l1ll1_opy_ - bstack1ll111l_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l1111ll_opy_[bstack11_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ೮")]):
        return None
      return bstack1l1111ll_opy_[bstack11_opy_ (u"ࠧࡪࡦࠪ೯")]
  else:
    return None
def bstack1llll111l_opy_(md5_hash, bstack11111l_opy_):
  bstack1lll111ll_opy_ = os.path.join(os.path.expanduser(bstack11_opy_ (u"ࠨࢀࠪ೰")), bstack11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩೱ"))
  if not os.path.exists(bstack1lll111ll_opy_):
    os.makedirs(bstack1lll111ll_opy_)
  bstack1l11l11_opy_ = os.path.join(os.path.expanduser(bstack11_opy_ (u"ࠪࢂࠬೲ")), bstack11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫೳ"), bstack11_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭೴"))
  bstack1ll1l1ll_opy_ = {
    bstack11_opy_ (u"࠭ࡩࡥࠩ೵"): bstack11111l_opy_,
    bstack11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ೶"): datetime.datetime.strftime(datetime.datetime.now(), bstack11_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬ೷")),
    bstack11_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ೸"): str(__version__)
  }
  if os.path.exists(bstack1l11l11_opy_):
    bstack1l1lll11_opy_ = json.load(open(bstack1l11l11_opy_,bstack11_opy_ (u"ࠪࡶࡧ࠭೹")))
  else:
    bstack1l1lll11_opy_ = {}
  bstack1l1lll11_opy_[md5_hash] = bstack1ll1l1ll_opy_
  with open(bstack1l11l11_opy_, bstack11_opy_ (u"ࠦࡼ࠱ࠢ೺")) as outfile:
    json.dump(bstack1l1lll11_opy_, outfile)
def bstack1ll11111_opy_(self):
  return
def bstack1l1ll1_opy_(self):
  return
def bstack1l1l111l_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1111ll_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack111l1ll_opy_
  global bstack111lllll_opy_
  global bstack1l111l1_opy_
  global bstack1lllll1l1_opy_
  global bstack11ll111l_opy_
  global bstack11ll1lll_opy_
  CONFIG[bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ೻")] = str(bstack11ll111l_opy_) + str(__version__)
  command_executor = bstack111l11l1_opy_()
  logger.debug(bstack1lll1ll11_opy_.format(command_executor))
  proxy = bstack11ll11_opy_(CONFIG, proxy)
  bstack11ll1l11_opy_ = 0 if bstack111lllll_opy_ < 0 else bstack111lllll_opy_
  if bstack1lllll1l1_opy_ is True:
    bstack11ll1l11_opy_ = int(threading.current_thread().getName())
  bstack1l111lll_opy_ = bstack1lll1l1_opy_(CONFIG, bstack11ll1l11_opy_)
  logger.debug(bstack1111llll_opy_.format(str(bstack1l111lll_opy_)))
  if bstack11111lll_opy_(CONFIG):
    bstack11l1l11l_opy_(bstack1l111lll_opy_)
  if desired_capabilities:
    bstack1lll11l1l_opy_ = bstack1lll1l1_opy_(bstack1lll11ll1_opy_(desired_capabilities))
    if bstack1lll11l1l_opy_:
      bstack1l111lll_opy_ = update(bstack1lll11l1l_opy_, bstack1l111lll_opy_)
    desired_capabilities = None
  if options:
    bstack11lll1_opy_(options, bstack1l111lll_opy_)
  if not options:
    options = bstack11lll1l1_opy_(bstack1l111lll_opy_)
  if options and bstack11l1lll1_opy_() >= version.parse(bstack11_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ೼")):
    desired_capabilities = None
  if (
      not options and not desired_capabilities
  ) or (
      bstack11l1lll1_opy_() < version.parse(bstack11_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭೽")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l111lll_opy_)
  logger.info(bstack1lll11l11_opy_)
  if bstack11l1lll1_opy_() >= version.parse(bstack11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ೾")):
    bstack11ll1lll_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11l1lll1_opy_() >= version.parse(bstack11_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩ೿")):
    bstack11ll1lll_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack11ll1lll_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  bstack111l1ll_opy_ = self.session_id
  if bstack11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ഀ") in CONFIG and bstack11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩഁ") in CONFIG[bstack11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨം")][bstack11ll1l11_opy_]:
    bstack1l111l1_opy_ = CONFIG[bstack11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩഃ")][bstack11ll1l11_opy_][bstack11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬഄ")]
  logger.debug(bstack111111_opy_.format(bstack111l1ll_opy_))
def bstack1l1l11l_opy_(self, test):
  global CONFIG
  global bstack111l1ll_opy_
  global bstack1ll1l111_opy_
  global bstack1l111l1_opy_
  global bstack11111l11_opy_
  if bstack111l1ll_opy_:
    try:
      data = {}
      bstack1l11ll_opy_ = None
      if test:
        bstack1l11ll_opy_ = str(test.data)
      if bstack1l11ll_opy_ and not bstack1l111l1_opy_:
        data[bstack11_opy_ (u"ࠨࡰࡤࡱࡪ࠭അ")] = bstack1l11ll_opy_
      if bstack1ll1l111_opy_:
        if bstack1ll1l111_opy_.status == bstack11_opy_ (u"ࠩࡓࡅࡘ࡙ࠧആ"):
          data[bstack11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪഇ")] = bstack11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫഈ")
        elif bstack1ll1l111_opy_.status == bstack11_opy_ (u"ࠬࡌࡁࡊࡎࠪഉ"):
          data[bstack11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ഊ")] = bstack11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧഋ")
          if bstack1ll1l111_opy_.message:
            data[bstack11_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨഌ")] = str(bstack1ll1l111_opy_.message)
      user = CONFIG[bstack11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ഍")]
      key = CONFIG[bstack11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭എ")]
      url = bstack11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠰ࡽࢀ࠲࡯ࡹ࡯࡯ࠩഏ").format(user, key, bstack111l1ll_opy_)
      headers = {
        bstack11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫഐ"): bstack11_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ഑"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1lll11ll_opy_.format(str(e)))
  bstack11111l11_opy_(self, test)
def bstack1l1l11l1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1l1l1l1_opy_
  bstack1l1l1l1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1ll1l111_opy_
  bstack1ll1l111_opy_ = self._test
def bstack1lll1l11_opy_(outs_dir, options, tests_root_name, stats, copied_artifacts, outputfile=None):
  from pabot import pabot
  outputfile = outputfile or options.get(bstack11_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺࠢഒ"), bstack11_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴ࠯ࡺࡰࡰࠧഓ"))
  output_path = os.path.abspath(
    os.path.join(options.get(bstack11_opy_ (u"ࠤࡲࡹࡹࡶࡵࡵࡦ࡬ࡶࠧഔ"), bstack11_opy_ (u"ࠥ࠲ࠧക")), outputfile)
  )
  files = sorted(pabot.glob(os.path.join(pabot._glob_escape(outs_dir), bstack11_opy_ (u"ࠦ࠯࠴ࡸ࡮࡮ࠥഖ"))))
  if not files:
    pabot._write(bstack11_opy_ (u"ࠬ࡝ࡁࡓࡐ࠽ࠤࡓࡵࠠࡰࡷࡷࡴࡺࡺࠠࡧ࡫࡯ࡩࡸࠦࡩ࡯ࠢࠥࠩࡸࠨࠧഗ") % outs_dir, pabot.Color.YELLOW)
    return bstack11_opy_ (u"ࠨࠢഘ")
  def invalid_xml_callback():
    global _ABNORMAL_EXIT_HAPPENED
    _ABNORMAL_EXIT_HAPPENED = True
  resu = pabot.merge(
    files, options, tests_root_name, copied_artifacts, invalid_xml_callback
  )
  pabot._update_stats(resu, stats)
  resu.save(output_path)
  return output_path
def bstack1l1lll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  from pabot import pabot
  from robot import __version__ as ROBOT_VERSION
  from robot import rebot
  if bstack11_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦങ") in options:
    del options[bstack11_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧച")]
  if ROBOT_VERSION < bstack11_opy_ (u"ࠤ࠷࠲࠵ࠨഛ"):
    stats = {
      bstack11_opy_ (u"ࠥࡧࡷ࡯ࡴࡪࡥࡤࡰࠧജ"): {bstack11_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࠥഝ"): 0, bstack11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧഞ"): 0, bstack11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨട"): 0},
      bstack11_opy_ (u"ࠢࡢ࡮࡯ࠦഠ"): {bstack11_opy_ (u"ࠣࡶࡲࡸࡦࡲࠢഡ"): 0, bstack11_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤഢ"): 0, bstack11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥണ"): 0},
    }
  else:
    stats = {
      bstack11_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࠥത"): 0,
      bstack11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧഥ"): 0,
      bstack11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨദ"): 0,
      bstack11_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠣധ"): 0,
    }
  if pabot_args[bstack11_opy_ (u"ࠣࡄࡖࡘࡆࡉࡋࡠࡒࡄࡖࡆࡒࡌࡆࡎࡢࡖ࡚ࡔࠢന")]:
    outputs = []
    for index, _ in enumerate(pabot_args[bstack11_opy_ (u"ࠤࡅࡗ࡙ࡇࡃࡌࡡࡓࡅࡗࡇࡌࡍࡇࡏࡣࡗ࡛ࡎࠣഩ")]):
      copied_artifacts = pabot._copy_output_artifacts(
        options, pabot_args[bstack11_opy_ (u"ࠥࡥࡷࡺࡩࡧࡣࡦࡸࡸࠨപ")], pabot_args[bstack11_opy_ (u"ࠦࡦࡸࡴࡪࡨࡤࡧࡹࡹࡩ࡯ࡵࡸࡦ࡫ࡵ࡬ࡥࡧࡵࡷࠧഫ")]
      )
      outputs += [
        bstack1lll1l11_opy_(
          os.path.join(outs_dir, str(index)+ bstack11_opy_ (u"ࠧ࠵ࠢബ")),
          options,
          tests_root_name,
          stats,
          copied_artifacts,
          outputfile=os.path.join(bstack11_opy_ (u"ࠨࡰࡢࡤࡲࡸࡤࡸࡥࡴࡷ࡯ࡸࡸࠨഭ"), bstack11_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺࠥࡴ࠰ࡻࡱࡱࠨമ") % index),
        )
      ]
    if bstack11_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴࠣയ") not in options:
      options[bstack11_opy_ (u"ࠤࡲࡹࡹࡶࡵࡵࠤര")] = bstack11_opy_ (u"ࠥࡳࡺࡺࡰࡶࡶ࠱ࡼࡲࡲࠢറ")
    pabot._write_stats(stats)
    return rebot(*outputs, **pabot._options_for_rebot(options, start_time_string, pabot._now()))
  else:
    return pabot._report_results(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1111l1l_opy_(self, ff_profile_dir):
  global bstack1l1l1l1l_opy_
  if not ff_profile_dir:
    return None
  return bstack1l1l1l1l_opy_(self, ff_profile_dir)
def bstack1lllll1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1llllll1_opy_
  bstack111lll11_opy_ = []
  if bstack11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧല") in CONFIG:
    bstack111lll11_opy_ = CONFIG[bstack11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨള")]
  bstack1l11lll_opy_ = len(suite_group) * len(pabot_args[bstack11_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡧ࡫࡯ࡩࡸࠨഴ")] or [(bstack11_opy_ (u"ࠢࠣവ"), None)]) * len(bstack111lll11_opy_)
  pabot_args[bstack11_opy_ (u"ࠣࡄࡖࡘࡆࡉࡋࡠࡒࡄࡖࡆࡒࡌࡆࡎࡢࡖ࡚ࡔࠢശ")] = []
  for q in range(bstack1l11lll_opy_):
    pabot_args[bstack11_opy_ (u"ࠤࡅࡗ࡙ࡇࡃࡌࡡࡓࡅࡗࡇࡌࡍࡇࡏࡣࡗ࡛ࡎࠣഷ")].append(str(q))
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦസ")],
      pabot_args[bstack11_opy_ (u"ࠦࡻ࡫ࡲࡣࡱࡶࡩࠧഹ")],
      argfile,
      pabot_args.get(bstack11_opy_ (u"ࠧ࡮ࡩࡷࡧࠥഺ")),
      pabot_args[bstack11_opy_ (u"ࠨࡰࡳࡱࡦࡩࡸࡹࡥࡴࠤ഻")],
      platform[0],
      bstack1llllll1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹ഼ࠢ")] or [(bstack11_opy_ (u"ࠣࠤഽ"), None)]
    for platform in enumerate(bstack111lll11_opy_)
  ]
def bstack1ll1l1l_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack11l11ll_opy_=bstack11_opy_ (u"ࠩࠪാ")):
  global bstack11111l1l_opy_
  self.platform_index = platform_index
  self.bstack11l1llll_opy_ = bstack11l11ll_opy_
  bstack11111l1l_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack1llll11_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack11111l1_opy_
  if not bstack11_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬി") in item.options:
    item.options[bstack11_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ീ")] = []
  for v in item.options[bstack11_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧു")]:
    if bstack11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬൂ") in v:
      item.options[bstack11_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩൃ")].remove(v)
  item.options[bstack11_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪൄ")].insert(0, bstack11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫ൅").format(item.platform_index))
  item.options[bstack11_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬെ")].insert(0, bstack11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫേ").format(item.bstack11l1llll_opy_))
  return bstack11111l1_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1l1ll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l11l11l_opy_
  command[0] = command[0].replace(bstack11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫൈ"), bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ൉"), 1)
  return bstack1l11l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack11l11l11_opy_(self, runner, quiet=False, capture=True):
  global bstack1l11l1l1_opy_
  bstack11l11111_opy_ = bstack1l11l1l1_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack11_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸࠧൊ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬോ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack11l11111_opy_
def bstack111ll1_opy_(self, name, context, *args):
  global bstack111lll_opy_
  if name in [bstack11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠪൌ"), bstack11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳ്ࠬ")]:
    bstack111lll_opy_(self, name, context, *args)
  if name == bstack11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠬൎ"):
    try:
      bstack111ll1l1_opy_ = str(self.feature.name)
      context.browser.execute_script(bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ൏") + json.dumps(bstack111ll1l1_opy_) + bstack11_opy_ (u"࠭ࡽࡾࠩ൐"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack11_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ൑").format(str(e)))
  if name == bstack11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ൒"):
    try:
      if not hasattr(self, bstack11_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ൓")):
        self.driver_before_scenario = True
      bstack1l1llll1_opy_ = args[0].name
      bstack1llll1111_opy_ = bstack111ll1l1_opy_ = str(self.feature.name)
      bstack111ll1l1_opy_ = bstack1llll1111_opy_ + bstack11_opy_ (u"ࠪࠤ࠲ࠦࠧൔ") + bstack1l1llll1_opy_
      if self.driver_before_scenario:
        context.browser.execute_script(bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩൕ") + json.dumps(bstack111ll1l1_opy_) + bstack11_opy_ (u"ࠬࢃࡽࠨൖ"))
    except Exception as e:
      logger.debug(bstack11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧൗ").format(str(e)))
  if name == bstack11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ൘"):
    try:
      bstack1lll1lll_opy_ = args[0].status.name
      if str(bstack1lll1lll_opy_).lower() == bstack11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ൙"):
        bstack11l11ll1_opy_ = bstack11_opy_ (u"ࠩࠪ൚")
        bstack1lll111l_opy_ = bstack11_opy_ (u"ࠪࠫ൛")
        bstack111ll11l_opy_ = bstack11_opy_ (u"ࠫࠬ൜")
        try:
          import traceback
          bstack11l11ll1_opy_ = self.exception.__class__.__name__
          bstack1111lll_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1lll111l_opy_ = bstack11_opy_ (u"ࠬࠦࠧ൝").join(bstack1111lll_opy_)
          bstack111ll11l_opy_ = bstack1111lll_opy_[-1]
        except Exception as e:
          logger.debug(bstack1llll1l1_opy_.format(str(e)))
        bstack11l11ll1_opy_ += bstack111ll11l_opy_
        context.browser.execute_script(bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ൞") + json.dumps(str(args[0].name) + bstack11_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨൟ") + str(bstack1lll111l_opy_)) + bstack11_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨൠ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩൡ") + json.dumps(bstack11_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢൢ") + str(bstack11l11ll1_opy_)) + bstack11_opy_ (u"ࠫࢂࢃࠧൣ"))
      else:
        context.browser.execute_script(bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ൤") + json.dumps(str(args[0].name) + bstack11_opy_ (u"ࠨࠠ࠮ࠢࡓࡥࡸࡹࡥࡥࠣࠥ൥")) + bstack11_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭൦"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠤࡳࡥࡸࡹࡥࡥࠤࢀࢁࠬ൧"))
    except Exception as e:
      logger.debug(bstack11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ൨").format(str(e)))
  if name == bstack11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪ൩"):
    try:
      if context.failed is True:
        bstack11llll1_opy_ = []
        bstack1l111ll1_opy_ = []
        bstack11111ll_opy_ = []
        bstack11111ll1_opy_ = bstack11_opy_ (u"ࠫࠬ൪")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack11llll1_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1111lll_opy_ = traceback.format_tb(exc_tb)
            bstack1l11ll1_opy_ = bstack11_opy_ (u"ࠬࠦࠧ൫").join(bstack1111lll_opy_)
            bstack1l111ll1_opy_.append(bstack1l11ll1_opy_)
            bstack11111ll_opy_.append(bstack1111lll_opy_[-1])
        except Exception as e:
          logger.debug(bstack1llll1l1_opy_.format(str(e)))
        bstack11l11ll1_opy_ = bstack11_opy_ (u"࠭ࠧ൬")
        for i in range(len(bstack11llll1_opy_)):
          bstack11l11ll1_opy_ += bstack11llll1_opy_[i] + bstack11111ll_opy_[i] + bstack11_opy_ (u"ࠧ࡝ࡰࠪ൭")
        bstack11111ll1_opy_ = bstack11_opy_ (u"ࠨࠢࠪ൮").join(bstack1l111ll1_opy_)
        if not self.driver_before_scenario:
          context.browser.execute_script(bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ൯") + json.dumps(bstack11111ll1_opy_) + bstack11_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪ൰"))
          context.browser.execute_script(bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ࠲ࠠࠣࡴࡨࡥࡸࡵ࡮ࠣ࠼ࠣࠫ൱") + json.dumps(bstack11_opy_ (u"࡙ࠧ࡯࡮ࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳࡸࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡝ࡰࠥ൲") + str(bstack11l11ll1_opy_)) + bstack11_opy_ (u"࠭ࡽࡾࠩ൳"))
      else:
        if not self.driver_before_scenario:
          context.browser.execute_script(bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ൴") + json.dumps(bstack11_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦ൵") + str(self.feature.name) + bstack11_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦ൶")) + bstack11_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩ൷"))
          context.browser.execute_script(bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧࡶࡡࡴࡵࡨࡨࠧࢃࡽࠨ൸"))
    except Exception as e:
      logger.debug(bstack11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ൹").format(str(e)))
  if name in [bstack11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ൺ"), bstack11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨൻ")]:
    bstack111lll_opy_(self, name, context, *args)
def bstack1ll111l1_opy_(bstack11llll1l_opy_):
  global bstack11ll111l_opy_
  bstack11ll111l_opy_ = bstack11llll1l_opy_
  logger.info(bstack11ll11l_opy_.format(bstack11ll111l_opy_.split(bstack11_opy_ (u"ࠨ࠯ࠪർ"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    bstack1l11l1ll_opy_(e, bstack1ll1111_opy_)
  Service.start = bstack1ll11111_opy_
  Service.stop = bstack1l1ll1_opy_
  webdriver.Remote.__init__ = bstack1111ll_opy_
  WebDriver.close = bstack1l1l111l_opy_
  if (bstack11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨൽ") in str(bstack11llll1l_opy_).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
      from pabot.pabot import QueueItem
      from pabot import pabot
    except Exception as e:
      bstack1l11l1ll_opy_(e, bstack111ll111_opy_)
    Output.end_test = bstack1l1l11l_opy_
    TestStatus.__init__ = bstack1l1l11l1_opy_
    WebDriverCreator._get_ff_profile = bstack1111l1l_opy_
    QueueItem.__init__ = bstack1ll1l1l_opy_
    pabot._create_items = bstack1lllll1_opy_
    pabot._run = bstack1l1ll1ll_opy_
    pabot._create_command_for_execution = bstack1llll11_opy_
    pabot._report_results = bstack1l1lll1_opy_
  if bstack11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪൾ") in str(bstack11llll1l_opy_).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l11l1ll_opy_(e, bstack1llll11l1_opy_)
    Runner.run_hook = bstack111ll1_opy_
    Step.run = bstack11l11l11_opy_
def bstack11l1l1ll_opy_():
  global CONFIG
  if bstack11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫൿ") in CONFIG and int(CONFIG[bstack11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ඀")]) > 1:
    logger.warn(bstack11ll1l1_opy_)
def bstack1l11lll1_opy_(bstack11l1l111_opy_, index):
  bstack1ll111l1_opy_(bstack1l111_opy_)
  exec(open(bstack11l1l111_opy_).read())
def bstack1ll1llll_opy_(arg):
  global CONFIG
  bstack1ll111l1_opy_(bstack11lll_opy_)
  os.environ[bstack11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧඁ")] = CONFIG[bstack11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩං")]
  os.environ[bstack11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫඃ")] = CONFIG[bstack11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ඄")]
  from _pytest.config import main as bstack1llll1lll_opy_
  bstack1llll1lll_opy_(arg)
def bstack11llll_opy_(arg):
  bstack1ll111l1_opy_(bstack111l1_opy_)
  from behave.__main__ import main as bstack111111ll_opy_
  bstack111111ll_opy_(arg)
def bstack111l1lll_opy_():
  logger.info(bstack1lll11lll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩඅ"), help=bstack11_opy_ (u"ࠫࡌ࡫࡮ࡦࡴࡤࡸࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡩ࡯࡯ࡨ࡬࡫ࠬආ"))
  parser.add_argument(bstack11_opy_ (u"ࠬ࠳ࡵࠨඇ"), bstack11_opy_ (u"࠭࠭࠮ࡷࡶࡩࡷࡴࡡ࡮ࡧࠪඈ"), help=bstack11_opy_ (u"࡚ࠧࡱࡸࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡺࡹࡥࡳࡰࡤࡱࡪ࠭ඉ"))
  parser.add_argument(bstack11_opy_ (u"ࠨ࠯࡮ࠫඊ"), bstack11_opy_ (u"ࠩ࠰࠱ࡰ࡫ࡹࠨඋ"), help=bstack11_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠫඌ"))
  parser.add_argument(bstack11_opy_ (u"ࠫ࠲࡬ࠧඍ"), bstack11_opy_ (u"ࠬ࠳࠭ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪඎ"), help=bstack11_opy_ (u"࡙࠭ࡰࡷࡵࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬඏ"))
  bstack11l1l11_opy_ = parser.parse_args()
  try:
    bstack11lll11l_opy_ = bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡧࡦࡰࡨࡶ࡮ࡩ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫඐ")
    if bstack11l1l11_opy_.framework and bstack11l1l11_opy_.framework not in (bstack11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨඑ"), bstack11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪඒ")):
      bstack11lll11l_opy_ = bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩඓ")
    bstack11l111l1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11lll11l_opy_)
    bstack111l11ll_opy_ = open(bstack11l111l1_opy_, bstack11_opy_ (u"ࠫࡷ࠭ඔ"))
    bstack111ll11_opy_ = bstack111l11ll_opy_.read()
    bstack111l11ll_opy_.close()
    if bstack11l1l11_opy_.username:
      bstack111ll11_opy_ = bstack111ll11_opy_.replace(bstack11_opy_ (u"ࠬ࡟ࡏࡖࡔࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬඕ"), bstack11l1l11_opy_.username)
    if bstack11l1l11_opy_.key:
      bstack111ll11_opy_ = bstack111ll11_opy_.replace(bstack11_opy_ (u"࡙࠭ࡐࡗࡕࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨඖ"), bstack11l1l11_opy_.key)
    if bstack11l1l11_opy_.framework:
      bstack111ll11_opy_ = bstack111ll11_opy_.replace(bstack11_opy_ (u"࡚ࠧࡑࡘࡖࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ඗"), bstack11l1l11_opy_.framework)
    file_name = bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫ඘")
    file_path = os.path.abspath(file_name)
    bstack1l11ll11_opy_ = open(file_path, bstack11_opy_ (u"ࠩࡺࠫ඙"))
    bstack1l11ll11_opy_.write(bstack111ll11_opy_)
    bstack1l11ll11_opy_.close()
    logger.info(bstack111l1111_opy_)
  except Exception as e:
    logger.error(bstack1l111111_opy_.format(str(e)))
def bstack1l1l1l11_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  bstack1lllll1l_opy_()
  logger.debug(bstack1l1l1lll_opy_.format(str(CONFIG)))
  bstack1ll1ll11_opy_()
  atexit.register(bstack11l11l1_opy_)
  signal.signal(signal.SIGINT, bstack11ll1ll1_opy_)
  signal.signal(signal.SIGTERM, bstack11ll1ll1_opy_)
def bstack1111111l_opy_(bstack1l1l1ll1_opy_, size):
  bstack1llllllll_opy_ = []
  while len(bstack1l1l1ll1_opy_) > size:
    bstack111l1l_opy_ = bstack1l1l1ll1_opy_[:size]
    bstack1llllllll_opy_.append(bstack111l1l_opy_)
    bstack1l1l1ll1_opy_   = bstack1l1l1ll1_opy_[size:]
  bstack1llllllll_opy_.append(bstack1l1l1ll1_opy_)
  return bstack1llllllll_opy_
def run_on_browserstack():
  if len(sys.argv) <= 1:
    logger.critical(bstack1lll1llll_opy_)
    return
  if sys.argv[1] == bstack11_opy_ (u"ࠪ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭ක")  or sys.argv[1] == bstack11_opy_ (u"ࠫ࠲ࡼࠧඛ"):
    logger.info(bstack11_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡕࡿࡴࡩࡱࡱࠤࡘࡊࡋࠡࡸࡾࢁࠬග").format(__version__))
    return
  if sys.argv[1] == bstack11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬඝ"):
    bstack111l1lll_opy_()
    return
  args = sys.argv
  bstack1l1l1l11_opy_()
  global CONFIG
  global bstack1l1l1l_opy_
  global bstack1lllll1l1_opy_
  global bstack111lllll_opy_
  global bstack1llllll1_opy_
  bstack11lll1l_opy_ = bstack11_opy_ (u"ࠧࠨඞ")
  if args[1] == bstack11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨඟ") or args[1] == bstack11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪච"):
    bstack11lll1l_opy_ = bstack11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪඡ")
    args = args[2:]
  elif args[1] == bstack11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪජ"):
    bstack11lll1l_opy_ = bstack11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫඣ")
    args = args[2:]
  elif args[1] == bstack11_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬඤ"):
    bstack11lll1l_opy_ = bstack11_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ඥ")
    args = args[2:]
  elif args[1] == bstack11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩඦ"):
    bstack11lll1l_opy_ = bstack11_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪට")
    args = args[2:]
  elif args[1] == bstack11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪඨ"):
    bstack11lll1l_opy_ = bstack11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫඩ")
    args = args[2:]
  elif args[1] == bstack11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬඪ"):
    bstack11lll1l_opy_ = bstack11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ණ")
    args = args[2:]
  else:
    if not bstack11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪඬ") in CONFIG or str(CONFIG[bstack11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫත")]).lower() in [bstack11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩථ"), bstack11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫද")]:
      bstack11lll1l_opy_ = bstack11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫධ")
      args = args[1:]
    elif str(CONFIG[bstack11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨන")]).lower() == bstack11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ඲"):
      bstack11lll1l_opy_ = bstack11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ඳ")
      args = args[1:]
    elif str(CONFIG[bstack11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫප")]).lower() == bstack11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨඵ"):
      bstack11lll1l_opy_ = bstack11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩබ")
      args = args[1:]
    elif str(CONFIG[bstack11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧභ")]).lower() == bstack11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬම"):
      bstack11lll1l_opy_ = bstack11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ඹ")
      args = args[1:]
    elif str(CONFIG[bstack11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪය")]).lower() == bstack11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨර"):
      bstack11lll1l_opy_ = bstack11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ඼")
      args = args[1:]
    else:
      bstack11l111ll_opy_(bstack1111l1ll_opy_)
  global bstack11ll1lll_opy_
  global bstack11111l11_opy_
  global bstack1l1l1l1_opy_
  global bstack1l1l1l1l_opy_
  global bstack1l11l11l_opy_
  global bstack11111l1l_opy_
  global bstack11111l1_opy_
  global bstack11l11lll_opy_
  global bstack111lll_opy_
  global bstack1l11l1l1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    bstack1l11l1ll_opy_(e, bstack1ll1111_opy_)
  bstack11ll1lll_opy_ = webdriver.Remote.__init__
  bstack11l11lll_opy_ = WebDriver.close
  if (bstack11lll1l_opy_ in [bstack11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩල"), bstack11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ඾"), bstack11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭඿")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
      from pabot.pabot import QueueItem
      from pabot import pabot
    except Exception as e:
      bstack1l11l1ll_opy_(e, bstack111ll111_opy_)
    bstack11111l11_opy_ = Output.end_test
    bstack1l1l1l1_opy_ = TestStatus.__init__
    bstack1l1l1l1l_opy_ = WebDriverCreator._get_ff_profile
    bstack1l11l11l_opy_ = pabot._run
    bstack11111l1l_opy_ = QueueItem.__init__
    bstack11111l1_opy_ = pabot._create_command_for_execution
  if bstack11lll1l_opy_ == bstack11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ව"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l11l1ll_opy_(e, bstack1llll11l1_opy_)
    bstack111lll_opy_ = Runner.run_hook
    bstack1l11l1l1_opy_ = Step.run
  if bstack11lll1l_opy_ == bstack11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧශ"):
    bstack1111l11_opy_()
    bstack11l1l1ll_opy_()
    if bstack11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫෂ") in CONFIG:
      bstack1lllll1l1_opy_ = True
      bstack1l1ll11l_opy_ = []
      for index, platform in enumerate(CONFIG[bstack11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬස")]):
        bstack1l1ll11l_opy_.append(threading.Thread(name=str(index),
                                      target=bstack1l11lll1_opy_, args=(args[0], index)))
      for t in bstack1l1ll11l_opy_:
        t.start()
      for t in bstack1l1ll11l_opy_:
        t.join()
    else:
      bstack1ll111l1_opy_(bstack1l111_opy_)
      exec(open(args[0]).read())
  elif bstack11lll1l_opy_ == bstack11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩහ") or bstack11lll1l_opy_ == bstack11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪළ"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l11l1ll_opy_(e, bstack111ll111_opy_)
    bstack1111l11_opy_()
    bstack1ll111l1_opy_(bstack11ll_opy_)
    if bstack11_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪෆ") in args:
      i = args.index(bstack11_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ෇"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1l1l1l_opy_))
    args.insert(0, str(bstack11_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ෈")))
    pabot.main(args)
  elif bstack11lll1l_opy_ == bstack11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ෉"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l11l1ll_opy_(e, bstack111ll111_opy_)
    for a in args:
      if bstack11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨ්") in a:
        bstack111lllll_opy_ = int(a.split(bstack11_opy_ (u"ࠪ࠾ࠬ෋"))[1])
      if bstack11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ෌") in a:
        bstack1llllll1_opy_ = str(a.split(bstack11_opy_ (u"ࠬࡀࠧ෍"))[1])
    bstack1ll111l1_opy_(bstack11ll_opy_)
    run_cli(args)
  elif bstack11lll1l_opy_ == bstack11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭෎"):
    try:
      from _pytest.config import _prepareconfig
      import importlib
      bstack1lllllll1_opy_ = importlib.find_loader(bstack11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩා"))
      if bstack1lllllll1_opy_ is None:
        bstack1l11l1ll_opy_(e, bstack1lll11l_opy_)
    except Exception as e:
      bstack1l11l1ll_opy_(e, bstack1lll11l_opy_)
    bstack1111l11_opy_()
    try:
      if bstack11_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪැ") in args:
        i = args.index(bstack11_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫෑ"))
        args.pop(i+1)
        args.pop(i)
      if bstack11_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫි") in args:
        i = args.index(bstack11_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬී"))
        args.pop(i+1)
        args.pop(i)
      if bstack11_opy_ (u"ࠬ࠳࡮ࠨු") in args:
        i = args.index(bstack11_opy_ (u"࠭࠭࡯ࠩ෕"))
        args.pop(i+1)
        args.pop(i)
    except Exception as exc:
      logger.error(str(exc))
    config = _prepareconfig(args)
    bstack111l1l1_opy_ = config.args
    bstack11l1l1_opy_ = config.invocation_params.args
    bstack11l1l1_opy_ = list(bstack11l1l1_opy_)
    bstack1l1111l1_opy_ = []
    for arg in bstack11l1l1_opy_:
      if arg not in bstack111l1l1_opy_:
        bstack1l1111l1_opy_.append(arg)
    bstack1l1111l1_opy_.append(bstack11_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩූ"))
    bstack1l1111l1_opy_.append(bstack11_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠧ෗"))
    bstack11ll1l1l_opy_ = []
    for spec in bstack111l1l1_opy_:
      bstack1l1l1ll_opy_ = []
      bstack1l1l1ll_opy_.append(spec)
      bstack1l1l1ll_opy_ += bstack1l1111l1_opy_
      bstack11ll1l1l_opy_.append(bstack1l1l1ll_opy_)
    bstack1lllll1l1_opy_ = True
    bstack1lll11_opy_ = 1
    if bstack11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩෘ") in CONFIG:
      bstack1lll11_opy_ = CONFIG[bstack11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪෙ")]
    bstack11l1l1l1_opy_ = int(bstack1lll11_opy_)*int(len(CONFIG[bstack11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧේ")]))
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨෛ")]):
      for bstack1l1l1ll_opy_ in bstack11ll1l1l_opy_:
        item = {}
        item[bstack11_opy_ (u"࠭ࡡࡳࡩࠪො")] = bstack1l1l1ll_opy_
        item[bstack11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ෝ")] = index
        execution_items.append(item)
    bstack11l11l1l_opy_ = bstack1111111l_opy_(execution_items, bstack11l1l1l1_opy_)
    for execution_item in bstack11l11l1l_opy_:
      bstack1l1ll11l_opy_ = []
      for item in execution_item:
        bstack1l1ll11l_opy_.append(threading.Thread(name=str(item[bstack11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧෞ")]),
                                            target=bstack1ll1llll_opy_,
                                            args=(item[bstack11_opy_ (u"ࠩࡤࡶ࡬࠭ෟ")],)))
      for t in bstack1l1ll11l_opy_:
        t.start()
      for t in bstack1l1ll11l_opy_:
        t.join()
  elif bstack11lll1l_opy_ == bstack11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ෠"):
    try:
      from behave.__main__ import main as bstack111111ll_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l11l1ll_opy_(e, bstack1llll11l1_opy_)
    bstack1111l11_opy_()
    bstack1lllll1l1_opy_ = True
    bstack1lll11_opy_ = 1
    if bstack11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ෡") in CONFIG:
      bstack1lll11_opy_ = CONFIG[bstack11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ෢")]
    bstack11l1l1l1_opy_ = int(bstack1lll11_opy_)*int(len(CONFIG[bstack11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ෣")]))
    config = Configuration(args)
    bstack111l1l1_opy_ = config.paths
    bstack11llllll_opy_ = []
    for arg in args:
      if arg not in bstack111l1l1_opy_:
        bstack11llllll_opy_.append(arg)
    bstack11ll1l1l_opy_ = []
    for spec in bstack111l1l1_opy_:
      bstack1l1l1ll_opy_ = []
      bstack1l1l1ll_opy_ += bstack11llllll_opy_
      bstack1l1l1ll_opy_.append(spec)
      bstack11ll1l1l_opy_.append(bstack1l1l1ll_opy_)
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ෤")]):
      for bstack1l1l1ll_opy_ in bstack11ll1l1l_opy_:
        item = {}
        item[bstack11_opy_ (u"ࠨࡣࡵ࡫ࠬ෥")] = bstack11_opy_ (u"ࠩࠣࠫ෦").join(bstack1l1l1ll_opy_)
        item[bstack11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ෧")] = index
        execution_items.append(item)
    bstack11l11l1l_opy_ = bstack1111111l_opy_(execution_items, bstack11l1l1l1_opy_)
    for execution_item in bstack11l11l1l_opy_:
      bstack1l1ll11l_opy_ = []
      for item in execution_item:
        bstack1l1ll11l_opy_.append(threading.Thread(name=str(item[bstack11_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ෨")]),
                                            target=bstack11llll_opy_,
                                            args=(item[bstack11_opy_ (u"ࠬࡧࡲࡨࠩ෩")],)))
      for t in bstack1l1ll11l_opy_:
        t.start()
      for t in bstack1l1ll11l_opy_:
        t.join()
  else:
    bstack11l111ll_opy_(bstack1111l1ll_opy_)