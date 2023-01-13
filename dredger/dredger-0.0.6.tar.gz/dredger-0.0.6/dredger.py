from datetime import datetime,date, timedelta
from urllib.request import urlopen
from time import strftime
import logging

#The following function gives date on last Tuesday/Thurday (Monday is 0;Sunday is 6)
def date_on_day(input_date:date,input_day:int):
    offset = (input_date.weekday() - input_day) % 7
    last_day = input_date - timedelta(days=offset)
    return last_day
#The following function return number of weekdays till input date in that year
def weekday_count(input_date:date,input_day:int):
    week_count, remainder = divmod((input_date-date(input_date.year,1,1)).days,7)
    
    if (7 -date(input_date.year,1,1).weekday() + input_day)%7<=remainder:
        return week_count+1
    else:
        return week_count


#The following function downloads file on given URL using 
def download_file(file_url,file_name):
    u = urlopen(file_url)
    meta = u.info()
    file_size = int(meta["Content-Length"])

    logging.warning(f"Downloading: {file_name} Bytes: {file_size}")

    block_size = int(file_size/100)
    file_size_dl = 0
    file_content = b""
    
    while True:
        buffer = u.read(block_size)
        if not buffer:
            break

        file_size_dl += len(buffer)
        file_content += buffer
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        logging.warning(status)
    return file_content

def get_uspto_file(file_type,input_date):
    if file_type == "applications":
        publishing_date = date_on_day(input_date,3)
        file_name = "ipa"+str(datetime.strftime(publishing_date,"%y%m%d"))+".zip"
        file_url = "https://bulkdata.uspto.gov/data/patent/application/redbook/fulltext/" + str(input_date.year) +"/" + file_name
        return download_file(file_url,file_name)
    elif file_type == 'grants':
        publishing_date = date_on_day(input_date,1)
        file_name = "ipg"+str(datetime.strftime(publishing_date,"%y%m%d"))+".zip"
        url = "https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/" + str(input_date.year) +"/" + file_name
        return download_file(file_url,file_name)
    elif file_type == 'pdfs':
        publishing_date = date_on_day(input_date,1)
        file_name = "grant_pdf_"+str(datetime.strftime(publishing_date,"%y%m%d"))+".tar"
        url = "https://bulkdata.uspto.gov/data/patent/application/multipagepdf/" + str(input_date.year) + "/" + file_name
        return download_file(file_url,file_name)
