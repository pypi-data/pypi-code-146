msg = """A Simple yet powerful terminal CLient. 😏

-dw, --download -p, --proxy [-r|-o](--rename) ::: Download file.
-d, --ddfile[size] ::: Create random file.
-ip [-p, --port]::: Curl cip.cc
-rc, --roundcorner [--radius] ::: Add rounded corner to images.
-gu, --githubupload ::: Upload files to GitHub.
-sm, --smms ::: Upload image to sm.ms image server.
-yd, --youdao ::: Youdao dict translation.
-fd, --find [-dir, --dir] ::: Find files from dir.

-m, --msg [-r, --write | -w, --write] ::: Messenger
-tgbot, --telegrambot ::: Telegram bot message.
-fund, --fund [fund_code] ::: Fund investment.
-stock, --stock [stock_code] ::: Stock trend.
"""

def display_message(message: str = msg):
    for l in message.split("\n"):
        c, e = (l + " ::: ").split(':::')[:2]
        print("{:<70} {:<20}".format(c, e))
