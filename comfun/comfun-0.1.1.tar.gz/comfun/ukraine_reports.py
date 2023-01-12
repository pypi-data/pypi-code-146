import wget
import datetime
import os


def get_reports(start_date: str = "2022-01-01",
                end_date: str = None,
                target_dir="/media/findux/DATA/Documents/ISW_UKRAINE_REPORTS/"):

    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    if end_date is None:
        end_date = datetime.datetime.now()
    else:
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    delta_d = (end_date - start_date).days
    print(delta_d)
    for i in range(delta_d):
        target_date = format(end_date - datetime.timedelta(days=i), "%Y%m%d")
        fname = f"{target_date} Russian Offensive Campaign Assessment.pdf"
        url = f"https://understandingwar.org/sites/default/files/{fname}"
        fpath_dst = os.path.join(target_dir, fname)
        wget.download(url, fpath_dst)
        #
        # try:
        #     wget.download(url, fpath_dst)
        # except:
        #     print(f"Couldnt download {fname}")


if __name__ == "__main__":
    get_reports()