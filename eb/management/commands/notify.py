# coding: UTF-8
"""
Created on 2016/01/12

@author: Yang Wanjun
"""
import os
import logging
import traceback

from django.core.management.base import BaseCommand
from django.conf import settings
from django.template import Context, Template
from django.core.mail import send_mail

from eb.biz import get_members_information, get_admin_user, get_salesperson_director


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = u'メール通知。'

    def handle(self, *args, **options):
        try:
            notify_members_info_for_director()
        except Exception as e:
            logger.error(traceback.format_exc())


def notify_members_info_for_director():
    # 営業部長取得する
    directors = get_salesperson_director()
    if not directors:
        return

    subject = u"社員稼働及びリリース情報（テスト）"
    admin = get_admin_user()
    from_email = admin.email
    recipient_list = []
    for salesperson in directors:
        recipient_list.extend(salesperson.get_notify_mail_list())
    recipient_list.append('jiangjie@e-business.co.jp')
    text = get_director_members_info_text(directors)
    send_mail(subject, "", from_email, recipient_list, html_message=text)
    logger.info(u"題名: %s; TO: %s; 送信完了。" % (subject, ','.join(recipient_list),))


def get_director_members_info_path():
    path = os.path.join(settings.MEDIA_ROOT, 'mail/mail_to_director_members_info.html')
    return path


def get_director_members_info_text(directors):
    path = get_director_members_info_path()
    f = open(path, 'r')
    text = f.read()
    f.close()
    t = Template(text)

    status_list, summary = get_members_information()
    context = Context({'directors': directors,
                       'status_list': status_list,
                       'summary': summary,
                       'domain': settings.DOMAIN_NAME,
                       })
    return t.render(context)
