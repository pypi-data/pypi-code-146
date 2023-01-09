import logging
from io import BytesIO
import xlsxwriter

logger = logging.getLogger(__name__)


# write_to_excel：把data数据写入到excel中
def write_to_excel(named_result, sheet_name):
    err_msg = ""
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    ws = workbook.add_worksheet(sheet_name)
    # 列名加粗显示
    bold = workbook.add_format({'bold': True})
    try:
        # 准备提取列明
        columns = []
        if named_result and len(named_result) > 0:
            if len(named_result[0]) > 0:
                for k in named_result[0][0]._fields:
                    columns.append(k)

                if len(columns) > 0:
                    ws.write(0, 0, "序号", bold)
                    ws.write_row(0, 1, columns, bold)
                    row_idx = 1

                    for d in named_result[0]:
                        ws.write(row_idx, 0, row_idx)
                        ws.write_row(row_idx, 1, d)
                        row_idx += 1
            elif len(named_result) > 1 and len(named_result[1]) > 0:
                ws.write_string(0, 0, named_result[1])
    except Exception as e:
        err_msg = "保存excel处理数据时时失败,原因: {be_str}".format(be_str=str(e))
        ws.write_string(0, 0, err_msg)
        logger.error(err_msg)
    finally:
        workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data, err_msg
