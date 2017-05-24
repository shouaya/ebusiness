# coding: UTF-8
"""
Created on 2015/08/21

@author: Yang Wanjun
"""
import os
import json
import requests

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.conf import settings

from eb.models import Company, Config


def home(request):
    if Company.objects.all().count() == 0:
        return HttpResponseRedirect("/admin/eb/company/add/")
    else:
        return HttpResponseRedirect("/eb/")


def page_not_found(request):
    return render_to_response('404.html')


def get_push_js(request):
    response = HttpResponse(
        content_type='text/javascript')  # mimetype is replaced by content_type for django 1.7
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str("push.js")
    response['X-Sendfile'] = smart_str(os.path.join(settings.BASE_DIR, '/static/admin/js/push.js'))
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response


def push_notification(request):
    gcm_url = 'https://fcm.googleapis.com/fcm/send'

    # 上で控えたregistrationIdとAPI key
    reg_id = "cyxRzXwSnjc:APA91bGDFos1DyXoZYuZ8jzgrsId9pTUtr-pDYVxjdXE4Xbc_P9C1L108WcVxQ1NBVsHpGoTUQN8NABFv1tIYc1w4VZQGRuUjl_ZtoBQrsmGX1KHzSo4UnJoU976T4x5epu9LB9lepGC"
    key = "key=" + Config.get_firebase_serverkey()

    headers = {'content-type': 'application/json', 'Authorization': key}
    # 渡すデータは適当です。
    # dictのkeyはAndroidのextrasのkeyと合わせましょう
    params = json.dumps({'registration_ids': [reg_id], 'data': {'id': 'admin', 'text': 'notifi'}})

    r = requests.post(gcm_url, data=params, headers=headers)
    return HttpResponse(r.content)
