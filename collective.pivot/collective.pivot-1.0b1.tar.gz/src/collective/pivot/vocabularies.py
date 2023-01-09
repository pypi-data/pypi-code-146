# -*- coding: utf-8 -*-
from collective.pivot import _
from collective.pivot.config import getFamilyProperties
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class FamilyVocabularyFactory:
    def __call__(self, context):
        family = [
            (getFamilyProperties().get("hosting").get("urn"), _("Hosting")),
            (getFamilyProperties().get("leisure").get("urn"), _("Leisure / discovery")),
            (
                getFamilyProperties().get("tourism_organizations").get("urn"),
                _("Tourism organizations"),
            ),
            (getFamilyProperties().get("events").get("urn"), _("Events")),
            (getFamilyProperties().get("terroir").get("urn"), _("Terroir")),
        ]
        terms = [
            SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in family
        ]
        return SimpleVocabulary(terms)


family_vocabulary_factory = FamilyVocabularyFactory()
