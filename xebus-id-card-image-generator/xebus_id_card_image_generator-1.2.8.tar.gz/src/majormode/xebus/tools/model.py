# Copyright (C) 2020 Majormode.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Majormode or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Majormode.
#
# MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
# OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE SHALL NOT BE LIABLE FOR ANY
# LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
# OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

import uuid

from majormode.perseus.utils import cast

from .constant import CARD_TYPE


class IdCardInfo:
    def __init__(
            self,
            card_type: CARD_TYPE,
            account_id: uuid.UUID,
            full_name: str,
            class_name: str = None,
            first_name: str = None,
            grade_level: str = None,
            grade_name: str = None,
            last_name: str = None,
            registration_id: str = None):
        if card_type and isinstance(card_type, str):
            card_type = cast.string_to_enum(card_type, CARD_TYPE)
        elif card_type not in CARD_TYPE:
            raise ValueError(f"Invalid card type '{str(card_type)}'")

        self.__card_type = card_type
        self.__account_id = account_id
        self.__class_name = class_name
        self.__full_name = full_name
        self.__first_name = first_name
        self.__grade_level = grade_level
        self.__grade_name = grade_name
        self.__last_name = last_name
        self.__registration_id = registration_id

    @property
    def account_id(self) -> uuid.UUID:
        return self.__account_id

    @property
    def card_type(self) -> CARD_TYPE:
        return self.__card_type

    @property
    def class_name(self) -> str or None:
        return self.__class_name

    @property
    def first_name(self) -> str or None:
        return self.__first_name

    @property
    def full_name(self) -> str or None:
        return self.__full_name

    @property
    def grade_level(self) -> str or None:
        return self.__grade_level

    @property
    def grade_name(self) -> str or None:
        return self.__grade_name

    @property
    def last_name(self) -> str or None:
        return self.__last_name

    @property
    def registration_id(self) -> uuid.UUID or None:
        return self.__registration_id
