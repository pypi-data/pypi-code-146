# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class KadiException(Exception):
    """Base exception class."""


class KadiConfigurationError(KadiException):
    """For general configuration errors."""


class KadiStorageError(KadiException):
    """For general file storage errors."""


class KadiFilesizeExceededError(KadiStorageError):
    """For errors relating to exceeded file size."""


class KadiFilesizeMismatchError(KadiStorageError):
    """For errors relating to file size validation."""


class KadiChecksumMismatchError(KadiStorageError):
    """For errors relating to file checksum validation."""


class KadiValidationError(KadiException):
    """For general validation errors."""


class KadiPermissionError(KadiException):
    """For general permissions errors."""


class KadiDatabaseError(KadiException):
    """For general database errors."""


class KadiDecryptionKeyError(KadiDatabaseError):
    """For errors relating to an invalid decryption key for encrypted fields."""
