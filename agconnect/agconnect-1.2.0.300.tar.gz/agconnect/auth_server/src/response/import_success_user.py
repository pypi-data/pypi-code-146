# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

class ImportSuccessUser:
    def __init__(self):
        self.uid = None
        self.import_uid = None

    def get_uid(self):
        return self.uid

    def set_uid(self, uid: str):
        self.uid = uid

    def get_import_uid(self):
        return self.import_uid

    def set_import_uid(self, import_uid: str):
        self.import_uid = import_uid
