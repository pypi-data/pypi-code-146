import enum


class EPMAttachmentType(enum.IntEnum):
    """ Necessary when using WorkflowService#createInstance or WorkflowService#addAttachments """

    EPM_target_attachment = 1
    EPM_reference_attachment = 3
    EPM_signoff_attachment = 4
    EPM_release_status_attachment = 5
    EPM_comment_attachment = 6
    EPM_instruction_attachment = 7
    EPM_interprocess_task_attachment = 8
    EPM_schedule_task_attachment = 9
    EPM_replica_target_attachment = 10
    EPM_user_attachment = 1000


class EPMAttachmentType2(enum.Enum):
    """ Necessary when using WorkflowService.createWorkflow or WorkflowService#createRemoteWorkflowAsync """

    EPM_ATT_TARGET = "target"
    EPM_ATT_REFERENCE = "reference"
    EPM_ATT_PROCESS = "process"
    EPM_ATT_SIGNOFF = "signoff"
    EPM_ATT_COMMENT = "comment"
    EPM_ATT_INSTRUCTION = "instruction"
    EPM_ATT_INTERPROCESS_TASK = "interprocess_task"
    EPM_ATT_SCHEDULE_TASK = "schedule_task"
    EPM_ATT_BOTH = "both"
    EPM_ATT_ALL = "all"


class EPMConditionTask(enum.IntEnum):
    EPM_RESULT_FALSE = 0
    EPM_RESULT_TRUE = 1
    EPM_RESULT_UNSET = 2


class RelationTypes(enum.Enum):
    EPM_TEMPLATE_BASED_ON_RELATION_TYPE = "EPM_template_based_on"
    EPM_SIGNOFF_PROFILE_RELATION_TYPE = "EPM_signoff_profile"
    SUBSCRIBED_REMOTEINBOXES_RELATION_TYPE = "subscribed_remoteinboxes"
