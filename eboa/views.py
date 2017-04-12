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
from utils import common
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
    # response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = "filename=eboa_member_list.csv"
    #
    # writer = csv.writer(response)      # , quoting=csv.QUOTE_ALL
    # header = [
    #     "%s" % unicodedata.normalize('NFKC', u"名前").encode('sjis', 'ignore'),
    #     "%s" % unicodedata.normalize('NFKC', u"名前（カナ）").encode('sjis', 'ignore'),
    #     "%s" % unicodedata.normalize('NFKC', u"生年月日").encode('sjis', 'ignore'),
    #     "%s" % unicodedata.normalize('NFKC', u"性別").encode('sjis', 'ignore'),
    #     "%s" % unicodedata.normalize('NFKC', u"郵便番号").encode('sjis', 'ignore'),
    #     "%s" % unicodedata.normalize('NFKC', u"住所").encode('sjis', 'ignore'),
    #     "%s" % unicodedata.normalize('NFKC', u"個人携帯番号").encode('sjis', 'ignore'),
    #     "%s" % unicodedata.normalize('NFKC', u"最寄り駅").encode('sjis', 'ignore'),
    #     "%s" % unicodedata.normalize('NFKC', u"個人メールアドレス").encode('sjis', 'ignore'),
    #     "%s" % unicodedata.normalize('NFKC', u"入社年月日").encode('sjis', 'ignore'),
    #     "%s" % unicodedata.normalize('NFKC', u"会社メールアドレス").encode('sjis', 'ignore'),
    #     "%s" % unicodedata.normalize('NFKC', u"在留カード番号").encode('sjis', 'ignore'),
    #     "%s" % unicodedata.normalize('NFKC', u"在留資格").encode('sjis', 'ignore'),
    #     "%s" % unicodedata.normalize('NFKC', u"在留期間").encode('sjis', 'ignore'),
    # ]
    # writer.writerow(header)
    # for member in member_list:
    #     # member = models.EbEmployee()
    #     sex = u"男" if member.sex == '1' else u"女"
    #     if member.residence_name_kana:
    #         name_kana = "%s" % unicodedata.normalize('NFKC', member.residence_name_kana.decode('utf8')).encode('sjis','ignore')
    #     else:
    #         name_kana = ''
    #     if member.address:
    #         address = "%s" % unicodedata.normalize('NFKC', member.address.decode('utf8')).encode('sjis','ignore')
    #     else:
    #         address = ''
    #     if member.station:
    #         station = "%s" % unicodedata.normalize('NFKC', member.station.decode('utf8')).encode('sjis','ignore')
    #     else:
    #         station = ''
    #     if member.id_number:
    #         id_number = "%s" % unicodedata.normalize('NFKC', member.id_number.decode('utf8')).encode('sjis','ignore')
    #     else:
    #         id_number = ''
    #     if member.residence_type:
    #         residence_type = "%s" % unicodedata.normalize('NFKC', member.residence_type.decode('utf8')).encode('sjis','ignore')
    #     else:
    #         residence_type = ''
    #     writer.writerow(["%s" % unicodedata.normalize('NFKC', member.name.decode('utf8')).encode('sjis','ignore'),
    #                      name_kana,
    #                      member.birthday,
    #                      "%s" % unicodedata.normalize('NFKC', sex).encode('sjis','ignore'),
    #                      member.zipcode,
    #                      address,
    #                      member.private_tel_number,
    #                      station,
    #                      member.private_mail_address,
    #                      member.join_date,
    #                      member.business_mail_addr,
    #                      member.id_number,
    #                      residence_type,
    #                      member.id_card_expired_date.date() if member.id_card_expired_date else '',
    #                      member.retire_date,
    #                      ])

    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename="eboa_member_list.xls"'

    template = loader.get_template('download_eboa_members.html')
    context = {
        'member_list': member_list,
    }
    response.write(template.render(context, request))
    return response
