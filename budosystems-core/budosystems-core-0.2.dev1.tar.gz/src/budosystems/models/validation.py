#
#  Copyright (c) 2021.  Budo Systems
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#

"""Validation helpers."""

from .. import typehints as th


class ValidationWarning(UserWarning):
    """Warning related to validation.
    Implemented as a Warning so that the flow doesn't get interrupted."""
    def __init__(self,
                 msg_txt: str = '',
                 details: th.Any = None,
                 exception: th.Optional[Exception] = None
                 ):
        super().__init__(msg_txt, details, exception)
        self.msg_txt = msg_txt
        self.details = details
        self.exception = exception


class ValidationError(Exception):
    """Validation related exception.  Identifies a more serious problem
    than a ValidationWarning."""

class DeserializationWarning(ValidationWarning):
    """Warning related to deserialization."""
