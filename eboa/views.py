# coding: UTF-8
import csv
import datetime
import urllib

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from . import biz
from utils import common

PAGE_SIZE = 50


@login_required(login_url='/eb/login/')
def attendance_list_monthly(request):
    today = datetime.date.today()
    year = request.GET.get('year', str(today.year))
    month = request.GET.get('month', "%02d" % (today.month,))
    all_attendance_list = biz.get_attendance_by_month(year, month)
    paginator = Paginator(all_attendance_list, PAGE_SIZE)
    page = request.GET.get('page')
    try:
        attendance_list = paginator.page(page)
    except PageNotAnInteger:
        attendance_list = paginator.page(1)
    except EmptyPage:
        attendance_list = paginator.page(paginator.num_pages)

    context = RequestContext(request, {
        'title': u'%s年%s月の出勤情報' % (year, month),
        'attendance_list': attendance_list,
        'paginator': paginator,
        'year': year,
        'month': month,
    })
    template = loader.get_template('attendance_list.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/eb/login/')
def download_attendance_list(request, year, month):
    attendance_list = biz.get_attendance_by_month(year, month)
    # ＥＢの休日を取得する。
    eb_holidays = biz.get_eb_holiday_list()
    # 就業日数
    business_days = common.get_business_days(year, month, eb_holidays)

    response = HttpResponse(content_type='text/csv')
    filename = u"%s年%s月出勤一覧_%s" % (year, month, datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    response['Content-Disposition'] = 'attachment; filename=' + urllib.quote(filename.encode('utf-8')) + '.csv' 
    writer = csv.writer(response)      # , quoting=csv.QUOTE_ALL
    for attendance in attendance_list:
        # 欠勤日数
        absence_days = (business_days - attendance.totalday) if (business_days - attendance.totalday) > 0 else 0
        # 有休日数
        used_holidays = biz.get_user_holidays_by_month(attendance.applicant, year, month)
        # 社員コード
        employee_code = attendance.applicant.ebemployee.code \
            if attendance.applicant and attendance.applicant.ebemployee else ''
        writer.writerow([employee_code,                               # 社員コード
                         business_days,                               # 就業日数
                         attendance.totalday if attendance.totalday else 0,      # 出勤日数
                         absence_days,                                # 欠勤日数
                         used_holidays,                               # 有休日数
                         0,                                           # 特休日数
                         0,                                           # 休出日数
                         0,                                           # 代休日数
                         0,                                           # 遅早回数
                         attendance.totaltime if attendance.totaltime else 0,    # 出勤時間
                         0,                                           # 遅早時間
                         0,                                           # 平日普通残業時間
                         attendance.nightcount if attendance.nightcount else 0,  # 平日深夜残業時間
                         0,                                           # 休日残業時間
                         0,                                           # 休日深夜残業時間
                         '',                                          # 予備項目
                         '',                                          # 予備項目
                         '',                                          # 予備項目
                         '',                                          # 予備項目
                         '',                                          # 予備項目
                         '',                                          # 予備項目
                         '',                                          # 予備項目
                         '',                                          # 予備項目
                         '',                                          # 予備項目
                         '',                                          # 予備項目
                         '',                                          # 予備項目
                         '',                                          # 予備項目
                         '',                                          # 予備項目
                         '',                                          # 予備項目
                         ''                                           # 予備項目
                         ])
    return response
