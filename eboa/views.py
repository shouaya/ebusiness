# coding: UTF-8
import csv, codecs, cStringIO
import datetime

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
        'title': u'要員一覧',
        'attendance_list': attendance_list,
        'paginator': paginator,
        'year': year,
        'month': month,
    })
    template = loader.get_template('attendance_list.html')
    return HttpResponse(template.render(context))


def download_attendance_list(request, year, month):
    attendance_list = biz.get_attendance_by_month(year, month)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance_list_%s%s.csv"' % (year, month)
    writer = csv.writer(response)
    for attendance in attendance_list:
        org = attendance.applicant.get_section()
        writer.writerow([attendance.applicant.ebemployee.code,
                         attendance.applicant.__unicode__().encode('utf-8'),
                         org.__unicode__().encode('utf-8') if org else '',
                         attendance.totalday,
                         attendance.totaltime,
                         attendance.get_cost_payment()])
    return response


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)