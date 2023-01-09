# -*- coding: utf-8 -*-
from collective.pivot.browser.controlpanel import IPivotSettings
from collective.pivot.config import getQueryCodeByUrn
from plone.registry.interfaces import IRegistry
from plone.rest import Service
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import Interface

import json
import logging
import requests

logger = logging.getLogger("Plone")


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class PivotEndpoint(object):

    language = "fr"

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        results = self.getResult()
        return self.treatResult(results)

    def getResult(self):
        headers = {"Accept": "application/json", "ws_key": self.settings.ws_key}
        result = requests.get(self.query_url, headers=headers)
        return result.json()

    def getTypeOffre(self, offre):
        type_offre = offre.get("typeOffre")
        type_offre_id = offre.get("typeOffre").get("idTypeOffre")
        gen = (
            label
            for label in type_offre.get("label")
            if label.get("lang") == self.language
        )
        label = next(gen).get("value")
        return {"offerTypeId": type_offre_id, "offerTypeLabel": label}

    def getLocality(self, offre):
        gen = (
            locality
            for locality in offre.get("adresse1").get("localite")
            if locality.get("lang") == self.language
        )
        locality = next(gen, None)
        locality = locality.get("value") if locality is not None else locality
        return locality

    def getSpecValueByUrn(self, offre, urn):
        spec = offre.get("spec")
        gen = (s for s in spec if s.get("urn") == urn)
        spec_value = next(gen, None)
        spec_value = spec_value.get("value") if spec_value is not None else spec_value
        return spec_value

    def treatResult(self, results):
        formated_datas = []
        for offre in results.get("offre"):
            try:
                if offre.get("spec") is not None:
                    phone1 = self.getSpecValueByUrn(offre, "urn:fld:phone1")
                    email1 = self.getSpecValueByUrn(offre, "urn:fld:mail1")
                sheet = {
                    u"title": offre.get("nom"),
                    u"latitude": offre.get("adresse1").get("latitude"),
                    u"longitude": offre.get("adresse1").get("longitude"),
                    u"cp": offre.get("adresse1").get("cp"),
                    u"locality": self.getLocality(offre),
                    u"offer": {
                        u"offerID": offre.get("codeCgt"),
                        u"offerTypeId": self.getTypeOffre(offre).get("offerTypeId"),
                        u"offerTypeLabel": self.getTypeOffre(offre).get(
                            "offerTypeLabel"
                        ),
                    },
                    u"phone": phone1,
                    u"email": email1,
                }
            except Exception as e:
                logger.exception(e)
            formated_datas.append(sheet)
        total_datas = len(formated_datas)
        self.request.response.setHeader("Content-Type", "application/json")
        return {u"items": formated_datas, u"items_total": total_datas}

    @property
    def settings(self):
        registry = getUtility(IRegistry)
        return registry.forInterface(IPivotSettings)

    @property
    def query_url(self):
        cp = "cp:{}".format("|".join(self.zip_codes))
        return "{}query/{};content=4;pretty=true;fmt=json;param={}".format(
            self.ws_url, getQueryCodeByUrn(self.context.family), cp
        )

    @property
    def ws_url(self):
        return self.settings.ws_url

    @property
    def zip_codes(self):
        if self.context.zip_codes is not None:
            return self.context.zip_codes
        else:
            return self.settings.zip_codes

    @property
    def ws_key(self):
        return self.settings.ws_key

    @property
    def test_config(self):
        if self.zip_codes is None:
            return False
        if self.ws_url is None:
            return False
        if self.ws_key is None:
            return False
        return True


class PivotEndpointGet(Service):
    def render(self):
        related_items = PivotEndpoint(self.context, self.request)
        return json.dumps(
            related_items(),
            indent=2,
            sort_keys=True,
            separators=(", ", ": "),
        )
