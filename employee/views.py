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
    gcm_url = 'https://android.googleapis.com/gcm/send'

    reg_id = "eU4IjUJu9Uk:APA91bGChpZNRcO4fkADblQbPfZfej9zAY8yNVGYAg44gtfk2tOXRkq6-pvFrvrae60KbLWszi_7dHCm9ZekQRQlh5eUC4tQnIS9K94ULpVXPmrJk_96a1rV0R2gnpEo1C76_xakNHfM"
    api_key = "key=" + Config.get_firebase_serverkey()

    headers = {'content-type': 'application/json', 'Authorization': api_key}
    # 渡すデータは適当です。
    # dictのkeyはAndroidのextrasのkeyと合わせましょう
    params = json.dumps({'to': reg_id,
                         "data": {
                             "title": u"営業支援システム",
                             "body": u"こんにちは"
                         },
                         })

    r = requests.post(gcm_url, data=params, headers=headers)
    return HttpResponse(r.content)
