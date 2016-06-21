# coding: UTF-8
import csv
import datetime
import urllib

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from . import biz

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

    response = HttpResponse(content_type='text/csv')
    filename = u"%s年%s月出勤一覧_%s" % (year, month, datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    response['Content-Disposition'] = 'attachment; filename=' + urllib.quote(filename.encode('utf-8')) + '.csv' 
    writer = csv.writer(response, quoting=csv.QUOTE_ALL)
    for attendance in attendance_list:
        org = attendance.applicant.get_section()
        writer.writerow([attendance.applicant.ebemployee.code,
                         attendance.applicant_name.encode('utf-8'),
                         org.orgname.encode('utf-8') if org else '',
                         attendance.totalday,
                         attendance.totaltime,
                         attendance.get_cost_payment()])
    return response
