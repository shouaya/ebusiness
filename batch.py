# coding: UTF-8
import datetime
import math
import time
import MySQLdb
import os
import django
import sys
import logging

from crontab import CronTab
from multiprocessing import Pool

from django.core.management import call_command
from utils import constants

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "employee.settings")
django.setup()


class JobConfig(object):
    """バッチの処理設定

    """
    def __init__(self, cron_tab, job, batch_name):
        """初期処理

        :param cron_tab: 実行時間設定
        :param job:実行する関数
        """
        self._cron_tab = cron_tab
        self.job = job
        self.batch_name = batch_name

    def schedule(self):
        """次回実行日時を取得する。

        :return:
        """
        cron_tab = self._cron_tab
        return datetime.datetime.now() + datetime.timedelta(seconds=math.ceil(cron_tab.next()))

    def next(self):
        """次回実行時刻まで待機する時間を取得する。

        :return:
        """
        cron_tab = self._cron_tab
        return math.ceil(cron_tab.next())


def job_controller(job_config):
    """処理コントローラ

    :param job_config:
    :return:
    """
    while True:
        try:
            # 次実行時刻まで待機
            time.sleep(job_config.next())
            # 処理を実行する。
            job_config.job(job_config.batch_name)
        except KeyboardInterrupt:
            break


def get_batches():
    """ＤＢから実行しようとするバッチを取得する。

    :return:
    """
    if sys.platform == 'linux2':
        user = os.environ['MYSQL_USER']
        password = os.environ['MYSQL_PASSWORD']
        host = os.environ['MYSQL_SERVER']
    else:
        user = 'root'
        password = 'root'
        host = 'localhost'
    con = MySQLdb.connect(user=user, passwd=password, db='eb_sales', host=host)
    cursor = con.cursor()
    cursor.execute("select name, cron_tab from eb_batchmanage "
                   " where is_deleted=0 "
                   "   and is_active=1"
                   "   and cron_tab is not null"
                   "   and cron_tab <> ''")
    records = cursor.fetchall()
    con.close()
    batches = []
    for record in records:
        name = record[0]
        cron_tab = record[1]

        batches.append((name, cron_tab))
    return batches


def call_batch(name):
    call_command(name)


def main():
    logger = logging.getLogger(constants.LOG_EB_SALES)
    batches = get_batches()
    job_configs = []
    logger.info(u"バッチ起動")
    if not batches:
        logger.info(u"バッチがありません！")
        return
    for name, cron_tab in batches:
        job_config = JobConfig(CronTab(cron_tab), call_batch, name)
        job_configs.append(job_config)
        logger.info(u"%s: %s" % (name, cron_tab))

    if not job_configs:
        return
    # 処理を並列に実行
    p = Pool(len(job_configs))
    try:
        p.map(job_controller, job_configs)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
