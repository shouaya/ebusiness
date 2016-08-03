# coding: UTF-8
from . import models


def get_attendance_by_month(year, month):
    period = year + "/" + month
    attendance_list = models.EbAttendance.objects.filter(period=period)
    for attendance in attendance_list:
        # 現場を取得する。
        member = attendance.get_eb_member()
        if member:
            project = member.get_project_by_month(year, month)
            if project:
                attendance.address = project.address
    return attendance_list


def get_eb_holiday_list():
    eb_holidays = models.EbHoliday.objects.all()
    holidays = []
    for holiday in eb_holidays:
        holidays.append(holiday.holiday.strftime("%Y/%m/%d"))
    return holidays
