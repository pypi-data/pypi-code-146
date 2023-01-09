# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Union
from xsdata.models.datatype import XmlDate, XmlDateTime, XmlPeriod
from tgclients.databinding.rdf import Rdf
from tgclients.databinding.textgrid_metadata_agent_2010 import (
    AgentType,
    PersonType,
)
from tgclients.databinding.textgrid_metadata_script_2010 import FormOfNotationType

__NAMESPACE__ = "http://textgrid.info/namespaces/metadata/core/2010"


@dataclass
class AuthorityType:
    """
    references to authority files like thesauri etc.
    """
    class Meta:
        name = "authorityType"

    id: List["AuthorityType.Id"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            "required": True,
        }
    )

    @dataclass
    class Id:
        """
        Attributes
            value:
            type: The type of the ID in a non-textgrid context
        """
        value: str = field(
            default="",
            metadata={
                "required": True,
            }
        )
        type: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )


@dataclass
class DateType:
    """
    same function as our old sub-schema.
    """
    class Meta:
        name = "dateType"

    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )
    date: Optional[Union[XmlDate, XmlPeriod]] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    not_before: Optional[Union[XmlDate, XmlPeriod]] = field(
        default=None,
        metadata={
            "name": "notBefore",
            "type": "Attribute",
        }
    )
    not_after: Optional[Union[XmlDate, XmlPeriod]] = field(
        default=None,
        metadata={
            "name": "notAfter",
            "type": "Attribute",
        }
    )


class GeneratedTypeAvailability(Enum):
    """
    possible values.
    """
    DEFAULT = "default"
    PUBLIC = "public"
    STABLE = "stable"


@dataclass
class IdentifierType:
    """An unambiguous reference to the resource within a given context.

    Same
    as: http://purl.org/dc/terms/identifier

    Attributes
        value:
        type: The type of the URI in a non-TextGrid context (e.g., a
            ISBN or ISSN, a shelfmark, a registration or inventary
            number)
    """
    class Meta:
        name = "identifierType"

    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class PidPidType(Enum):
    HANDLE = "handle"
    URN = "urn"
    DOI = "doi"
    ARK = "ark"
    PURL = "purl"
    OTHER = "other"


class WorkTypeGenre(Enum):
    """The genre of the work. Same as:

    http://purl.org/dc/terms/type - Hier natürlich englische Bezeichnungen,
    wenn wir mal die Liste finalisiert haben. Siehe
    http://www.textgrid.de/intern/wiki1/wiki/Genres.html
    """
    DRAMA = "drama"
    PROSE = "prose"
    VERSE = "verse"
    REFERENCE_WORK = "reference work"
    NON_FICTION = "non-fiction"
    NON_TEXT = "non-text"
    OTHER = "other"


@dataclass
class BibliographicCitationType:
    """
    Attributes
        author: A person or organization chiefly responsible for the
            intellectual or artistic content of the source, usually
            printed text. Same as:
            http://id.loc.gov/vocabulary/relators/aut.html. For a
            detailed description of the author the "agent" element in
            the "workType" has to be used.
        editor: A person or organization who prepares for publication a
            work not primarily his/her own, such as by elucidating text,
            adding introductory or other critical matter, or technically
            directing an editorial staff. Same as:
            http://id.loc.gov/vocabulary/relators/edt.htmln
        edition_title: Name of the source (e.g., the titel of a book or
            a journal).
        place_of_publication: Place where the source was published.
        publisher: A person or organization that makes the source
            available to the public. Same as:
            http://id.loc.gov/vocabulary/relators/pbl.html
        date_of_publication: TG dateType.
        edition_no: Statement of the edition of the source - usually a
            phrase with or without numbers (e.g., first edition, 4th
            ed., etc.)
        series: Titel of a series in which the source was issued.
        volume: Volume designation - is usually expressed as a number
            but could be roman numerals or non-numeric (e.g., 124, VI,
            etc.)
        issue: Designation of the issue of a journal the source was
            published. While usually numeric, it could be non-numeric
            (e.g. Spring)
        spage: Designates the page the source starts in a volume or
            issue. Pages are not always numeric.
        epage: Designates the page the source ends in a volume or issue.
            Page are not always numeric.
        bib_identifier:
    """
    class Meta:
        name = "bibliographicCitationType"

    author: List[PersonType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    editor: List[PersonType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    edition_title: List[str] = field(
        default_factory=list,
        metadata={
            "name": "editionTitle",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            "min_occurs": 1,
        }
    )
    place_of_publication: List[AuthorityType] = field(
        default_factory=list,
        metadata={
            "name": "placeOfPublication",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    publisher: List[PersonType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    date_of_publication: Optional[DateType] = field(
        default=None,
        metadata={
            "name": "dateOfPublication",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    edition_no: Optional[str] = field(
        default=None,
        metadata={
            "name": "editionNo",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    series: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    volume: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    issue: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    spage: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    epage: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    bib_identifier: Optional[IdentifierType] = field(
        default=None,
        metadata={
            "name": "bibIdentifier",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )


@dataclass
class CollectionType:
    """
    TODO.

    Attributes
        collector: Person or corporate body creating a collection. Same
            as: http://id.loc.gov/vocabulary/relators/col.html
        abstract: A summary of the collection. Same as:
            http://purl.org/dc/terms/abstract
        collection_description: URL of a description of this collection
            (e.g., project description on the website of a funding
            agency) FIXME is this still the Same as:
            http://purl.org/dc/terms/description
        spatial: Spatial characteristics of the collection. Same as:
            http://purl.org/dc/terms/spatial
        temporal: Temporal characteristics of the collection. Same as:
            http://purl.org/dc/terms/temporal
        subject: The topic of the collection. Same as:
            http://purl.org/dc/terms/subject.
    """
    class Meta:
        name = "collectionType"

    collector: List[PersonType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            "min_occurs": 1,
        }
    )
    abstract: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    collection_description: List[str] = field(
        default_factory=list,
        metadata={
            "name": "collectionDescription",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    spatial: List[AuthorityType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    temporal: List[AuthorityType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    subject: List[AuthorityType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )


@dataclass
class GeneratedType:
    """The generatedType is cerated by the middleware (TG-crud), and is
    delivered with every T-crud call, that delivers back the metadata
    ObjectType.

    With every #UPDATE or #UPDATEMETADATA call this generatedType must
    also be sent in the request parameter's objectType, to be able to
    handle concurrent modification of TextGrid objects.

    Attributes
        created: Date of creation of the resource. Same as:
            http://purl.org/dc/terms/created. TODO Datentyp
            spezifizieren
        last_modified: Date on which the resource was changed. Same as:
            http://purl.org/dc/terms/modified. TODO Datentyp
            spezifizieren
        issued: Date of formal issuance (e.g., publication) of the
            resource. Same as: http://purl.org/dc/terms/issued. TODO
            Datentyp (oder xs:date?) spezifizieren
        textgrid_uri: Subproperty of identifier. An unambiguous
            reference to the resource within the textgrid context.
            Subproperty of identifier:
            http://purl.org/dc/elements/1.1/identifier. Hier in jedem
            Falle die TextGrid-URI (NOID). FIXME für die Fälle (1)
            veröffentlicht (PID – oder kommt der in
            ../provided/identifier?), (2) externe Datenquelle (oder auch
            der nicht hier?) noch weitere Identifier hier? Sonst
            Kardinalität auf 1..1 setzen.
        revision: revision number
        pid: persistent identifier
        extent: The size of the resource in bytes. Same as:
            http://purl.org/dc/terms/extent.
        fixity: "Information used to verify whether an object has been
            altered in an undocumented or unauthorized way." - stolen
            from the PREMIS Object Entity sub-schema, see
            http://www.loc.gov/standards/premis/v1/Object-v1-1.xsd. For
            detailed documentation see the PREMIS Data Dictionary
            (http://www.loc.gov/standards/premis/v2/premis-dd-2-0.pdf)
            section 1.5.2
        data_contributor: Use for a person that submits data in
            textgrid. Same as:
            http://lcweb2.loc.gov/diglib/loc.terms/relators/DTC.
        project: Project name and id.
        warning: Error report provided by the middleware when an
            incorrect textgrid object has been stored.
        permissions: Same as accessRights ("Information about who can
            access the resource or an indication of its security status"
            http://purl.org/dc/terms/accessRights) in textgrid? In
            TextGrid, this is dependent on the role of the person that
            accesses the resource.
        availability: information whether the TG object is subject of
            the (role based) rights management or isPublic or isStable
        any_element: Reserved for future additions
    """
    class Meta:
        name = "generatedType"

    created: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            "required": True,
        }
    )
    last_modified: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "lastModified",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            "required": True,
        }
    )
    issued: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    textgrid_uri: Optional["GeneratedType.TextgridUri"] = field(
        default=None,
        metadata={
            "name": "textgridUri",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            "required": True,
        }
    )
    revision: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            "required": True,
        }
    )
    pid: List["GeneratedType.Pid"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    extent: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            "required": True,
        }
    )
    fixity: List["GeneratedType.Fixity"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    data_contributor: Optional[str] = field(
        default=None,
        metadata={
            "name": "dataContributor",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            "required": True,
        }
    )
    project: Optional["GeneratedType.Project"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            "required": True,
        }
    )
    warning: List["GeneratedType.Warning"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    permissions: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    availability: Optional[GeneratedTypeAvailability] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            "required": True,
        }
    )
    any_element: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        }
    )

    @dataclass
    class TextgridUri:
        """
        Attributes
            value:
            ext_ref: The TG metadata refer to an external object
        """
        value: str = field(
            default="",
            metadata={
                "required": True,
            }
        )
        ext_ref: Optional[str] = field(
            default=None,
            metadata={
                "name": "extRef",
                "type": "Attribute",
            }
        )

    @dataclass
    class Pid:
        """
        Attributes
            value:
            pid_type: PID type
        """
        value: str = field(
            default="",
            metadata={
                "required": True,
            }
        )
        pid_type: PidPidType = field(
            default=PidPidType.HANDLE,
            metadata={
                "name": "pidType",
                "type": "Attribute",
            }
        )

    @dataclass
    class Fixity:
        """
        Attributes
            message_digest_algorithm: The specific algorithm used to
                construct the message digest for the digital object,
                e.g. MD5, SHA-1..n etc.
            message_digest: The output of the message digest algorithm,
                i.e. the checksum
            message_digest_originator: The agent that created the
                original message digest that is compared in a fixity
                check. In TextGrid: "TG-crud" or Service-endpoint?
        """
        message_digest_algorithm: Optional[str] = field(
            default=None,
            metadata={
                "name": "messageDigestAlgorithm",
                "type": "Element",
                "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
                "required": True,
            }
        )
        message_digest: Optional[str] = field(
            default=None,
            metadata={
                "name": "messageDigest",
                "type": "Element",
                "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
                "required": True,
            }
        )
        message_digest_originator: Optional[str] = field(
            default=None,
            metadata={
                "name": "messageDigestOriginator",
                "type": "Element",
                "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            }
        )

    @dataclass
    class Project:
        value: str = field(
            default="",
            metadata={
                "required": True,
            }
        )
        id: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )

    @dataclass
    class Warning:
        """
        Attributes
            value:
            uri: The URI the warning occured.
        """
        value: str = field(
            default="",
            metadata={
                "required": True,
            }
        )
        uri: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )


@dataclass
class ItemType:
    """
    Attributes
        rights_holder: Person or organization with copyright for an
            item. Same as: http://purl.org/dc/terms/rightsHolder FIXME
            dcterms-Problem wieder: Damit ist möglicherweise auch die
            Entscheidung, als Datentyp für die diversen Personenfelder
            wie rightsHolder etc. dcterms:irgendwas zu nehmen,
            hinfällig, da damit wohl keine Möglichkeit zur Spezifikation
            einer ID zusätzlich zum Inhaltsstring (Namen) gegeben ist.
    """
    class Meta:
        name = "itemType"

    rights_holder: List[PersonType] = field(
        default_factory=list,
        metadata={
            "name": "rightsHolder",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )


@dataclass
class ObjectCitationType:
    """
    Attributes
        object_title: Name of the source (e.g., the name of a painting,
            sculpture, furniture, etc. ).
        object_contributor: A person or organization responsible for the
            intellectual or artistic content of a work. Same as:
            http://purl.org/dc/terms/contributor.
        object_date: Date of an event in the lifecycle of the resource.
            Same as: http://purl.org/dc/terms/date. For a detailed
            description of the date of creation the "dateOfCreation" and
            "timeOfCreation" elements in the "workType" have to be used.
        object_identifier:
    """
    class Meta:
        name = "objectCitationType"

    object_title: List[str] = field(
        default_factory=list,
        metadata={
            "name": "objectTitle",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            "min_occurs": 1,
        }
    )
    object_contributor: List[AgentType] = field(
        default_factory=list,
        metadata={
            "name": "objectContributor",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    object_date: Optional[DateType] = field(
        default=None,
        metadata={
            "name": "objectDate",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    object_identifier: Optional[IdentifierType] = field(
        default=None,
        metadata={
            "name": "objectIdentifier",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )


@dataclass
class ProvidedType:
    """
    Attributes
        title: A name given to the resource. Same as:
            http://purl.org/dc/terms/title; FIXME Uniform-Title
            allerdings ist 1..1 :-(
        identifier:
        format: File format of a textgrid object. Same as:
            http://purl.org/dc/terms/format. TODO Specification of type.
        notes: Anything that doesn't fit into the other fields.
    """
    class Meta:
        name = "providedType"

    title: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            "min_occurs": 1,
        }
    )
    identifier: List[IdentifierType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    format: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            "required": True,
        }
    )
    notes: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )


@dataclass
class RelationType:
    """
    Attributes
        is_derived_from: Link to an object the described textgrid object
            is derived from.
        is_alternative_format_of: Link to an object having the same
            content as the described textgrid object but in another
            format.
        has_adaptor: Link to an object which is an adaptor of the
            described textgrid object.
        has_schema: Link to an object which is a schema of the described
            textgrid object.
        rdf:
    """
    class Meta:
        name = "relationType"

    is_derived_from: Optional[str] = field(
        default=None,
        metadata={
            "name": "isDerivedFrom",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    is_alternative_format_of: Optional[str] = field(
        default=None,
        metadata={
            "name": "isAlternativeFormatOf",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    has_adaptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "hasAdaptor",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    has_schema: Optional[str] = field(
        default=None,
        metadata={
            "name": "hasSchema",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    rdf: Optional[Rdf] = field(
        default=None,
        metadata={
            "name": "RDF",
            "type": "Element",
            "namespace": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        }
    )


@dataclass
class WorkType:
    """
    FIXME Grobklassifikation.

    Attributes
        agent:
        abstract: A summary of the work. Same as:
            http://purl.org/dc/terms/abstract
        date_of_creation: unser (TextGrid) Datumsmodell FIXME: "created"
            gibts schon in generated
        spatial: Spatial characteristics of the work. Same as:
            http://purl.org/dc/terms/spatial
        temporal: Temporal characteristics of the work. Same as:
            http://purl.org/dc/terms/temporal
        subject: The topic of the work. Same as:
            http://purl.org/dc/terms/subject.
        genre: Grobklassifikation
        type: The nature or genre of the work. Same as:
            http://purl.org/dc/terms/type FIXME Feinklassifikation,
            editierbare Auswahlliste
    """
    class Meta:
        name = "workType"

    agent: List[AgentType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    abstract: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    date_of_creation: Optional[DateType] = field(
        default=None,
        metadata={
            "name": "dateOfCreation",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            "required": True,
        }
    )
    spatial: List[AuthorityType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    temporal: List[AuthorityType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    subject: List[AuthorityType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    genre: List[WorkTypeGenre] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            "min_occurs": 1,
        }
    )
    type: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )


@dataclass
class GenericType:
    """
    Attributes
        provided: Metadata provided by the client.
        generated: Metadata generated by the middleware components.
    """
    class Meta:
        name = "genericType"

    provided: Optional[ProvidedType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            "required": True,
        }
    )
    generated: Optional[GeneratedType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )


@dataclass
class SourceType:
    """Relation between the textgrid object and the description of the source
    of this object.

    Same as: http://purl.org/dc/terms/source
    """
    class Meta:
        name = "sourceType"

    bibliographic_citation: Optional[BibliographicCitationType] = field(
        default=None,
        metadata={
            "name": "bibliographicCitation",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    object_citation: Optional[ObjectCitationType] = field(
        default=None,
        metadata={
            "name": "objectCitation",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )


@dataclass
class EditionType:
    """
    Attributes
        is_edition_of: Manifestation of which work? Value must be the
            TextGrid URI of a TextGrid Work object. Field is mandatory
            on publication. Same as:
            http://rdvocab.info/RDARelationshipsWEMI/manifestationOfWork
        agent:
        source:
        form_of_notation:
        language:
        license: A legal document giving official permission to do
            something with the resource. Same as:
            http://purl.org/dc/terms/license.
    """
    class Meta:
        name = "editionType"

    is_edition_of: Optional[str] = field(
        default=None,
        metadata={
            "name": "isEditionOf",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    agent: List[AgentType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            "min_occurs": 1,
        }
    )
    source: List[SourceType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    form_of_notation: List[FormOfNotationType] = field(
        default_factory=list,
        metadata={
            "name": "formOfNotation",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )
    language: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            "pattern": r"[a-z][a-z][a-z]",
        }
    )
    license: Optional["EditionType.License"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
        }
    )

    @dataclass
    class License:
        """
        Attributes
            value:
            license_uri: The context in which a license originates.
                Recommendation is to use Creative Commons (see:
                http://creativecommons.org/licenses/)
        """
        value: str = field(
            default="",
            metadata={
                "required": True,
            }
        )
        license_uri: Optional[str] = field(
            default=None,
            metadata={
                "name": "licenseUri",
                "type": "Attribute",
            }
        )


@dataclass
class Object:
    """
    The root element should also be used in CRUD arguments and returned by TG-
    search whenever TG-search returns complete metadata records.

    Attributes
        generic: Metadata available in all kinds of TextGrid objects.
        item: Item specific metadata.
        edition: Metadata specific for editions. - An embodiment of a
            work. Broader than:
            http://rdvocab.info/uri/schema/FRBRentitiesRDA/Manifestation
        work: Metadata specific for works. - A distinct intellectual or
            artistic creation. Broader than:
            http://rdvocab.info/uri/schema/FRBRentitiesRDA/Work
        collection: FIXME - je nach Sammlungs-Konzept und dessen
            Umsetzung - public-Bereich
        custom: The custom field may contain any additional metadata
            records for specific projects or specific applications.
        relations: FIXME wir haben ein paar spezifische Relationen,
            wollen aber auch beliebige Beziehungen durch die Anwender
            erlauben. Die Optionen hier sind vermutlich: (a) wir
            erlauben beliebiges RDF/XML und werten bestimmte
            bestandteile aus. (b) wir erlauben "unsere" relationen +
            beliebiges RDF/XML, also eine Substruktur
    """
    class Meta:
        name = "object"
        namespace = "http://textgrid.info/namespaces/metadata/core/2010"

    generic: Optional[GenericType] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    item: Optional[ItemType] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    edition: Optional[EditionType] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    work: Optional[WorkType] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    collection: Optional[CollectionType] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    custom: Optional["Object.Custom"] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    relations: Optional[RelationType] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )

    @dataclass
    class Custom:
        other_element: List[object] = field(
            default_factory=list,
            metadata={
                "type": "Wildcard",
                "namespace": "##other",
            }
        )


@dataclass
class MetadataContainerType:
    """
    Container type that contains exactly one metadata record, complete with
    it's root element (tns:object)
    """
    class Meta:
        name = "metadataContainerType"

    object_value: Optional[Object] = field(
        default=None,
        metadata={
            "name": "object",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            "required": True,
        }
    )


@dataclass
class TgObjectMetadata(MetadataContainerType):
    """
    Element for the container type.
    """
    class Meta:
        name = "tgObjectMetadata"
        namespace = "http://textgrid.info/namespaces/metadata/core/2010"
