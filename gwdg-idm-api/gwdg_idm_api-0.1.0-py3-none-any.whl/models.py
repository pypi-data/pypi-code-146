import os
import json
import logging
import typing

import pydantic
import requests

from .util import IDMNotReachableError

if typing.TYPE_CHECKING:
    from requests import Response


__all__ = ["BaseGWDGUser"]


DATA_TYPE = str | list | dict | None


class IDMRequest(pydantic.BaseModel):
    username: str
    password: str
    api_url: str = os.environ["IDM_API_URL"]

    def run_request(
        self, func: typing.Callable[..., "Response"], url: str, data: DATA_TYPE = None
    ) -> "Response":
        try:
            return func(
                url,
                auth=(self.username, self.password),
                timeout=60,  # Needs to be this high to allow for an all-objects query
                headers={
                    "Accept": "application/json",
                    "Accept-Language": "en",
                    "Content-Type": "application/json",
                },
                data=data,
            )
        except Exception as e:
            raise IDMNotReachableError(
                f"Could not connect to IDM: IDM not reachable!\n{e}"
            )

    def get_request(self, url: str) -> "Response":
        return self.run_request(requests.get, url)

    def put_request(self, url: str, data: DATA_TYPE) -> "Response":
        return self.run_request(requests.put, url, data)

    def post_request(self, url: str, data: DATA_TYPE) -> "Response":
        return self.run_request(requests.post, url, data)


class ChangeTemplate(pydantic.BaseModel):
    id: str
    goesternExpirationDate: str = ""
    isScheduledForDeletion: str = ""
    goesternUserStatus: str = ""

    @staticmethod
    def update_json(name: str, value: str | list[str]) -> str:
        data = {
            "name": name,
            "value": [value] if not isinstance(value, list) else value,
        }
        return json.dumps({"attributes": [data]})

    @classmethod
    def from_json(cls, json: dict) -> "ChangeTemplate":
        response_dict: dict[str, list[str] | str]

        response_dict = {
            "id": [json["id"]],
            "dn": [json["dn"]],
        }
        response_dict.update(
            {entry["name"]: entry["value"] for entry in json["attributes"]}
        )

        remove_keys = []
        for key, value in response_dict.items():
            try:
                expected_type = type(cls.__fields__[key].outer_type_())
            except KeyError:
                remove_keys.append(key)
                logging.debug(
                    "\n"
                    "  key unknown to model\n"
                    f"  User: {response_dict['id']}\n"
                    f"  Key: {key}"
                    f"  Value: {value}"
                )
                continue
            if isinstance(value, expected_type):
                continue

            if isinstance(value, expected_type):
                continue
            elif expected_type is str and isinstance(value, list):
                if len(value) > 1:
                    logging.warning(
                        "\n"
                        "  str expected, but found list: Using first element\n"
                        "  Please check your class specifications.\n"
                        f"  User: {response_dict['id']}\n"
                        f"  Key: {key}"
                        f"  Value: {value}"
                    )
                try:
                    new_val: str = value[0]
                except IndexError:
                    logging.warning(
                        "  str expected, but empty list found: Set to empty string\n"
                        "  Please check your class specifications.\n"
                        f"  User: {response_dict['id']}\n"
                        f"  Key: {key}"
                        f"  Value: {value}"
                    )
                    new_val: str = ""
                response_dict[key] = new_val
            else:
                assert False, (
                    "  Only str and list types are supported so far!"
                    "  Please check your class specifications.\n"
                    f"  User: {response_dict['id']}\n"
                    f"  Key: {key}"
                    f"  Value: {value}"
                )

        return cls(**{key: value for key, value in response_dict.items() if key not in set(remove_keys)})  # type: ignore


class CreateTemplate(pydantic.BaseModel):
    create_template_name: str

    def to_json(self) -> str:
        data = [
            {
                "name": key.removeprefix("_"),
                "value": [value] if not isinstance(value, list) else value,
            }
            for key, value in self.dict().items()
            if key != "create_template_name"
        ]
        return json.dumps({"attributes": data})


class BaseGWDGUser(ChangeTemplate):
    # Common fields
    ou: str = ""
    employeeNumber: str = ""
    mpgEmployeeNumber: str = ""
    employeeType: str = ""
    employeeStatus: str = ""
    accountType: str = ""
    uid: str = ""
    oldUid: list[str] = []
    goesternSAMAccountName: str = ""
    ou: str = ""
    goesternUserType: str = ""
    givenName: str = ""
    sn: str = ""
    goesternGWDGadDisplayName: str = ""
    description: str = ""
    departmentNumber: str = ""
    title: str = ""
    telephoneNumber: str = ""
    mobile: str = ""
    facsimileTelephoneNumber: str = ""
    roomNumber: str = ""
    street: str = ""
    postalCode: str = ""
    city: str = ""
    st: str = ""
    l: str = ""
    goesternProxyAddresses: list[str] = []
    mail: str = ""
    goesternExchangeQuota: str = ""
    goesternMailboxServer: str = ""
    goesternMailboxZugehoerigkeit: str = ""
    exchangeTargetAddress: str = ""
    goesternMailRoutingAddresses: list[str] = []
    goesternExchHideFromAddressLists: str = ""
    externalEmailAddress: list[str] = []
    filterAttribute1: list[str] = []
    filterAttribute2: list[str] = []
    filterAttribute3: list[str] = []
    goesternDisableReason: str = ""
    goesternDisableDate: str = ""
    goesternRemoveDate: str = ""
    goesternLockoutTime: str = ""
    ownCloudQuota: str = ""
    memberOfStaticExchangeDistGrp: list[str] = []
    isInitialPassword: str = ""
    createTimestamp: str = ""
    modifyTimeStamp: str = ""
    pwdChangedTime: str = ""
    passwordExpirationTime: str = ""
    isInitialAdditionalPassword: str = ""
    additionalPasswordModifyTime: str = ""
    additionalPasswordExpirationTime: str = ""
    eduPersonPrincipalName: str = ""
    effectivePrivilege: list[str] = []
    responsiblePerson: list[str] = []
