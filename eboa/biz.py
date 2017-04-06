# coding: UTF-8
from utils import common
from . import models

from django.db.models import Q


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


def get_user_holidays_by_month(sys_user, year, month):
    used_days = 0
    if sys_user:
        first_day = common.get_first_day_from_ym('%s%02d' % (year, int(month)))
        last_day = common.get_last_day_by_month(first_day)
        used_holidays = models.HolidaysApplication.objects.\
            filter(Q(start_date__gte=first_day) | Q(end_date__lte=last_day),
                   employee=sys_user)
        for holiday in used_holidays:
            used_days += holiday.use_days
    return used_days


def get_members():
    """ＤＢから社員一覧を取得する

    :return:
    """
    return models.EbEmployee.objects.filter(retire_date__isnull=True)
