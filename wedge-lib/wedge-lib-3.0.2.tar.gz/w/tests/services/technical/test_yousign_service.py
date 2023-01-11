import re

import pytest
from django.conf import settings

from w.services.technical.models.yousign import (
    YousignSignatureRequestCreation,
    YousignSigner,
    YousignProcedureStart,
    YousignMentionField,
    YousignSignatureField,
)
from w.services.technical.yousign_service import YousignService
from w.tests.helpers import request_test_helper
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestYousignService(TestCaseMixin):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.filename = cls.get_datasets_dir("pdf/exemple_pdf.pdf")
        cls.signer = YousignSigner(
            first_name="John",
            last_name="Doe",
            email="john.doe@test.com",
            phone_number="+33612345678",
            locale="fr",
        )
        cls.document_id = "9fcd97c2-b4c0-496d-baea-a09c820cf6c6"
        cls.signature_field = YousignSignatureField(
            page_number=2,
            top_left_x_coordinate=100,
            top_left_y_coordinate=300,
        )
        cls.mention_field = YousignMentionField(
            page_number=2,
            top_left_x_coordinate=100,
            top_left_y_coordinate=200,
            text="Lu et approuvé le",
        )
        cls.signature_request_creation_data_without_mention_field = (
            YousignSignatureRequestCreation(
                name="test signature request creation without mention field",
                documents=[cls.document_id],
                signers=[cls.signer],
                signature_field=cls.signature_field,
            )
        )
        cls.signature_request_creation_data_with_mention_field = (
            YousignSignatureRequestCreation(
                name="test signature request creation with mention field",
                documents=[cls.document_id],
                signers=[cls.signer],
                signature_field=cls.signature_field,
                mention_field=cls.mention_field,
            )
        )
        cls.signature_request_id = "5cff6052-ea18-48d3-b81c-5242967597bf"
        cls.procedure_data = YousignProcedureStart(
            signature_request_name="test procedure",
            filename=cls.filename,
            signer=cls.signer,
            signature_field=cls.signature_field,
            mention_field=cls.mention_field,
        )
        cls.signer_id = "52079693-f049-4615-bc3d-4a99a9067f85"
        cls.upload_failure_response = {
            "json_file": cls.get_datasets_dir(
                "yousign/upload_document_bad_request.json"
            ),
        }
        cls.upload_failure_msg = re.escape(
            f"Failed to upload {cls.filename} (400 - Bad Request) : Malformed or "
            f"invalid Content-Type header, please refer to the documentation."
        )
        cls.signature_request_creation_failure_msg = re.escape(
            "Failed to create signature request (400 - Bad Request) : "
            'Invalid authentication mode. "null" given but "sms" or "no_code" are '
            'allowed for the "simple" signature level'
        )
        cls.signature_request_activation_failure_msg = re.escape(
            f"Failed to activate signature request (id = {cls.signature_request_id}) "
            f"(400 - Bad Request) : Signer '{cls.signer_id}' "
            f"does not have any field. You need at least one field per signer."
        )

    @staticmethod
    def setup_method():
        YousignService.clear()
        YousignService.init(settings.YOUSIGN_API_URL, settings.YOUSIGN_API_KEY)

    """
    upload_document
    """

    def test_upload_document_with_service_not_initialized_raise_runtime_error(self):
        """Ensure method raises RuntimeError if service is not initialized"""
        YousignService.clear()
        match = "Service YousignService must be initialized first"
        with pytest.raises(RuntimeError, match=match):
            YousignService.upload_document(self.filename)

    def test_upload_document_with_non_existing_file_raise_runtime_error(self):
        """Ensure method raises RuntimeError if file to be uploaded does not exist"""
        filename = "non_existent_file.pdf"
        match = f"{filename} does not exists"
        with pytest.raises(RuntimeError, match=match):
            YousignService.upload_document(filename=filename)

    def test_upload_document_with_unsupported_file_type_raise_runtime_error(
        self,
    ):
        """Ensure method raises RuntimeError if the type of the file to be uploaded is
        not supported"""
        match = re.escape("Unsupported file type (only pdf file type is supported)")
        with pytest.raises(RuntimeError, match=match):
            YousignService.upload_document(
                filename=self.get_datasets_dir("json/example.json")
            )

    def test_upload_document_with_upload_failure_raise_runtime_error(self):
        """Ensure method raises RuntimeError if call to Yousign API fails"""
        with request_test_helper.request_failure(
            self.upload_failure_response, method="post"
        ):
            with pytest.raises(RuntimeError, match=self.upload_failure_msg):
                YousignService.upload_document(filename=self.filename)

    def test_upload_document_with_success_return_uploaded_document_info(self):
        """Ensure method succeeds"""
        response = {
            "json_file": self.get_datasets_dir("yousign/upload_document_success.json")
        }
        with request_test_helper.request_success(response, method="post") as m:
            actual = YousignService.upload_document(filename=self.filename)
        mock_calls = self.get_mock_calls(m)
        assert mock_calls[0]["kwargs"]["files"]["file"][0] == self.filename
        assert mock_calls[0]["kwargs"]["files"]["file"][2] == "application/pdf"
        # Remove files from mock_calls
        # because path in CI context is different from path in local !
        mock_calls[0]["kwargs"].pop("files")
        self.assert_equals_resultset({"result": actual, "mocks": mock_calls})

    """
    create_signature_request
    """

    def test_create_signature_request_with_service_not_initialized_raise_runtime_error(
        self,
    ):
        """Ensure method raises RuntimeError if service is not initialized"""
        YousignService.clear()
        match = "Service YousignService must be initialized first"
        with pytest.raises(RuntimeError, match=match):
            YousignService.create_signature_request(
                self.signature_request_creation_data_without_mention_field
            )

    def test_create_signature_request_with_creation_failure_raise_runtime_error(self):
        """Ensure method raises RuntimeError if call to Yousign API fails"""
        response = {
            "json_file": self.get_datasets_dir(
                "yousign/create_signature_request_bad_request.json"
            ),
        }
        with request_test_helper.request_failure(response, method="post"):
            with pytest.raises(
                RuntimeError, match=self.signature_request_creation_failure_msg
            ):
                YousignService.create_signature_request(
                    self.signature_request_creation_data_without_mention_field
                )

    def test_create_signature_request_without_mention_field_success_return_created_signature_request_info(  # noqa
        self,
    ):
        """Ensure method succeeds"""
        response = {
            "json_file": self.get_datasets_dir(
                "yousign/create_signature_request_without_mention_field_success.json"
            )
        }
        with request_test_helper.request_success(response, method="post") as m:
            actual = YousignService.create_signature_request(
                self.signature_request_creation_data_without_mention_field
            )
        self.assert_equals_resultset(
            {"result": actual, "mocks": self.get_mock_calls(m)}
        )

    def test_create_signature_request_with_mention_field_success_return_created_signature_request_info(  # noqa
        self,
    ):
        """Ensure method succeeds when a mention field is also wanted"""
        response = {
            "json_file": self.get_datasets_dir(
                "yousign/create_signature_request_with_mention_field_success.json"
            )
        }
        with request_test_helper.request_success(response, method="post") as m:
            actual = YousignService.create_signature_request(
                self.signature_request_creation_data_with_mention_field
            )
        self.assert_equals_resultset(
            {"result": actual, "mocks": self.get_mock_calls(m)}
        )

    """
    activate_signature_request
    """

    def test_activate_signature_request_with_service_not_initialized_raise_runtime_error(  # noqa
        self,
    ):
        """Ensure method raises RuntimeError if service is not initialized"""
        YousignService.clear()
        match = "Service YousignService must be initialized first"
        with pytest.raises(RuntimeError, match=match):
            YousignService.activate_signature_request(self.signature_request_id)

    def test_activate_signature_request_with_activation_failure_raise_runtime_error(
        self,
    ):
        """Ensure method raises RuntimeError if call to Yousign API fails"""
        response = {
            "json_file": self.get_datasets_dir(
                "yousign/activate_signature_request_bad_request.json"
            ),
        }
        with request_test_helper.request_failure(response, method="post"):
            with pytest.raises(
                RuntimeError, match=self.signature_request_activation_failure_msg
            ):
                YousignService.activate_signature_request(self.signature_request_id)

    def test_activate_signature_request_with_success_return_activated_signature_request_info(  # noqa
        self,
    ):
        """Ensure method succeeds"""
        response = {
            "json_file": self.get_datasets_dir(
                "yousign/activate_signature_request_success.json"
            )
        }
        with request_test_helper.request_success(response, method="post") as m:
            actual = YousignService.activate_signature_request(
                self.signature_request_id
            )
        assert actual.signature_request_status == "ongoing"
        self.assert_equals_resultset(
            {"result": actual.to_dict(), "mocks": self.get_mock_calls(m)}
        )

    """
    start_procedure
    """

    def test_start_procedure_with_service_not_initialized_raise_runtime_error(
        self,
    ):
        """Ensure method raises RuntimeError if service is not initialized"""
        YousignService.clear()
        match = "Service YousignService must be initialized first"
        with pytest.raises(RuntimeError, match=match):
            YousignService.start_procedure(self.procedure_data)

    def test_start_procedure_with_invalid_authentication_raise_runtime_error(
        self,
    ):
        """Ensure method raises RuntimeError if access to Yousign APIs is
        unauthorized"""
        response = {
            "json_file": self.get_datasets_dir("yousign/unauthorized_access.json"),
            "status_code": 401,
        }
        match = re.escape(
            f"Failed to upload {self.filename} (401 - Bad Request) : " f"no detail"
        )
        with request_test_helper.request_failure(response, method="post"):
            with pytest.raises(RuntimeError, match=match):
                YousignService.start_procedure(self.procedure_data)

    def test_start_procedure_with_document_upload_failure_raise_runtime_error(
        self,
    ):
        """Ensure method raises RuntimeError if the document upload fails"""
        with request_test_helper.request_failure(
            self.upload_failure_response, method="post"
        ):
            with pytest.raises(RuntimeError, match=self.upload_failure_msg):
                YousignService.start_procedure(self.procedure_data)

    def test_start_procedure_with_signature_request_creation_failure_raise_runtime_error(  # noqa
        self,
    ):
        """Ensure method raises RuntimeError if the signature request creation fails"""
        responses = [
            request_test_helper.get_response(
                json_file=self.get_datasets_dir("yousign/upload_document_success.json")
            ),
            request_test_helper.get_400_response(
                json_file=self.get_datasets_dir(
                    "yousign/create_signature_request_bad_request.json"
                ),
            ),
        ]
        with request_test_helper.mock_request(responses, method="post"):
            with pytest.raises(
                RuntimeError, match=self.signature_request_creation_failure_msg
            ):
                YousignService.start_procedure(self.procedure_data)

    def test_start_procedure_with_signature_request_activation_failure_raise_runtime_error(  # noqa
        self,
    ):
        """Ensure method raises RuntimeError if the signature request activation
        fails"""
        responses = [
            request_test_helper.get_response(
                json_file=self.get_datasets_dir("yousign/upload_document_success.json")
            ),
            request_test_helper.get_response(
                json_file=self.get_datasets_dir(
                    "yousign/create_signature_request_with_mention_field_success.json"
                ),
            ),
            request_test_helper.get_400_response(
                json_file=self.get_datasets_dir(
                    "yousign/activate_signature_request_bad_request.json"
                ),
            ),
        ]
        with request_test_helper.mock_request(responses, method="post"):
            with pytest.raises(
                RuntimeError, match=self.signature_request_activation_failure_msg
            ):
                YousignService.start_procedure(self.procedure_data)

    def test_start_procedure_with_success_return_procedure_info(self):
        """Ensure method succeeds"""
        response = {
            "json_file": [
                self.get_datasets_dir("yousign/upload_document_success.json"),
                self.get_datasets_dir(
                    "yousign/create_signature_request_with_mention_field_success.json"
                ),
                self.get_datasets_dir(
                    "yousign/activate_signature_request_success.json"
                ),
            ]
        }
        with request_test_helper.request_success(response, method="post") as m:
            actual = YousignService.start_procedure(self.procedure_data)
        mock_calls = self.get_mock_calls(m)
        assert mock_calls[0]["kwargs"]["files"]["file"][0] == self.filename
        assert mock_calls[0]["kwargs"]["files"]["file"][2] == "application/pdf"
        # Remove files from mock_calls
        # because path in CI context is different from path in local !
        mock_calls[0]["kwargs"].pop("files")
        self.assert_equals_resultset({"result": actual.to_dict(), "mocks": mock_calls})

    """
    download_signature_request_document
    """

    def test_download_signature_request_document_with_service_not_initialized_raise_runtime_error(  # noqa
        self,
    ):
        """Ensure method raises RuntimeError if service is not initialized"""
        YousignService.clear()
        match = "Service YousignService must be initialized first"
        with pytest.raises(RuntimeError, match=match):
            YousignService.download_signature_request_document(
                self.signature_request_id
            )

    def test_download_signature_request_document_with_download_failure_raise_runtime_error(  # noqa
        self,
    ):
        """Ensure method raises RuntimeError if call to Yousign API fails"""
        response = {
            "json_file": self.get_datasets_dir(
                "yousign/download_signature_request_document_bad_request.json"
            ),
        }
        document_download_failure_msg = re.escape(
            f"Failed to download signature request document "
            f"(id = {self.signature_request_id}) "
            f"(400 - Bad Request) : The signature request "
            f'"5cff6052-ea18-48d3-b81c-5242967597bd" has no document.'
        )
        with request_test_helper.request_failure(response, method="get"):
            with pytest.raises(RuntimeError, match=document_download_failure_msg):
                YousignService.download_signature_request_document(
                    self.signature_request_id
                )

    def test_download_signature_request_document_with_success_return_document(self):
        """Ensure method succeeds"""
        response = {
            # "file": self.get_datasets_dir(
            #     "yousign/download_signature_request_document_success"
            # ),
            "content": bytes("%PDF fake document content %EOF", "utf-8")
        }
        with request_test_helper.request_success(response, method="get") as m:
            actual = YousignService.download_signature_request_document(
                self.signature_request_id
            )
        assert actual[0:4] == b"%PDF"
        assert actual[-4:] == b"%EOF"
        self.assert_equals_resultset({"mocks": self.get_mock_calls(m)})
