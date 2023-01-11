# encoding: utf-8
"""
@project: djangoModel->doc_export
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis:
@created_time: 2022/11/23 16:53
"""
from io import BytesIO
import os
import platform

from docxtpl import DocxTemplate

from main.settings import BASE_DIR

TEMPLET_PATH_MAP = {
    "bid-online-contract": str(BASE_DIR) + "/resource_files/templet/bxtx_contract_templet.docx"  # 镖行天下合同
}


class DocExportService:
    @staticmethod
    def export(variable_params, templet_path=None, save_path=None):
        if not templet_path or not os.path.exists(templet_path):
            return None, "模板地址不正确"

        # 模板变量替换
        doc = DocxTemplate(templet_path)
        doc.render(variable_params)
        # 保存文件位置
        if not save_path is None and os.path.exists(templet_path):
            doc.save(save_path)
            return save_path, None
        # 文件路径
        return DocExportService.__export_stream(doc), None

    #  exce保存文件流
    @staticmethod
    def __export_stream(save_obj):
        try:
            from StringIO import StringIO
        except ImportError:
            from io import StringIO

        if platform.python_version()[0] == "2":
            # python 2.*.*
            output = StringIO()
            save_obj.save(output)
            output.seek(0)
            return output.getvalue()
        else:
            # python 3.*.*
            output = BytesIO()
            save_obj.save(output)
            output.seek(0)
            return output.getvalue()
