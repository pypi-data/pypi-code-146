"""
批量读取数据对象。用于批计算/离线计算。
"""


def read_delta_table(spark_ob, db, table, date_col, recent_days=1, limit_num=5000, limit_date='2022-12-14', test=False):
    sql = f"select * from {db}.{table} where {date_col} == CURRENT_DATE() - INTERVAL '{recent_days}' DAY "
    if test:
        print(f"select * from {db}.{table} where {date_col} == to_date('{limit_date}') limit {limit_num}")
        return spark_ob.read.table(f"{db}.{table}").where(f"{date_col} == to_date('{limit_date}') limit {limit_num}")
    else:
        sql += f"limit {limit_num}"
        return spark_ob.sql(
            f"select * from {db}.{table} where {date_col} == CURRENT_DATE() - INTERVAL '{recent_days}' DAY ")
