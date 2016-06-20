# coding: UTF-8
from . import models


def get_attendance_by_month(year, month):
    period = year + "/" + month
    attendance_list = models.EbAttendance.objects.filter(period=period)
    return attendance_list
