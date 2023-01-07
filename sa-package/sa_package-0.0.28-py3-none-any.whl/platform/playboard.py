import time
import pandas as pd

from selenium.webdriver.common.by import By

from sa_package.my_selenium.webdriver import MyChromeDriver
from sa_package.convert.datetime_format import convert_date_to_timestamp


# ========================================================================
# 플레이보드 크리에이터 광고 순위 불러오기
# ========================================================================
def get_url(rank_type, period_type, target_date):
    """
    Creates playboard url

    Parameters
    -----------
    rank_type: str {"channel", "ad", "short_ad"}
    period_type: str {"daily", "weekly", "monthly"}
    target_date: `datetime.date`

    Returns
    -------
    str
        A url of playboard
    """

    if rank_type == "channel":
        url = "https://playboard.co/youtube-ranking/most-popular-gaming-channels-in-south-korea"
    
    elif rank_type == "ad":
        url = "https://playboard.co/chart/ad/most-viewed-gaming-videos-in-south-korea"
    
    elif rank_type == "short_ad":
        url = "https://playboard.co/chart/short-ad/most-viewed-gaming-videos-in-south-korea"

    url += f"-{period_type}"
    url += f"?period={convert_date_to_timestamp(target_date)}"

    return url



def get_list_from_playboard(url, under=300, headless=True):
    """
    Parameters
    ----------
    url: str
    under: int, default 300
    headless: bool, default True

    Returns
    -------
    DataFrame
        columns: "rank", "change", "video_id", "channel", "title", "upload_date", "viewership", "subscriber"
    """

    driver = MyChromeDriver(headless=headless)
    driver.get(url)

    last_height = driver.execute_script("return document.body.scrollHeight")
    rank_df = pd.DataFrame(columns=['rank', 'change', 'video_id', 'channel', 'title', 'upload_date', 'viewership', 'subscriber'])
    
    num, rank = 1, 0
    while True:
        if rank == str(under):
            break

        try:
            chart__row = driver.find_element(By.CSS_SELECTOR, f'table > tbody > tr:nth-child({num})')

            if chart__row.get_attribute("class") != "chart__row":
                pass
            else:
                rank = chart__row.find_elements(By.CLASS_NAME, "current")[0].text

                fluc_class = chart__row.find_elements(By.CLASS_NAME, "fluc")[0].get_attribute("class").split()[-1]
                fluc_text = chart__row.find_elements(By.CLASS_NAME, "fluc")[0].text

                if fluc_class == "same":
                    change = 0
                elif fluc_class == "new":
                    change = "NEW"
                elif fluc_class == "up":
                    change = int(fluc_text)
                else:
                    change = -1 * (int(fluc_text))

                vod_link = chart__row.find_elements(By.CLASS_NAME, "title__label")[0].get_attribute("href")
                video_id = vod_link.split("/")[-1]

                channel = chart__row.find_elements(By.CLASS_NAME, "name")[0].text

                title = chart__row.find_elements(By.CLASS_NAME, "title__label")[0].get_attribute("title")

                upload_date = chart__row.find_elements(By.CLASS_NAME, "title__date")[0].text

                viewership = chart__row.find_elements(By.CLASS_NAME, "score")[0].text.replace(",", "")

                subscriber = chart__row.find_elements(By.CLASS_NAME, "subs")[0].text.replace(",", "")


                rank_df = rank_df.append({
                    'rank': rank,
                    'change': change,
                    'video_id': video_id,
                    'channel': channel,
                    'title': title,
                    'upload_date': upload_date.replace(".", "-"),
                    'viewership': viewership,
                    'subscriber': subscriber
                }, ignore_index=True)

            num += 1

        except Exception as e:
            # print(num, "::", e)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            # print(last_height, new_height)
            last_height = new_height

    driver.close()

    return rank_df