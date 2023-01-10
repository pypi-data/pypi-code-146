#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from typing import Set
from colorama import Fore, Style


class UnsupportedFileFormat(Exception):
    def __init__(self, file_format):
        super().__init__(f"Provided file format {self._format} is not supported.")


class KfsClassImportError(Exception):
    def __init__(self, module_name, class_name, class_type="provider"):
        super().__init__(
            f"Could not import {class_type} '{class_name}' from module '{module_name}'"
        )

class TtlTypeError(Exception):
    def __init__(self,type):
        super().__init__(
            f"{type} is not supported. Please provide in Number of Days."
        )


class KfsModuleImportError(Exception):
    def __init__(self, module_name: str, module_type: str):
        super().__init__(f"Could not import {module_type} module '{module_name}'")


class KfsClassImportError(Exception):
    def __init__(self, module_name, class_name, class_type="provider"):
        super().__init__(
            f"Could not import {class_type} '{class_name}' from module '{module_name}'"
        )


class KfsClassInvalidName(Exception):
    def __init__(self, class_name: str, class_type: str):
        super().__init__(
            f"Config Class '{class_name}' "
            f"should end with the string `{class_type}`.'"
        )


class KfsProviderNotImplementedError(Exception):
    def __init__(self, provider_name):
        super().__init__(f"Provider '{provider_name}' is not implemented")


class KfsEntityDFMissingColumnsError(Exception):
    def __init__(self, expected, missing):
        super().__init__(
            f"The entity dataframe you have provided must contain columns {expected}, "
            f"but {missing} were missing."
        )


class KfsJoinKeysDuringMaterialization(Exception):
    def __init__(
        self, source: str, join_key_columns: Set[str], source_columns: Set[str]
    ):
        super().__init__(
            f"The DataFrame from '{source}' being materialized must have at least '{join_key_columns}' columns present, "
            f"but these were missing: {join_key_columns - source_columns} "
        )


class KfsObjectNotFoundException(Exception):
    pass


class FeatureViewNotFoundException(KfsObjectNotFoundException):
    def __init__(self, name, project=None):
        if project:
            super().__init__(f"Feature view '{name}' does not exist in project '{project}'")
        else:
            super().__init__(f"Feature view '{name}' does not exist")

class KfsObjectNotFoundException(Exception):
    pass


class EntityNotFoundException(KfsObjectNotFoundException):
    def __init__(self, name, project=None):
        if project:
            super().__init__(f"Entity '{name}' does not exist in project '{project}'")
        else:
            super().__init__(f"Entity {name} does not exist")


class EntityTimestampInferenceException(Exception):
    def __init__(self, expected_column_name: str):
        super().__init__(
            f"Please provide an entity_df with a column named '{expected_column_name}' representing the time of events."
        )