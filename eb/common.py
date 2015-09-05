# coding: UTF-8
"""
Created on 2015/08/25

@author: Yang Wanjun
"""
import datetime
import calendar


def add_months(source_date, months=1):
    month = source_date.month - 1 + months
    year = int(source_date.year + month / 12)
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def get_release_months(cnt):
    if not cnt:
        cnt = 3

    now = datetime.date.today()
    release_month_list = []
    for i in range(cnt):
        next_month = add_months(now, i)
        release_month_list.append((next_month.year, next_month.month))

    return release_month_list


if __name__ == "__main__":
    lst = get_release_months(10)
    for y, m in lst:
        print y, m