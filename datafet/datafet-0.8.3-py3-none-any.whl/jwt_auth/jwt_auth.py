import base64
import logging
import os
import random
import sys
import time
from datetime import datetime, timedelta
from hashlib import sha256
from typing import Any, Dict, List, Union

import boto3
import ecdsa
import jwt
import spookyhash
from botocore.client import Config as Boto3Config
from ecdsa import SigningKey, VerifyingKey
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from jinja2 import Template
from mypy_boto3_secretsmanager import SecretsManagerClient
from mypy_boto3_s3.type_defs import PutObjectOutputTypeDef
from pydantic import EmailStr


from ..aws_operations import (
    get_secret_binary,
    s3_get_object_bytes,
    s3_put_object_bytes,
    ses_send_email,
)
from ..custom_types import (
    AuthClients,
    AuthConfig,
    CustomError,
    HttpError,
    HttpSuccess,
    JwtParam,
    LoginHash,
    MagicLinkDomain,
    MagicLinkDto,
    MagicLinkInternal,
    RoleEnum,
    WhoAmI,
    UserEmailAndId,
    EmailDomainAndOrgId,
    CategorySummary,
    CategorySummaries,
    EvaluationSummary,
    EvaluationSummaries,
)
from ..eid import get_org_eid, get_user_eid
from ..http_return import (
    http_200_json,
    http_400_json,
    http_403_json,
    http_500_json,
    http_error,
    http_error_to_json_response,
)

LOG: logging.Logger = logging.getLogger(__name__)


class Auth:

    default_algorithm: str = "ES256"
    default_boto3_config: Boto3Config = Boto3Config(
        connect_timeout=5, read_timeout=5, region_name="eu-west-1"
    )
    clients: AuthClients = AuthClients(
        s3_client=boto3.client("s3", config=default_boto3_config),
        s3_resource=boto3.resource("s3", config=default_boto3_config),
        sqs_client=boto3.client(
            "sqs", endpoint_url="https://sqs.eu-west-1.amazonaws.com"
        ),
        secretsmanager_client=boto3.client(
            "secretsmanager", config=default_boto3_config
        ),
        glue_client=boto3.client("glue", config=default_boto3_config),
        ses_client=boto3.client("ses", config=default_boto3_config),
        athena_client=boto3.client("athena", config=default_boto3_config),
    )
    config: AuthConfig = None
    boto3_config: Boto3Config = None
    router: APIRouter = None

    def __init__(self, config: AuthConfig, boto3_config=default_boto3_config):

        self.config: AuthConfig = config
        self.boto3_config = boto3_config
        self.router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
        self.router.add_api_route(
            path="/magic-link",
            endpoint=self.send_magic_link,
            methods=["POST"],
            response_model=HttpSuccess,
        )
        self.router.add_api_route(
            path="/login",
            endpoint=self.login,
            methods=["POST"],
            response_model=HttpSuccess,
        )
        self.router.add_api_route(
            path="/logout",
            endpoint=self.logout,
            methods=["POST"],
            response_model=HttpSuccess,
        )
        self.router.add_api_route(
            path="/who-am-i",
            endpoint=self.get_who_am_i,
            methods=["GET"],
            response_model=WhoAmI,
        )

    @staticmethod
    def get_signing_key(
        secrets_manager_client: SecretsManagerClient, secret_id: str
    ) -> Union[SigningKey, HttpError]:
        try:
            signing_key_b64_maybe = get_secret_binary(
                secrets_manager_client=secrets_manager_client, secret_id=secret_id
            )
            if isinstance(signing_key_b64_maybe, HttpError):
                return signing_key_b64_maybe
            signing_key_der = base64.b64decode(signing_key_b64_maybe)
            return ecdsa.SigningKey.generate().from_der(signing_key_der)
        except Exception as ex:
            return http_error(
                status_code=500,
                message="SigningKey Error",
                reasons=[
                    f"Could not fetch signing key: {secret_id} and a Exception happened: {ex}"
                ],
            )

    @staticmethod
    def create_jwt(
        jwt_param: JwtParam,
        signing_key: SigningKey,
        audience: str,
        issuer: str,
        exp_days: int,
        algorithm="ES256",
    ) -> Union[str, CustomError]:
        try:
            now = int(time.time())
            expiry = now + exp_days * 24 * 60 * 60
            return jwt.encode(
                {
                    "aud": audience,
                    "email": jwt_param.email,
                    "exp": expiry,
                    "first_name": jwt_param.first_name,
                    "iat": now,
                    "iss": issuer,
                    "nbf": now,
                    "role": jwt_param.role,
                    "org_id": jwt_param.org_id,
                    "user_id": jwt_param.user_id,
                },
                signing_key.to_pem(),
                algorithm=algorithm,
            )
        except Exception as ex:
            return CustomError(message="JWT Encoding Error", reasons=[f"{ex}"])

    @staticmethod
    def decode_jwt(
        jwt_string: str, verifying_key: VerifyingKey, audience: str, algorithm="ES256"
    ) -> Union[Dict[str, Any], CustomError]:
        try:
            return jwt.decode(
                jwt=jwt_string,
                key=verifying_key.to_pem(),
                algorithms=[algorithm],
                audience=audience,
            )
        except Exception as ex:
            return CustomError(message="JWT Decoding Error", reasons=[f"{ex}"])

    @staticmethod
    def get_jwt_token_from_cookies(
        cookies: Dict[str, Any], jwt_name: str
    ) -> Union[str, CustomError]:
        return cookies.get(
            jwt_name,
            CustomError(
                message="Cookie Error", reasons=["Could not get JWT from cookies"]
            ),
        )

    @staticmethod
    def get_jwt_field_from_cookies(
        cookies: Dict[str, Any],
        jwt_name: str,
        verifying_key: VerifyingKey,
        audience: str,
        jwt_field_name: str,
    ) -> Union[str, CustomError]:
        try:
            jwt_token_maybe = Auth.get_jwt_token_from_cookies(cookies, jwt_name)
            if isinstance(jwt_token_maybe, CustomError):
                return jwt_token_maybe

            jwt_decoded_maybe = Auth.decode_jwt(
                jwt_token_maybe, verifying_key, audience
            )
            if isinstance(jwt_decoded_maybe, CustomError):
                return jwt_decoded_maybe

            return jwt_decoded_maybe.get(
                jwt_field_name,
                CustomError(
                    message="JWT Error",
                    reasons=["Could not get field from JWT token"],
                ),
            )
        except Exception as ex:
            return CustomError(
                message="JWT Error",
                reasons=[f"Could not get field from JWT token {ex}"],
            )

    @staticmethod
    def get_jwt_fields_from_cookies(
        cookies: Dict[str, Any],
        jwt_name: str,
        verifying_key: VerifyingKey,
        audience: str,
        jwt_field_names: List[str],
    ) -> Union[List[str], List[CustomError]]:
        try:

            jwt_token_maybe = Auth.get_jwt_token_from_cookies(cookies, jwt_name)
            if isinstance(jwt_token_maybe, CustomError):
                return [jwt_token_maybe]

            jwt_decoded_maybe = Auth.decode_jwt(
                jwt_token_maybe, verifying_key, audience
            )
            if isinstance(jwt_decoded_maybe, CustomError):
                return [jwt_decoded_maybe]

            return list(
                map(
                    lambda field_name: jwt_decoded_maybe.get(
                        field_name,
                        CustomError(
                            message="JWT Error",
                            reasons=[
                                f"Could not get field: {field_name} from JWT token"
                            ],
                        ),
                    ),
                    jwt_field_names,
                ),
            )

        except Exception as ex:
            return CustomError(
                message="JWT Error",
                reasons=[
                    f"Could not get fields: {jwt_field_names} from JWT token {ex}"
                ],
            )

    @staticmethod
    def get_user_email_from_cookies(
        cookies: Dict[str, Any],
        jwt_name: str,
        verifying_key: VerifyingKey,
        audience: str,
    ) -> Union[str, CustomError]:
        return Auth.get_jwt_field_from_cookies(
            cookies, jwt_name, verifying_key, audience, "email"
        )

    @staticmethod
    def get_user_role_from_cookies(
        cookies: Dict[str, Any],
        jwt_name: str,
        verifying_key: VerifyingKey,
        audience: str,
    ) -> Union[str, CustomError]:
        return Auth.get_jwt_field_from_cookies(
            cookies, jwt_name, verifying_key, audience, "role"
        )

    @staticmethod
    def get_cookie_domain_from_cors(cors_allow_origin: str) -> str:
        if "localhost" in cors_allow_origin:
            return "localhost"
        else:
            # This was not written by me.
            return f".{'.'.join(cors_allow_origin.split('/')[2].split(':')[0].split('.')[1:])}"

    def convert_magic_link_domain_to_internal(
        self, magic_link: MagicLinkDomain, source_ip: str
    ) -> MagicLinkInternal:
        random_bytes = random.randint(0, sys.maxsize).to_bytes(8, byteorder="little")
        hash_64_hex = (
            spookyhash.hash64(random_bytes, seed=1337)
            .to_bytes(8, byteorder="little")
            .hex()
        )
        data = f"{magic_link.email}-{self.config.cors_allow_origin}-{magic_link.now}-{hash_64_hex}"
        hash = sha256(data.encode("utf-8")).hexdigest()

        return MagicLinkInternal(magic_link=magic_link, hash=hash, source_ip=source_ip)

    def save_magic_link_internal_to_s3(
        self, magic_link_internal: MagicLinkInternal, utc_now_str: str
    ) -> Union[HttpSuccess, HttpError]:
        try:
            utc_now_str = datetime.now().strftime("%Y-%m-%dT%H:00:00Z")
            body_bytes = magic_link_internal.json().encode("utf-8")
            key = f"api/auth/login/{utc_now_str}/hash-{magic_link_internal.hash}.json"

            s3_success_maybe = s3_put_object_bytes(
                s3_client=Auth.clients.s3_client,
                s3_bucket=self.config.s3_bucket,
                s3_key=key,
                s3_body_bytes=body_bytes,
            )
            if isinstance(s3_success_maybe, HttpError):
                LOG.error(f"{s3_success_maybe.json()}")
                return s3_success_maybe

            return HttpSuccess(ok="ok")

        except Exception as ex:
            message, reasons = "Save MagicLinkInternal Error", [f"{ex}"]
            LOG.error(f"Error: {message} Reasons: {reasons}")
            return HttpError(
                status_code=500, error=CustomError(message=message, reasons=reasons)
            )

    def render_email_body(
        self,
        magic_link_internal: MagicLinkInternal,
    ) -> Union[str, CustomError]:
        try:
            name = magic_link_internal.magic_link.first_name
            email = magic_link_internal.magic_link.email
            link = (
                f"{self.config.cors_allow_origin}/login-hash/{magic_link_internal.hash}"
            )

            current_file_dir = os.path.dirname(os.path.realpath("__file__"))
            template_file = os.path.join(
                current_file_dir, "templates", "login_email.html"
            )
            with open(template_file) as f:
                rendered = Template(f.read()).render(name=name, email=email, link=link)

            return rendered

        except Exception as ex:
            message, reasons = f"Could not render template because of", [f"{ex}"]
            LOG.error(f"{message} {reasons}")
            return CustomError(message=message, reasons=reasons)

    def get_hash_from_s3(
        self, login_hash: LoginHash
    ) -> Union[MagicLinkInternal, HttpError]:
        try:

            def get_hash(key):
                return s3_get_object_bytes(
                    s3_client=Auth.clients.s3_client,
                    s3_bucket=self.config.s3_bucket,
                    s3_key=key,
                )

            time_format = "%Y-%m-%dT%H:00:00Z"
            now = datetime.now()
            this_hour = now.strftime(time_format)
            prev_hour = (now - timedelta(hours=1)).strftime(time_format)
            key_this_hour = f"api/auth/login/{this_hour}/hash-{login_hash.hash}.json"
            key_previous_hour = (
                f"api/auth/login/{prev_hour}/hash-{login_hash.hash}.json"
            )

            login_hash_maybe = b""
            this_hour_hash_maybe = get_hash(key=key_this_hour)
            if isinstance(this_hour_hash_maybe, HttpError):
                prev_hour_hash_maybe = get_hash(key=key_previous_hour)
                if isinstance(prev_hour_hash_maybe, HttpError):
                    LOG.error(
                        f"This hour hash: {this_hour_hash_maybe}"
                        f"Previous hour hash: {prev_hour_hash_maybe}"
                    )
                    return HttpError(
                        status_code=403,
                        error=CustomError(
                            message="S3 Error",
                            reasons=["Could not fetch login hash from S3"],
                        ),
                    )
                else:
                    login_hash_maybe = prev_hour_hash_maybe
            else:
                login_hash_maybe = this_hour_hash_maybe

            return MagicLinkInternal.parse_raw(login_hash_maybe)

        except Exception as ex:
            message, reasons = "Error while trying to process magic link", [f"{ex}"]
            LOG.error(f"Message: {message}. Reasons: {reasons}")
            return http_500_json(message=message, reasons=reasons)

    @staticmethod
    def magic_link_dto_to_domain(
        magic_link_dto: MagicLinkDto,
    ) -> Union[MagicLinkDomain, CustomError]:
        try:
            mld = magic_link_dto
            return MagicLinkDomain(
                email=EmailStr(mld.email),
                first_name=mld.firstName,
                accepted_terms_and_conditions=mld.acceptedTermsAndConditions,
                accepted_gdpr_terms=mld.acceptedTermsAndConditions,
                accepted_cookie_policy=mld.acceptedCookiePolicy,
                now=mld.now,
            )
        except Exception as ex:
            return CustomError(
                message="Dto to domain conversion error", reasons=[f"{ex}"]
            )

    # @router.post("/magic-link", response_model=HttpSuccess)
    async def send_magic_link(
        self, magic_link_dto: MagicLinkDto, request: Request
    ) -> JSONResponse:
        try:

            magic_link_domain_maybe = Auth.magic_link_dto_to_domain(magic_link_dto)
            if isinstance(magic_link_domain_maybe, CustomError):
                return http_400_json(
                    message=magic_link_domain_maybe.message,
                    reasons=magic_link_domain_maybe.reasons,
                )

            source_ip = request.client.host
            magic_link_internal = self.convert_magic_link_domain_to_internal(
                magic_link_domain_maybe, source_ip
            )
            utc_now_str = datetime.now().strftime("%Y-%m-%dT%H:00:00Z")

            mli_saved_maybe = self.save_magic_link_internal_to_s3(
                magic_link_internal=magic_link_internal, utc_now_str=utc_now_str
            )
            if isinstance(mli_saved_maybe, HttpError):
                LOG.error(f"{mli_saved_maybe.json()}")
                return http_403_json(
                    message=mli_saved_maybe.error.message,
                    reasons=mli_saved_maybe.error.reasons,
                )

            email_body_maybe = self.render_email_body(magic_link_internal)

            if isinstance(email_body_maybe, CustomError):
                return http_500_json(
                    message=email_body_maybe.message,
                    reasons=email_body_maybe.reasons,
                )

            email_sent_maybe = ses_send_email(
                ses_client=Auth.clients.ses_client,
                ses_from_email=self.config.ses_from_email,
                ses_to_emails=[magic_link_domain_maybe.email],
                ses_email_subject=self.config.ses_email_subject,
                ses_email_body=email_body_maybe,
            )
            if isinstance(email_sent_maybe, HttpError):
                email_sent_maybe.error.reasons.append(
                    f"AWSStatusCode: {email_sent_maybe.status_code}"
                )
                message, reasons = (
                    email_sent_maybe.error.message,
                    email_sent_maybe.error.reasons,
                )
                LOG.error(f"Message: {message}. Reasons: {reasons}.")
                return http_403_json(
                    message=message,
                    reasons=reasons,
                )

            return http_200_json(HttpSuccess(ok="ok"))

        except Exception as ex:
            message, reasons = "Magic-link Error", [f"{ex}"]
            LOG.error(f"Message: {message}. Reasons: {reasons}")
            return http_500_json(message=message, reasons=reasons)

    def set_cookie_with_domain_on_response(
        self,
        cookie_domain: str,
        http_response: JSONResponse,
        jwt_token: str,
        max_age: int,
    ) -> JSONResponse:

        if cookie_domain == "localhost":
            http_response.set_cookie(
                key=self.config.jwt_name,
                value=jwt_token,
                max_age=max_age,
                secure=False,
                httponly=True,
            )

        else:
            http_response.set_cookie(
                key=self.config.jwt_name,
                value=jwt_token,
                max_age=max_age,
                secure=self.config.cookie_security,
                httponly=True,
                domain=cookie_domain,
            )
        return http_response

    def verify_email_domain(self, email_address: EmailStr) -> Union[bool, CustomError]:
        error_msg = (
            f"Email domain is not allowed for the email address: {email_address}"
        )
        try:
            if self.config.allowed_email_domains == "*":
                return True

            allowed_email_domains = self.config.allowed_email_domains.split(",")
            email_domain = email_address.split("@")[-1]
            if email_domain in allowed_email_domains:
                return True
            else:
                LOG.error(error_msg)
                return CustomError(
                    message=error_msg,
                    reasons=["Incorrect email domain"],
                )
        except Exception as ex:
            LOG.error(error_msg)
            return CustomError(
                message=error_msg,
                reasons=[f"{ex}"],
            )

    def get_organization_id_for_user(
        self, email_address: EmailStr
    ) -> Union[str, CustomError]:
        try:
            error_msg = f"Could not get organization id for: {email_address}"

            email_domain = email_address.split("@")[-1]
            s3_response = s3_get_object_bytes(
                s3_client=Auth.clients.s3_client,
                s3_bucket=self.config.s3_bucket,
                s3_key=f"api/index/email-domain/{email_domain}.json",
            )

            if isinstance(s3_response, HttpError) and s3_response.status_code != 404:
                LOG.error(s3_response)
                return CustomError(
                    message=s3_response.error.message,
                    reasons=s3_response.error.reasons,
                )

            if isinstance(s3_response, HttpError) and s3_response.status_code == 404:
                org_id = get_org_eid("examplecorp.com")

            else:
                domain_and_org_id = EmailDomainAndOrgId.parse_raw(s3_response)
                org_id = domain_and_org_id.orgId

            return org_id

        except Exception as ex:
            LOG.error(error_msg)
            return CustomError(
                message=error_msg,
                reasons=[f"{ex}"],
            )

    def put_user_email_and_id(
        self, email_address: EmailStr, user_id: str, org_id: str
    ) -> Union[PutObjectOutputTypeDef, CustomError]:
        try:
            error_msg = f"Could not put user email and user id: {user_id}"
            user_email_and_id = UserEmailAndId(
                emailAddress=email_address, userId=user_id
            )
            s3_response = s3_put_object_bytes(
                Auth.clients.s3_client,
                self.config.s3_bucket,
                f"api/index/email/{org_id}/{user_id}.json",
                user_email_and_id.json().encode("utf-8"),
            )

            if isinstance(s3_response, HttpError):
                LOG.error(s3_response)
                return CustomError(
                    message=s3_response.error.message,
                    reasons=s3_response.error.reasons,
                )
            else:
                return s3_response

        except Exception as ex:
            LOG.error(error_msg)
            return CustomError(
                message=error_msg,
                reasons=[f"{ex}"],
            )

    def put_category_summaries(
        self, user_id: str
    ) -> Union[PutObjectOutputTypeDef, CustomError]:
        try:
            error_msg = f"Could not put category summary: {user_id}"
            cats = [
                CategorySummary(
                    categoryId="cat-xbyckrvqbjbpq2aoboa7o4zb7y",
                    categoryName="360º Review",
                    description="A 360-degree feedback is ...",
                    hasUnfilled=False,
                ),
                CategorySummary(
                    categoryId="cat-pj4ofwyimnapusd3toqoetb2ou",
                    categoryName="Employee Satisfaction",
                    description="How satisifed the employees are",
                    hasUnfilled=True,
                ),
                CategorySummary(
                    categoryId="cat-h54wcy7l7fdrrxq425mcmvoaci",
                    categoryName="Other",
                    description="Miscellaneous",
                    hasUnfilled=False,
                ),
            ]
            category_summaries = CategorySummaries.parse_obj(cats)
            s3_response = s3_put_object_bytes(
                Auth.clients.s3_client,
                self.config.s3_bucket,
                f"api/index/evals/{user_id}/category-summaries.json",
                category_summaries.json().encode("utf-8"),
            )

            if isinstance(s3_response, HttpError):
                LOG.error(s3_response)
                return CustomError(
                    message=s3_response.error.message,
                    reasons=s3_response.error.reasons,
                )
            else:
                return s3_response

        except Exception as ex:
            LOG.error(error_msg)
            return CustomError(
                message=error_msg,
                reasons=[f"{ex}"],
            )

    def put_favorite_drinks_eval(
        self, user_id: str
    ) -> Union[PutObjectOutputTypeDef, CustomError]:
        try:
            error_msg = f"Could not put evaluation starter pack: {user_id}"
            favorite_drinks_eval = [
                EvaluationSummary(
                    evaluationId="eva-pze4xhqb5rbmedhqrmgd2l7i6m",
                    evaluationName="Favorite Drinks",
                    matId="mat-7wby5o6exxce3md5yczyv26y5m",
                    status="unfilled",
                    createDate="2023-01-11",
                    dueDate="2023-09-30",
                    targetGroup="All",
                )
            ]
            evaluation_summaries = EvaluationSummaries.parse_obj(favorite_drinks_eval)
            s3_response = s3_put_object_bytes(
                Auth.clients.s3_client,
                self.config.s3_bucket,
                f"api/index/evals/{user_id}/cat-pj4ofwyimnapusd3toqoetb2ou/unfilled.json",
                evaluation_summaries.json().encode("utf-8"),
            )

            if isinstance(s3_response, HttpError):
                LOG.error(s3_response)
                return CustomError(
                    message=s3_response.error.message,
                    reasons=s3_response.error.reasons,
                )
            else:
                return s3_response

        except Exception as ex:
            LOG.error(error_msg)
            return CustomError(
                message=error_msg,
                reasons=[f"{ex}"],
            )

    def put_empty_eval_summaries(self, user_id: str) -> Union[None, CustomError]:
        try:
            error_msg = f"Could not put empty evaluation summaries: {user_id}"
            empty_file = EvaluationSummaries(__root__=[])

            keys = [
                f"api/index/evals/{user_id}/cat-pj4ofwyimnapusd3toqoetb2ou/filled.json",
                f"api/index/evals/{user_id}/cat-xbyckrvqbjbpq2aoboa7o4zb7y/filled.json",
                f"api/index/evals/{user_id}/cat-xbyckrvqbjbpq2aoboa7o4zb7y/unfilled.json",
                f"api/index/evals/{user_id}/cat-h54wcy7l7fdrrxq425mcmvoaci/filled.json",
                f"api/index/evals/{user_id}/cat-h54wcy7l7fdrrxq425mcmvoaci/unfilled.json",
            ]
            bu = self.config.s3_bucket
            cl = Auth.clients.s3_client
            bo = empty_file.json().encode("utf-8")

            s3_responses = list(
                map(lambda key: s3_put_object_bytes(cl, bu, key, bo), keys)
            )
            error_maybe = list(filter(lambda x: isinstance(x, HttpError), s3_responses))
            if len(error_maybe) > 0:
                LOG.error(error_maybe)
                return CustomError(
                    message=error_msg,
                    reasons=error_maybe,
                )

        except Exception as ex:
            LOG.error(error_msg)
            return CustomError(
                message=error_msg,
                reasons=[f"{ex}"],
            )

    def create_user(self, email_address: EmailStr, user_id: str, org_id: str):
        try:
            error_msg = f"Could not create user: {user_id}"

            s3_responses = []

            user_email_and_id_response = self.put_user_email_and_id(
                email_address, user_id, org_id
            )
            s3_responses.append(user_email_and_id_response)

            category_summaries_response = self.put_category_summaries(user_id)
            s3_responses.append(category_summaries_response)

            favorite_drinks_eval_repsponse = self.put_favorite_drinks_eval(user_id)
            s3_responses.append(favorite_drinks_eval_repsponse)

            put_empty_evals_response = self.put_empty_eval_summaries(user_id)
            s3_responses.append(put_empty_evals_response)

            error_maybe = list(
                filter(lambda x: isinstance(x, CustomError), s3_responses)
            )
            if len(error_maybe) > 0:
                LOG.error(error_maybe)
                return CustomError(
                    message="Error while talking to aws s3",
                    reasons=error_maybe,
                )

        except Exception as ex:
            LOG.error(error_msg)
            return CustomError(
                message=error_msg,
                reasons=[f"{ex}"],
            )

    def get_user_id_for_user(
        self, org_id: str, email_address: EmailStr
    ) -> Union[str, CustomError]:
        try:
            error_msg = f"Could not get user id for: {email_address}"

            user_id = get_user_eid(email_address)
            s3_response = s3_get_object_bytes(
                s3_client=Auth.clients.s3_client,
                s3_bucket=self.config.s3_bucket,
                s3_key=f"api/index/email/{org_id}/{user_id}.json",
            )

            if isinstance(s3_response, HttpError) and s3_response.status_code != 404:
                LOG.error(s3_response)
                return CustomError(
                    message=s3_response.error.message,
                    reasons=s3_response.error.reasons,
                )

            if isinstance(s3_response, HttpError) and s3_response.status_code == 404:
                user_creation_maybe = self.create_user(email_address, user_id, org_id)
                if isinstance(user_creation_maybe, CustomError):
                    LOG.error(user_creation_maybe)
                    return CustomError(
                        message=user_creation_maybe.message,
                        reasons=user_creation_maybe.reasons,
                    )

            return user_id

        except Exception as ex:
            LOG.error(error_msg)
            return CustomError(
                message=error_msg,
                reasons=[f"{ex}"],
            )

    # @router.post("/login", response_model=HttpSuccess)
    async def login(self, login_hash: LoginHash) -> JSONResponse:
        try:
            signing_key_maybe: Union[SigningKey, HttpError] = Auth.get_signing_key(
                secrets_manager_client=Auth.clients.secretsmanager_client,
                secret_id=self.config.jwt_secret_id,
            )

            if isinstance(signing_key_maybe, HttpError):
                LOG.error(f"{signing_key_maybe}")
                return http_error_to_json_response(signing_key_maybe)

            mli_maybe = self.get_hash_from_s3(login_hash)
            if isinstance(mli_maybe, HttpError):
                mli_maybe.error.reasons.append(
                    f"AWSStatusCode: {mli_maybe.status_code}"
                )
                LOG.error(
                    f"Message: {mli_maybe.error.message}. Reasons: {mli_maybe.error.reasons}"
                )
                return http_403_json(
                    message=mli_maybe.error.message, reasons=mli_maybe.error.reasons
                )

            email_address = mli_maybe.magic_link.email
            org_id_maybe = self.get_organization_id_for_user(email_address)
            if isinstance(org_id_maybe, CustomError):
                LOG.error(f"{org_id_maybe}")
                return http_500_json(
                    message=org_id_maybe.message, reasons=org_id_maybe.reasons
                )

            user_id_maybe = self.get_user_id_for_user(org_id_maybe, email_address)
            if isinstance(user_id_maybe, CustomError):
                LOG.error(f"{user_id_maybe}")
                return http_500_json(
                    message=user_id_maybe.message, reasons=user_id_maybe.reasons
                )

            jwt_param = JwtParam(
                email=mli_maybe.magic_link.email,
                first_name=mli_maybe.magic_link.first_name,
                role=RoleEnum.user,
                org_id=org_id_maybe,
                user_id=user_id_maybe,
            )

            jwt_token_maybe = Auth.create_jwt(
                jwt_param=jwt_param,
                signing_key=signing_key_maybe,
                audience=self.config.jwt_audience,
                issuer=self.config.jwt_audience,
                exp_days=self.config.cookie_max_age_days,
            )
            if isinstance(jwt_token_maybe, CustomError):
                LOG.error(
                    f"Message: {jwt_token_maybe.message}. Reasons: {jwt_token_maybe.reasons}"
                )
                return http_403_json(
                    message=jwt_token_maybe.message, reasons=jwt_token_maybe.reasons
                )

            verified_email_domain = self.verify_email_domain(jwt_param.email)
            if isinstance(verified_email_domain, CustomError):
                LOG.error(
                    f"Message: {verified_email_domain.message}. Reasons: {verified_email_domain.reasons}"
                )
                return http_403_json(
                    message=verified_email_domain.message,
                    reasons=verified_email_domain.reasons,
                )

            http_response = http_200_json(HttpSuccess(ok="ok"))
            max_age = self.config.cookie_max_age_days * 24 * 60 * 60
            cookie_domain = Auth.get_cookie_domain_from_cors(
                self.config.cors_allow_origin
            )
            return self.set_cookie_with_domain_on_response(
                cookie_domain=cookie_domain,
                http_response=http_response,
                jwt_token=jwt_token_maybe,
                max_age=max_age,
            )

        except Exception as ex:
            message, reasons = "Login Error", [f"{ex}"]
            LOG.error(f"Message: {message}. Reasons: {reasons}")
            return http_500_json(message=message, reasons=reasons)

    # @router.post("/logout")
    async def logout(self) -> JSONResponse:
        try:
            signing_key_maybe: Union[SigningKey, HttpError] = Auth.get_signing_key(
                secrets_manager_client=Auth.clients.secretsmanager_client,
                secret_id=self.config.jwt_secret_id,
            )

            if isinstance(signing_key_maybe, HttpError):
                LOG.error(f"{signing_key_maybe}")
                return http_error_to_json_response(self.signing_key_maybe)

            jwt_token_maybe = Auth.create_jwt(
                jwt_param=JwtParam(
                    email="log@out.com",
                    first_name="Logout",
                    role=RoleEnum.user,
                    org_id="",
                    user_id="",
                ),
                signing_key=signing_key_maybe,
                audience=self.config.jwt_audience,
                issuer=self.config.jwt_audience,
                exp_days=self.config.cookie_max_age_days,
            )

            http_response = http_200_json(HttpSuccess(ok="ok"))
            max_age = 0
            cookie_domain = Auth.get_cookie_domain_from_cors(
                self.config.cors_allow_origin
            )
            return self.set_cookie_with_domain_on_response(
                cookie_domain=cookie_domain,
                http_response=http_response,
                jwt_token=jwt_token_maybe,
                max_age=max_age,
            )
        except Exception as ex:
            message, reasons = "Logout Error", [f"{ex}"]
            LOG.error(f"Message: {message}. Reasons: {reasons}")
            return http_500_json(message=message, reasons=reasons)

    # @router.get("/who-am-i")
    async def get_who_am_i(self, request: Request) -> JSONResponse:
        try:
            signing_key_maybe: Union[SigningKey, HttpError] = Auth.get_signing_key(
                secrets_manager_client=Auth.clients.secretsmanager_client,
                secret_id=self.config.jwt_secret_id,
            )

            token_fields_maybe = Auth.get_jwt_fields_from_cookies(
                request.cookies,
                self.config.jwt_name,
                signing_key_maybe,
                self.config.jwt_audience,
                ["email", "first_name", "role", "org_id", "user_id"],
            )
            if isinstance(token_fields_maybe, CustomError):
                return http_403_json(
                    message=token_fields_maybe.message,
                    reasons=token_fields_maybe.reasons,
                )

            token_fields_maybe_errors: List[CustomError] = list(
                filter(lambda t: isinstance(t, CustomError), token_fields_maybe)
            )
            if token_fields_maybe_errors:
                message, reasons = "JWT Error", list(
                    map(lambda x: x.reasons, token_fields_maybe_errors)
                )
                LOG.error(f"Error: {message}. Reasons: {reasons}")
                return http_403_json(
                    message=message,
                    reasons=reasons,
                )

            email, first_name, role, org_id, user_id = token_fields_maybe

            return http_200_json(
                WhoAmI(
                    email=EmailStr(email),
                    firstName=first_name,
                    role=role,
                    orgId=org_id,
                    userId=user_id,
                )
            )
        except Exception as ex:
            message, reasons = "WhoAmI Error", [f"{ex}"]
            LOG.error(f"Message: {message}. Reasons: {reasons}")
            return http_500_json(message=message, reasons=reasons)
