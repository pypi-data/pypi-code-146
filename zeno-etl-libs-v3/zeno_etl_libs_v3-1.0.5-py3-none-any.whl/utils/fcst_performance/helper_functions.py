from datetime import timedelta


def get_store_ids(reset_date, exclude_stores, db, schema):
    """
    Get IPC and Non-IPC store-ids which was reset on specified reset date
    Parameters:
        reset_date: (datetime.date) format
    Returns:
        store_ids: (list) of ipc and non-ipc store ids
        store_type_map: (list) of ipc and non-ipc store types respectively
    """
    reset_date = reset_date.strftime('%Y-%m-%d')
    if not exclude_stores:
        exclude_stores = "(0)"
    else:
        exclude_stores = tuple(exclude_stores)

    # Get list of all store_ids
    q_stores = f"""
        select "id", name, "opened-at" as opened_at
        from "{schema}".stores
        where name <> 'Zippin Central'
        and "is-active" = 1
        and "opened-at" != '0101-01-01 00:00:00'
        and id not in {exclude_stores}
        """
    stores_list = list(db.get_df(q_stores)["id"])

    stores_list_sql = str(stores_list).replace('[', '(').replace(']', ')')

    # Get list of IPC stores which was reset on specified reset date
    q_ipc = """
        select distinct "store-id"
        from "{schema}"."ipc-safety-stock" 
        where "store-id" in {0} and "reset-date" = '{1}'
        """.format(stores_list_sql, reset_date, schema=schema)
    ipc_stores = list(db.get_df(q_ipc)["store-id"])

    # Get list of Non-IPC stores which was reset on specified reset date
    q_non_ipc = """
        select distinct "store-id"
        from "{schema}"."non-ipc-safety-stock"
        where "store-id" in {0} and "reset-date" = '{1}'
        """.format(stores_list_sql, reset_date, schema=schema)
    non_ipc_stores = list(db.get_df(q_non_ipc)["store-id"])

    # Get list of Non-IPC stores which was reset on specified reset date
    q_ipc2 = """
            select distinct "store-id"
            from "{schema}"."ipc2-safety-stock"
            where "store-id" in {0} and "reset-date" = '{1}'
            """.format(stores_list_sql, reset_date, schema=schema)
    ipc2_stores = list(db.get_df(q_ipc2)["store-id"])

    store_ids = ipc_stores + non_ipc_stores + ipc2_stores
    store_type_map = ["ipc"] * len(ipc_stores) \
                     + ["non_ipc"] * len(non_ipc_stores) \
                     + ["ipc2"] * len(ipc2_stores)
    return store_ids, store_type_map


def handle_multiple_resets(reset_date, store_id, store_type, db, schema, logger):
    """
    Check if multiple reset occurred on specified reset date
    Parameters:
        reset_date: (datetime.date) format
        store_id: (int) format
        store_type: (str) format IPC or Non-IPC
    Returns:
        sql_cut_off_condition: (str) sql condition to use in query for taking
            only the latest reset that occurred.
    """
    sql_reset_date = reset_date.strftime('%Y-%m-%d')
    if store_type == "ipc":
        sql_store_type = "ipc"
    elif store_type == "non_ipc":
        sql_store_type = "non-ipc"
    else:
        sql_store_type = "ipc2"

    q_drug = """
        select "drug-id" 
        from "{schema}"."{0}-safety-stock"
        where "store-id" = {1} and "reset-date" = '{2}'
        limit 1
        """.format(sql_store_type, store_id, sql_reset_date, schema=schema)
    rand_drug_id = db.get_df(q_drug)["drug-id"][0]
    q_upload_time = """
        select *
        from "{schema}"."{0}-safety-stock"
        where "store-id" = {1} and "reset-date" = '{2}' and "drug-id" = {3}
        order by "updated-at" desc 
        """.format(sql_store_type, store_id, sql_reset_date, rand_drug_id,
                   schema=schema)
    df_upload_time = db.get_df(q_upload_time)["updated-at"]
    reset_count = df_upload_time.shape[0]

    if reset_count > 1:
        logger.info(f"Multiple resets detected for store_id: {store_id}")
        cut_off_datetime = df_upload_time[0] - timedelta(minutes=1)
        sql_cut_off_condition = """ and "updated-at" > '{}' """.format(
            str(cut_off_datetime))
    else:
        sql_cut_off_condition = ""

    return sql_cut_off_condition

