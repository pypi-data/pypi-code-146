import xlwings as xw
import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
import datetime

TEST_MODE = False

# Paths
server_path = Path(r'\\gvwac53\users\voucher\export')
this_path = Path(__file__).parent.resolve()
if TEST_MODE:
    server_path = this_path

# Set workbook variables
wb = xw.Book.caller()
ws_pricelist = wb.sheets['Data_Pricelist']
ws_inv_ent = wb.sheets['Individual Invoice Entry']
ws_msgbox = wb.sheets['Msgbox']
ws_overview = wb.sheets['Overview']
ws_import_link = wb.sheets['Import_Link']
ws_recon = wb.sheets['Recon']


def _sql_inv_ent(search_on, pack_or_po):
    conn = sqlite3.connect(this_path / 'ava.db')
    if pack_or_po == 'pack':
        df = pd.read_sql_query(
            f"""
            SELECT u.Packslip, u.Purchase_Order_Nr AS Purchase_Order, u.Item_Number, u.Qty_Open AS Qty_Shipped, '' AS UOM, u.Purchase_Cost AS Invoice_Unit_Price,
                '' AS Extended_Price, '' AS Unit_Price_to_Pay, u.Receiver, u.Line, u.Qty_Open,
                u.Rcpt_Dt AS Receiver_Date, '' AS Extended_Price_to_Pay, u.Purchase_Cost AS PO_Unit_Price,
                u.Supplier AS Supplier_Nr, '' AS Pricelist_Unit_Price, '' AS Invoice_Qty, '' AS Shortpay
            FROM t_Unvouchered u
            WHERE u.Packslip LIKE '%{search_on}%';
            """,
            conn
        )
    elif pack_or_po == 'po':
        df = pd.read_sql_query(
            f"""
            SELECT u.Packslip, u.Purchase_Order_Nr AS Purchase_Order, u.Item_Number, u.Qty_Open AS Qty_Shipped, '' AS UOM, u.Purchase_Cost AS Invoice_Unit_Price,
                '' AS Extended_Price, '' AS Unit_Price_to_Pay, u.Receiver, u.Line, u.Qty_Open,
                u.Rcpt_Dt AS Receiver_Date, '' AS Extended_Price_to_Pay, u.Purchase_Cost AS PO_Unit_Price,
                u.Supplier AS Supplier_Nr, '' AS Pricelist_Unit_Price, '' AS Invoice_Qty, '' AS Shortpay
            FROM t_Unvouchered u
            WHERE u.Purchase_Order_Nr LIKE '%{search_on}%';
            """,
            conn
        )
    conn.close()

    # Calculate Qty_Open & Qty_Shipped minus Qty_Submitted_Shipped
    df['Receiver_Line'] = df['Receiver'] + '-' + df['Line']
    try:
        df_receiver_line = _sql_receiver_line()
        df = df.merge(df_receiver_line, how='left', on='Receiver_Line').fillna(0)
    except Exception:
        df['Qty_Submitted_Shipped'] = 0
    df['Qty_Open'] = df['Qty_Open'] - df['Qty_Submitted_Shipped']
    df['Qty_Shipped'] = df['Qty_Shipped'] - df['Qty_Submitted_Shipped']

    # Drop unused columns
    df.drop(['Qty_Submitted_Shipped', 'Receiver_Line'], 1, inplace=True)

    return df


def _sql_supplier_name(search_supplier_nr):
    conn = sqlite3.connect(this_path / 'ava.db')
    df = pd.read_sql_query(
        f"""
        SELECT DISTINCT po.Supplier_Name
        FROM t_Purchase_Order po
        WHERE po.Supplier_Nr = '{search_supplier_nr}';
        """,
        conn
    )
    conn.close()
    return df


def _sql_import_inv_nr():
    conn = sqlite3.connect(this_path / 'ava.db')
    df = pd.read_sql_query(
        """
        SELECT DISTINCT i.Invoice_Number
        FROM t_Invoices_to_Import i;
        """,
        conn
    )
    conn.close()
    return df


def _sql_receiver_line():
    conn = sqlite3.connect(this_path / 'ava.db')
    df = pd.read_sql_query(
        """
        SELECT i."Receiver_Line", i.Qty_Shipped AS Qty_Submitted_Shipped
        FROM t_Invoices_to_Import i;
        """,
        conn
    )
    conn.close()
    return df


def _sql_item_number(search_item_number):
    conn = sqlite3.connect(this_path / 'ava.db')
    df = pd.read_sql_query(
        f"""
        SELECT DISTINCT '' AS Use_Receiver, u.Name AS Supplier_Name, u.Packslip, u.Purchase_Order_Nr AS Purchase_Order,
            Qty_Open, u.Rcpt_Dt AS Receiver_Date, u.Purchase_Cost AS PO_Unit_Price, pr.UM AS UOM,
            u.Receiver, u.Line, u.Supplier AS Supplier_Nr, u.Item_Number
        FROM t_Unvouchered u
        LEFT OUTER JOIN t_Pricelist pr
            ON u.Item_Number = pr.Item_Number
        WHERE u.Item_Number LIKE '%{search_item_number}%';
        """,
        conn
    )
    conn.close()

    # Fix UOM 0 column
    df['UOM'] = df['UOM'].fillna('EA')

    # Calculate Qty_Open & Qty_Shipped minus Qty_Submitted_Shipped
    df['Receiver_Line'] = df['Receiver'] + '-' + df['Line']
    try:
        df_receiver_line = _sql_receiver_line()
        df = df.merge(df_receiver_line, how='left', on='Receiver_Line').fillna(0)
    except Exception:
        df['Qty_Submitted_Shipped'] = 0
    df['Qty_Open'] = df['Qty_Open'] - df['Qty_Submitted_Shipped']

    # Drop unused columns
    df.drop(['Qty_Submitted_Shipped', 'Receiver_Line'], 1, inplace=True)

    return df


def _sql_get_invoices_to_import():
    conn = sqlite3.connect(this_path / 'ava.db')
    df = pd.read_sql_query(
        """
        SELECT *
        FROM t_Invoices_to_Import;
        """,
        conn
    )
    conn.close()
    return df


def _sql_retrieve_invoices_to_import_header(search_invoice_number):
    conn = sqlite3.connect(this_path / 'ava.db')
    df = pd.read_sql_query(
        f"""
        SELECT *
        FROM t_Invoices_to_Import i
        WHERE i.Invoice_Number = '{search_invoice_number}';
        """,
        conn
    )
    conn.close()
    return df


def _sql_retrieve_invoices_to_import_table(search_invoice_number):
    conn = sqlite3.connect(this_path / 'ava.db')
    df = pd.read_sql_query(
        f"""
        SELECT u.Packslip, u.Purchase_Order, u.Item_Number, u.Qty_Shipped, u.UOM, u.Invoice_Unit_Price,
            '' AS Extended_Price, '' AS Unit_Price_to_Pay, u.Receiver, u.Line, u.Qty_Open,
            u.Receiver_Date, '' AS Extended_Price_to_Pay, u.PO_Unit_Price,
            u.Supplier_Nr, '' AS Pricelist_Unit_Price, '' AS Invoice_Qty, '' AS Shortpay
        FROM t_Invoices_to_Import u
        WHERE u.Invoice_Number='{search_invoice_number}';
        """,
        conn
    )
    conn.close()
    return df


def _sql_delete_invoice(search_invoice_number):
    conn = sqlite3.connect(this_path / 'ava.db')
    sql = f"DELETE FROM t_Invoices_to_Import WHERE Invoice_Number='{search_invoice_number}';"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()


def _sql_check_valid_open_qty():
    conn = sqlite3.connect(this_path / 'ava.db')
    df = pd.read_sql_query(
        """
        SELECT i.Invoice_Number, i.Item_Number, i.Qty_Shipped AS Import_Qty_Shipped, u.Qty_Open AS Unvouchered_Qty_Open
        FROM t_Invoices_to_Import i
        LEFT OUTER JOIN t_Unvouchered u
            ON i.Receiver_Line = u.Unique_Rec_Line;
        """,
        conn
    )
    conn.close()
    return df


def _sql_import_link():
    conn = sqlite3.connect(this_path / 'ava.db')
    df = pd.read_sql_query(
        """
        SELECT i.Invoice_Number AS Invoice, i.Purchase_Order AS "Order", i.Supplier_Nr AS Supplier,
            i.Invoice_Date AS Date, i.Receiver, i.Line, i.Qty_Shipped AS "Inv Qty",
            i.Unit_Price_to_Pay AS "Curr Amt", i.Account AS Account_1, i.Cost_Center AS CC_1,
            i.Account_Amount AS Amount_1, i.Number_of_Pages
            FROM t_Invoices_to_Import i
        """,
        conn
    )
    conn.close()
    return df


def _sql_drop_invoices_to_import():
    conn = sqlite3.connect(this_path / 'ava.db')
    sql = 'DROP TABLE t_Invoices_to_Import'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()


def _sql_backup_invoices_to_import():
    dttime_now = datetime.datetime.now()
    backup_date = dttime_now.strftime('%m_%d_%Y_%H_%M_%S')

    conn = sqlite3.connect(this_path / 'ava.db')
    sql = f"""CREATE TABLE t_Backup_{backup_date} AS
            SELECT *
            FROM t_Invoices_to_Import;
    """
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()


def init():
    if ws_msgbox['M2'].value == '2.1':  # HARD CODED range - change to rng_avaver later
        conn = sqlite3.connect(this_path / 'ava.db')

        # Unvouchered
        df_unvouch = pd.read_csv(
            server_path / 'ava_unvouchered_receipt_export.csv', low_memory=False,
            converters={
                'Order': str,
                'Supplier': str,
                'Name': str,
                'Receiver': str,
                'Line': str,
                'Item Number': str,
                'Packslip#': str,
                # 'Rcpt Dt': str,
                # 'Eff Dt': str,
                # 'Qty Open': str,
                'Receipt Type': str,
                'Account': str,
                'Sub-Account': str,
                'Cost Center': str,
                # 'GL Cost': str,
                'C': str,
                # 'Purchase Cost': str,
                # 'Ext GL Cost': str,
                # 'Ext PO Cost': str,
                'Accrued Tax': str,
                'PO-GL Var': str
            },
            parse_dates=['Rcpt Dt', 'Eff Dt']
        )
        df_unvouch['Unique_Rec_Line'] = df_unvouch['Receiver'] + '-' + df_unvouch['Line']

        df_unvouch.rename(columns={
            'Order': 'Purchase_Order_Nr',
            'Packslip#': 'Packslip',
            'Item Number': 'Item_Number',
            'Receipt Type': 'Receipt_Type',
            'Cost Center': 'Cost_Center',
            'Accrued Tax': 'Accrued_Tax',
            'PO-GL Var': 'PO_GL_Var',
            'Rcpt Dt': 'Rcpt_Dt',
            'Eff Dt': 'Eff_Dt',
            'Qty Open': 'Qty_Open',
            'Purchase Cost': 'Purchase_Cost',
            'Ext GL Cost': 'Ext_GL_Cost',
            'Ext PO Cost': 'Ext_PO_Cost'
        }, inplace=True)

        df_unvouch.sort_values(by=['Rcpt_Dt'], ascending=False, inplace=True)
        df_unvouch.sort_values(by=['Item_Number'], inplace=True)
        df_unvouch.drop_duplicates(subset=['Unique_Rec_Line'], inplace=True)
        df_unvouch = df_unvouch[df_unvouch['Qty_Open'] != 0]
        df_unvouch.to_sql('t_Unvouchered', conn, if_exists='replace', index=False)

        # Pricelist
        df_pricelist = pd.read_csv(
            server_path / 'ava_price_list_export.csv', low_memory=False,
            converters={
                'Price List': str,
                'Supplier Name': str,
                'Curr': str,
                'Line': str,
                'Item Number': str,
                'Description': str,
                'UM': str,
                'Start': str,
                'Expire': str,
                'Modified Date': str,
                'AT': str,
                # 'Min Qty[1]': str,
                # 'Amount[1]': str,
                # 'Min Qty[2]': str,
                # 'Amount[2]': str,
                # 'Min Qty[3]': str,
                # 'Amount[3]': str,
                # 'Min Qty[4]': str,
                # 'Amount[4]': str,
                # 'Min Qty[5]': str,
                # 'Amount[5]': str,
            },
            # parse_dates=['Start', 'Modified Date']
        )
        today_date = datetime.date.today().strftime('%m/%d/%y')
        df_pricelist['Start'] = df_pricelist['Start'].str.replace('?', today_date)
        df_pricelist['Start'] = pd.to_datetime(df_pricelist['Start'], errors='coerce')
        df_pricelist['Custom_Lookup'] = df_pricelist['Price List'] + '-' + df_pricelist['Item Number']
        df_pricelist.rename(columns={
            'Price List': 'Price_List',
            'Supplier Name': 'Supplier_Name',
            'Item Number': 'Item_Number',
            'Min Qty[1]': 'Min_Qty_1',
            'Min Qty[2]': 'Min_Qty_2',
            'Min Qty[3]': 'Min_Qty_3',
            'Min Qty[4]': 'Min_Qty_4',
            'Min Qty[5]': 'Min_Qty_5',
            'Amount[1]': 'Amount_1',
            'Amount[2]': 'Amount_2',
            'Amount[3]': 'Amount_3',
            'Amount[4]': 'Amount_4',
            'Amount[5]': 'Amount_5',
        }, inplace=True)
        df_pricelist['UM'] = df_pricelist['UM'].str.upper()
        ws_pricelist.tables['t_pricelist'].update(df_pricelist)
        df_pricelist.to_sql('t_Pricelist', conn, if_exists='replace', index=False)

        # Purchase Order
        df_purchase_order = pd.read_csv(
            server_path / 'ava_purchase_order_export.csv', low_memory=False,
            converters={
                'Purchase Order': str,
                'Supplier Nr': str,
                'Supplier Name': str,
            }
        )
        df_purchase_order.rename(columns={
            'Purchase Order': 'Purchase_Order_Nr',
            'Supplier Nr': 'Supplier_Nr',
            'Supplier Name': 'Supplier_Name',

        }, inplace=True)
        df_purchase_order.to_sql('t_Purchase_Order', conn, if_exists='replace', index=False)

        conn.close()
    else:
        ws_msgbox['rng_msgbox_1'].value = 1


def button_find_receivers():
    rng_ref_inv = str(ws_inv_ent['rng_ref_inv'].value).strip()
    if rng_ref_inv == '':
        rng_ref_inv = 'None'
    rng_ref_packslip = str(ws_inv_ent['rng_ref_packslip'].value).strip()
    if rng_ref_packslip == '':
        rng_ref_packslip = 'None'
    rng_ref_po = str(ws_inv_ent['rng_ref_po'].value).strip()
    if rng_ref_po == '':
        rng_ref_po = 'None'
    bool_packslip_search = False
    bool_found = False
    bool_exit = False

    if rng_ref_inv != 'None' or rng_ref_packslip != 'None':
        bool_packslip_search = True

    # Search Invoice Nr
    if bool_packslip_search:
        df_inv_ent = _sql_inv_ent(rng_ref_inv, 'pack')
        if df_inv_ent.empty:
            if rng_ref_packslip != 'None':
                df_inv_ent = _sql_inv_ent(rng_ref_packslip, 'pack')
                if not df_inv_ent.empty:
                    ws_inv_ent['rng_ref_po'].value = df_inv_ent['Purchase_Order'].iloc[0]
                    bool_found = True
        else:
            ws_inv_ent['rng_ref_po'].value = df_inv_ent['Purchase_Order'].iloc[0]
            bool_found = True
    # Search PO
    if not bool_found and rng_ref_po != 'None':
        df_inv_ent = _sql_inv_ent(rng_ref_po, 'po')
        if not df_inv_ent.empty:
            bool_found = True

    if bool_found:
        # Check for multiple supplier nrs
        for _, r in df_inv_ent.iterrows():
            if r['Supplier_Nr'] != df_inv_ent['Supplier_Nr'].iloc[0]:
                ws_msgbox['rng_msgbox_1'].value = 1

        # Check for more than 300 receivers
        if len(df_inv_ent.index) > 300:
            ws_msgbox['rng_msgbox_2'].value = 1
            bool_exit = True

        # Update sheet
        if not bool_exit:
            ws_inv_ent.tables['t_inv_ent'].update(df_inv_ent)
            ws_inv_ent['rng_t_sup_nr'].value = df_inv_ent['Supplier_Nr'].iloc[0]
            df_supplier_name = _sql_supplier_name(df_inv_ent['Supplier_Nr'].iloc[0])
            ws_inv_ent['rng_sup_name'].value = df_supplier_name['Supplier_Name'].iloc[0]
    else:
        # Not found
        ws_msgbox['rng_msgbox_3'].value = 1

    _ws_inv_ent_formulas()


def _ws_inv_ent_formulas():
    ws_inv_ent['t_inv_ent[Extended_Price]'].value = '=ROUND([@[Invoice_Unit_Price]]*[@[Qty_Shipped]],2)'
    ws_inv_ent['t_inv_ent[Pricelist_Unit_Price]'].value = '=LET(' + \
        'amount_1,XLOOKUP([@[Supplier_Nr]]&"-"&[@[Item_Number]],t_pricelist[Custom_Lookup],t_pricelist[Amount_1]),' + \
        'amount_2,XLOOKUP([@[Supplier_Nr]]&"-"&[@[Item_Number]],t_pricelist[Custom_Lookup],t_pricelist[Amount_2]),' + \
        'amount_3,XLOOKUP([@[Supplier_Nr]]&"-"&[@[Item_Number]],t_pricelist[Custom_Lookup],t_pricelist[Amount_3]),' + \
        'amount_4,XLOOKUP([@[Supplier_Nr]]&"-"&[@[Item_Number]],t_pricelist[Custom_Lookup],t_pricelist[Amount_4]),' + \
        'amount_5,XLOOKUP([@[Supplier_Nr]]&"-"&[@[Item_Number]],t_pricelist[Custom_Lookup],t_pricelist[Amount_5]),' + \
        'qty_2,XLOOKUP([@[Supplier_Nr]]&"-"&[@[Item_Number]],t_pricelist[Custom_Lookup],t_pricelist[Min_Qty_2]),' + \
        'qty_3,XLOOKUP([@[Supplier_Nr]]&"-"&[@[Item_Number]],t_pricelist[Custom_Lookup],t_pricelist[Min_Qty_3]),' + \
        'qty_4,XLOOKUP([@[Supplier_Nr]]&"-"&[@[Item_Number]],t_pricelist[Custom_Lookup],t_pricelist[Min_Qty_4]),' + \
        'qty_5,XLOOKUP([@[Supplier_Nr]]&"-"&[@[Item_Number]],t_pricelist[Custom_Lookup],t_pricelist[Min_Qty_5]),' + \
        'IFNA(IFS(NOT(AND(amount_1>0,amount_2>0)),amount_1,[@[Invoice_Qty]]<qty_2,amount_1,OR([@[Invoice_Qty]]<qty_3,qty_3=0),' + \
        'amount_2,OR([@[Invoice_Qty]]<qty_4,qty_4=0),amount_3,OR([@[Invoice_Qty]]<qty_5,qty_5=0),amount_4,[@[Invoice_Qty]]>=qty_5,amount_5),"NO PL"))'
    ws_inv_ent['t_inv_ent[Unit_Price_to_Pay]'].value = '=IF(rng_shrt_pay_accept="YES",' + \
        '[@[Invoice_Unit_Price]],IFERROR(IF([@[Invoice_Unit_Price]]>([@[Pricelist_Unit_Price]]+0.5),[@[Pricelist_Unit_Price]],[@[Invoice_Unit_Price]]),' + \
        'IF([@[Invoice_Unit_Price]]>([@[PO_Unit_Price]]+0.5),[@[PO_Unit_Price]],[@[Invoice_Unit_Price]])))'
    ws_inv_ent['t_inv_ent[Extended_Price_to_Pay]'].value = '=IFERROR(ROUND([@[Unit_Price_to_Pay]]*[@[Qty_Shipped]],2),"NO PL")'
    ws_inv_ent['t_inv_ent[Shortpay]'].value = '=[@[Unit_Price_to_Pay]]<[@[Invoice_Unit_Price]]'
    ws_inv_ent['t_inv_ent[Invoice_Qty]'].value = '=SUMIFS([Qty_Shipped],[Item_Number],[@[Item_Number]])'
    ws_inv_ent['t_inv_ent[UOM]'].value = '=UPPER(XLOOKUP([@[Item_Number]],t_pricelist[Item_Number],t_pricelist[UM],"NO PL"))'

    ws_inv_ent['rng_sup_nr'].value = '=IF(rng_ref_po="","",' + \
        'XLOOKUP(rng_t_sup_nr,t_supplier_correct[Supplier Number],t_supplier_correct[Correct Supplier Number],rng_t_sup_nr))'
    ws_inv_ent['rng_shrt_pay_accept'].value = '=IF(rng_sup_nr="10000041","YES","NO")'
    ws_inv_ent['rng_l_inv_tot_rec'].value = '=IF(rng_inv_total="","Invoice Total",IF(rng_inv_tot_rec=rng_inv_total,"Invoice Total Reconciles","Invoice Total NOT Reconciling"))'
    ws_inv_ent['rng_l_inv_tot_to_pay'].value = '=IF(rng_inv_total="","Invoice Total",IF(rng_inv_tot_to_pay="Not Received","Not Received",' + \
        'IF(rng_inv_tot_rec=rng_inv_total,IF(rng_inv_tot_to_pay<rng_inv_tot_rec,"Short Pay","Invoice Total to Pay"),"")))'
    ws_inv_ent['rng_inv_tot_rec'].value = '=ROUND(SUM(t_inv_ent[Extended_Price])+rng_ref_acnt_amnt,2)'
    ws_inv_ent['rng_inv_tot_to_pay'].value = '=IF(COUNTBLANK(t_inv_ent[Receiver])>0,"Not Received",ROUND(SUM(t_inv_ent[Extended_Price_to_Pay])+rng_ref_acnt_amnt,2))'


def button_submit_good():
    ref_inv = ws_inv_ent['rng_ref_inv'].value
    inv_date = ws_inv_ent['rng_inv_date'].value
    sup_nr = ws_inv_ent['rng_sup_nr'].value
    inv_total = ws_inv_ent['rng_inv_total'].value

    acnt = ws_inv_ent['rng_ref_acnt'].value
    cc = ws_inv_ent['rng_ref_cc'].value
    acnt_amnt = ws_inv_ent['rng_ref_acnt_amnt'].value
    nr_pages = ws_inv_ent['rng_nr_pages'].value

    conn = sqlite3.connect(this_path / 'ava.db')

    df_inv_ent: pd.DataFrame = ws_inv_ent['t_inv_ent[[#All]]'].options(pd.DataFrame, index=False).value

    # Account, Cost Centre, Amount
    df_inv_ent['Account'] = ''
    df_inv_ent['Account'].iloc[0] = acnt
    df_inv_ent['Cost_Center'] = ''
    df_inv_ent['Cost_Center'].iloc[0] = cc
    df_inv_ent['Account_Amount'] = 0
    if acnt_amnt != 0 and acnt_amnt is not None:
        df_inv_ent['Account_Amount'].iloc[0] = acnt_amnt
    df_inv_ent['Number_of_Pages'] = np.nan
    df_inv_ent['Number_of_Pages'].iloc[0] = nr_pages

    # Invoice number & date & supplier nr & packslip & invoice total
    df_inv_ent['Invoice_Number'] = ref_inv
    df_inv_ent['Invoice_Date'] = inv_date
    df_inv_ent['Supplier_Nr'] = sup_nr
    df_inv_ent['Entered_Invoice_Total'] = inv_total

    # Change types
    df_inv_ent['Supplier_Nr'] = df_inv_ent['Supplier_Nr'].astype(str)
    df_inv_ent['Line'] = df_inv_ent['Line'].astype(str)
    df_inv_ent['Receiver'] = df_inv_ent['Receiver'].astype(str)

    # Calculations
    df_inv_ent['Receiver_Line'] = df_inv_ent['Receiver'].astype(str) + '-' + df_inv_ent['Line'].astype(str)
    df_inv_ent['Invoice_Total'] = df_inv_ent['Extended_Price_to_Pay'] + df_inv_ent['Account_Amount'].fillna(0)
    df_inv_ent['Capture_Date'] = datetime.date.today().strftime('%m/%d/%y')

    # Calculate Qty_Open & Qty_Shipped minus Qty_Submitted_Shipped
    try:
        df_receiver_line = _sql_receiver_line()
        df_inv_ent = df_inv_ent.merge(df_receiver_line, how='left', on='Receiver_Line')
        df_inv_ent['Qty_Submitted_Shipped'] = df_inv_ent['Qty_Submitted_Shipped'].fillna(0)
    except Exception:
        df_inv_ent['Qty_Submitted_Shipped'] = 0
    df_inv_ent['Qty_Open'] = df_inv_ent['Qty_Open'] - df_inv_ent['Qty_Submitted_Shipped']
    df_inv_ent['Qty_Shipped'] = df_inv_ent['Qty_Shipped'] - df_inv_ent['Qty_Submitted_Shipped']

    # Drop unused columns
    # TODO: drop Extended shortpay column below
    df_inv_ent.drop([' ', 'Qty_Submitted_Shipped'], 1, inplace=True)

    # Reorder columns
    df_inv_ent = df_inv_ent.reindex(columns=[
        'Invoice_Number', 'Supplier_Nr', 'Invoice_Date', 'Purchase_Order', 'Packslip', 'Entered_Invoice_Total',
        'Item_Number', 'Qty_Shipped', 'UOM', 'Invoice_Unit_Price', 'Extended_Price', 'Receiver', 'Line', 'Qty_Open', 'Receiver_Date',
        'Unit_Price_to_Pay', 'Extended_Price_to_Pay', 'PO_Unit_Price', 'Pricelist_Unit_Price', 'Account', 'Cost_Center',
        'Account_Amount', 'Number_of_Pages', 'Shortpay', 'Receiver_Line', 'Invoice_Total', 'Capture_Date'
    ])

    df_inv_ent.to_sql('t_Invoices_to_Import', conn, if_exists='append', index=False)

    conn.close()


def check_inv_exist_in_import():
    ref_inv = ws_inv_ent['rng_ref_inv'].value
    bool_exit = False
    try:
        df_import_inv = _sql_import_inv_nr()
    except Exception:
        bool_exit = True

    if not bool_exit:
        if ref_inv in df_import_inv['Invoice_Number'].values:
            ws_msgbox['rng_msgbox_1'].value = 1


def button_find_missing_receiver():
    ref_itemnr = ws_inv_ent['rng_ref_itemnr'].value

    df_mis_rec = _sql_item_number(ref_itemnr)

    if not df_mis_rec.empty:
        df_mis_rec['UOM'] = df_mis_rec['UOM'].str.upper()
        ws_inv_ent.tables['t_mis_rec'].update(df_mis_rec)
    else:
        ws_msgbox['rng_msgbox_1'].value = 1


def button_use_receivers():
    df_inv_ent: pd.DataFrame = ws_inv_ent['t_inv_ent[[#All]]'].options(pd.DataFrame, index=False).value

    df_mis_rec: pd.DataFrame = ws_inv_ent['t_mis_rec[[#All]]'].options(pd.DataFrame, index=False).value
    df_mis_rec = df_mis_rec[df_mis_rec['Use_Receiver'].notnull()]
    df_mis_rec = df_mis_rec.loc[df_mis_rec['Use_Receiver'] != '']

    bool_exit = False

    if df_mis_rec.empty:
        ws_msgbox['rng_msgbox_1'].value = 1
        bool_exit = True

    if not bool_exit:
        df_mis_rec['Qty_Shipped'] = df_mis_rec['Qty_Open']
        df_mis_rec['Invoice_Unit_Price'] = df_mis_rec['PO_Unit_Price']
        df_mis_rec['Extended_Price'] = ''
        df_mis_rec['Unit_Price_to_Pay'] = ''
        df_mis_rec['Extended_Price_to_Pay'] = ''
        df_mis_rec['Pricelist_Unit_Price'] = ''
        df_mis_rec['Invoice_Qty'] = ''
        df_mis_rec['Shortpay'] = ''
        df_mis_rec.drop(['Use_Receiver', 'Supplier_Name'], 1, inplace=True)

        df_inv_ent = df_inv_ent.append(df_mis_rec, ignore_index=True)
        df_inv_ent.drop(' ', 1, inplace=True)
        # df_inv_ent Drop nan rows
        df_inv_ent = df_inv_ent[df_inv_ent['Receiver'].notna()]

        ws_inv_ent.tables['t_inv_ent'].update(df_inv_ent)

        # Add supplier nr & po nr
        ws_inv_ent['rng_t_sup_nr'].value = df_mis_rec['Supplier_Nr'].iloc[0]
        df_supplier_name = _sql_supplier_name(df_mis_rec['Supplier_Nr'].iloc[0])
        ws_inv_ent['rng_sup_name'].value = df_supplier_name['Supplier_Name'].iloc[0]
        ws_inv_ent['rng_ref_po'].value = df_mis_rec['Purchase_Order'].iloc[0]

        _ws_inv_ent_formulas()


def button_refresh_overview():
    bool_exit = False

    try:
        df_overview = _sql_get_invoices_to_import()
    except Exception:
        ws_msgbox['rng_msgbox_1'].value = 1
        bool_exit = True

    if not bool_exit:
        p_overview = pd.pivot_table(df_overview, values='Invoice_Total', index='Invoice_Number', aggfunc=np.sum)
        df_overview.drop_duplicates(subset='Invoice_Number', keep='first', inplace=True)
        p_overview = p_overview.merge(df_overview[['Invoice_Number', 'Supplier_Nr']], how='left', on='Invoice_Number')
        p_overview['Retrieve'] = ''
        p_overview = p_overview.reindex(columns=['Retrieve', 'Invoice_Number', 'Supplier_Nr', 'Invoice_Total'])

        ws_overview.tables['p_overview'].update(p_overview)


def button_bring_back():
    bool_exit = False

    df_overview: pd.DataFrame = ws_overview['p_overview[[#All]]'].options(pd.DataFrame, index=False).value
    df_overview = df_overview[df_overview['Retrieve'].notnull()]
    df_overview = df_overview[df_overview['Retrieve'] != '']

    if df_overview.empty:
        ws_msgbox['rng_msgbox_1'].value = 1
        bool_exit = True

    if not bool_exit:
        invoice_number = df_overview['Invoice_Number'].iloc[0]
        df_inv_import = _sql_retrieve_invoices_to_import_header(invoice_number)

        # Header
        ws_inv_ent['rng_ref_inv'].value = invoice_number
        _date = str(df_inv_import['Invoice_Date'].iloc[0])
        _date = _date[5:7] + '/' + _date[8:10] + '/' + _date[:4]
        ws_inv_ent['rng_inv_date'].value = _date
        ws_inv_ent['rng_ref_packslip'].value = df_inv_import['Packslip'].iloc[0]
        ws_inv_ent['rng_ref_po'].value = df_inv_import['Purchase_Order'].iloc[0]
        ws_inv_ent['rng_inv_total'].value = df_inv_import['Entered_Invoice_Total'].iloc[0]
        ws_inv_ent['rng_nr_pages'].value = df_inv_import['Number_of_Pages'].iloc[0]

        # Table
        df_inv_ent = _sql_retrieve_invoices_to_import_table(invoice_number)

        ws_inv_ent.tables['t_inv_ent'].update(df_inv_ent)
        ws_inv_ent['rng_t_sup_nr'].value = df_inv_ent['Supplier_Nr'].iloc[0]
        df_supplier_name = _sql_supplier_name(df_inv_ent['Supplier_Nr'].iloc[0])
        ws_inv_ent['rng_sup_name'].value = df_supplier_name['Supplier_Name'].iloc[0]

        # Clear SQL table of this invoice
        _sql_delete_invoice(invoice_number)

        # Refresh Overview
        button_refresh_overview()

        _ws_inv_ent_formulas()


def check_valid_open_qty():
    # Check for valid open qty
    df_import_inv = _sql_check_valid_open_qty()
    df_import_inv['Unvouchered_Qty_Open'] = df_import_inv['Unvouchered_Qty_Open'].fillna(0)
    df_import_inv['Qty_Open_Check'] = df_import_inv['Unvouchered_Qty_Open'] - df_import_inv['Import_Qty_Shipped']

    df_check = df_import_inv[df_import_inv['Qty_Open_Check'] < 0]
    if not df_check.empty:
        ws_msgbox['rng_msgbox_1'].value = 1
        ws_msgbox.tables['t_check'].update(df_check)


def button_import(user_name: str = 'Unknown_User'):
    dttime_now = datetime.datetime.now()
    file_date = dttime_now.strftime('%m-%d-%Y-%H-%M-%S')

    df_import_link = _sql_import_link()

    # Round unit price and journal amount to pay to 9 digits
    df_import_link['Curr Amt'] = df_import_link['Curr Amt'].round(9)
    df_import_link['Amount_1'] = df_import_link['Amount_1'].round(9)

    df_import_link['Enty_1'] = '2000'

    df_import_link['Extended_Amount'] = 0

    df_import_csv = df_import_link

    df_import_csv = df_import_csv.drop(['Extended_Amount', 'Number_of_Pages'], 1)
    df_import_csv['Date'] = df_import_csv['Date'].str[5:7] + '/' + df_import_csv['Date'].str[8:10] + '/' + df_import_csv['Date'].str[2:4]

    # Change Amount_1 = 0 to Nan
    df_import_csv['Amount_1'].replace(0, np.nan, inplace=True)

    # Add columns (not used)
    df_import_csv['Sub-Acct_1'] = ''
    df_import_csv['Project_1'] = ''
    df_import_csv['Project_1'] = ''
    df_import_csv['Account_2'] = ''
    df_import_csv['Sub-Acct_2'] = ''
    df_import_csv['CC_2'] = ''
    df_import_csv['Project_2'] = ''
    df_import_csv['Enty_2'] = ''
    df_import_csv['Amount_2'] = ''
    df_import_csv['Account_3'] = ''
    df_import_csv['Sub-Acct_3'] = ''
    df_import_csv['CC_3'] = ''
    df_import_csv['Project_3'] = ''
    df_import_csv['Enty_3'] = ''
    df_import_csv['Amount_3'] = ''
    df_import_csv['Account_4'] = ''
    df_import_csv['Sub-Acct_4'] = ''
    df_import_csv['CC_4'] = ''
    df_import_csv['Project_4'] = ''
    df_import_csv['Enty_4'] = ''
    df_import_csv['Amount_4'] = ''

    # Reorder columns
    df_import_csv = df_import_csv.reindex(columns=[
        'Invoice',
        'Order',
        'Supplier',
        'Date',
        'Receiver',
        'Line',
        'Inv Qty',
        'Curr Amt',
        'Account_1',
        'Sub-Acct_1',
        'CC_1',
        'Project_1',
        'Enty_1',
        'Amount_1',
        'Account_2',
        'Sub-Acct_2',
        'CC_2',
        'Project_2',
        'Enty_2',
        'Amount_2',
        'Account_3',
        'Sub-Acct_3',
        'CC_3',
        'Project_3',
        'Enty_3',
        'Amount_3',
        'Account_4',
        'Sub-Acct_4',
        'CC_4',
        'Project_4',
        'Enty_4',
        'Amount_4',
    ])

    # Save CSV
    if TEST_MODE:
        csv_location = this_path
    else:
        csv_location = Path(r'\\gvwac53\users\voucher\import')
    csv_filename = 'ava-' + user_name + '-' + file_date + '.csv'

    df_import_csv.to_csv(csv_location / csv_filename, index=False)
    ws_import_link.tables['t_import_link'].update(df_import_link)

    ws_import_link['t_import_link[Extended_Amount]'].value = '=ROUND([@[Inv Qty]]*[@[Curr Amt]],2)+ROUND([@[Amount_1]],2)'

    ws_recon['B2'].value = csv_filename


def button_clear_captured():
    try:
        _sql_drop_invoices_to_import()
    except Exception:
        ws_msgbox['rng_msgbox_1'].value = 1


def button_finish_recon(user_name: str = 'Unknown_User', batch: str = 'Unknown_Batch'):
    dttime_now = datetime.datetime.now()
    file_date = dttime_now.strftime('%m-%d-%Y-%H-%M-%S')

    df_import = _sql_get_invoices_to_import()

    # Adjust df_import to match previous files
    # Renamed columns Invoice Number
    df_import.rename(columns={'Invoice_Number': 'Invoice Number'}, inplace=True)
    # Renamed columns Supplier Nr
    df_import.rename(columns={'Supplier_Nr': 'Supplier Nr'}, inplace=True)
    # Renamed columns Invoice Date
    df_import.rename(columns={'Invoice_Date': 'Invoice Date'}, inplace=True)
    # Renamed columns PO Number
    df_import.rename(columns={'Purchase_Order': 'PO Number'}, inplace=True)
    # Renamed columns Pack Slip
    df_import.rename(columns={'Packslip': 'Pack Slip'}, inplace=True)
    # Renamed columns Entered Invoice Total
    df_import.rename(columns={'Entered_Invoice_Total': 'Entered Invoice Total'}, inplace=True)
    # Renamed columns Item Number
    df_import.rename(columns={'Item_Number': 'Item Number'}, inplace=True)
    # Renamed columns Qty Shipped
    df_import.rename(columns={'Qty_Shipped': 'Qty Shipped'}, inplace=True)
    # Renamed columns  Invoice Unit Price
    df_import.rename(columns={'Invoice_Unit_Price': ' Invoice Unit Price '}, inplace=True)
    # Renamed columns  Extended Price
    df_import.rename(columns={'Extended_Price': ' Extended Price '}, inplace=True)
    # Renamed columns  Receiver
    df_import.rename(columns={'Receiver': ' Receiver '}, inplace=True)
    # Renamed columns  Line
    df_import.rename(columns={'Line': ' Line '}, inplace=True)
    # Renamed columns  Qty Open
    df_import.rename(columns={'Qty_Open': ' Qty Open '}, inplace=True)
    # Renamed columns  Receiver Date
    df_import.rename(columns={'Receiver_Date': ' Receiver Date '}, inplace=True)
    # Renamed columns  Unit Price to Pay
    df_import.rename(columns={'Unit_Price_to_Pay': ' Unit Price to Pay '}, inplace=True)
    # Renamed columns  Extended Price to Pay
    df_import.rename(columns={'Extended_Price_to_Pay': ' Extended Price to Pay '}, inplace=True)
    # Renamed columns  PO Unit Price
    df_import.rename(columns={'PO_Unit_Price': ' PO Unit Price '}, inplace=True)
    # Renamed columns  Pricelist Unit Price
    df_import.rename(columns={'Pricelist_Unit_Price': ' Pricelist Unit Price '}, inplace=True)
    # Renamed columns  Account
    df_import.rename(columns={'Account': ' Account '}, inplace=True)
    # Renamed columns  Cost Center
    df_import.rename(columns={'Cost_Center': ' Cost Center '}, inplace=True)
    # Renamed columns  Account Amount
    df_import.rename(columns={'Account_Amount': ' Account Amount '}, inplace=True)
    # Renamed columns  Number of Pages
    df_import.rename(columns={'Number_of_Pages': ' Number of Pages '}, inplace=True)
    # Renamed columns  Shortpay
    df_import.rename(columns={'Shortpay': ' Shortpay '}, inplace=True)
    # Renamed columns  Receiver-Line
    df_import.rename(columns={'Receiver_Line': ' Receiver-Line '}, inplace=True)
    # Renamed columns  Invoice Total
    df_import.rename(columns={'Invoice_Total': ' Invoice Total '}, inplace=True)
    # Renamed columns Capture Date
    df_import.rename(columns={'Capture_Date': 'Capture Date'}, inplace=True)
    # Added column Qty_Less
    df_import.insert(19, ' Qty_Less ', 0)
    # Added column Qty Open Check
    df_import.insert(28, ' Qty Open Check ', 0)

    # Fix date formats
    df_import['Invoice Date'] = df_import['Invoice Date'].str[5:7] + '/' + df_import['Invoice Date'].str[8:10] + '/' + df_import['Invoice Date'].str[2:4]
    df_import[' Receiver Date '] = df_import[' Receiver Date '].str[5:7] + '/' + df_import[' Receiver Date '].str[8:10] + '/' + df_import[' Receiver Date '].str[2:4]
    df_import[' Shortpay '] = df_import[' Shortpay '].map({0: 'FALSE', 1: 'TRUE'})

    # Save CSV
    if TEST_MODE:
        csv_location = this_path
    else:
        csv_location = Path(r'\\gvwac09\Public\Finance\AP Batch\Database\AVA')

    csv_filename = batch + '-' + user_name + '-' + file_date + '.csv'
    df_import.to_csv(csv_location / csv_filename, index=False)

    # Backup and drop invoices to import
    _sql_backup_invoices_to_import()
    _sql_drop_invoices_to_import()


if __name__ == "__main__":
    xw.Book(this_path / 'AVA_2.1.xlsb').set_mock_caller()
    # Only used to debug Set workbook variables
    # ---------
    # wb = xw.Book.caller()
    # ws_pricelist = wb.sheets['Data_Pricelist']
    # ws_inv_ent = wb.sheets['Individual Invoice Entry']
    # ws_msgbox = wb.sheets['Msgbox']
    # ws_overview = wb.sheets['Overview']
    # ws_import_link = wb.sheets['Import_Link']
    # ws_recon = wb.sheets['Recon']
    # ---------
    init()
