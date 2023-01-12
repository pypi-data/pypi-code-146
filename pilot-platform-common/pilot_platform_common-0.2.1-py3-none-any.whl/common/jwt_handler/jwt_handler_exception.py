# Copyright (C) 2022 Indoc Research
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from enum import Enum


class JWTHandlerError(Enum):
    GET_TOKEN_ERROR = 'Failed to get token'
    VALIDATE_TOKEN_ERROR = 'Failed to validate token'


class JWTHandlerException(Exception):
    def __init__(self, error: JWTHandlerError):
        self.error = error

    def __str__(self):
        return self.error.value
