""" 日历"""


"""日历采集器"""

import polars as pl
import datetime
from pathlib import Path
from vxsched import vxengine
from vxutils import vxtime, to_datetime, logger, to_timestring


@vxengine.event_handler("on_hans", 30)
@vxengine.event_handler("init", 30)
def collector_calendar_init(context, _):
    """初始化

    交易所 SSE上交所,SZSE深交所,CFFEX 中金所,SHFE 上期所,CZCE 郑商所,DCE 大商所,INE 上能源

    """
    start_date = to_datetime("1990-01-01")
    end_date = start_date

    data_path = context.params.get("data_path", "~/.vxdataset/")
    calendar_file = Path(data_path, "calendar.csv")
    if calendar_file.exists():
        calendars = pl.read_csv(calendar_file, parse_dates=True).sort(by="date")
        end_date = calendars["date"][-1] + datetime.timedelta(days=1)

    today = to_datetime(vxtime.today())
    if end_date > today:
        logger.info(f"交易日历最后一天{end_date}，并未更新")
        return

    df = context.ts_pro.trade_cal(
        "SSE",
        start_date=to_timestring(end_date, "%Y%m%d"),
        end_date=to_timestring(today, "%Y%m%d"),
        is_open=1,
    )
    if df.empty():
        logger.info(f"交易日历最后一天{end_date}，并未更新")
        return
    vxengine.submit_event("load_date", df["cal_date"])
