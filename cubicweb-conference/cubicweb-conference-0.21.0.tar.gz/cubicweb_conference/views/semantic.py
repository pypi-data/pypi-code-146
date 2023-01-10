from rdflib import Literal, BNode, URIRef
from cubicweb.entities.adapters import EntityRDFAdapter
from cubicweb.predicates import is_instance


class SwcConferenceView(EntityRDFAdapter):
    __select__ = is_instance("Conference")

    def triples(self):
        RDFS = self._use_namespace("rdfs")
        DC = self._use_namespace("dc")
        RDF = self._use_namespace("rdf")

        SWC = self._use_namespace("swc", "http://data.semanticweb.org/ns/swc/ontology#")
        SWRC = self._use_namespace("swrc", "http://swrc.ontoware.org/ontology#")
        ICAL = self._use_namespace("ical", "http://www.w3.org/2002/12/cal/ical#")

        entity = self.entity.complete()
        entity.complete()

        yield (self.uri, RDF.type, SWC.ConferenceEvent)
        yield (self.uri, DC.title, Literal(entity.dc_title()))
        yield (self.uri, RDFS.label, Literal(entity.dc_title()))
        yield (self.uri, SWC.hasAcronym, Literal(entity.url_id))

        event = BNode()
        yield (self.uri, ICAL.dtstart, event)
        yield (event, ICAL.date, Literal(entity.start_on))

        event = BNode()
        yield (self.uri, ICAL.dtend, event)
        yield (event, ICAL.date, Literal(entity.end_on))
        yield (self.uri, ICAL.url, URIRef(entity.absolute_url))

        tracks = self._cw.execute(
            "Any T WHERE T is Track, T in_conf C, C eid %(x)s", {"x": entity.eid}
        ).entities()
        for track in tracks:
            yield (self.uri, SWRC.isSuperEventOf, URIRef(track.absolute_url()))


class SwcTrackView(EntityRDFAdapter):
    __select__ = is_instance("Track")

    def triples(self):
        DC = self._use_namespace("dc")
        RDF = self._use_namespace("rdf")

        SWC = self._use_namespace("swc", "http://data.semanticweb.org/ns/swc/ontology#")
        SWRC = self._use_namespace("swrc", "http://swrc.ontoware.org/ontology#")

        entity = self.entity.complete()
        entity.complete()

        yield (self.uri, RDF.type, SWC.TrackEvent)
        yield (self.uri, DC.title, Literal(entity.dc_title()))

        for conf in entity.in_conf:
            yield (self.uri, SWC.isPartOf, URIRef(conf.absolute_url()))

        for track in entity.reverse_in_track:
            yield (self.uri, SWRC.isSuperEventOf, URIRef(track.absolute_url()))


class SwcTalkView(EntityRDFAdapter):
    __select__ = is_instance("Talk")

    def triples(self):
        DC = self._use_namespace("dc")
        RDF = self._use_namespace("rdf")

        SWC = self._use_namespace("swc", "http://data.semanticweb.org/ns/swc/ontology#")
        SWRC = self._use_namespace("swrc", "http://swrc.ontoware.org/ontology#")

        entity = self.entity.complete()
        entity.complete()

        yield (self.uri, RDF.type, SWC.TalkEvent)

        for conf in entity.in_conf:
            yield (self.uri, SWC.isPartOf, URIRef(conf.absolute_url()))

        for track in entity.in_track:
            yield (self.uri, SWC.isPartOf, URIRef(track.absolute_url()))

        yield (self.uri, DC.title, Literal(entity.dc_title()))
        yield (self.uri, SWRC.abstract, Literal(entity.description))

        for author in entity.reverse_leads:
            yield (self.uri, SWRC.author, URIRef(author.absolute_url()))

        for doc in entity.has_attachments:
            yield (self.uri, SWC.hasRelatedDocument, URIRef(doc.absolute_url()))
