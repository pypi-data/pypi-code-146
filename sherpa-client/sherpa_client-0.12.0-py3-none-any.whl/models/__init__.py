""" Contains all the data models used in inputs/outputs """

from .ack import Ack
from .aggregation import Aggregation
from .annotate_binary_form import AnnotateBinaryForm
from .annotate_binary_with_plan_ref_multipart_data import AnnotateBinaryWithPlanRefMultipartData
from .annotate_documents_with_many import AnnotateDocumentsWithMany
from .annotate_format_binary_with_plan_ref_multipart_data import AnnotateFormatBinaryWithPlanRefMultipartData
from .annotate_text_with_many import AnnotateTextWithMany
from .annotated_doc_annotation import AnnotatedDocAnnotation
from .annotated_doc_annotation_creation_mode import AnnotatedDocAnnotationCreationMode
from .annotated_doc_annotation_properties import AnnotatedDocAnnotationProperties
from .annotated_doc_category import AnnotatedDocCategory
from .annotated_doc_category_creation_mode import AnnotatedDocCategoryCreationMode
from .annotated_doc_category_properties import AnnotatedDocCategoryProperties
from .annotated_document import AnnotatedDocument
from .annotated_document_metadata import AnnotatedDocumentMetadata
from .annotation import Annotation
from .annotation_creation_mode import AnnotationCreationMode
from .annotation_facets import AnnotationFacets
from .annotation_id import AnnotationId
from .annotation_metrics import AnnotationMetrics
from .annotation_patch import AnnotationPatch
from .annotation_patch_status import AnnotationPatchStatus
from .annotation_plan import AnnotationPlan
from .annotation_status import AnnotationStatus
from .annotation_term import AnnotationTerm
from .annotation_term_properties import AnnotationTermProperties
from .annotator import Annotator
from .annotator_multimap import AnnotatorMultimap
from .apply_to import ApplyTo
from .bearer_token import BearerToken
from .bucket import Bucket
from .campaign import Campaign
from .campaign_id import CampaignId
from .campaign_patch import CampaignPatch
from .campaign_roles_change import CampaignRolesChange
from .campaign_session import CampaignSession
from .campaign_session_mode import CampaignSessionMode
from .campaign_user_group import CampaignUserGroup
from .campaign_user_session import CampaignUserSession
from .campaign_user_session_state import CampaignUserSessionState
from .categories_facets import CategoriesFacets
from .category import Category
from .category_action import CategoryAction
from .category_creation_mode import CategoryCreationMode
from .category_id import CategoryId
from .category_metrics import CategoryMetrics
from .category_patch import CategoryPatch
from .category_patch_status import CategoryPatchStatus
from .category_status import CategoryStatus
from .classification_config import ClassificationConfig
from .classification_options import ClassificationOptions
from .config_patch_options import ConfigPatchOptions
from .convert_annotation_plan import ConvertAnnotationPlan
from .convert_format_annotation_plan import ConvertFormatAnnotationPlan
from .converter import Converter
from .converter_parameters import ConverterParameters
from .corpus_metrics import CorpusMetrics
from .create_lexicon_response_200 import CreateLexiconResponse200
from .create_project_from_archive_multipart_data import CreateProjectFromArchiveMultipartData
from .create_term_json_body import CreateTermJsonBody
from .create_term_response_200 import CreateTermResponse200
from .created_by_count import CreatedByCount
from .creation_mode import CreationMode
from .credentials import Credentials
from .delete_group_result import DeleteGroupResult
from .delete_response import DeleteResponse
from .depends_on import DependsOn
from .doc_alt_text import DocAltText
from .doc_annotation import DocAnnotation
from .doc_annotation_creation_mode import DocAnnotationCreationMode
from .doc_annotation_status import DocAnnotationStatus
from .doc_category import DocCategory
from .doc_category_creation_mode import DocCategoryCreationMode
from .doc_category_status import DocCategoryStatus
from .doc_sentence import DocSentence
from .doc_sentence_metadata import DocSentenceMetadata
from .document import Document
from .document_facets import DocumentFacets
from .document_hit import DocumentHit
from .document_hits import DocumentHits
from .document_metadata import DocumentMetadata
from .email_notifications import EmailNotifications
from .engine_config import EngineConfig
from .engine_config_import_summary import EngineConfigImportSummary
from .engine_name import EngineName
from .error import Error
from .experiment import Experiment
from .experiment_parameters import ExperimentParameters
from .experiment_patch import ExperimentPatch
from .experiment_patch_parameters import ExperimentPatchParameters
from .format_binary_form import FormatBinaryForm
from .format_documents_with_many import FormatDocumentsWithMany
from .format_text_with_many import FormatTextWithMany
from .formatter import Formatter
from .formatter_parameters import FormatterParameters
from .gazetteer import Gazetteer
from .gazetteer_parameters import GazetteerParameters
from .gazetteer_patch import GazetteerPatch
from .gazetteer_patch_parameters import GazetteerPatchParameters
from .generated_label_hint import GeneratedLabelHint
from .get_app_state_response_200 import GetAppStateResponse200
from .get_engine_parameters_schema_response_200 import GetEngineParametersSchemaResponse200
from .get_generated_label_names_response_200_item import GetGeneratedLabelNamesResponse200Item
from .get_project_engine_parameters_schema_response_200 import GetProjectEngineParametersSchemaResponse200
from .get_project_messages_scopes_item import GetProjectMessagesScopesItem
from .get_segment_context_context_output import GetSegmentContextContextOutput
from .get_services_distinct_values_response_200_item import GetServicesDistinctValuesResponse200Item
from .get_suggestions_response_200 import GetSuggestionsResponse200
from .group_desc import GroupDesc
from .group_name import GroupName
from .group_patch import GroupPatch
from .group_share import GroupShare
from .http_service_metadata import HttpServiceMetadata
from .http_service_metadata_operations import HttpServiceMetadataOperations
from .http_service_record import HttpServiceRecord
from .import_archive_multipart_data import ImportArchiveMultipartData
from .import_models_multipart_data import ImportModelsMultipartData
from .input_document import InputDocument
from .input_document_metadata import InputDocumentMetadata
from .input_label import InputLabel
from .job_status import JobStatus
from .job_type import JobType
from .label import Label
from .label_count import LabelCount
from .label_names import LabelNames
from .label_set import LabelSet
from .label_set_update import LabelSetUpdate
from .label_update import LabelUpdate
from .launch_document_import_multipart_data import LaunchDocumentImportMultipartData
from .launch_document_import_segmentation_policy import LaunchDocumentImportSegmentationPolicy
from .launch_project_restoration_from_backup_multipart_data import LaunchProjectRestorationFromBackupMultipartData
from .launch_uploaded_document_import_segmentation_policy import LaunchUploadedDocumentImportSegmentationPolicy
from .lexicon import Lexicon
from .lexicon_update import LexiconUpdate
from .localized_message import LocalizedMessage
from .maybe_create_projects_and_import_models_from_archive_multipart_data import (
    MaybeCreateProjectsAndImportModelsFromArchiveMultipartData,
)
from .message import Message
from .message_id import MessageId
from .message_localized import MessageLocalized
from .message_mark import MessageMark
from .message_patch import MessagePatch
from .message_patch_localized import MessagePatchLocalized
from .metadata_count import MetadataCount
from .metadata_definition import MetadataDefinition
from .metadata_definition_entry import MetadataDefinitionEntry
from .model_metrics import ModelMetrics
from .model_metrics_options import ModelMetricsOptions
from .models_metrics import ModelsMetrics
from .named_annotation_plan import NamedAnnotationPlan
from .new_campaign import NewCampaign
from .new_campaign_session import NewCampaignSession
from .new_campaign_session_mode import NewCampaignSessionMode
from .new_campaign_user_session import NewCampaignUserSession
from .new_experiment import NewExperiment
from .new_experiment_parameters import NewExperimentParameters
from .new_gazetteer import NewGazetteer
from .new_gazetteer_parameters import NewGazetteerParameters
from .new_group_desc import NewGroupDesc
from .new_message import NewMessage
from .new_message_localized import NewMessageLocalized
from .new_named_annotation_plan import NewNamedAnnotationPlan
from .new_role import NewRole
from .new_suggester import NewSuggester
from .new_suggester_parameters import NewSuggesterParameters
from .new_user import NewUser
from .next_step import NextStep
from .operation_count import OperationCount
from .partial_label import PartialLabel
from .partial_lexicon import PartialLexicon
from .plan_patch import PlanPatch
from .project_annotators import ProjectAnnotators
from .project_bean import ProjectBean
from .project_config_creation import ProjectConfigCreation
from .project_config_creation_properties import ProjectConfigCreationProperties
from .project_open_session import ProjectOpenSession
from .project_open_session_state import ProjectOpenSessionState
from .project_property import ProjectProperty
from .project_status import ProjectStatus
from .projects_annotators import ProjectsAnnotators
from .quality_figures import QualityFigures
from .relation import Relation
from .report import Report
from .report_classes import ReportClasses
from .request_jwt_token_project_access_mode import RequestJwtTokenProjectAccessMode
from .role_desc import RoleDesc
from .role_update import RoleUpdate
from .search_total import SearchTotal
from .search_total_relation import SearchTotalRelation
from .segment import Segment
from .segment_context import SegmentContext
from .segment_contexts import SegmentContexts
from .segment_hit import SegmentHit
from .segment_hits import SegmentHits
from .segment_metadata import SegmentMetadata
from .session_corpus_permission_change import SessionCorpusPermissionChange
from .share_mode import ShareMode
from .sherpa_job_bean import SherpaJobBean
from .sherpa_job_bean_status import SherpaJobBeanStatus
from .sherpa_job_bean_type import SherpaJobBeanType
from .simple_metadata import SimpleMetadata
from .suggester import Suggester
from .suggester_parameters import SuggesterParameters
from .suggester_patch import SuggesterPatch
from .suggester_patch_parameters import SuggesterPatchParameters
from .suggestion_facets import SuggestionFacets
from .term_hit import TermHit
from .term_hit_term import TermHitTerm
from .term_hits import TermHits
from .term_identifier import TermIdentifier
from .term_import import TermImport
from .term_importer_spec import TermImporterSpec
from .term_importer_spec_parameters import TermImporterSpecParameters
from .text_count import TextCount
from .upload_files_multipart_data import UploadFilesMultipartData
from .uploaded_file import UploadedFile
from .uploaded_file_info import UploadedFileInfo
from .user_permissions_update import UserPermissionsUpdate
from .user_profile import UserProfile
from .user_profile_update import UserProfileUpdate
from .user_response import UserResponse
from .user_session_action_action import UserSessionActionAction
from .user_session_state import UserSessionState
from .with_annotator import WithAnnotator
from .with_annotator_condition import WithAnnotatorCondition
from .with_annotator_parameters import WithAnnotatorParameters
from .with_processor import WithProcessor
from .with_processor_condition import WithProcessorCondition
from .with_processor_parameters import WithProcessorParameters
from .with_sentencizer import WithSentencizer
from .with_sentencizer_condition import WithSentencizerCondition
from .with_sentencizer_parameters import WithSentencizerParameters

__all__ = (
    "Ack",
    "Aggregation",
    "AnnotateBinaryForm",
    "AnnotateBinaryWithPlanRefMultipartData",
    "AnnotatedDocAnnotation",
    "AnnotatedDocAnnotationCreationMode",
    "AnnotatedDocAnnotationProperties",
    "AnnotatedDocCategory",
    "AnnotatedDocCategoryCreationMode",
    "AnnotatedDocCategoryProperties",
    "AnnotatedDocument",
    "AnnotatedDocumentMetadata",
    "AnnotateDocumentsWithMany",
    "AnnotateFormatBinaryWithPlanRefMultipartData",
    "AnnotateTextWithMany",
    "Annotation",
    "AnnotationCreationMode",
    "AnnotationFacets",
    "AnnotationId",
    "AnnotationMetrics",
    "AnnotationPatch",
    "AnnotationPatchStatus",
    "AnnotationPlan",
    "AnnotationStatus",
    "AnnotationTerm",
    "AnnotationTermProperties",
    "Annotator",
    "AnnotatorMultimap",
    "ApplyTo",
    "BearerToken",
    "Bucket",
    "Campaign",
    "CampaignId",
    "CampaignPatch",
    "CampaignRolesChange",
    "CampaignSession",
    "CampaignSessionMode",
    "CampaignUserGroup",
    "CampaignUserSession",
    "CampaignUserSessionState",
    "CategoriesFacets",
    "Category",
    "CategoryAction",
    "CategoryCreationMode",
    "CategoryId",
    "CategoryMetrics",
    "CategoryPatch",
    "CategoryPatchStatus",
    "CategoryStatus",
    "ClassificationConfig",
    "ClassificationOptions",
    "ConfigPatchOptions",
    "ConvertAnnotationPlan",
    "Converter",
    "ConverterParameters",
    "ConvertFormatAnnotationPlan",
    "CorpusMetrics",
    "CreatedByCount",
    "CreateLexiconResponse200",
    "CreateProjectFromArchiveMultipartData",
    "CreateTermJsonBody",
    "CreateTermResponse200",
    "CreationMode",
    "Credentials",
    "DeleteGroupResult",
    "DeleteResponse",
    "DependsOn",
    "DocAltText",
    "DocAnnotation",
    "DocAnnotationCreationMode",
    "DocAnnotationStatus",
    "DocCategory",
    "DocCategoryCreationMode",
    "DocCategoryStatus",
    "DocSentence",
    "DocSentenceMetadata",
    "Document",
    "DocumentFacets",
    "DocumentHit",
    "DocumentHits",
    "DocumentMetadata",
    "EmailNotifications",
    "EngineConfig",
    "EngineConfigImportSummary",
    "EngineName",
    "Error",
    "Experiment",
    "ExperimentParameters",
    "ExperimentPatch",
    "ExperimentPatchParameters",
    "FormatBinaryForm",
    "FormatDocumentsWithMany",
    "Formatter",
    "FormatterParameters",
    "FormatTextWithMany",
    "Gazetteer",
    "GazetteerParameters",
    "GazetteerPatch",
    "GazetteerPatchParameters",
    "GeneratedLabelHint",
    "GetAppStateResponse200",
    "GetEngineParametersSchemaResponse200",
    "GetGeneratedLabelNamesResponse200Item",
    "GetProjectEngineParametersSchemaResponse200",
    "GetProjectMessagesScopesItem",
    "GetSegmentContextContextOutput",
    "GetServicesDistinctValuesResponse200Item",
    "GetSuggestionsResponse200",
    "GroupDesc",
    "GroupName",
    "GroupPatch",
    "GroupShare",
    "HttpServiceMetadata",
    "HttpServiceMetadataOperations",
    "HttpServiceRecord",
    "ImportArchiveMultipartData",
    "ImportModelsMultipartData",
    "InputDocument",
    "InputDocumentMetadata",
    "InputLabel",
    "JobStatus",
    "JobType",
    "Label",
    "LabelCount",
    "LabelNames",
    "LabelSet",
    "LabelSetUpdate",
    "LabelUpdate",
    "LaunchDocumentImportMultipartData",
    "LaunchDocumentImportSegmentationPolicy",
    "LaunchProjectRestorationFromBackupMultipartData",
    "LaunchUploadedDocumentImportSegmentationPolicy",
    "Lexicon",
    "LexiconUpdate",
    "LocalizedMessage",
    "MaybeCreateProjectsAndImportModelsFromArchiveMultipartData",
    "Message",
    "MessageId",
    "MessageLocalized",
    "MessageMark",
    "MessagePatch",
    "MessagePatchLocalized",
    "MetadataCount",
    "MetadataDefinition",
    "MetadataDefinitionEntry",
    "ModelMetrics",
    "ModelMetricsOptions",
    "ModelsMetrics",
    "NamedAnnotationPlan",
    "NewCampaign",
    "NewCampaignSession",
    "NewCampaignSessionMode",
    "NewCampaignUserSession",
    "NewExperiment",
    "NewExperimentParameters",
    "NewGazetteer",
    "NewGazetteerParameters",
    "NewGroupDesc",
    "NewMessage",
    "NewMessageLocalized",
    "NewNamedAnnotationPlan",
    "NewRole",
    "NewSuggester",
    "NewSuggesterParameters",
    "NewUser",
    "NextStep",
    "OperationCount",
    "PartialLabel",
    "PartialLexicon",
    "PlanPatch",
    "ProjectAnnotators",
    "ProjectBean",
    "ProjectConfigCreation",
    "ProjectConfigCreationProperties",
    "ProjectOpenSession",
    "ProjectOpenSessionState",
    "ProjectProperty",
    "ProjectsAnnotators",
    "ProjectStatus",
    "QualityFigures",
    "Relation",
    "Report",
    "ReportClasses",
    "RequestJwtTokenProjectAccessMode",
    "RoleDesc",
    "RoleUpdate",
    "SearchTotal",
    "SearchTotalRelation",
    "Segment",
    "SegmentContext",
    "SegmentContexts",
    "SegmentHit",
    "SegmentHits",
    "SegmentMetadata",
    "SessionCorpusPermissionChange",
    "ShareMode",
    "SherpaJobBean",
    "SherpaJobBeanStatus",
    "SherpaJobBeanType",
    "SimpleMetadata",
    "Suggester",
    "SuggesterParameters",
    "SuggesterPatch",
    "SuggesterPatchParameters",
    "SuggestionFacets",
    "TermHit",
    "TermHits",
    "TermHitTerm",
    "TermIdentifier",
    "TermImport",
    "TermImporterSpec",
    "TermImporterSpecParameters",
    "TextCount",
    "UploadedFile",
    "UploadedFileInfo",
    "UploadFilesMultipartData",
    "UserPermissionsUpdate",
    "UserProfile",
    "UserProfileUpdate",
    "UserResponse",
    "UserSessionActionAction",
    "UserSessionState",
    "WithAnnotator",
    "WithAnnotatorCondition",
    "WithAnnotatorParameters",
    "WithProcessor",
    "WithProcessorCondition",
    "WithProcessorParameters",
    "WithSentencizer",
    "WithSentencizerCondition",
    "WithSentencizerParameters",
)
