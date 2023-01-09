"""
Owner: kuldeep.singh@zeno.health
Purpose: This script calculates the movement(all reasons) of inventory, for all the stores, between two dates.
"""
import argparse
import datetime
import sys
import os

import numpy as np
# from memory_profiler import profile

import pandas as pd

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.db.db import DB
# from zeno_etl_libs.utils.inventory.inventory_2 import Data
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper import helper


def remove_duplicates(df: pd.DataFrame, f):
    """
    #remove duplicates from dataframe of the form id, f, ptr
    #f corresponds to quantity which is added up for duplicate ids
    #ptr remains same for all
    """
    print(f"Removed duplicates on column: {f}")
    df1 = df.groupby('id', as_index=False)[f].sum()
    df2 = df.drop_duplicates(subset='id').drop(columns=f)
    df = pd.merge(left=df1, right=df2, on='id', how='left')
    return df


def getids(df: pd.DataFrame):
    """
    utility function to generate string to be used in "in" query
    """
    return ",".join(str(i) for i in df['id'].unique())


def combin_xin(recon_l: pd.DataFrame, xin_l: pd.DataFrame):
    """
    this will take care of stores own inventory coming back
    """

    return pd.concat([recon_l, xin_l], axis=0).drop_duplicates(subset='id')


class Data:
    """
    class to get the inventory related data

    Example:
        'o', 'cr', 'xin', 'xout', 'ret', 'sold', 'del', 'ar', 'rr', 'c'
    """

    def __init__(self, db, csv_store_ids, start_date, end_date, snapshot_ist_time_delta=0):
        """
        :param db: database connection
        :param csv_store_ids: multiple store ids in csv
        :param start_date: start date in IST
        :param end_date: end date in IST
        """

        self.db = db
        self.csv_store_ids = csv_store_ids
        self.start_ts = f"{start_date}  02:00:00"  # in IST
        self.end_ts = f"{end_date} 03:00:00"  # in IST

        """ since snapshots names are in UTC so tables alias is one day back"""
        start_date_utc = datetime.datetime.strptime(start_date, '%Y-%m-%d') - datetime.timedelta(
            days=snapshot_ist_time_delta)
        start_date_utc = start_date_utc.strftime("%Y-%m-%d")

        end_date_utc = datetime.datetime.strptime(end_date, '%Y-%m-%d') - datetime.timedelta(
            days=snapshot_ist_time_delta)
        end_date_utc = end_date_utc.strftime("%Y-%m-%d")

        self.s_alias = f"-mis-{start_date_utc}"
        if start_date == "2022-06-01":
            # Only for  2022-06-01 manual snapshot, since snapshot name and date are same
            self.s_alias = f"-mis-{start_date}"

        self.e_alias = f"-inv-{end_date_utc}"

        self.s_schema = "public"
        self.e_schema = "public"

        """ Data frames """
        self.recon_l = pd.DataFrame()  # Final reconciled data frame
        self.p_l = pd.DataFrame()  # purchased / received
        self.prd_l = pd.DataFrame()  # purchased return dispatched
        self.prs_l = pd.DataFrame()  # purchased return settled
        self.pr_l = pd.DataFrame()  # purchased return cogs
        self.o_l = pd.DataFrame()  # opening / initial
        self.cr_l = pd.DataFrame()  #
        self.xin_l = pd.DataFrame()  #
        self.xout_l = pd.DataFrame()  #
        self.sold_l = pd.DataFrame()  #
        self.ret_l = pd.DataFrame()  #
        self.ar_l = pd.DataFrame()  #
        self.rr_l = pd.DataFrame()  #
        self.del_l = pd.DataFrame()  #
        self.c_l = pd.DataFrame()  #

    def take_union(self):
        """
        select one value of barcode from left or right data frame
        """
        for col in ['barcode', 'ptr']:
            self.recon_l[col] = np.where(self.recon_l[f'{col}_x'].isna(), self.recon_l[f'{col}_y'],
                                         self.recon_l[f'{col}_x'])
            self.recon_l.drop(columns=[f'{col}_x', f'{col}_y'], axis=1, inplace=True)

    def opening(self):
        """
        opening inventory calculation
        """

        q = f"""
        select
            id,
            nvl("barcode-reference", 0) barcode,
            quantity o,
            ptr
        from
            "{self.s_schema}"."inventory-1{self.s_alias}"
        where
            "store-id" in ({self.csv_store_ids})
            and "barcode-reference" is null
            and quantity != 0
        order by
            id
        """
        o_l_1 = self.db.get_df(query=q)

        q = f"""
            select
                id,
                nvl("barcode-reference", 0) barcode,
                quantity o,
                ptr
            from
                "{self.s_schema}"."inventory-1{self.s_alias}"
            where
                "store-id" in ({self.csv_store_ids})
                and "barcode-reference" is not null
                and quantity != 0
            order by
                id
            """
        o_l_2 = self.db.get_df(query=q)

        self.o_l = pd.concat([o_l_1, o_l_2], ignore_index=True)
        return self.o_l

    def purchased(self):
        """
        purchased inventory calculation
        """

        q = f"""
        select
            c.id,
            nvl("barcode-reference", 0) barcode,
            a."actual-quantity" p,
            c.ptr
        from
            "{self.e_schema}"."invoice-items-1{self.e_alias}" a
        join "{self.e_schema}"."invoices-1{self.e_alias}" b on
            a."franchisee-invoice-id" = b.id
        join "{self.e_schema}"."inventory-1{self.e_alias}" c on
            (c."invoice-item-id" = a.id
                and c."store-id" = b."store-id")
        where
            b."store-id" in ({self.csv_store_ids})
            and b."received-at" >= '{self.start_ts}'
            and b."received-at" <= '{self.end_ts}'
            and a."actual-quantity" !=0
        """
        self.p_l = self.db.get_df(query=q)
        return self.p_l

    def purchase_returns(self):
        """
        purchase returns cogs inventory calculation
        """

        q = f"""
        select
            e.id,
            nvl("barcode-reference", 0) barcode,
            sum(nvl(d."returned-quantity", 0)) pr,
            e.ptr
        from
            "{self.e_schema}"."debit-notes-1{self.e_alias}" a
        join "{self.e_schema}"."debit-note-items-1{self.e_alias}" c on
            c."debit-note-id" = a."id"
        join "{self.e_schema}"."return-items-1{self.e_alias}" d on
            d."id" = c."item-id"
        join "{self.e_schema}"."inventory-1{self.e_alias}" e on
            e."id" = d."inventory-id"
        where
            a."store-id" in ({self.csv_store_ids})
            and c."is-active" = true
            and a."settled-at" >= '{self.start_ts}'
            and a."settled-at" <= '{self.end_ts}'
            and d."returned-quantity" !=0
        group by 
            e.id, "barcode-reference", e.ptr
        """
        self.pr_l = self.db.get_df(query=q)
        return self.pr_l

    def purchased_return_dispatched(self):
        """
        purchased return dispatched inventory calculation
        """

        q = f"""
        select
            d.id ,
            nvl("barcode-reference", 0) barcode,
            sum(nvl(c."returned-quantity", 0)) prd,
            d."ptr" 
        from
            "{self.e_schema}"."debit-notes-1{self.e_alias}" a
        join "{self.e_schema}"."debit-note-items-1{self.e_alias}" b on
            b."debit-note-id" = a.id
        join "{self.e_schema}"."return-items-1{self.e_alias}" c on
            b."item-id" = c.id
        join "{self.e_schema}"."returns-to-dc-1{self.e_alias}" e on
            c."return-id" = e.id
        join "{self.e_schema}"."inventory-1{self.e_alias}" d on
            c."inventory-id" = d.id
        where
            e."store-id" in ({self.csv_store_ids})
            and a."dispatched-at" >= '{self.start_ts}'
            and a."dispatched-at" <= '{self.end_ts}'
        group by 
            d.id, "barcode-reference", d.ptr
        """

        self.prd_l = self.db.get_df(query=q)
        return self.prd_l

    def purchased_return_settled(self):
        """
        purchased return settled inventory calculation
        """

        q = f"""
        select
            d.id ,
            nvl("barcode-reference", 0) barcode,
            sum(nvl(c."returned-quantity",0)) prs,
            d."ptr" 
        from
            "{self.e_schema}"."debit-notes-1{self.e_alias}" a
        join "{self.e_schema}"."debit-note-items-1{self.e_alias}" b on
            b."debit-note-id" = a.id
        join "{self.e_schema}"."return-items-1{self.e_alias}" c on
            b."item-id" = c.id
        join "{self.e_schema}"."returns-to-dc-1{self.e_alias}" e on
            c."return-id" = e.id
        join "{self.e_schema}"."inventory-1{self.e_alias}" d on
            c."inventory-id" = d.id
        where
            e."store-id" in ({self.csv_store_ids})
            and a."settled-at" >= '{self.start_ts}'
            and a."settled-at" <= '{self.end_ts}'
        group by
            d.id, "barcode-reference", d.ptr
        """

        self.prs_l = self.db.get_df(query=q)
        return self.prs_l

    def customer_returns(self):
        """
        customer return inventory calculation
        """
        q = f"""
        select
            c.id,
            nvl("barcode-reference", 0) barcode,
            a."returned-quantity" cr,
            c.ptr
        from
            "{self.e_schema}"."customer-return-items-1{self.e_alias}" a
        join "{self.e_schema}"."customer-returns-1{self.e_alias}" b on
            a."return-id" = b.id
        join "{self.e_schema}"."inventory-1{self.e_alias}" c on
            (a."inventory-id" = c.id
                and c."store-id" = b."store-id")
        where
            b."store-id" in ({self.csv_store_ids})
            and b."returned-at" >= '{self.start_ts}'
            and b."returned-at" <= '{self.end_ts}'
            and a."returned-quantity" !=0
        union all
        select
            c.id,
            nvl("barcode-reference", 0) barcode,
            a."returned-quantity" cr,
            c.ptr
        from
            "{self.e_schema}"."customer-return-items-1{self.e_alias}" a
        join "{self.e_schema}"."customer-returns-1{self.e_alias}" b on
            a."return-id" = b.id
        join "{self.e_schema}"."inventory-1{self.e_alias}" c on
            (a."inventory-id" = c."barcode-reference"
                and c."store-id" = b."store-id")
        where
            b."store-id" in ({self.csv_store_ids})
            and b."returned-at" >= '{self.start_ts}'
            and b."returned-at" <= '{self.end_ts}'
            and a."returned-quantity" !=0
        """

        self.cr_l = self.db.get_df(query=q)
        self.cr_l = remove_duplicates(df=self.cr_l, f="cr")
        return self.cr_l

    def xin(self):
        """
        Stock transfer in - inventory calculation
        """
        q = f"""
        select
            c.id,
            nvl("barcode-reference", 0) barcode,
            a.quantity xin,
            c.ptr
        from
            "{self.e_schema}"."stock-transfer-items-1{self.e_alias}" a
        join "{self.e_schema}"."stock-transfers-1{self.e_alias}" b on
            a."transfer-id" = b.id
        join "{self.e_schema}"."inventory-1{self.e_alias}" c on
            (a."inventory-id" = c.id
                and c."store-id" = b."destination-store")
        where
            b."destination-store" in ({self.csv_store_ids})
            and b."received-at" >= '{self.start_ts}'
            and b."received-at" <= '{self.end_ts}'
            and a.quantity !=0
        union all

        select
            c.id,
            nvl("barcode-reference", 0) barcode,
            a.quantity xin,
            c.ptr
        from
            "{self.e_schema}"."stock-transfer-items-1{self.e_alias}" a
        join "{self.e_schema}"."stock-transfers-1{self.e_alias}" b on
            a."transfer-id" = b.id
        join "{self.e_schema}"."inventory-1{self.e_alias}" c on
            (a."inventory-id" = c."barcode-reference"
                and c."store-id" = b."destination-store")
        where
            b."destination-store" in ({self.csv_store_ids})
            and b."received-at" >= '{self.start_ts}'
            and b."received-at" <= '{self.end_ts}'
            and a.quantity !=0
        """
        self.xin_l = self.db.get_df(query=q)
        self.xin_l = remove_duplicates(df=self.xin_l, f="xin")
        return self.xin_l

    def xout(self):
        """
        Stock transfer out inventory calculation
        """

        q = f"""
        select
            c.id,
            nvl("barcode-reference", 0) barcode,
            a."quantity" xout,
            c.ptr
        from
            "{self.e_schema}"."stock-transfer-items-1{self.e_alias}" a
        join "{self.e_schema}"."stock-transfers-1{self.e_alias}" b on
            a."transfer-id" = b.id
        join "{self.e_schema}"."inventory-1{self.e_alias}" c on
            (a."inventory-id" = c.id
                and c."store-id" = b."source-store")
        where
            b."source-store" in ({self.csv_store_ids})
            and a."transferred-at" >= '{self.start_ts}'
            and a."transferred-at" <= '{self.end_ts}'
            and a.quantity !=0

        union all

        select
            c.id,
            nvl("barcode-reference", 0) barcode,
            a."quantity" xout,
            c.ptr
        from
            "{self.e_schema}"."stock-transfer-items-1{self.e_alias}" a
        join "{self.e_schema}"."stock-transfers-1{self.e_alias}" b on
            a."transfer-id" = b.id
        join "{self.e_schema}"."inventory-1{self.e_alias}" c on
            (a."inventory-id" = c."barcode-reference"
                and c."store-id" = b."source-store")
        where
            b."source-store" in ({self.csv_store_ids})
            and a."transferred-at" >= '{self.start_ts}'
            and a."transferred-at" <= '{self.end_ts}'
            and a.quantity !=0    
        """
        self.xout_l = self.db.get_df(query=q)
        self.xout_l = remove_duplicates(self.xout_l, "xout")
        return self.xout_l

    def sold(self):
        """
        Sold inventory calculation
        """
        q = f"""
        select
            c.id,
            nvl("barcode-reference", 0) barcode,
            a."quantity" sold,
            c.ptr
        from
            "{self.e_schema}"."bill-items-1{self.e_alias}" a
        join "{self.e_schema}"."bills-1{self.e_alias}" b on
            a."bill-id" = b.id
        join "{self.e_schema}"."inventory-1{self.e_alias}" c on
            (a."inventory-id" = c.id
                and c."store-id" = b."store-id")
        where
            b."store-id" in ({self.csv_store_ids})
            and b."created-at" >= '{self.start_ts}'
            and b."created-at" <= '{self.end_ts}'
            and a.quantity !=0

        union all 

        select
            c.id,
            nvl("barcode-reference", 0) barcode,
            a."quantity" sold,
            c.ptr
        from
            "{self.e_schema}"."bill-items-1{self.e_alias}" a
        join "{self.e_schema}"."bills-1{self.e_alias}" b on
            a."bill-id" = b.id
        join "{self.e_schema}"."inventory-1{self.e_alias}" c on
            (a."inventory-id" = c."barcode-reference"
                and c."store-id" = b."store-id")
        where
            b."store-id" in ({self.csv_store_ids})
            and b."created-at" >= '{self.start_ts}'
            and b."created-at" <= '{self.end_ts}'
            and a.quantity !=0
        """
        self.sold_l = self.db.get_df(query=q)
        self.sold_l = remove_duplicates(self.sold_l, "sold")
        return self.sold_l

    def returned_to_dc(self):
        """
        Return to dc - inventory calculation
        """
        q = f"""
        select
            c.id,
            nvl("barcode-reference", 0) barcode,
            a."returned-quantity" ret,
            c.ptr
        from
            "{self.e_schema}"."return-items-1{self.e_alias}" a
        join "{self.e_schema}"."returns-to-dc-1{self.e_alias}" b on
            a."return-id" = b.id
        join "{self.e_schema}"."inventory-1{self.e_alias}" c on
            (a."inventory-id" = c.id
                and c."store-id" = b."store-id")
        where
            b."store-id" in ({self.csv_store_ids})
            and b."created-at" >= '{self.start_ts}'
            and b."created-at" <= '{self.end_ts}'
            and a."returned-quantity" !=0

        union all

        select
            c.id,
            nvl("barcode-reference", 0) barcode,
            a."returned-quantity" ret,
            c.ptr
        from
            "{self.e_schema}"."return-items-1{self.e_alias}" a
        join "{self.e_schema}"."returns-to-dc-1{self.e_alias}" b on
            a."return-id" = b.id
        join "{self.e_schema}"."inventory-1{self.e_alias}" c on
            (a."inventory-id" = c."barcode-reference"
                and c."store-id" = b."store-id")
        where
            b."store-id" in ({self.csv_store_ids})
            and b."created-at" >= '{self.start_ts}'
            and b."created-at" <= '{self.end_ts}'
            and a."returned-quantity" !=0
        """
        self.ret_l = self.db.get_df(query=q)
        self.ret_l = remove_duplicates(self.ret_l, "ret")
        return self.ret_l

    def deleted(self):
        """
        Deleted - inventory calculation

        """
        q = f"""
        select
            a.id,
            nvl("barcode-reference", 0) barcode,
            a.quantity del,
            a.ptr
        from
            "{self.s_schema}"."inventory-1{self.s_alias}" a
        join "{self.e_schema}"."deleted-invoices{self.e_alias}" c on
            a."invoice-id" = c.id
        where
            a."store-id" in ({self.csv_store_ids})
            and c."deleted-at" >= '{self.start_ts}'
            and c."deleted-at" <= '{self.end_ts}'
            and a.quantity !=0

        union

        select
            a.id,
            nvl("barcode-reference", 0) barcode,
            a.quantity del,
            a.ptr
        from
            "{self.s_schema}"."inventory-1{self.s_alias}" a
        join "{self.e_schema}"."deleted-invoices-1{self.e_alias}" c on
            a."franchisee-invoice-id" = c.id
        where
            a."store-id" in ({self.csv_store_ids})
            and c."deleted-at" >= '{self.start_ts}'
            and c."deleted-at" <= '{self.end_ts}'
            and a.quantity !=0
        """
        self.del_l = self.db.get_df(query=q)
        self.del_l = remove_duplicates(self.del_l, "del")
        return self.del_l

    def closing(self):
        """
        Closing inventory calculation
        """
        q = f"""
        select
            id,
            nvl("barcode-reference", 0) barcode,
            quantity c,
            ptr
        from
            "{self.e_schema}"."inventory-1{self.e_alias}"
        where
            "store-id" in ({self.csv_store_ids})
            and "barcode-reference" is null
            and quantity !=0
        order by
            id
        """
        c_l_1 = self.db.get_df(query=q)

        q = f"""
            select
                id,
                nvl("barcode-reference", 0) barcode,
                quantity c,
                ptr
            from
                "{self.e_schema}"."inventory-1{self.e_alias}"
            where
                "store-id" in ({self.csv_store_ids})
                and "barcode-reference" is not null
                and quantity !=0
            order by
                id
            """
        c_l_2 = self.db.get_df(query=q)

        self.c_l = pd.concat([c_l_1, c_l_2], ignore_index=True)
        return self.c_l

    def audit_recon(self):
        """
        Audit recon - inventory calculation
        """
        q = f"""
        select
            b.id,
            nvl("barcode-reference", 0) barcode,
            a.change ar,
            b.ptr
        from
            "{self.e_schema}"."inventory-changes-1{self.e_alias}" a
        join "{self.e_schema}"."inventory-1{self.e_alias}" b on
            (a."inventory-id" = b.id
                and b."store-id" = a."store-id")
        where
            a."store-id" in ({self.csv_store_ids})
            and a."created-at" >= '{self.start_ts}'
            and a."created-at" <= '{self.end_ts}'
            and a.change !=0

        union all

        select
            b.id,
            nvl("barcode-reference", 0) barcode,
            a.change ar,
            b.ptr
        from
            "{self.e_schema}"."inventory-changes-1{self.e_alias}" a
        join "{self.e_schema}"."inventory-1{self.e_alias}" b on
            (a."inventory-id" = b."barcode-reference"
                and b."store-id" = a."store-id")
        where
            a."store-id" in ({self.csv_store_ids})
            and a."created-at" >= '{self.start_ts}'
            and a."created-at" <= '{self.end_ts}'
            and a.change !=0
        """
        self.ar_l = self.db.get_df(query=q)
        self.ar_l = remove_duplicates(self.ar_l, "ar")
        return self.ar_l

    def reverted_returns(self):
        """
        Reverted returns - inventory calculation
        """
        q = f"""
        select
            c.id,
            nvl("barcode-reference", 0) barcode,
            a."returned-quantity" rr,
            c.ptr
        from
            "{self.e_schema}"."return-items-1{self.e_alias}" a
        join "{self.e_schema}"."returns-to-dc-1{self.e_alias}" b on
            a."return-id" = b.id
        join "{self.e_schema}"."inventory-1{self.e_alias}" c on
            (a."inventory-id" = c.id
                and c."store-id" = b."store-id")
        where
            b."store-id" in ({self.csv_store_ids})
            and a."reverted-at" >= '{self.start_ts}'
            and a."reverted-at" <= '{self.end_ts}'
            and a."returned-quantity" !=0

        union all 

        select
            c.id,
            nvl("barcode-reference", 0) barcode,
            a."returned-quantity" rr,
            c.ptr
        from
            "{self.e_schema}"."return-items-1{self.e_alias}" a
        join "{self.e_schema}"."returns-to-dc-1{self.e_alias}" b on
            a."return-id" = b.id
        join "{self.e_schema}"."inventory-1{self.e_alias}" c on
            (a."inventory-id" = c."barcode-reference"
                and c."store-id" = b."store-id")
        where
            b."store-id" in ({self.csv_store_ids})
            and a."reverted-at" >= '{self.start_ts}'
            and a."reverted-at" <= '{self.end_ts}'
            and a."returned-quantity" !=0
        """
        self.rr_l = self.db.get_df(query=q)
        self.rr_l = remove_duplicates(self.rr_l, "rr")
        return self.rr_l

    def get_meta_data(self):
        """ extra data needed for inventory """
        q = f"""
        select
            i.id,
            i."purchase-rate" ,
            d."drug-name"
        from
            "prod2-generico"."prod2-generico"."inventory-1" i
        left join "prod2-generico"."prod2-generico".drugs d on
            i."drug-id" = d.id
        where
            i."store-id" in ({self.csv_store_ids})
        """
        return self.db.get_df(query=q)

    # @profile
    def start_data_fetch(self):
        """ calls all the function which fetch the data from database """
        print("Starting data fetch.")
        self.opening()
        print("opening: Successfully fetched.")
        self.purchased()
        print("purchased: Successfully fetched.")
        self.purchase_returns()
        print("purchase returns: Successfully fetched.")
        self.purchased_return_dispatched()
        print("purchased_return_dispatched : Successfully fetched.")
        self.purchased_return_settled()
        print("purchased_return_settled : Successfully fetched.")
        self.customer_returns()
        print("customer_returns: Successfully fetched.")
        self.xin()
        print("xin: Successfully fetched.")
        self.xout()
        print("xout: Successfully fetched.")
        self.sold()
        print("sold: Successfully fetched.")
        self.returned_to_dc()
        print("returned_to_dc: Successfully fetched.")
        self.deleted()
        print("deleted: Successfully fetched.")
        self.closing()
        print("closing: Successfully fetched.")
        self.audit_recon()
        print("audit_recon: Successfully fetched.")
        self.reverted_returns()
        print("reverted_returns: Successfully fetched.")

    # @profile
    def concat(self):
        """ data fetching from database """

        self.start_data_fetch()

        """
        ## combine initial and received
        temp_l = select(p_l, :id, :barcode, :p => :o, :ptr)
        recon_l = vcat(o_l, temp_l)
        ## following handles inventory lying in inventory-1 but received later
        recon_l = remove_duplicates(recon_l, "o")

        recon_l = combine_cr(recon_l, cr_l)
        recon_l = combine_xin(recon_l, xin_l)
        recon_l = combine_xout(recon_l, xout_l)
        recon_l = combine_sold(recon_l, sold_l)
        recon_l = combine_ret(recon_l, ret_l)
        recon_l = combine_ar(recon_l, ar_l)
        recon_l = combine_rr(recon_l, rr_l)
        recon_l = leftjoin(recon_l, select(del_l, :id, :del), on = :id)
        recon_l = leftjoin(recon_l, select(c_l, :id, :c), on = :id)
        """
        # """ combine initial and received and call it opening(o) """
        # self.p_l.rename(columns={'p': 'o'}, inplace=True)
        # self.recon_l = remove_duplicates(self.o_l, f="o")
        self.recon_l = self.o_l

        # """ following handles inventory lying in inventory-1 but received later """
        # self.recon_l = pd.concat([self.p_l, self.o_l], ignore_index=True)
        # self.recon_l = remove_duplicates(self.recon_l, "o")

        """ purchase """
        self.recon_l = pd.merge(self.recon_l, self.p_l, on='id', how='outer')
        self.take_union()

        """ purchase returns """
        self.recon_l = pd.merge(self.recon_l, self.pr_l, on='id', how='outer')
        self.take_union()

        """ purchase_return_deleted """
        self.recon_l = pd.merge(self.recon_l, self.prd_l, on='id', how='outer')
        self.take_union()

        """ purchase_return_settled """
        self.recon_l = pd.merge(self.recon_l, self.prs_l, on='id', how='outer')
        self.take_union()

        # self.recon_l['pr'] = 0
        # self.recon_l['prd'] = 0
        # self.recon_l['prs'] = 0

        """combine_cr: following handles the case where inventory was stock transferred, 
        after the start time and returned before end time """
        self.recon_l = pd.merge(self.recon_l, self.cr_l, on='id', how='outer')
        self.take_union()

        """combine_xin: this will take care of stores own inventory coming back"""
        self.recon_l = pd.merge(self.recon_l, self.xin_l, on='id', how='outer')
        self.take_union()

        """combine_xout: this will take care of stores own inventory transferred out"""
        self.recon_l = pd.merge(self.recon_l, self.xout_l, on='id', how='outer')
        self.take_union()

        """combine_sold: this will take care of stores inventory sold """
        self.recon_l = pd.merge(self.recon_l, self.sold_l, on='id', how='outer')
        self.take_union()

        """combine_ret: this will take care of stores inventory returned """
        self.recon_l = pd.merge(self.recon_l, self.ret_l, on='id', how='outer')
        self.take_union()

        """combine_ar: """
        self.recon_l = pd.merge(self.recon_l, self.ar_l, on='id', how='outer')
        self.take_union()

        """combine_rr: """
        self.recon_l = pd.merge(self.recon_l, self.rr_l, on='id', how='outer')
        self.take_union()

        """ deleted """
        self.recon_l = pd.merge(self.recon_l, self.del_l, on='id', how='left')
        self.take_union()

        """ closing """
        self.recon_l = pd.merge(self.recon_l, self.c_l, on='id', how='left')
        self.take_union()

        """ calculate the error """
        self.recon_l = self.recon_l.fillna(0)

        for col in ['id', 'o', 'p', 'pr', 'prd', 'prs', 'cr', 'xin', 'xout', 'ret', 'sold', 'del',
                    'ar',
                    'rr', 'c', 'barcode']:
            self.recon_l[col] = pd.to_numeric(self.recon_l[col])
            self.recon_l[col] = self.recon_l[col].astype('int', errors='raise')

        self.recon_l['e'] = self.recon_l['o'] + self.recon_l['p'] + self.recon_l['cr'] + \
                            self.recon_l['xin'] - \
                            self.recon_l['xout'] - \
                            self.recon_l['ret'] - self.recon_l['sold'] - self.recon_l['del'] + \
                            self.recon_l['ar'] + \
                            self.recon_l['rr'] - self.recon_l['c']

        return self.recon_l


parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stage, prod)")
parser.add_argument('-sd', '--start_date', default="NA", type=str, required=False,
                    help="Start date in IST")
parser.add_argument('-ed', '--end_date', default="NA", type=str, required=False,
                    help="End date in IST")
parser.add_argument('-sitd', '--snapshot_ist_time_delta', default=0, type=int, required=False,
                    help="End date in IST")
parser.add_argument('-bs', '--batch_size', default=1, type=int, required=False,
                    help="How many stores to process in one go")
parser.add_argument('-fr', '--is_full_run', default="NO", type=str, required=False,
                    help="Only one batch or all to process")

args, unknown = parser.parse_known_args()
env = args.env
start_date = args.start_date
end_date = args.end_date
batch_size = args.batch_size
snapshot_ist_time_delta = args.snapshot_ist_time_delta
is_full_run = args.is_full_run

os.environ['env'] = env
logger = get_logger()

# schema = "test-generico"
schema = "public"
if env == "prod":
    schema = "prod2-generico"
prefix = "-inv-2022-04-01"
""" read connection """
db = DB()
db.open_connection()

""" write connection """
w_db = DB(read_only=False)
w_db.open_connection()

s3 = S3(bucket_name=f"{env}-zeno-s3-db")

if not (start_date and end_date) or start_date == "NA" or end_date == "NA":
    """ if no dates given, then run for yesterday """
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    start_date = datetime.datetime.now() + datetime.timedelta(days=-1)
    start_date = start_date.strftime("%Y-%m-%d")

"""
Instructions to use(README):
    0. Make sure tables for both the dates (start and end) are present in public schema (eg: bills-1-mis-2022-06-11)
    1. set the start date and end date
    2. Set the store id if only one store changes are required, if all stores are required then don't set store id
    3. Data is uploaded to s3(prod-zeno-s3-db) inside "inventory/ledger/" folder (eg: s3://dev-zeno-s3-db/inventory/ledger/2022/06/11/240.csv)
    4. S3 Data can be queried using AWS Athena

Tables Required:
    inventory-1,invoice-items-1,invoices-1,customer-return-items-1,customer-returns-1,stock-transfer-items-1,
    stock-transfers-1,bill-items-1,bills-1,return-items-1,returns-to-dc-1,deleted-invoices,deleted-invoices-1,
    inventory-changes-1 

Improvements:
    1. use parquet format to store the data
        import pandas as pd
        df = pd.read_csv('example.csv')
        df.to_parquet('output.parquet')

Meaning of columns:
    "o": Opening/Start
    "cr": Customer Return
    "xin": Stock transfer in
    "xout": Stock transfer out
    "sold": Sold to customer
    "ret": Return to DC
    "ar": Audit
    "rr": Reverted Return 
    "del": Invoice Deleted
    "c": closing 
"""

""" get all the stores """
q = f"""
    select
        distinct "store-id" as "store-id"
    from
        "{schema}"."inventory-1{prefix}" i
"""
stores = db.get_df(query=q)

""" this column order will be maintained across all csv files """
column_order = ["id", "barcode", "ptr", "o", "p", "pr", "prd", "prs", "cr", "xin", "xout", "sold",
                "ret", "ar", "rr", "del", "c", "e"]
inventory_ledger_table = "inventory-ledger-v2"
""" clean existing records, if any """
q = f"""
    delete from "{schema}"."{inventory_ledger_table}" 
    -- where date("start-time") = '{start_date}'; 
"""
w_db.execute(query=q)

batch = 0
for store_id_batch in helper.batch(stores['store-id'], batch_size):
    csv_store_ids = ','.join([str(s) for s in store_id_batch])
    batch += 1
    logger.info(f"batch: {batch}, csv store ids: {csv_store_ids}")

    data = Data(db=db, csv_store_ids=csv_store_ids, start_date=start_date, end_date=end_date,
                snapshot_ist_time_delta=snapshot_ist_time_delta)
    recon_df = data.concat()

    uri = s3.save_df_to_s3(df=recon_df[column_order],
                           file_name=f"inventory/ledger/{start_date.replace('-', '/')}/batch_{batch}.csv",
                           index=False)

    table_info = helper.get_table_info(db=w_db, table_name=inventory_ledger_table, schema=schema)

    recon_df['start-time'] = data.start_ts
    recon_df['end-time'] = data.end_ts
    recon_df['created-at'] = datetime.datetime.now()
    recon_df['updated-at'] = datetime.datetime.now()
    recon_df['created-by'] = "etl-automation"
    recon_df['updated-by'] = "etl-automation"

    s3.write_df_to_db(df=recon_df[table_info['column_name']], table_name=inventory_ledger_table,
                      db=w_db, schema=schema)

    logger.info(f"Uploaded successfully @ {uri}")

    if is_full_run.lower() == "no":
        logger.info(f"Stopping after one batch, since is_full_run: {is_full_run}")
        db.close_connection()
        w_db.close_connection()
        break

db.close_connection()
w_db.close_connection()
