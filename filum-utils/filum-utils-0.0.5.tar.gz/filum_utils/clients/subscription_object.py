from abc import abstractmethod, ABC
from typing import Callable, List, Any, Dict, Optional, TypedDict

from glom import glom

from filum_utils.clients.action import ActionClient, ActionError
from filum_utils.clients.filum import FilumClient
from filum_utils.clients.log import LogClient, LogType
from filum_utils.clients.notification import (
    NotificationClient,
    PublisherType,
    RoutePath,
    NOTIFICATION_ERROR_MESSAGE_MAPPINGS,
)
from filum_utils.clients.subscription import SubscriptionClient
from filum_utils.config import config
from filum_utils.enums import ParentType


class ProcessFunctionResponse(TypedDict):
    success_count: int
    errors: List[Dict[str, Any]]


class TriggerFunctionResponse(TypedDict):
    is_finished: bool


ActionType = Dict[str, Any]
AutomatedActionType = Dict[str, Any]
CampaignType = Dict[str, Any]
EventType = Optional[Dict[str, Any]]
SegmentType = Optional[Dict[str, Any]]
UserType = Optional[Dict[str, Any]]
SubscriptionDataType = Optional[Dict[str, Any]]


class BaseSubscriptionObjectClient(ABC):
    def __init__(self, subscription_id: int):
        self.subscription_client = SubscriptionClient(subscription_id)
        self.action_client = ActionClient(action_id=self.subscription_client.get_action_id())
        self.filum_client = FilumClient()
        self.log_client = LogClient()
        self.notification_client = NotificationClient()

    @property
    @abstractmethod
    def object(self):
        ...

    def get_object_source_type(self):
        object_source = self.object.get("source") or {}
        return object_source.get("type")

    @abstractmethod
    def update_object_status(self, status: str):
        ...

    def get_action_data(self, key):
        return self.action_client.get_data(key)

    def update_action_data(self, updated_data: Dict[str, Any]):
        return self.action_client.update_data(updated_data)

    def get_subscription_data(self):
        return self.subscription_client.get_data()

    def update_subscription_data(self, updated_data: Dict[str, Any]):
        self.subscription_client.update_data(updated_data)

    @abstractmethod
    def handle_trigger_failed(self, error: ActionError, notify: bool):
        ...

    @abstractmethod
    def handle_transactional_trigger(
        self, process_transactional_fn: Callable, events: List[Dict[str, Any]]
    ) -> TriggerFunctionResponse:
        ...

    @abstractmethod
    def handle_segment_users_on_demand_trigger(
        self,
        process_segment_user_fn: Callable,
        properties: List[str] = None,
        required_properties: List[List[str]] = None
    ) -> TriggerFunctionResponse:
        ...

    @abstractmethod
    def handle_segment_on_demand_trigger(self, process_segment_fn: Callable) -> TriggerFunctionResponse:
        ...

    def _get_object_source_data(self):
        object_source = self.object.get("source") or {}
        return object_source.get("data") or {}

    @abstractmethod
    def _get_object_route(self):
        ...

    def _log(self, parent_type: str, type: str, code: str, title: str, subtitle: str, data: str = None):
        self.log_client.create_log(
            parent_type=parent_type,
            parent_id=self.object["id"],
            type=type,
            code=code,
            title=title,
            subtitle=subtitle,
            data=data,
            member_account_id=self.object.get("member_account_id"),
            member_organization_id=self.object.get("organization_id"),
        )

    def _notify(self, publisher_type: str, title: str, subtitle: str):
        self.notification_client.create_notification(
            publisher_type=publisher_type,
            title=title,
            subtitle=subtitle,
            route=self._get_object_route(),
            member_account_id=self.object.get("member_account_id"),
            member_organization_id=self.object.get("organization_id"),
        )


class AutomatedActionClient(BaseSubscriptionObjectClient):
    def __init__(self, subscription_id: int):
        super().__init__(subscription_id)
        self.automated_action = self.filum_client.get_automated_action(self.subscription_client.get_object_id())

    @property
    def object(self):
        return self.automated_action

    def update_object_status(self, status: str):
        self.filum_client._request(
            endpoint=f"/internal/automated-actions/{self.automated_action['id']}/status",
            method="PUT",
            data={
                "status": status
            }
        )

    def handle_trigger_failed(self, error: ActionError, notify: bool):
        self._log(
            parent_type=ParentType.AUTOMATED_ACTION,
            type=LogType.ERROR,
            code="400",
            title="An error occurred when triggering your action, please contact Filum for support.",
            subtitle=error["message"],
            data=error["data"],
        )

        if notify:
            self._notify(
                publisher_type=PublisherType.AUTOMATED_ACTION,
                title=f"{self.automated_action.get('name')} failed to run",
                subtitle=error.get("notification_message") or NOTIFICATION_ERROR_MESSAGE_MAPPINGS[error["type"]],
            )

    def handle_transactional_trigger(
        self,
        process_transactional_fn: Callable[
            [ActionType, AutomatedActionType, EventType, SubscriptionDataType],
            ProcessFunctionResponse
        ],
        events: List[Dict[str, Any]]
    ) -> TriggerFunctionResponse:
        for event in events:
            data = {
                "action": self.action_client.action,
                "automated_action": self.automated_action,
                "data": event,
                "subscription_data": self.get_subscription_data()
            }
            process_transactional_fn(**data)

        return {"is_finished": True}

    def handle_segment_users_on_demand_trigger(
        self,
        process_segment_user_fn: Callable[
            [ActionType, AutomatedActionType, UserType, SubscriptionDataType],
            ProcessFunctionResponse
        ],
        properties: List[str] = None,
        required_properties: List[List[str]] = None
    ) -> TriggerFunctionResponse:
        subscription_data = self.get_subscription_data()
        current_index = subscription_data.get("last_current_index") or 0

        source_data = self._get_object_source_data()

        users = self.filum_client.get_user_csv_reader(
            properties=properties,
            object_ids=[source_data.get("segment_id")],
            object_type="segment",
            organization=self.subscription_client.get_organization(),
            required_properties=required_properties,
            offset=current_index,
            limit=config.SEGMENT_RECORD_LIMIT
        )

        total_processed_users = 0
        for user in users:
            current_index += 1
            total_processed_users += 1
            data = {
                "action": self.action_client.action,
                "automated_action": self.automated_action,
                "data": user,
                "subscription_data": subscription_data
            }
            process_segment_user_fn(**data)

        if total_processed_users >= config.SEGMENT_RECORD_LIMIT:
            self.update_subscription_data({"last_current_index": current_index})
            self.action_client.sync({
                "subscription_id": self.subscription_client.subscription["id"]
            })

            return {"is_finished": False}

        return {"is_finished": True}

    def handle_segment_on_demand_trigger(self, process_segment_fn: Callable[
        [ActionType, AutomatedActionType, SegmentType, SubscriptionDataType],
        ProcessFunctionResponse
    ]) -> TriggerFunctionResponse:
        source_data = self._get_object_source_data()

        segment = self.filum_client.get_segment(
            segment_id=source_data.get("segment_id"),
            organization=self.subscription_client.get_organization()
        )

        data = {
            "action": self.action_client.action,
            "automated_action": self.automated_action,
            "data": segment,
            "subscription_data": self.get_subscription_data()
        }

        process_segment_fn(**data)

        return {"is_finished": True}

    def _get_object_route(self):
        return {
            "path": RoutePath.AUTOMATED_ACTIONS_DETAIL,
            "params": {
                "automatedActionId": self.automated_action["id"]
            }
        }


class CampaignClient(BaseSubscriptionObjectClient):
    def __init__(self, subscription_id: int):
        super().__init__(subscription_id)
        self.campaign = self.filum_client.get_campaign(self.subscription_client.get_object_id())

    @property
    def object(self):
        return self.campaign

    def get_run_type(self):
        return self.campaign.get("run_type")

    def get_segment_id(self):
        return self.campaign.get("segment_id")

    def get_template(self):
        campaign_survey = self.object and self.object.get("survey")
        action_id = self.action_client.action['id']

        template = glom(campaign_survey, f"action_data.{action_id}", default=None)
        if not template:
            template = glom(self.object, f"action_input_data.{action_id}", default=None)

        if template and template["status"] == "active":
            return template

        return None

    def get_template_third_party_id(self):
        template = self.get_template()
        return template and template.get("third_party_id")

    def update_object_status(self, status: str):
        self.filum_client._request(
            endpoint=f"/internal/survey-campaigns/{self.campaign['id']}/status",
            method="PUT",
            data={
                "status": status
            }
        )

    def handle_trigger_failed(self, error: ActionError, notify: bool = False):
        self._log(
            parent_type=ParentType.CAMPAIGN,
            type=LogType.ERROR,
            code="400",
            title="An error occurred when triggering your action, please contact Filum for support.",
            subtitle=error["message"],
            data=error["data"],
        )

        if notify:
            self._notify(
                publisher_type=PublisherType.FEEDBACK_360,
                title=f"{self.campaign.get('name')} failed to run",
                subtitle=error.get("notification_message") or NOTIFICATION_ERROR_MESSAGE_MAPPINGS[error["type"]],
            )

    def handle_transactional_trigger(
        self,
        process_transactional_fn: [
            [ActionType, CampaignType, EventType, SubscriptionDataType],
            ProcessFunctionResponse
        ],
        events: List[Dict[str, Any]],
        connections: List[Dict[str, Any]] = None
    ) -> TriggerFunctionResponse:
        for event in events:
            data = {
                "action": self.action_client.action,
                "campaign": self.campaign,
                "data": event,
                "subscription_data": self.get_subscription_data(),
                "connections": connections
            }
            process_transactional_fn(**data)

        return {"is_finished": True}

    def handle_segment_users_on_demand_trigger(
        self,
        process_segment_user_fn: [
            [ActionType, CampaignType, UserType, SubscriptionDataType],
            ProcessFunctionResponse
        ],
        properties: List[str] = None,
        required_properties: List[List[str]] = None,
        connections: List[Dict[str, Any]] = None
    ) -> TriggerFunctionResponse:
        subscription_data = self.get_subscription_data()
        current_index = subscription_data.get("last_current_index") or 0

        users = self.filum_client.get_user_csv_reader(
            properties=properties,
            object_ids=[self.get_segment_id()],
            object_type="segment",
            organization=self.subscription_client.get_organization(),
            required_properties=required_properties,
            offset=current_index,
            limit=config.SEGMENT_RECORD_LIMIT
        )

        total_processed_users = 0
        for user in users:
            current_index += 1
            total_processed_users += 1
            data = {
                "action": self.action_client.action,
                "campaign": self.campaign,
                "data": user,
                "subscription_data": subscription_data,
                "connections": connections
            }
            process_segment_user_fn(**data)

        if total_processed_users >= config.SEGMENT_RECORD_LIMIT:
            self.action_client.update_data({"last_current_index": current_index})
            self.action_client.sync({
                "subscription_id": self.subscription_client.subscription["id"]
            })

            return {"is_finished": False}

        return {"is_finished": True}

    def handle_segment_on_demand_trigger(self, process_segment_fn: Callable[
        [ActionType, CampaignType, SegmentType, SubscriptionDataType],
        ProcessFunctionResponse
    ]) -> TriggerFunctionResponse:
        ...

    def _get_object_route(self):
        return {
            "path": RoutePath.CAMPAIGNS_DETAIL,
            "params": {
                "solutionGroup": "cx",
                "solutionSlug": "feedback360",
                "campaignId": self.campaign["id"]
            }
        }
