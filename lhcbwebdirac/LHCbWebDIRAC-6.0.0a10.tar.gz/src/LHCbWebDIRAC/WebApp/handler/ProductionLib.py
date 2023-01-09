###############################################################################
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import re
import json

from DIRAC import S_ERROR


class PrTpl:
    """Production Template engine
    AZ: I know it is not the best :)
    It undestand: {{<sep><ParName>[#<Label>[#<DefaultValue>]]}}
    Where:
      <sep> - not alpha character to be inserted
              before parameter value in case it
              is not empty
      <ParName> - parameter name (must begin
              with alpha character) to substitute
      <Label> - if '#' is found after '{{', everything after
              it till '#' or '}}' is the Label for the parameter
              (default to ParName) In case you use one parameter
              several times, you can specify the label only once.
      <DefaultValue> - the value in the disalog by default
              (empty string if not specified)
    """

    __par_re = r"\{\{(\W)?(.+?)(|(#.*?))\}\}"
    __par_i_re = r"#([^\#]*)#?(.*)"
    __par_sub = r"\{\{(\W|)?%s(|(#.*?))\}\}"

    def __init__(self, tpl_xml):
        self.tpl = tpl_xml
        self.pdict = {}
        self.ddict = {}
        for x in re.findall(self.__par_re, self.tpl):
            rest = re.findall(self.__par_i_re, x[3])
            if rest:
                rest = rest[0]
            else:
                rest = ("", "")
            if not x[1] in self.ddict or rest[1]:
                self.ddict[x[1]] = rest[1]
            if x[1] in self.pdict and not rest[0]:
                continue
            label = rest[0]
            if not label:
                label = x[1]
            self.pdict[x[1]] = label

    def getParams(self):
        """Return the dictionary with parameters (value is label)"""
        return self.pdict

    def getDefaults(self):
        """Return the dictionary with parameters defaults"""
        return self.ddict

    def apply(self, pdict):
        """Return template with substituted values from pdict"""
        result = self.tpl
        for p in self.pdict:
            value = str(pdict.get(p, ""))
            if value:
                value = "\\g<1>" + value
            result = re.sub(self.__par_sub % p, value, result)
        return result


def SelectAndSort(request, rows, default_sort):
    """Can be used to return extJS adopted list of rows"""
    total = len(rows)
    if total == 0:
        return {"OK": True, "result": [], "total": 0}
    try:
        start = int(request.arguments.get("start", 0)[-1])

        if start != 0:
            start = int(json.loads(request.arguments.get("start")[-1]))

        limit = int(request.arguments.get("limit", total)[-1])
        if limit != total:
            limit = int(json.loads(request.arguments.get("limit", total)[-1]))

        sortList = request.arguments.get("sort", default_sort)[-1]
        dir = "ASC"
        if sortList != default_sort:
            sortList = json.loads(request.arguments.get("sort", default_sort)[-1])
            dir = sortList[0]["direction"]
            sort = sortList[0]["property"]

        if sort not in rows[0]:
            raise Exception("Sort field " + sort + " is not found")
    except Exception as e:
        return S_ERROR("Badly formatted list request: " + str(e))

    rows.sort(key=lambda x: x[sort], reverse=(dir != "ASC"))
    return {"OK": True, "result": rows[start : start + limit], "total": total}
