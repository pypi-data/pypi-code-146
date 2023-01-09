import warnings
import re
from pathlib import Path

from PyPDF2 import PdfFileMerger
import xlwings as xw

# Ignore warnings
warnings.filterwarnings('ignore')

# Set workbook variables
xl_app = xw.apps.active
wb: xw.Book = xw.Book.caller()
ws_input: xw.Sheet = wb.sheets['Input']


def main(current_dir):
    current_dir = str(current_dir).replace('/', '\\')

    # Input
    user_name = ws_input['c_user'].value

    index_names = ['batch', 'index', 'cover', 'start']
    pdfs = []

    directory = Path(current_dir)

    for file in directory.iterdir():
        filename = file.name
        if filename.endswith('.pdf') or filename.endswith('.PDF'):
            if any(_ in filename.lower() for _ in index_names):
                index = file
            else:
                pdfs.append(file)

    pdfs.sort()
    try:
        pdfs.insert(0, index)
        list_index = re.findall(r'\d+', index.stem)
        str_index = ''.join(list_index)
        result = user_name + ' ' + str_index + '.pdf'
    except NameError:
        result = 'Merged.pdf'

    merger = PdfFileMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write((directory / result))
    merger.close()
    xl_app.alert('Complete', title='Complete', mode='info')


if __name__ == "__main__":
    xw.Book('Merge PDF.xlsb').set_mock_caller()

    # wb: xw.Book = xw.Book.caller()
    # ws_input: xw.Sheet = wb.sheets['Input']
    # main()
