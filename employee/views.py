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

    reg_id = "fmXw6HqlAKw:APA91bGwY6TsKrAWb2QkX9z__7oNMyXFAm4r8hr6demDEdQCF66KZ0yL6w0L8IG_2lgrIFPVvzL2cnL2iP2Oq-AQUcLkvJ-WhlsZKQ7mWnDOq-TCHlM5hvBIGOQg4vpkjr3b3qTfxVe7"
    api_key = "key=" + Config.get_firebase_serverkey()

    headers = {'content-type': 'application/json', 'Authorization': api_key}
    # 渡すデータは適当です。
    # dictのkeyはAndroidのextrasのkeyと合わせましょう
    params = json.dumps({'to': reg_id,
                         "data": {
                             "message": "This is a GCM Topic Message!",
                         },
                         })

    r = requests.post(gcm_url, data=params, headers=headers)
    return HttpResponse(r.content)
