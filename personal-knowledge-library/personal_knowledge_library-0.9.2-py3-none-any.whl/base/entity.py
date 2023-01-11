# -*- coding: utf-8 -*-
# Copyright © 2021 Wacom. All rights reserved.
import abc
import enum
from datetime import datetime
from typing import List, Dict, Any, NewType, Optional

import dateutil.parser

#  ---------------------------------------- Type definitions -----------------------------------------------------------
LanguageCode = NewType("LanguageCode", str)
LocaleCode = NewType("LocaleCode", str)
ReferenceId = NewType("ReferenceId", str)


#  ---------------------------------------- Exceptions -----------------------------------------------------------------
class ServiceException(Exception):
    """Service exception."""
    pass


class KnowledgeException(Exception):
    """Knowledge exception."""
    pass


#  ---------------------------------------- Constants ------------------------------------------------------------------
VND_WACOM_INK_MODEL: str = 'application/vnd.wacom-knowledge.model'
RDF_SYNTAX_NS_TYPE: str = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'
RDF_SCHEMA_COMMENT: str = 'http://www.w3.org/2000/01/rdf-schema#comment'
RDF_SCHEMA_LABEL: str = 'http://www.w3.org/2000/01/rdf-schema#label'
ALIAS_TAG: str = 'alias'
DATA_PROPERTY_TAG: str = 'literal'
VALUE_TAG: str = 'value'
LANGUAGE_TAG: str = 'lang'
LOCALE_TAG: str = 'locale'
DATA_PROPERTIES_TAG: str = 'literals'
SEND_TO_NEL_TAG: str = 'sendToNEL'
SOURCE_REFERENCE_ID_TAG: str = 'source_reference_id'
SOURCE_SYSTEM_TAG: str = 'source_system'
OBJECT_PROPERTIES_TAG: str = 'relations'
OWNER_TAG: str = 'owner'
OWNER_ID_TAG: str = 'ownerId'
GROUP_IDS: str = 'groupIds'
LOCALIZED_CONTENT_TAG: str = 'LocalizedContent'
STATUS_FLAG_TAG: str = 'status'
CONTENT_TAG: str = 'value'
URI_TAG: str = 'uri'
URIS_TAG: str = 'uris'
ERRORS_TAG: str = 'errors'
TEXT_TAG: str = 'text'
TYPE_TAG: str = 'type'
IMAGE_TAG: str = 'image'
DESCRIPTION_TAG: str = 'description'
COMMENT_TAG: str = 'text'
COMMENTS_TAG: str = 'comments'
DESCRIPTIONS_TAG: str = 'descriptions'
USE_NEL_TAG: str = 'use_for_nel'
VISIBILITY_TAG: str = 'visibility'
RELATIONS_TAG: str = 'relations'
LABELS_TAG: str = 'labels'
IS_MAIN_TAG: str = 'isMain'
DATA_TYPE_TAG: str = 'dataType'
RELATION_TAG: str = 'relation'
OUTGOING_TAG: str = 'out'
INCOMING_TAG: str = 'in'
TENANT_RIGHTS_TAG: str = 'tenantRights'
INFLECTION_CONCEPT_CLASS: str = 'concept'
INFLECTION_SETTING: str = 'inflection'
INFLECTION_CASE_SENSITIVE: str = 'caseSensitive'


class EntityStatus(enum.Enum):
    """
    Entity Status
    -------------
    Status of the entity synchronization (client and knowledge graph).
    """
    UNKNOWN = 0
    """Unknown status."""
    CREATED = 1
    """Entity has been created and not yet update."""
    UPDATED = 2
    """Entity has been updated by the client and must be synced."""
    SYNCED = 3
    """State of entity is in sync with knowledge graph."""


class LocalizedContent(abc.ABC):
    """
    Localized content
    -----------------
    Content that is multi-lingual.

    Parameters
    ----------
    content: str
        Content value
    language_code: LanguageCode (default:= 'en_US')
        ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>, e.g., en_US.
    """

    def __init__(self, content: str, language_code: LanguageCode = 'en_US'):
        self.__content: str = content
        self.__language_code: LanguageCode = language_code

    @property
    def content(self) -> str:
        """String representation of the content."""
        return self.__content

    @content.setter
    def content(self, value: str):
        self.__content = value

    @property
    def language_code(self) -> LanguageCode:
        """Language code of the content."""
        return self.__language_code

    def __repr__(self):
        return f'{self.content}@{self.language_code}'


class Label(LocalizedContent):
    """
    Label
    -----
    Label that is multi-lingual.

    Parameters
    ----------
    content: str
        Content value
    language_code: LanguageCode (default:= 'en_US')
        Language code of content
    main: bool (default:=False)
        Main content
    """

    def __init__(self, content: str, language_code: LanguageCode = 'en_US', main: bool = False):
        self.__main: bool = main
        super().__init__(content, language_code)

    @property
    def main(self) -> bool:
        """Flag if the content is the  main content or an alias."""
        return self.__main

    @staticmethod
    def create_from_dict(dict_label: Dict[str, Any], tag_name: str = CONTENT_TAG, locale_name: str = LOCALE_TAG) \
            -> 'Label':
        if tag_name not in dict_label:
            raise ValueError("Dict is does not contain a localized label.")
        if locale_name not in dict_label:
            raise ValueError("Dict is does not contain a language code")
        if IS_MAIN_TAG in dict_label:
            return Label(dict_label[tag_name], dict_label[locale_name], dict_label[IS_MAIN_TAG])
        else:
            return Label(dict_label[tag_name], dict_label[locale_name])

    @staticmethod
    def create_from_list(param: List[dict]) -> List[LOCALIZED_CONTENT_TAG]:
        return [Label.create_from_dict(p) for p in param]

    def __dict__(self):
        return {
            CONTENT_TAG: self.content,
            LOCALE_TAG: self.language_code,
            IS_MAIN_TAG: self.main
        }


class OntologyLabel(LocalizedContent):
    """
    Ontology Label
    --------------
    Label that is multi-lingual.

    Parameters
    ----------
    content: str
        Content value
    language_code: LanguageCode (default:= 'en')
        Language code of content
    main: bool (default:=False)
        Main content
    """

    def __init__(self, content: str, language_code: LanguageCode = 'en', main: bool = False):
        self.__main: bool = main
        super().__init__(content, language_code)

    @property
    def main(self) -> bool:
        """Flag if the content is the  main content or an alias."""
        return self.__main

    @staticmethod
    def create_from_dict(dict_label: Dict[str, Any], tag_name: str = CONTENT_TAG, locale_name: str = LOCALE_TAG) \
            -> 'OntologyLabel':
        if tag_name not in dict_label:
            raise ValueError("Dict is does not contain a localized label.")
        if locale_name not in dict_label:
            raise ValueError("Dict is does not contain a language code")
        if IS_MAIN_TAG in dict_label:
            return OntologyLabel(dict_label[tag_name], dict_label[locale_name], dict_label[IS_MAIN_TAG])
        else:
            return OntologyLabel(dict_label[tag_name], dict_label[locale_name])

    @staticmethod
    def create_from_list(param: List[dict]) -> List[LOCALIZED_CONTENT_TAG]:
        return [Label.create_from_dict(p) for p in param]

    def __dict__(self):
        return {
            CONTENT_TAG: self.content,
            LOCALE_TAG: self.language_code,
            IS_MAIN_TAG: self.main
        }


class Description(LocalizedContent):
    """
    Description
    -----------
    Description that is multi-lingual.

    Parameters
    ----------
    description: str
        Description value
    language_code: LanguageCode (default:= 'en_US')
        Language code of content
    """

    def __init__(self, description: str, language_code: LanguageCode = 'en_US'):
        super().__init__(description, language_code)

    @staticmethod
    def create_from_dict(dict_description: Dict[str, Any]) -> 'Description':
        if DESCRIPTION_TAG not in dict_description or LOCALE_TAG not in dict_description:
            raise ValueError("Dict is does not contain a localized label.")
        return Description(dict_description[DESCRIPTION_TAG], dict_description[LOCALE_TAG])

    @staticmethod
    def create_from_list(param: List[Dict[str, Any]]) -> List['Description']:
        return [Description.create_from_dict(p) for p in param]

    def __dict__(self):
        return {
            DESCRIPTION_TAG: self.content,
            LOCALE_TAG: self.language_code,
        }


class Comment(LocalizedContent):
    """
    Comment
    -------
    Comment that is multi-lingual.

    Parameters
    ----------
    text: str
        Text value
    language_code: LanguageCode (default:= 'en')
        Language code of content
    """

    def __init__(self, text: str, language_code: LanguageCode = 'en'):
        super().__init__(text, language_code)

    @staticmethod
    def create_from_dict(dict_description: Dict[str, Any]) -> 'Comment':
        if VALUE_TAG not in dict_description or LANGUAGE_TAG not in dict_description:
            raise ValueError("Dict is does not contain a localized comment.")
        return Comment(dict_description[VALUE_TAG], dict_description[LANGUAGE_TAG])

    @staticmethod
    def create_from_list(param: List[Dict[str, Any]]) -> List['Comment']:
        return [Comment.create_from_dict(p) for p in param]

    def __dict__(self):
        return {
            COMMENT_TAG: self.content,
            LOCALE_TAG: self.language_code,
        }


class OntologyObject(abc.ABC):
    """
    Generic ontology object
    -----------------------

    Parameters
    ----------
    tenant_id: str
        Reference id for tenant
    iri: str
        IRI of the ontology object
    icon: str
        Icon assigned to object, visually representing it
    labels: List[Label]
        List of multi-language_code labels
    comments: List[Label]
        List of multi-language_code comments
    context: str
        Context
    """

    def __init__(self, tenant_id: str, iri: str, icon: str, labels: List[OntologyLabel],
                 comments: List[Comment], context: str):
        self.__tenant_id: str = tenant_id
        self.__labels: List[OntologyLabel] = labels
        self.__comments: List[Comment] = comments
        self.__iri: str = iri
        self.__icon: str = icon
        self.__context: str = context

    @property
    def tenant_id(self) -> str:
        """Tenant id."""
        return self.__tenant_id

    @property
    def iri(self) -> str:
        """IRI """
        return self.__iri

    @property
    def context(self) -> str:
        """Context."""
        return self.__context

    @property
    def icon(self) -> str:
        """Icon."""
        return self.__icon

    @icon.setter
    def icon(self, value: str):
        self.__icon = value

    @property
    def labels(self) -> List[OntologyLabel]:
        return self.__labels

    def label_for_lang(self, language_code: LanguageCode) -> Optional[OntologyLabel]:
        for label in self.labels:
            if label.language_code == language_code:
                return label
        return None

    @property
    def comments(self) -> List[Comment]:
        """Comment related to ontology object."""
        return self.__comments

    def comment_for_lang(self, language_code: LanguageCode) -> Optional[Comment]:
        for comment in self.comments:
            if comment.language_code == language_code:
                return comment
        return None


class OntologyContextSettings(object):
    """
    OntologyContextSettings
    -----------------------
    Describes the settings of the context, such as:
    - prefixes for RDF, RDFS and OWL
    - Base literal URI
    - Base class URI
    - Description literal name
    - depth
    """

    def __init__(self, rdf_prefix: str, rdfs_prefix: str, owl_prefix: str, base_literal_uri: str, base_class_uri: str,
                 description_literal_name: str, depth: int):
        self.__rdf_prefix: str = rdf_prefix
        self.__rdfs_prefix: str = rdfs_prefix
        self.__owl_prefix: str = owl_prefix
        self.__base_literal_uri: str = base_literal_uri
        self.__base_class_uri: str = base_class_uri
        self.__description_literal_name: str = description_literal_name
        self.__depth: int = depth

    @property
    def rdf_prefix(self):
        """RDF prefix"""
        return self.__rdf_prefix

    @property
    def rdfs_prefix(self):
        """RDFS prefix"""
        return self.__rdfs_prefix

    @property
    def owl_prefix(self):
        """OWL prefix"""
        return self.__owl_prefix

    @property
    def base_literal_uri(self):
        """Base literal URI."""
        return self.__base_literal_uri

    @property
    def base_class_uri(self):
        """Base class URI."""
        return self.__base_class_uri

    @property
    def description_literal_name(self) -> str:
        """Literal name of the description."""
        return self.__description_literal_name

    @property
    def depth(self) -> int:
        """Depth."""
        return self.__depth


class OntologyContext(OntologyObject):
    """
    OntologyContext
    ----------------
    Ontology context representation.

    Parameters
    ----------
    cid: str
        Context id
    tenant_id: str
        Tenant id.
    name: str
        Name of the ontology context
    icon: str
        Icon or Base64 encoded
    labels: List[Label]
        List of labels
    comments: List[Comment]
        List of comments
    context: str
        context name
    base_uri: str
        Base URI
    concepts: List[str]
        List of classes / concepts
    properties: List[str]
        List of properties (data and object properties)
    """

    def __init__(self, cid: str, tenant_id: str, name: str, icon: str, labels: List[Label],
                 comments: List[Comment], date_added: datetime, date_modified: datetime, context: str, base_uri: str,
                 version: int, orphaned: bool, concepts: List[str], properties: List[str]):
        self.__id = cid
        self.__base_uri: str = base_uri
        self.__version: int = version
        self.__date_added: datetime = date_added
        self.__date_modified: datetime = date_modified
        self.__orphaned: bool = orphaned
        self.__concepts: List[str] = concepts
        self.__properties: List[str] = properties
        super().__init__(tenant_id, name, icon, labels, comments, context)

    @property
    def id(self) -> str:
        return self.__id

    @property
    def base_uri(self) -> str:
        return self.__base_uri

    @property
    def orphaned(self) -> bool:
        return self.__orphaned

    @classmethod
    def from_dict(cls, context_dict: Dict[str, Any]):
        context_data: Dict[str, Any] = context_dict['context']
        labels: List[Label] = [] if context_data['labels'] is None else \
            [Label(content=la[VALUE_TAG], language_code=la[LANGUAGE_TAG]) for la in context_data['labels']]
        comments: List[Comment] = [] if context_data['comments'] is None else \
            [Comment(text=la[VALUE_TAG], language_code=la[LANGUAGE_TAG]) for la in context_data['comments']]
        added: datetime = dateutil.parser.isoparse(context_data['dateAdded'])
        modified: datetime = dateutil.parser.isoparse(context_data['dateModified'])
        return OntologyContext(context_data['id'], context_data['tenantId'], context_data['name'],
                               context_data['icon'], labels, comments, added, modified,
                               context_data['context'], context_data['baseURI'],
                               context_dict['version'], context_data['orphaned'],
                               context_dict.get('concepts'), context_dict.get('properties'))

    def __repr__(self):
        return f'<OntologyContext> - [id:={self.id}, iri:={self.iri}]'
