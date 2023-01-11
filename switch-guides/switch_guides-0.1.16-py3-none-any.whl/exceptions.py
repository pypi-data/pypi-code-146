# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


class SwitchGuideDefinitionInvalidException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidStepApiReponseException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidStepStatusReponseException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
