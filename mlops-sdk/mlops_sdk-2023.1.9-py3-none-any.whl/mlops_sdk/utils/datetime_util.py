from datetime import datetime, timedelta


class DateTimeUtil:
    @staticmethod
    def getDateTimeVal():
        now = datetime.now()
        diff = 7
        before_one_year = now - timedelta(days=365 + diff)

        # 2달 (60일) 전
        before_60_day = now - timedelta(days=60)
        yearwk1 = str(int(before_60_day.strftime("%Y") + before_60_day.strftime("%V")) + 1)
        first1, last1 = DateTimeUtil.getWeekNumberFirstLastDate(yearwk1)
        # 6개월 (180일) 전
        before_180_day = now - timedelta(days=180)
        yearwk2 = str(int(before_180_day.strftime("%Y") + before_180_day.strftime("%V")) + 1)
        first2, last2 = DateTimeUtil.getWeekNumberFirstLastDate(yearwk2)
        # 1년 전
        first3, last3 = DateTimeUtil.getWeekNumberFirstLastDate(now.strftime("%Y") + now.strftime("%V"))
        this_yearwk = str(int(now.strftime("%Y") + now.strftime("%V")) + 1)
        yearwk = str(this_yearwk)
        stdt1 = first1
        eddt1 = last3
        stdt2 = first2
        eddt2 = last3
        stdt3 = str(int(before_one_year.strftime("%Y") + before_one_year.strftime("%V")) + 1)
        stdt3, _ = DateTimeUtil.getWeekNumberFirstLastDate(stdt3)
        eddt3 = last3

        return yearwk, stdt1, eddt1, stdt2, eddt2, stdt3, eddt3

    @staticmethod
    def getWeekNumberFirstLastDate(yk):
        year = int(yk[:4])
        weekNumber = int(yk[4:6])
        yearFirstDate = datetime(year, 1, 1)
        currentDate = yearFirstDate + timedelta(weeks=weekNumber - 1)
        first = currentDate - timedelta(days=currentDate.isoweekday() % 7 - 1)
        last = currentDate + timedelta(days=2)  # 지난 주 토요일

        # 만약 입력이 202140 주차라면,
        # first는 2021년 9월 27일 (월)
        # last는 2021년 10월 3일 (일)
        return first.strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")
