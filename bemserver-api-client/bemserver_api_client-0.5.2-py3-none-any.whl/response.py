"""BEMServer API client response"""
import logging
import json

from .exceptions import (
    BEMServerAPIValidationError,
    BEMServerAPINotFoundError,
    BEMServerAPINotModified,
    BEMServerAPIAuthenticationError,
    BEMServerAPIPreconditionError,
    BEMServerAPIInternalError,
)


class BEMServerApiClientResponse:
    """API client response"""

    def __init__(self, raw_response, *, logger=None):
        self._logger = logger or logging.getLogger(__name__)
        self._raw_response = raw_response
        content_type = self._raw_response.headers.get("Content-Type", "")
        self._mimetype = content_type.split("; ")[0]

        # Process redirection or error, if any.
        if self.status_code == 304:
            raise BEMServerAPINotModified
        elif self.status_code < 300 or self.status_code > 500:
            self._raw_response.raise_for_status()
        else:
            self._process_client_error()

    @property
    def status_code(self):
        return self._raw_response.status_code

    @property
    def etag(self):
        return self._raw_response.headers.get("ETag", "")

    @property
    def pagination(self):
        """Get pagination data, if any.

        Example:
            {"total": 4, "total_pages": 1, "first_page": 1, "last_page": 1, "page": 1}
        """
        return json.loads(self._raw_response.headers.get("X-Pagination", "{}"))

    @property
    def is_json(self):
        """Check if the mimetype indicates JSON data, either
        :mimetype:`application/json` or :mimetype:`application/*+json`.
        """
        return self._mimetype == "application/json" or (
            self._mimetype.startswith("application/")
            and self._mimetype.endswith("+json")
        )

    @property
    def is_csv(self):
        """Check if the mimetype indicates CSV data, either
        :mimetype:`application/csv` or :mimetype:`application/*+csv`.
        """
        return self._mimetype == "application/csv" or (
            self._mimetype.startswith("application/")
            and self._mimetype.endswith("+csv")
        )

    @property
    def data(self):
        if self.is_json:
            return self._raw_response.json()
        return self._raw_response.content

    def _process_client_error(self):
        self._logger.error(f"{self.status_code} {self._raw_response.url}")

        # Authentication error
        if self.status_code in (401, 403):
            raise BEMServerAPIAuthenticationError(status_code=self.status_code)

        # Precondition error (etag)
        elif self.status_code in (412, 428):
            raise BEMServerAPIPreconditionError(status_code=self.status_code)

        # Resource not found
        elif self.status_code == 404:
            raise BEMServerAPINotFoundError

        # Conflict or validation error
        elif self.status_code in (409, 422):
            # TODO: rework this part
            errors = {}
            if self.is_json:
                if self.status_code == 409:
                    # Unique constraint error
                    if self.data.get("errors", {}).get("type") == "unique_constraint":
                        errors = {
                            # TODO: manage multiple columns constraint
                            field: ["Must be unique."]
                            for field in self.data["errors"]["fields"]
                        }
                    # Foreign key constraint error (and default case)
                    else:
                        errors = {"_general": ["Operation failed (409)."]}
                elif self.status_code == 422:
                    if "errors" in self.data:
                        # Marshmallow ValidationError
                        for loc in ("json", "query", "files"):
                            if loc in self.data["errors"]:
                                errors = {**errors, **self.data["errors"][loc]}
                                if "_schema" in errors:
                                    errors["_general"] = errors.pop("_schema")
                    # BEMServer ValidationError
                    elif "message" in self.data:
                        errors = {"_general": [self.data["message"]]}
            raise BEMServerAPIValidationError(errors=errors)

        # Issue in BEMServer
        raise BEMServerAPIInternalError(status_code=self.status_code)

    def toJSON(self):
        # Allows to set this response instance in a serializable object.
        return {
            "status_code": self.status_code,
            "data": self.data,
            "etag": self.etag,
            "pagination": self.pagination,
        }
