# coding: UTF-8
"""
Created on 2016/01/12

@author: Yang Wanjun
"""
import logging
import os
import traceback

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template import Context, Template

from eb.biz_logic.biz import get_members_information, get_admin_user, get_salesperson_director, get_salesperson_members

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = u'メール通知。'
    subject = u"社員稼働及びリリース情報（テスト）"

    def handle(self, *args, **options):
        try:
            status_list, summary = get_members_information()
            notify_members_info_for_director(status_list, summary)
            notify_members_into_for_salesperson(status_list, summary)
        except Exception as e:
            print e.message
            logger.error(traceback.format_exc())


def notify_members_info_for_director(status_list, summary):
    """営業部長にメールを通知する。

    :param status_list 通知の内容リスト
    :param summary 通知の集計情報
    """
    # 営業部長取得する
    directors = get_salesperson_director()
    if not directors:
        return

    from_email = get_admin_email()
    recipient_list = []
    for salesperson in directors:
        recipient_list.extend(salesperson.get_notify_mail_list())
    recipient_list.append('jiangjie@e-business.co.jp')
    text = get_sales_members_info_text(directors, status_list, summary)

    send_mail(Command.subject, "", from_email, recipient_list, html_message=text)
    logger.info(u"題名: %s; TO: %s; 送信完了。" % (Command.subject, ','.join(recipient_list),))


def notify_members_into_for_salesperson(status_list, summary):
    """営業部長にメールを通知する。

    :param status_list 通知の内容リスト
    :param summary 通知の集計情報
    """
    salesperson_list = get_salesperson_members()
    if not salesperson_list:
        return

    def get_status_info(salesperson_id):
        for status in status_list:
            if status['salesperson'].pk == salesperson_id:
                return [status]
        return []

    from_email = get_admin_email()
    for salesperson in salesperson_list:
        recipient_list = salesperson.get_notify_mail_list()
        text = get_sales_members_info_text([salesperson], get_status_info(salesperson.pk))

        send_mail(Command.subject, "", from_email, recipient_list, html_message=text)
        logger.info(u"題名: %s; TO: %s; 送信完了。" % (Command.subject, ','.join(recipient_list),))


def get_sales_members_info_path():
    """営業部長に通知内容のテンプレートの位置を取得する。
    """
    path = os.path.join(settings.MEDIA_ROOT, 'mail/mail_to_sales_members_info.html')
    return path


def get_sales_members_info_text(salesperson_list, status_list, summary=None):
    """営業部長に通知内容を取得する。

    :param salesperson_list 宛先の営業員
    :param status_list 通知の内容リスト
    :param summary 通知の集計情報
    """
    path = get_sales_members_info_path()
    f = open(path, 'r')
    text = f.read()
    f.close()
    t = Template(text)

    context = Context({'salesperson_list': salesperson_list,
                       'status_list': status_list,
                       'summary': summary,
                       'domain': settings.DOMAIN_NAME,
                       })
    return t.render(context)


def get_admin_email():
    """メール通知の差出人のアドレスを取得する。
    """
    admin = get_admin_user()
    return admin.email
