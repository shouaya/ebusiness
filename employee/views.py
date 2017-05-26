# coding: UTF-8
"""
Created on 2015/08/21

@author: Yang Wanjun
"""
import os
import json

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.http import HttpResponse
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
    path = os.path.join(settings.BASE_DIR, 'static/admin/js/push.js')
    response = HttpResponse(open(path, 'rb'), content_type='text/javascript')
    response['Content-Disposition'] = 'attachment; filename=push.js'
    return response


def push_notification(request):
    import requests
    gcm_url = 'https://fcm.googleapis.com/fcm/send'

    reg_id = "cuJ235fUGEQ:APA91bHHdLmMA-hc5dDO8SrYcvWNfyDrbxGgaUafmnwh3DCtH0GplMK7uN1k7TalW52tzhZTVTeO2fK9V0imvrE6d3IYnRaKR1EEZmmMwRWDpc6nxrjMu7VN70qtdU0Er-vSdN2e3OKw"
    api_key = "key=" + Config.get_firebase_serverkey()

    headers = {'content-type': 'application/json',
               'Authorization': api_key,
               'Encryption': 'salt=BnALjqTuUuk6lv4jVM3C3w==',
               'Crypto-Key': 'dh=BKbndB0NDEiugNa8VShuKp8cuQV14ZDhLZCUeNw0Ow814sbtREOEa80NIivfebkd8_D-if0NPFtGN0jh-guy-A0=',
               'Content-Encoding': 'aesgcm'}
    # 渡すデータは適当です。
    # dictのkeyはAndroidのextrasのkeyと合わせましょう
    params = json.dumps({'to': reg_id,
                         "data": {
                             "title": u"営業支援システム",
                             "body": u"こんにちは"
                         },
                         "notification": {
                             "title": "Portugal vs. Denmark",
                             "body": "5 to 1"
                         },
                         })

    r = requests.post(gcm_url, data=params, headers=headers)
    return HttpResponse(r.content)


def notification_data(request):
    data = {
        'title': u"新入社員",
        'message': u"歓迎！"
    }
    return HttpResponse(json.dumps(data))
