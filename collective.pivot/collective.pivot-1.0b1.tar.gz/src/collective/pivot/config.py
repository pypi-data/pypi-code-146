# -*- coding: utf-8 -*-


def getFamilyProperties():
    """
    Don't store query identifier (OTH-xxx) in Family.family field
    """
    return {
        "hosting": {"urn": "urn:fam:1", "query": "OTH-A0-003P-2PWS"},
        "leisure": {"urn": "urn:fam:2", "query": "OTH-A0-003P-2QH4"},
        "tourism_organizations": {"urn": "urn:fam:3", "query": "OTH-A0-003P-2QHT"},
        "events": {"urn": "urn:fam:5", "query": "OTH-A0-003P-2QL2"},
        "terroir": {"urn": "urn:fam:6", "query": "OTH-A0-003P-2QHH"},
    }


def getQueryCodeByUrn(urn):
    dic = getFamilyProperties()
    result = [props["query"] for name, props in dic.items() if props["urn"] == urn]
    return result[0]
