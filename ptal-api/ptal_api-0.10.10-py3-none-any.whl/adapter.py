from copy import copy
from dataclasses import dataclass
from functools import wraps
from time import time
from typing import Optional, List, Any, Iterable, Dict, Sequence
import logging

from .core.values.value_mapping import get_map_helper
from .tdm_builder.tdm_builder import AbstractTdmBuilder
from .providers.gql_providers import AbstractGQLClient
from .schema.api_schema import Query, Mutation, StoryPagination, ConceptLinkPagination, ConceptFactPagination, \
    ConceptPropertyPagination, SortDirection, ConceptSorting, DocumentSorting, DocumentGrouping, TimestampInterval
from .schema.api_schema import \
    ValueInput, IntValueInput, StringValueInput, DateTimeValue, StringLocaleValue, StringValue, LinkValue, \
    DoubleValue, IntValue, ConceptPropertyFilterSettings, ConceptLinkFilterSettings, ExtraSettings, Story, Document,\
    DocumentFilterSettings, Concept, ConceptLink, ConceptPagination, ConceptFilterSettings, PropertyFilterSettings, \
    StringFilter, ConceptType, ConceptTypeFilterSettings, ConceptTypePagination, ConceptPropertyType, \
    ConceptPropertyTypePagination, ConceptPropertyTypeFilterSettings, ConceptLinkType, ConceptLinkTypePagination, \
    ConceptLinkTypeFilterSettings, ConceptPropertyValueType, ConceptPropertyValueTypePagination, \
    ConceptPropertyValueTypeFilterSettings, ConceptPropertyValueTypeUpdateInput, ConceptProperty, \
    ConceptMutationInput, ConceptUpdateInput, ConceptPropertyUpdateInput, ConceptPropertyCreateInput, \
    ConceptLinkPropertyInput, ConceptLinkCreationMutationInput, ComponentValueInput, CompositeConcept, \
    CompositeConceptWidgetRowPagination, DocumentLinkFilterSetting, ConceptFact
from .schema.crawlers_api_schema import Query as CrQuery
from .schema.crawlers_api_schema import Crawler, CrawlerPagination
from .schema import utils_api_schema as uas
from sgqlc.operation import Operation, Fragment


@dataclass
class KBIteratorConfig:
    max_total_count: int
    earliest_created_time: int


logger = logging.getLogger(__name__)


def check_utils_gql_client(f):
    @wraps(f)
    def wrapper(self: 'TalismanAPIAdapter', *args, **kwargs):
        if self._utils_gql_client is None:
            raise Exception('Utils methods cannot be used because the corresponding gql_client is not specified.')
        return f(self, *args, **kwargs)

    return wrapper


class TalismanAPIAdapter:
    def __init__(
        self, gql_client: Optional[AbstractGQLClient], types: Dict, tdm_builder: AbstractTdmBuilder = None,
        utils_gql_client: Optional[AbstractGQLClient] = None, kb_iterator_config: KBIteratorConfig = None
    ) -> None:
        self._gql_client = gql_client
        self._utils_gql_client = utils_gql_client
        self._types = types
        self._cache = {}

        self.document_fields_truncated = ('id', 'external_url')
        self.document_fields = (
            'id', 'title', 'external_url', 'publication_author', 'publication_date', 'internal_url', 'markers'
        )

        self.document_text_fields_truncated = ('text',)
        self.document_text_fields = ('node_id', 'text')
        self.document_text_metadata_fields = ('paragraph_type',)

        self.concept_fields = (
            'id', 'name', 'notes', 'metric', 'markers', 'system_registration_date', 'system_update_date'
        )
        self.concept_type_fields = ('id', 'name')

        self.concept_property_fields = ('is_main', 'id', 'system_registration_date')
        self.concept_property_type_fields_truncated = ('id',)
        self.concept_property_type_fields = ('id', 'name')
        self.cpvt_fields_truncated = ('id', 'name', 'value_type')
        self.cpvt_fields = ('id', 'name', 'value_type', 'value_restriction', 'pretrained_nercmodels')

        self.concept_link_fields = ('id', 'notes')
        self.concept_link_concept_from_fields = ('id',)
        self.concept_link_concept_to_fields = ('id',)
        self.concept_link_type_fields = ('id', 'name', 'is_directed', 'is_hierarchical')
        self.concept_link_type_fields_truncated = ('id', 'name', 'is_directed')

        self.concept_fact_fields = ('id',)
        self.concept_fact_document_fields = (
            'id', 'title', 'publication_author', 'publication_date', 'external_url',
            'markers', 'notes', 'access_level', 'trust_level'
        )
        self.concept_fact_document_platform_fields = ('id',)
        self.concept_fact_document_account_fields = ('id',)

        self.composite_concept_widget_type = ('id', 'name')
        self.composite_concept_widget_type_columns_info = ('name',)

        self.date_time_value_date_fields = ('year', 'month', 'day')
        self.date_time_value_time_fields = ('hour', 'minute', 'second')

        self.tdm_builder = tdm_builder

        if kb_iterator_config:
            self.kb_iterator_config = kb_iterator_config
        else:
            self.kb_iterator_config = KBIteratorConfig(1000, 1609448400)  # Fri Jan 01 2021 00:00:00 GMT+0300

    def get_tdm_builder(self) -> AbstractTdmBuilder:
        return self.tdm_builder

    def _configure_property_value_type_fields(self, graphql_value, truncated: bool = True):
        conpvt_frag: Fragment = Fragment(ConceptPropertyValueType, 'ConceptPropertyValueType')
        for f in self.cpvt_fields_truncated if truncated else self.cpvt_fields:
            conpvt_frag.__getattr__(f)()

        # TODO: add composite types
        # compvt_frag = Fragment(CompositePropertyValueTemplate, 'CompositePropertyValueTemplate')
        # compvt_frag.__fields__('id', 'name')
        # compvt_frag.component_value_types()

        graphql_value.__fragment__(conpvt_frag)

    def _configure_output_value_fields(self, graphql_value):
        dtv_frag = Fragment(DateTimeValue, 'DateTimeFull')
        dtv_frag.date().__fields__(*self.date_time_value_date_fields)
        dtv_frag.time().__fields__(*self.date_time_value_time_fields)

        # dtiv_frag = Fragment(DateTimeIntervalValue, 'DateTimeIntervalFull')
        # dtiv_frag.start.__fragment__(dtv_frag)
        # dtiv_frag.end.__fragment__(dtv_frag)

        slv_frag = Fragment(StringLocaleValue, 'StringLocaleFull')
        slv_frag.value()
        slv_frag.locale()

        sv_frag = Fragment(StringValue, 'StringFull')
        sv_frag.value()

        lv_frag = Fragment(LinkValue, 'LinkFull')
        lv_frag.link()

        dv_frag = Fragment(DoubleValue, 'DoubleFull')
        dv_frag.value(__alias__='double')

        iv_frag = Fragment(IntValue, 'IntFull')
        iv_frag.value(__alias__='number')

        graphql_value.__fragment__(slv_frag)
        graphql_value.__fragment__(sv_frag)
        graphql_value.__fragment__(lv_frag)
        graphql_value.__fragment__(dv_frag)
        graphql_value.__fragment__(iv_frag)
        graphql_value.__fragment__(dtv_frag)
        # graphql_value.__fragment__(dtiv_frag)

    def _configure_output_concept_fields(
        self, concept_object, with_aliases=False, with_properties=False, with_links=False,
        with_link_properties=False
    ):

        concept_object.__fields__(*self.concept_fields)
        concept_object.concept_type.__fields__(*self.concept_type_fields)
        if with_aliases:
            sv_frag = Fragment(StringValue, 'StringFull')
            sv_frag.value()
            concept_object.list_alias.value.__fragment__(sv_frag)
        if with_properties:
            pcp: ConceptPropertyPagination = concept_object.pagination_concept_property(
                offset=0,
                limit=10000,
                filter_settings=ConceptPropertyFilterSettings()
            )
            lcp = pcp.list_concept_property()
            lcp.__fields__(*self.concept_property_fields)
            lcp.property_type().__fields__(*self.concept_property_type_fields)
            self._configure_output_value_fields(lcp.value)
        if with_links:
            pcl: ConceptLinkPagination = concept_object.pagination_concept_link(
                offset=0,
                limit=10000,
                filter_settings=ConceptLinkFilterSettings()
            )
            lcl = pcl.list_concept_link()
            lcl.__fields__(*self.concept_link_fields)
            lcl.concept_from().__fields__(*self.concept_link_concept_from_fields)
            lcl.concept_to().__fields__(*self.concept_link_concept_to_fields)
            lcl.concept_link_type().__fields__(*self.concept_link_type_fields_truncated)

            if with_link_properties:
                pcp: ConceptPropertyPagination = lcl.pagination_concept_link_property(
                    offset=0,
                    limit=10000,
                    filter_settings=ConceptPropertyFilterSettings()
                )
                lcp = pcp.list_concept_property()
                lcp.__fields__(*self.concept_property_fields)
                lcp.property_type().__fields__(*self.concept_property_type_fields)
                self._configure_output_value_fields(lcp.value)

    def _create_concept_with_input(
        self, input: ConceptMutationInput, with_properties=False, with_links=False, with_link_properties=False
    ) -> Concept:

        op = Operation(Mutation)
        ac = op.add_concept(
            # performance_control=PerformSynchronously(
            #     perform_synchronously=False
            # ),
            form=input
        )
        self._configure_output_concept_fields(
            ac, with_properties=with_properties, with_links=with_links,
            with_link_properties=with_link_properties
        )
        res = self._gql_client.execute(op)
        res = op + res

        if self.tdm_builder is not None:
            self.tdm_builder.add_concept_fact(res.add_concept)

        return res.add_concept

    def get_all_documents(
        self, grouping: DocumentGrouping = 'none', query: str = None,
        filter_settings: DocumentFilterSettings = None, direction: SortDirection = 'descending',
        sort_field: DocumentSorting = 'score', extra_settings: ExtraSettings = None
    ) -> Iterable[Story]:
        if filter_settings is None:
            filter_settings = DocumentFilterSettings()
        if extra_settings is None:
            extra_settings = ExtraSettings()

        total = self.get_documents_count(filter_settings=filter_settings)

        if total > self.kb_iterator_config.max_total_count:
            had_creation_date = hasattr(filter_settings, 'registration_date')
            old_timestamp_interval = None
            if had_creation_date:
                old_timestamp_interval = copy(filter_settings.registration_date)
            start: int = getattr(old_timestamp_interval, 'start', self.kb_iterator_config.earliest_created_time)
            end: int = getattr(old_timestamp_interval, 'end', int(time()))
            middle: int = (end + start) // 2

            for start, end in (start, middle), (middle, end):
                filter_settings.registration_date = TimestampInterval(start=start, end=end)
                for c in self.get_all_documents(grouping=grouping, query=query, filter_settings=filter_settings,
                                                direction=direction, sort_field=sort_field,
                                                extra_settings=extra_settings):
                    yield c

            if had_creation_date:
                filter_settings.registration_date = old_timestamp_interval
            else:
                delattr(filter_settings, 'registration_date')
            return
        elif not total:
            return

        documents: Iterable = [None]
        i: int = 0
        while documents:
            documents = self.get_documents(
                skip=i * 20, take=20, grouping=grouping, query=query,
                filter_settings=filter_settings, direction=direction,
                sort_field=sort_field, extra_settings=extra_settings
            )
            for d in documents:
                yield d
            i += 1

    def get_documents(
        self, skip: int = 0, take: int = 20, grouping: DocumentGrouping = 'none', query: str = None,
        filter_settings: DocumentFilterSettings = None, direction: SortDirection = 'descending',
        sort_field: DocumentSorting = 'score', extra_settings: ExtraSettings = None
    ) -> Sequence[Story]:
        pagination_story_kwargs = dict()
        if filter_settings is None:
            filter_settings = DocumentFilterSettings()
        if extra_settings is None:
            extra_settings = ExtraSettings()

        if query:
            pagination_story_kwargs['query'] = query

        op = Operation(Query)
        ps: StoryPagination = op.pagination_story(
            offset=skip,
            limit=take,
            grouping=grouping,
            filter_settings=filter_settings,
            direction=direction,
            sort_field=sort_field,
            extra_settings=extra_settings,
            **pagination_story_kwargs
        )
        ps.list_story().list_document().__fields__(*self.document_fields_truncated)
        m = ps.list_story().main()
        m.__fields__(*self.document_fields_truncated)
        m.text().__fields__(*self.document_text_fields_truncated)

        res = self._gql_client.execute(op)
        res = op + res
        return res.pagination_story.list_story

    def get_documents_count(self, filter_settings: DocumentFilterSettings = None) -> int:
        if filter_settings is None:
            filter_settings = DocumentFilterSettings()

        op = Operation(Query)
        ps: StoryPagination = op.pagination_story(
            limit=1,
            filter_settings=filter_settings,
            extra_settings=ExtraSettings()
        )
        ps.show_total()
        res = self._gql_client.execute(op)
        res = op + res
        return res.pagination_story.show_total

    def get_documents_by_limit_offset_filter_extra_settings(
        self, skip: int, take: int, filter_settings: DocumentFilterSettings, extra_settings: ExtraSettings
    ) -> Sequence[Story]:

        op = Operation(Query)
        ps: StoryPagination = op.pagination_story(
            offset=skip,
            limit=take,
            extra_settings=extra_settings,
            filter_settings=filter_settings
        )
        ps.list_story().list_document().__fields__(*self.document_fields_truncated)
        m = ps.list_story().main()
        m.__fields__(*self.document_fields_truncated)
        m.text().__fields__(*self.document_text_fields_truncated)

        res = self._gql_client.execute(op)
        res = op + res
        return res.pagination_story.list_story

    def get_documents_by_limit_offset_query_extra_settings(
        self, skip: int, take: int, query: str, extra_settings: ExtraSettings
    ) -> Sequence[Story]:

        op = Operation(Query)
        ps: StoryPagination = op.pagination_story(
            offset=skip,
            limit=take,
            extra_settings=extra_settings,
            query=query
        )
        ps.list_story().list_document().__fields__(*self.document_fields_truncated)
        m = ps.list_story().main()
        m.__fields__(*self.document_fields_truncated)
        m.text().__fields__(*self.document_text_fields_truncated)

        res = self._gql_client.execute(op)
        res = op + res
        return res.pagination_story.list_story

    def get_document(self, document_id: str) -> Document:
        op = Operation(Query)
        d: Document = op.document(
            id=document_id
        )
        d.__fields__(*self.document_fields)
        dt = d.text(show_hidden=True)
        dt.__fields__(*self.document_text_fields)
        dt.metadata().__fields__(*self.document_text_metadata_fields)
        cd = d.list_child()
        cd.__fields__(*self.document_fields)
        cdt = cd.text(show_hidden=True)
        cdt.__fields__(*self.document_text_fields)
        cdt.metadata().__fields__(*self.document_text_metadata_fields)

        res = self._gql_client.execute(op)
        res = op + res
        return res.document

    def get_concept_count(self, filter_settings: ConceptFilterSettings = None) -> int:
        op = Operation(Query)
        pc: ConceptPagination = op.pagination_concept(
            filter_settings=filter_settings if filter_settings else ConceptFilterSettings()
        )
        pc.show_total()
        res = self._gql_client.execute(op)
        res = op + res
        return res.pagination_concept.show_total

    def get_concept_link_count(self, filter_settings: ConceptLinkFilterSettings = None) -> int:
        op = Operation(Query)
        pcl: ConceptLinkPagination = op.pagination_concept_link(
            filter_settings=filter_settings if filter_settings else ConceptLinkFilterSettings()
        )
        pcl.total()
        res = self._gql_client.execute(op)
        res = op + res
        return res.pagination_concept_link.total

    def get_concept(self, concept_id: str, with_aliases: bool = False) -> Concept:
        op = Operation(Query)
        c: Concept = op.concept(
            id=concept_id
        )
        self._configure_output_concept_fields(
            c, with_aliases=with_aliases, with_link_properties=True, with_links=True, with_properties=True
        )
        res = self._gql_client.execute(op)
        res = op + res

        if self.tdm_builder is not None:
            self.tdm_builder.add_concept_fact(res.concept)

        return res.concept

    def get_concept_facts(
        self, concept_id: str, filter_settings: DocumentLinkFilterSetting = None
    ) -> Sequence[ConceptFact]:

        op = Operation(Query)
        c: Concept = op.concept(
            id=concept_id
        )
        pcf: ConceptFactPagination = c.pagination_concept_fact(
            filter_settings=filter_settings if filter_settings else DocumentLinkFilterSetting()
        )
        lcf = pcf.list_concept_fact()
        lcf.__fields__(*self.concept_fact_fields)
        d = lcf.document()
        d.__fields__(*self.concept_fact_document_fields)
        dm = d.metadata()
        dm.platform().__fields__(*self.concept_fact_document_platform_fields)
        dm.account().__fields__(*self.concept_fact_document_account_fields)

        res = self._gql_client.execute(op)
        res = op + res

        return res.concept.pagination_concept_fact.list_concept_fact

    def get_concept_link(self, link_id: str) -> ConceptLink:
        op = Operation(Query)
        cl: ConceptLink = op.concept_link(
            id=link_id
        )
        cl.__fields__(*self.concept_link_fields)
        self._configure_output_concept_fields(cl.concept_from)
        self._configure_output_concept_fields(cl.concept_to)
        cl.concept_link_type.__fields__(*self.concept_link_type_fields_truncated)
        res = self._gql_client.execute(op)
        res = op + res

        if self.tdm_builder is not None:
            self.tdm_builder.add_link_fact(res.concept_link)

        return res.concept_link

    def get_all_concepts(
        self, query: str = None, filter_settings: ConceptFilterSettings = None,
        direction: SortDirection = 'descending', sort_field: ConceptSorting = 'score',
        with_aliases: bool = False, with_properties: bool = False, with_links: bool = False,
        with_link_properties: bool = False
    ) -> Iterable[Concept]:
        if not filter_settings:
            filter_settings = ConceptFilterSettings()
        total = self.get_concept_count(filter_settings=filter_settings)

        if total > self.kb_iterator_config.max_total_count:
            had_creation_date = hasattr(filter_settings, 'creation_date')
            old_timestamp_interval = None
            if had_creation_date:
                old_timestamp_interval = copy(filter_settings.creation_date)
            start: int = getattr(old_timestamp_interval, 'start', self.kb_iterator_config.earliest_created_time)
            end: int = getattr(old_timestamp_interval, 'end', int(time()))
            middle: int = (end + start) // 2

            for start, end in (start, middle), (middle, end):
                filter_settings.creation_date = TimestampInterval(start=start, end=end)
                for c in self.get_all_concepts(query=query, filter_settings=filter_settings,
                                               direction=direction, sort_field=sort_field, with_aliases=with_aliases,
                                               with_properties=with_properties, with_links=with_links,
                                               with_link_properties=with_link_properties):
                    yield c

            if had_creation_date:
                filter_settings.creation_date = old_timestamp_interval
            else:
                delattr(filter_settings, 'creation_date')
            return
        elif not total:
            return

        concepts: Iterable = [None]
        i: int = 0
        while concepts:
            concepts = self.get_concepts(
                skip=i * 20, take=20, query=query, filter_settings=filter_settings,
                direction=direction, sort_field=sort_field, with_aliases=with_aliases,
                with_properties=with_properties, with_links=with_links, with_link_properties=with_link_properties
            )
            for c in concepts:
                yield c
            i += 1

    def get_concepts(
        self, skip: int = 0, take: int = 20, query: str = None,
        filter_settings: ConceptFilterSettings = None,
        direction: SortDirection = 'descending', sort_field: ConceptSorting = 'score',
        with_aliases: bool = False, with_properties: bool = False, with_links: bool = False,
        with_link_properties: bool = False
    ) -> Sequence[Concept]:
        pagination_concept_kwargs = dict()
        if not filter_settings:
            filter_settings = ConceptFilterSettings()

        if query:
            pagination_concept_kwargs['query'] = query

        op = Operation(Query)
        cp: ConceptPagination = op.pagination_concept(
            limit=take,
            offset=skip,
            filter_settings=filter_settings,
            direction=direction,
            sort_field=sort_field,
            **pagination_concept_kwargs
        )
        self._configure_output_concept_fields(
            cp.list_concept(), with_aliases=with_aliases,
            with_properties=with_properties, with_links=with_links, with_link_properties=with_link_properties
        )
        res = self._gql_client.execute(op)
        res = op + res
        return res.pagination_concept.list_concept

    def get_concepts_by_limit_offset_filter_settings(
        self, skip: int, take: int, filter_settings: ConceptFilterSettings, with_aliases: bool = False
    ) -> Sequence[Concept]:

        op = Operation(Query)
        cp: ConceptPagination = op.pagination_concept(
            filter_settings=filter_settings,
            offset=skip,
            limit=take
        )
        self._configure_output_concept_fields(cp.list_concept(), with_aliases=with_aliases)
        res = self._gql_client.execute(op)
        res = op + res
        return res.pagination_concept.list_concept

    def get_all_concept_links(
        self, filter_settings: ConceptLinkFilterSettings = None
    ) -> Iterable[ConceptLink]:
        if not filter_settings:
            filter_settings = ConceptLinkFilterSettings()

        total = self.get_concept_link_count(filter_settings=filter_settings)

        if total > self.kb_iterator_config.max_total_count:
            had_creation_date = hasattr(filter_settings, 'creation_date')
            old_timestamp_interval = None
            if had_creation_date:
                old_timestamp_interval = copy(filter_settings.creation_date)
            start: int = getattr(old_timestamp_interval, 'start', self.kb_iterator_config.earliest_created_time)
            end: int = getattr(old_timestamp_interval, 'end', int(time()))
            middle: int = (end + start) // 2

            for start, end in (start, middle), (middle, end):
                filter_settings.creation_date = TimestampInterval(start=start, end=end)
                for c in self.get_all_concept_links(filter_settings=filter_settings):
                    yield c

            if had_creation_date:
                filter_settings.creation_date = old_timestamp_interval
            else:
                delattr(filter_settings, 'creation_date')
            return
        elif not total:
            return

        links: Iterable = [None]
        i: int = 0
        while links:
            links = self.get_concept_links_by_limit_offset_filter_settings(
                skip=i * 20, take=20,
                filter_settings=filter_settings
            )
            for link in links:
                yield link
            i += 1

    def get_concept_links_by_limit_offset_filter_settings(
        self, skip: int = 0, take: int = 20,
        filter_settings: ConceptLinkFilterSettings = None
    ) -> Sequence[ConceptLink]:

        op = Operation(Query)
        pcl: ConceptLinkPagination = op.pagination_concept_link(
            filter_settings=filter_settings if filter_settings else ConceptLinkFilterSettings(),
            offset=skip,
            limit=take
        )
        lcl = pcl.list_concept_link()
        lcl.__fields__(*self.concept_link_fields)
        lcl.concept_from().__fields__(*self.concept_link_concept_from_fields)
        lcl.concept_to().__fields__(*self.concept_link_concept_to_fields)
        lcl.concept_link_type().__fields__(*self.concept_link_type_fields_truncated)

        res = self._gql_client.execute(op)
        res = op + res
        return res.pagination_concept_link.list_concept_link

    def get_concepts_by_limit_offset_query(
        self, skip: int, take: int, query: str, with_aliases: bool = False
    ) -> Sequence[Concept]:

        op = Operation(Query)
        cp: ConceptPagination = op.pagination_concept(
            offset=skip,
            limit=take,
            query=query
        )
        self._configure_output_concept_fields(cp.list_concept(), with_aliases=with_aliases)
        res = self._gql_client.execute(op)
        res = op + res
        return res.pagination_concept.list_concept

    def get_concepts_by_type_id_with_offset(
        self, type_id: str, skip: int, take: int, direction='descending', sort_field='systemRegistrationDate',
        with_aliases: bool = False, with_properties: bool = False, with_links: bool = False,
        with_link_properties: bool = False
    ) -> ConceptPagination:

        op = Operation(Query)
        cp: ConceptPagination = op.pagination_concept(
            filter_settings=ConceptFilterSettings(
                concept_type_ids=[type_id]
            ),
            limit=take,
            offset=skip,
            direction=direction,
            sort_field=sort_field
        )
        cp.total()
        self._configure_output_concept_fields(
            cp.list_concept(), with_aliases, with_properties, with_links, with_link_properties
        )
        res = self._gql_client.execute(op)
        res = op + res
        return res.pagination_concept

    def get_concepts_by_type_id_with_offset_with_markers(
        self, type_id: str, skip: int, take: int, markers: List[str], direction='descending',
        sort_field='systemRegistrationDate', with_aliases: bool = False
    ) -> ConceptPagination:

        op = Operation(Query)
        cp: ConceptPagination = op.pagination_concept(
            filter_settings=ConceptFilterSettings(
                concept_type_ids=[type_id],
                markers=markers,
            ),
            limit=take,
            offset=skip,
            direction=direction,
            sort_field=sort_field
        )
        cp.total()
        self._configure_output_concept_fields(cp.list_concept(), with_aliases=with_aliases)
        res = self._gql_client.execute(op)
        res = op + res
        return res.pagination_concept

    def get_concepts_by_name(
        self, name: str, type_id: Optional[str] = None, with_aliases: bool = False
    ) -> Sequence[Concept]:

        op = Operation(Query)
        if type_id:
            concept_filter_settings: ConceptFilterSettings = ConceptFilterSettings(
                exact_name=name,
                concept_type_ids=[type_id]
            )
        else:
            concept_filter_settings: ConceptFilterSettings = ConceptFilterSettings(
                exact_name=name
            )
        cp: ConceptPagination = op.pagination_concept(
            filter_settings=concept_filter_settings
        )
        self._configure_output_concept_fields(cp.list_concept(), with_aliases=with_aliases)
        res = self._gql_client.execute(op)
        res = op + res
        return res.pagination_concept.list_concept

    def get_concepts_by_near_name(
        self, name: str, type_id: Optional[str] = None, with_aliases: bool = False
    ) -> Sequence[Concept]:

        op = Operation(Query)
        if type_id:
            concept_filter_settings: ConceptFilterSettings = ConceptFilterSettings(
                name=name,
                concept_type_ids=[type_id]
            )
        else:
            concept_filter_settings: ConceptFilterSettings = ConceptFilterSettings(
                name=name
            )
        cp: ConceptPagination = op.pagination_concept(
            filter_settings=concept_filter_settings
        )
        self._configure_output_concept_fields(cp.list_concept(), with_aliases=with_aliases)
        res = self._gql_client.execute(op)
        res = op + res
        return res.pagination_concept.list_concept

    def get_concepts_by_property_name(
        self, property_type_id: str, string_filter: str, property_type: str = 'concept', with_aliases: bool = False
    ) -> Sequence[Concept]:

        op = Operation(Query)
        cp: ConceptPagination = op.pagination_concept(
            filter_settings=ConceptFilterSettings(
                property_filter_settings=[PropertyFilterSettings(
                    property_type=property_type,
                    property_type_id=property_type_id,
                    string_filter=StringFilter(
                        str=string_filter
                    )
                )]
            )
        )
        self._configure_output_concept_fields(cp.list_concept(), with_aliases=with_aliases)
        res = self._gql_client.execute(op)
        res = op + res
        return res.pagination_concept.list_concept

    def get_concept_properties(self, concept_id: str) -> Sequence[ConceptProperty]:
        op = Operation(Query)
        concept: Concept = op.concept(
            id=concept_id
        )
        pcp: ConceptPropertyPagination = concept.pagination_concept_property(
            offset=0,
            limit=10000,
            filter_settings=ConceptPropertyFilterSettings()
        )
        lcp = pcp.list_concept_property()
        lcp.__fields__(*self.concept_property_fields)
        lcp.property_type().__fields__(*self.concept_property_type_fields)
        self._configure_output_value_fields(lcp.value)

        res = self._gql_client.execute(op)
        res = op + res  # type: Query
        return res.concept.pagination_concept_property.list_concept_property

    def get_concept_links(self, concept_id: str) -> Sequence[ConceptLink]:
        op = Operation(Query)

        concept: Concept = op.concept(
            id=concept_id
        )
        pcl: ConceptLinkPagination = concept.pagination_concept_link(
            offset=0,
            limit=10000,
            filter_settings=ConceptLinkFilterSettings()
        )
        lcl = pcl.list_concept_link()
        lcl.__fields__(*self.concept_link_fields)
        lcl.concept_from().__fields__(*self.concept_link_concept_from_fields)
        lcl.concept_to().__fields__(*self.concept_link_concept_to_fields)
        lcl.concept_link_type().__fields__(*self.concept_link_type_fields_truncated)

        res = self._gql_client.execute(op)
        res = op + res  # type: Query
        return res.concept.pagination_concept_link.list_concept_link

    def get_concept_links_concept(self, concept_id: str, link_type_id: str) -> Sequence[ConceptLink]:
        op = Operation(Query)

        concept = op.concept(
            id=concept_id
        )
        pcl = concept.pagination_concept_link(
            offset=0,
            limit=10000,
            filter_settings=ConceptLinkFilterSettings(
                concept_link_type=[link_type_id]
            )
        )
        lcl = pcl.list_concept_link()
        lcl.__fields__(*self.concept_link_fields)
        lcl.concept_from().__fields__(*self.concept_link_concept_from_fields)
        lcl.concept_to().__fields__(*self.concept_link_concept_to_fields)
        lcl.concept_link_type().__fields__(*self.concept_link_type_fields_truncated)

        res = self._gql_client.execute(op)
        res = op + res  # type: Query
        return res.concept.pagination_concept_link.list_concept_link

    def get_link_properties(self, link_id: str) -> Sequence[ConceptProperty]:
        op = Operation(Query)
        concept_link: ConceptLink = op.concept_link(
            id=link_id
        )
        pcp: ConceptPropertyPagination = concept_link.pagination_concept_link_property(
            offset=0,
            limit=10000,
            filter_settings=ConceptPropertyFilterSettings()
        )
        lcp = pcp.list_concept_property()
        lcp.__fields__(*self.concept_property_fields)
        lcp.property_type().__fields__(*self.concept_property_type_fields)
        self._configure_output_value_fields(lcp.value)

        res = self._gql_client.execute(op)
        res = op + res  # type: Query
        return res.concept_link.pagination_concept_link_property.list_concept_property

    def create_concept(
        self, name: str, type_id: str, notes: str = None, with_properties=False, with_links=False,
        with_link_properties=False
    ) -> Concept:

        cmi: ConceptMutationInput = ConceptMutationInput(
            name=name,
            concept_type_id=type_id,
            notes=notes
        )
        return self._create_concept_with_input(
            cmi, with_properties=with_properties, with_links=with_links,
            with_link_properties=with_link_properties
        )

    def update_concept(self, c: Concept, markers: List[str] = None, notes: str = None) -> Concept:
        op = Operation(Mutation)
        uc: Concept = op.update_concept(
            # performance_control=PerformSynchronously(
            #     perform_synchronously=False
            # ),
            form=ConceptUpdateInput(
                concept_id=c.id,
                name=c.name,
                concept_type_id=c.concept_type.id,
                markers=markers if markers is not None else c.markers,
                notes=notes if notes is not None else c.notes
            )
        )
        self._configure_output_concept_fields(uc)
        res = self._gql_client.execute(op)
        res = op + res

        return res.update_concept

    def update_concept_property_value_types(self, cpvt: ConceptPropertyValueType) -> ConceptPropertyValueType:
        op = Operation(Mutation)
        ucpvt = op.update_concept_property_value_type(
            form=ConceptPropertyValueTypeUpdateInput(
                id=cpvt.id,
                name=cpvt.name,
                value_type=cpvt.value_type,
                pretrained_nercmodels=cpvt.pretrained_nercmodels,
                value_restriction=cpvt.value_restriction
            )
        )
        ucpvt.__fields__('id')
        res = self._gql_client.execute(op)
        res = op + res

        return res.update_concept_property_value_type

    def update_concept_string_property(self, cp: ConceptProperty) -> ConceptProperty:
        op = Operation(Mutation)
        ucp: ConceptProperty = op.update_concept_property(
            # performance_control=PerformSynchronously(
            #     perform_synchronously=False
            # ),
            form=ConceptPropertyUpdateInput(
                property_id=cp.id,
                is_main=cp.is_main,
                value_input=[
                    ComponentValueInput(
                        value=ValueInput(
                            string_value_input=StringValueInput(
                                value=cp.value.value
                            )
                        )
                    )
                ]
            )
        )
        ucp.__fields__('id')
        res = self._gql_client.execute(op)
        res = op + res

        return res.update_concept_property

    def update_concept_int_property(self, cp: ConceptProperty) -> ConceptProperty:
        op = Operation(Mutation)
        ucp: ConceptProperty = op.update_concept_property(
            form=ConceptPropertyUpdateInput(
                property_id=cp.id,
                is_main=cp.is_main,
                value_input=[
                    ComponentValueInput(
                        value=ValueInput(
                            int_value_input=IntValueInput(
                                value=cp.value.number
                            )
                        )
                    )
                ]
            )
        )
        ucp.__fields__('id')
        res = self._gql_client.execute(op)
        res = op + res

        return res.update_concept_property

    def delete_concept_property(self, cp_id: str) -> bool:
        op = Operation(Mutation)
        dcp = op.delete_concept_property(
            id=cp_id
        )
        dcp.__fields__('is_success')
        res = self._gql_client.execute(op)
        res = op + res

        return res.delete_concept_property.is_success

    def get_concept_types_by_name(self, name: str) -> Sequence[ConceptType]:
        op = Operation(Query)
        ctp: ConceptTypePagination = op.pagination_concept_type(
            filter_settings=ConceptTypeFilterSettings(
                name=name
            )
        )
        ctp.list_concept_type().__fields__(*self.concept_type_fields)
        res = self._gql_client.execute(op)
        res = op + res
        return res.pagination_concept_type.list_concept_type

    def get_concept_type_info(self, concept_type_id: str) -> ConceptType:
        op = Operation(Query)
        ct = op.concept_type(
            id=concept_type_id
        )
        ct.__fields__(*self.concept_type_fields)
        lcpt = ct.list_concept_property_type()
        lcpt.__fields__(*self.concept_property_type_fields)
        lclt = ct.list_concept_link_type()
        lclt.__fields__(*self.concept_link_type_fields)
        lclt.list_concept_link_property_type().__fields__(*self.concept_property_type_fields)

        res = self._gql_client.execute(op)
        res = op + res
        return res.concept_type

    def get_concept_type(self, concept_type_code: str) -> Optional[ConceptType]:
        concept_type: Optional[ConceptType] = self._cache.get(f'concept_type_{concept_type_code}', None)
        if concept_type:
            return concept_type
        concept_type_name = self._types['concepts_types_mapping'][concept_type_code]['name']
        types = self.get_concept_types_by_name(concept_type_name)
        if not types:
            return None
        concept_type = None
        for t in types:
            if t.name == concept_type_name:
                concept_type = t
                break
        if not concept_type:
            return None
        self._cache[f'concept_type_{concept_type_code}'] = concept_type
        return concept_type

    def get_concept_properties_types_by_name(
            self, concept_type_id: str, prop_name: str
    ) -> Sequence[ConceptPropertyType]:

        op = Operation(Query)
        cptp: ConceptPropertyTypePagination = op.pagination_concept_property_type(
            filter_settings=ConceptPropertyTypeFilterSettings(
                name=prop_name,
                concept_type_id=concept_type_id
            )
        )
        lcpt = cptp.list_concept_property_type()
        lcpt.__fields__(*self.concept_property_type_fields)
        self._configure_property_value_type_fields(lcpt.value_type, True)
        res = self._gql_client.execute(op)
        res = op + res
        return res.pagination_concept_property_type.list_concept_property_type

    def get_concept_property_type(
        self, concept_type_code: str, property_type_code: str
    ) -> Optional[ConceptPropertyType]:

        concept_type: ConceptType = self.get_concept_type(concept_type_code)
        if not concept_type:
            raise Exception('Cannot get concept property type: no concept type id')

        prop_type = self._cache.get(f'concept_property_type_{concept_type_code}_{property_type_code}', None)
        if prop_type:
            return prop_type
        prop_type_name = self._types['concepts_types_mapping'][concept_type_code]['properties'][property_type_code]
        types = self.get_concept_properties_types_by_name(concept_type.id, prop_type_name)
        for prop_type in types:
            if prop_type.name == prop_type_name:
                self._cache[f'concept_property_type_{concept_type_code}_{property_type_code}'] = prop_type
                return prop_type
        return None

    def get_concept_property_value_types_by_name(self, prop_value_type_name: str) -> Sequence[ConceptPropertyValueType]:
        op = Operation(Query)
        cpvtp: ConceptPropertyValueTypePagination = op.pagination_concept_property_value_type(
            filter_settings=ConceptPropertyValueTypeFilterSettings(
                name=prop_value_type_name
            )
        )
        cpvtp.list_concept_property_value_type().__fields__(*self.cpvt_fields)
        res = self._gql_client.execute(op)
        res = op + res
        return res.pagination_concept_property_value_type.list_concept_property_value_type

    def get_concept_property_value_type(
        self, concept_property_value_type_code: str
    ) -> Optional[ConceptPropertyValueType]:

        concept_property_value_type: Optional[ConceptPropertyValueType] = self._cache.get(
            f'concept_property_value_type_{concept_property_value_type_code}', None
        )
        if concept_property_value_type:
            return concept_property_value_type
        concept_property_value_type_name = self._types['value_types_mapping'][concept_property_value_type_code]
        types = self.get_concept_property_value_types_by_name(concept_property_value_type_name)
        if not types:
            return None
        concept_property_value_type = None
        for t in types:
            if t.name == concept_property_value_type_name:
                concept_property_value_type = t
                break
        if not concept_property_value_type:
            return None
        self._cache[f'concept_property_value_type_{concept_property_value_type_code}'] = concept_property_value_type
        return concept_property_value_type

    def get_link_properties_types_by_name(self, link_type_id: str, prop_name: str) -> Sequence[ConceptPropertyType]:
        op = Operation(Query)
        cptp: ConceptPropertyTypePagination = op.pagination_concept_link_property_type(
            filter_settings=ConceptPropertyTypeFilterSettings(
                name=prop_name,
                concept_link_type_id=link_type_id
            )
        )
        lcpt = cptp.list_concept_property_type()
        lcpt.__fields__(*self.concept_property_type_fields)
        self._configure_property_value_type_fields(lcpt.value_type, True)
        res = self._gql_client.execute(op)
        res = op + res
        return res.pagination_concept_link_property_type.list_concept_property_type

    def get_link_property_type(
        self, link_type_code: str, link_type: ConceptLinkType, property_type_code: str
    ) -> Optional[ConceptPropertyType]:
        # link_type = self.get_link_type(link_type_code)
        # if not link_type:
        #     raise Exception('Cannot get link property type: no link type id')

        prop_type: Optional[ConceptPropertyType] = self._cache.get(
            f'link_property_type_{link_type_code}_{property_type_code}', None
        )
        if prop_type:
            return prop_type
        link_type_mapping = None
        for r in self._types['relations_types_mapping']:
            if r['old_relation_type'] == link_type_code:
                link_type_mapping = r
                break
        if not link_type_mapping:
            raise Exception('Cannot get link mapping object')
        prop_type_name = link_type_mapping['properties'][property_type_code]
        types = self.get_link_properties_types_by_name(link_type.id, prop_type_name)
        for prop_type in types:
            if prop_type.name == prop_type_name:
                self._cache[f'link_property_type_{link_type_code}_{property_type_code}'] = prop_type
                return prop_type
        return None

    def add_property_by_id(self, id: str, type_id: str, value: Any, is_main: bool, value_type: str) -> ConceptProperty:
        op = Operation(Mutation)
        acp = op.add_concept_property(
            # performance_control=PerformSynchronously(
            #     perform_synchronously=False
            # ),
            form=ConceptPropertyCreateInput(
                concept_id=id,
                property_type_id=type_id,
                is_main=is_main,
                value_input=[
                    ComponentValueInput(
                        value=get_map_helper(value_type).get_value_input(value)
                    )
                ]
            )
        )
        acp.__fields__('id')
        acp.property_type().__fields__(*self.concept_property_type_fields)
        res = self._gql_client.execute(op)
        res = op + res

        return res.add_concept_property

    def add_property(
        self, concept_id: str, concept_type_code: str, property_type_code: str, value: Any, is_main: bool = False
    ) -> ConceptProperty:

        property_type: ConceptPropertyType = self.get_concept_property_type(concept_type_code, property_type_code)
        if not property_type:
            raise Exception('Cannot add property: no property type id')
        prop = self.add_property_by_id(
            concept_id, property_type.id, value, is_main, property_type.value_type.value_type
        )

        if self.tdm_builder is not None:
            self.tdm_builder.add_concept_property_fact(prop, self.get_concept(concept_id), value, property_type)

        return prop

    def add_link_property_by_id(
        self, link_id: str, type_id: str, value: str, is_main: bool, value_type: str
    ) -> ConceptProperty:

        op = Operation(Mutation)

        aclp = op.add_concept_link_property(
            # performance_control=PerformSynchronously(
            #     perform_synchronously=False
            # ),
            form=ConceptLinkPropertyInput(
                property_type_id=type_id,
                link_id=link_id,
                is_main=is_main,
                value_input=[
                    ComponentValueInput(
                        value=get_map_helper(value_type).get_value_input(value)
                    )
                ]
            )
        )
        aclp.__fields__('id')
        aclp.property_type().__fields__(*self.concept_property_type_fields)
        res = self._gql_client.execute(op)
        res = op + res

        return res.add_concept_link_property

    def add_link_property(
        self, link_id: str, link_type_code: str, link_type: ConceptLinkType, property_type_code: str, value: Any,
        is_main: bool = False
    ) -> ConceptProperty:

        property_type: ConceptPropertyType = self.get_link_property_type(link_type_code, link_type, property_type_code)
        if not property_type:
            raise Exception('Cannot add property: no property type id')
        link_property = self.add_link_property_by_id(
            link_id, property_type.id, value, is_main,
            property_type.value_type.value_type
        )

        if self.tdm_builder is not None:
            self.tdm_builder.add_link_property_fact(link_property, self.get_concept_link(link_id), value, property_type)

        return self.add_link_property_by_id(
            link_id, property_type.id, value, is_main,
            property_type.value_type.value_type
        )

    def get_concept_link_type_by_name(
        self, link_name: str, from_type_id: str, to_type_id: str
    ) -> Sequence[ConceptLinkType]:

        op = Operation(Query)
        pclt: ConceptLinkTypePagination = op.pagination_concept_link_type(
            filter_settings=ConceptLinkTypeFilterSettings(
                name=link_name,
                concept_from_type_id=from_type_id,
                concept_to_type_id=to_type_id
            )
        )
        pclt.list_concept_link_type().__fields__(*self.concept_link_type_fields)
        res = self._gql_client.execute(op)
        res = op + res
        return res.pagination_concept_link_type.list_concept_link_type

    def get_link_type(
        self, concept_from_type_code: str, concept_to_type_code: str, link_type_code: str
    ) -> Optional[ConceptLinkType]:

        link_type = self._cache.get(f'concept_link_type_{concept_from_type_code}_{link_type_code}', None)
        if link_type:
            return link_type
        from_type = self.get_concept_type(concept_from_type_code)
        to_type = self.get_concept_type(concept_to_type_code)
        if not from_type or not to_type:
            raise Exception('Cannot get link type: no concept type id')
        link_type_name = None
        for r in self._types['relations_types_mapping']:
            if r['old_relation_type'] == link_type_code:
                link_type_name = r['new_relation_type']
        if not link_type_name:
            raise Exception('Cannot get link type name')
        types = self.get_concept_link_type_by_name(link_type_name, from_type.id, to_type.id)
        for link_type in types:
            if link_type.name == link_type_name:
                self._cache[f'concept_link_type_{concept_from_type_code}_{link_type_code}'] = link_type
                return link_type
        return None

    def add_relation_by_id(self, from_id: str, to_id: str, link_type_id: str) -> ConceptLink:
        op = Operation(Mutation)
        acl = op.add_concept_link(
            # performance_control=PerformSynchronously(
            #     perform_synchronously=False
            # ),
            form=ConceptLinkCreationMutationInput(
                concept_from_id=from_id,
                concept_to_id=to_id,
                link_type_id=link_type_id
            )
        )
        acl.__fields__(*self.concept_link_fields)
        acl.concept_link_type.__fields__(*self.concept_property_type_fields)
        acl.concept_link_type.__fields__(*self.concept_link_type_fields_truncated)
        self._configure_output_concept_fields(acl.concept_from)
        self._configure_output_concept_fields(acl.concept_to)

        res = self._gql_client.execute(op)
        res = op + res

        return res.add_concept_link

    def add_relation(
        self, concept_from_id: str, concept_to_id: str, concept_from_type_code: str, concept_to_type_code: str,
        type_code: str
    ) -> ConceptLink:

        link_type = self.get_link_type(concept_from_type_code, concept_to_type_code, type_code)
        if not link_type:
            raise Exception('Cannot add relation: no link type')
        relation = self.add_relation_by_id(concept_from_id, concept_to_id, link_type.id)

        if self.tdm_builder is not None:
            self.tdm_builder.add_link_fact(relation)

        return relation

    def delete_concept(self, concept_id: str) -> bool:

        op = Operation(Mutation)
        dc: Concept = op.delete_concept(
            id=concept_id
        )
        dc.__fields__('is_success')
        res = self._gql_client.execute(op)
        res = op + res

        return res.delete_concept.is_success

    def delete_concept_link(self, link_id: str) -> bool:

        op = Operation(Mutation)
        dcl: ConceptLink = op.delete_concept_link(
            id=link_id
        )
        dcl.__fields__('is_success')
        res = self._gql_client.execute(op)
        res = op + res

        return res.delete_concept_link.is_success

    def delete_concept_link_property(self, link_property_id: str) -> bool:

        op = Operation(Mutation)
        clp: ConceptProperty = op.delete_concept_link_property(
            id=link_property_id
        )
        clp.__fields__('is_success')
        res = self._gql_client.execute(op)
        res = op + res

        return res.delete_concept_link_property.is_success

    def add_concept_markers(self, concept_id: str, markers: List[str]) -> Concept:
        c = self.get_concept(concept_id)
        c.markers.extend(markers)
        new_markers = list(set(c.markers))
        return self.update_concept(c, markers=new_markers)

    def set_concept_markers(self, concept_id: str, markers: List[str]) -> Concept:
        c = self.get_concept(concept_id)
        return self.update_concept(c, markers=markers)

    def get_composite_concept(self, root_concept_id: str, composite_concept_type_id: str) -> CompositeConcept:
        op = Operation(Query)
        cc: CompositeConcept = op.composite_concept(
            root_concept_id=root_concept_id,
            composite_concept_type_id=composite_concept_type_id
        )
        self._configure_output_concept_fields(
            cc.root_concept, with_aliases=False, with_link_properties=False,
            with_links=False, with_properties=False
        )
        lwt = cc.composite_concept_type().list_widget_type()
        lwt.__fields__(*self.composite_concept_widget_type)
        lwt.columns_info.__fields__(*self.composite_concept_widget_type_columns_info)

        res = self._gql_client.execute(op)
        res = op + res
        return res.composite_concept

    def get_single_widget(
        self, root_concept_id: str, composite_concept_type_id: str, widget_type_id: str,
        limit: int = 20, offset: int = 0
    ) -> CompositeConceptWidgetRowPagination:

        op = Operation(Query)
        cc: CompositeConcept = op.composite_concept(
            root_concept_id=root_concept_id,
            composite_concept_type_id=composite_concept_type_id
        )
        psw: CompositeConceptWidgetRowPagination = cc.paginate_single_widget(
            widget_type_id=widget_type_id,
            limit=limit,
            offset=offset
        )
        psw.__fields__('total')
        self._configure_output_value_fields(psw.rows)

        res = self._gql_client.execute(op)
        res = op + res
        return res.composite_concept.paginate_single_widget

    # region Crawlers methods

    def get_crawler_start_urls(self, take: int) -> Sequence[Crawler]:
        op = Operation(CrQuery)
        pc: CrawlerPagination = op.pagination_crawler(
            limit=take
        )
        lc = pc.list_crawler()
        lc.__fields__('start_urls')

        res = self._gql_client.execute(op)
        res = op + res
        return res.pagination_crawler.list_crawler

    # endregion

    # region Utils methods

    @check_utils_gql_client
    def create_or_get_concept_by_name(
        self, name: str, type_id: str, notes: str = None, take_first_result: bool = False,
        with_properties=False, with_links=False, with_link_properties=False
    ) -> Concept:

        if type_id:
            concept_filter_settings: ConceptFilterSettings = uas.ConceptFilterSettings(
                exact_name=name,
                concept_type_ids=[type_id]
            )
        else:
            concept_filter_settings: ConceptFilterSettings = uas.ConceptFilterSettings(
                exact_name=name
            )

        op = Operation(uas.Mutation)
        goac = op.get_or_add_concept(
            filter_settings=concept_filter_settings,
            form=uas.ConceptMutationInput(
                name=name,
                concept_type_id=type_id,
                notes=notes
            ),
            take_first_result=take_first_result
        )
        self._configure_output_concept_fields(
            goac, with_properties=with_properties, with_links=with_links,
            with_link_properties=with_link_properties
        )

        res = self._utils_gql_client.execute(op)
        res = op + res  # type: uas.Mutation

        if self.tdm_builder is not None:
            self.tdm_builder.add_concept_fact(res.get_or_add_concept)

        return res.get_or_add_concept

    # endregion
