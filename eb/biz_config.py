# coding: UTF-8
"""
Created on 2017/02/23

@author: Yang Wanjun
"""
from utils import constants
from eb import models


def get_config(name, default_value=None):
    """システム設定を取得する。

    DBから値を取得する。

    :param name: 設定名
    :param default_value: デフォルト値
    :return:
    """
    return models.Config.get(name, default_value)


def get_year_start():
    """年リストのスタート

    :return:
    """
    return get_config(constants.CONFIG_YEAR_LIST_START, 2015)


def get_year_end():
    """年リストのエンド

    :return:
    """
    return get_config(constants.CONFIG_YEAR_LIST_END, 2020)


def get_domain_name():
    """ドメイン名を取得する。

    :return:
    """
    return get_config(constants.CONFIG_DOMAIN_NAME)


def get_page_size():
    """１ページに表示するレコード数を取得する。

    :return:
    """
    return get_config(constants.CONFIG_PAGE_SIZE, 50)


def get_theme():
    """主題を表示する。

    :return:
    """
    return get_config(constants.CONFIG_THEME, 'common')
