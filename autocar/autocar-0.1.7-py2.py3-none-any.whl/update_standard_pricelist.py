from pathlib import Path
import datetime

import pandas as pd
import pyperclip
import xlwings as xw

# Set workbook variables
xl_app = xw.apps.active
wb: xw.Book = xw.Book.caller()
ws_input: xw.Sheet = wb.sheets['Input']
ws_settings: xw.Sheet = wb.sheets['Settings']

server_path = Path(ws_settings['c_std_path'].value)
pricelist_path = Path(ws_settings['c_price_path'].value)


def button_update_standard_pricelist():
    today_date = datetime.datetime.today().strftime('%m%d%Y')
    df_pricelist: pd.DataFrame = ws_input['t_input[[#All]]'].options(pd.DataFrame, index=False).value
    df_std_export = df_pricelist[['Part_Nr', 'Cost']]
    df_std_export = df_std_export.rename({
        'Part_Nr': 'Item_Number',
        'Cost': 'Standard_Material_Cost'
    }, axis='columns')

    price_name = df_pricelist['Supplier_Nr'].iloc[0]
    file_name = today_date + ' ' + price_name + '.csv'

    msgbox_return = xl_app.alert('Are you ready to continue?', title='Ready', mode='info', buttons='yes_no')

    if msgbox_return == 'yes':
        df_pricelist.to_csv(pricelist_path / file_name, index=False, header=False)
        df_std_export.to_csv(server_path / 'stdprod.csv', index=False)
        pyperclip.copy(file_name)
        xl_app.alert('Complete. Copied the Price List Import file name: ' + file_name, title='Complete', mode='info')


def button_update_standard_only():
    df_pricelist: pd.DataFrame = ws_input['t_input[[#All]]'].options(pd.DataFrame, index=False).value
    df_std_export = df_pricelist[['Part_Nr', 'Cost']]
    df_std_export = df_std_export.rename({
        'Part_Nr': 'Item_Number',
        'Cost': 'Standard_Material_Cost'
    }, axis='columns')

    msgbox_return = xl_app.alert('Are you ready to continue?', title='Ready', mode='info', buttons='yes_no')

    if msgbox_return == 'yes':
        df_std_export.to_csv(server_path / 'stdprod.csv', index=False)
        xl_app.alert('Complete', title='Complete', mode='info')


def button_update_pricelist_only():
    today_date = datetime.datetime.today().strftime('%m%d%Y')
    df_pricelist: pd.DataFrame = ws_input['t_input[[#All]]'].options(pd.DataFrame, index=False).value

    price_name = df_pricelist['Supplier_Nr'].iloc[0]
    file_name = today_date + ' ' + price_name + '.csv'

    msgbox_return = xl_app.alert('Are you ready to continue?', title='Ready', mode='info', buttons='yes_no')

    if msgbox_return == 'yes':
        df_pricelist.to_csv(pricelist_path / file_name, index=False, header=False)
        pyperclip.copy(file_name)
        xl_app.alert('Complete. Copied the Price List Import file name: ' + file_name, title='Complete', mode='info')


if __name__ == "__main__":
    xw.Book('Update Standard and Pricelist.xlsb').set_mock_caller()

    # wb: xw.Book = xw.Book.caller()
    # ws_input: xw.Sheet = wb.sheets['Input']
    button_update_standard_pricelist()
