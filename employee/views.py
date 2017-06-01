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
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.views.generic.base import ContextMixin
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.http.response import JsonResponse

from eb import models
from utils import constants


@method_decorator(login_required(login_url=constants.LOGIN_IN_URL), name='dispatch')
class BaseView(View, ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        kwargs.update({
            'request': request
        })
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        pass


class HomeView(BaseView):

    def get(self, request, *args, **kwargs):
        if models.Company.objects.all().count() == 0:
            return HttpResponseRedirect(reverse('admin:eb_company_add'))
        else:
            return HttpResponseRedirect(reverse('index'))


def page_not_found(request):
    return render_to_response('404.html')


def get_push_js(request):
    path = os.path.join(settings.BASE_DIR, 'static/admin/js/push.js')
    response = HttpResponse(open(path, 'rb'), content_type='text/javascript')
    response['Content-Disposition'] = 'attachment; filename=push.js'
    return response


class UpdateSubscription(BaseView):

    def post(self, request, *args, **kwargs):
        result = {}
        subscription = request.POST.get('subscription', None)
        if subscription:
            subscription = json.loads(subscription)
            endpoint = subscription.get('endpoint')
            registration_id = endpoint.split('/')[-1]
            if models.PushNotification.objects.filter(registration_id=registration_id).count() == 0:
                notification = models.PushNotification(
                    user=request.user,
                    registration_id=registration_id,
                    key_auth=subscription.get('keys').get('auth'),
                    key_p256dh=subscription.get('keys').get('p256dh')
                )
                notification.save()
                LogEntry.objects.log_action(request.user.id,
                                            ContentType.objects.get_for_model(notification).pk,
                                            notification.pk,
                                            unicode(notification),
                                            ADDITION,
                                            change_message=u"デバイスを追加しました：" + registration_id)
            result['error'] = 0
        else:
            result['error'] = 1
        return HttpResponse(json.dumps(result))


class GetNotificationData(View):

    def get(self, request, *args, **kwargs):
        registration_id = request.GET.get('registration_id', None)
        data = {}
        if registration_id:
            try:
                notification = models.PushNotification.objects.get(registration_id=registration_id)
                title = notification.title
                message = notification.message
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                title = ''
                message = ''
            data = {
                'title': title,
                'message': message,
            }
        else:
            data['error'] = 1
        return JsonResponse(data)
