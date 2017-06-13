# coding: UTF-8
import csv
import datetime
import urllib
import unicodedata

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from . import biz, models
from utils import file_gen
from eb import biz_config

PAGE_SIZE = 50


def get_base_context():
    context = {
        'theme': biz_config.get_theme(),
    }
    return context


@login_required(login_url='/eb/login/')
def download_eboa_members(request):
    member_list = biz.get_members()
    output = file_gen.generate_eboa_members(member_list)
    filename = u"社員一覧_%s" % datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    response = HttpResponse(output, content_type="application/ms-excel")
    response['Content-Disposition'] = "filename=" + urllib.quote(filename.encode('utf-8')) + ".xlsx"
    return response
