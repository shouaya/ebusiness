# coding: UTF-8
"""
Created on 2015/10/15

@author: Yang Wanjun
"""


class MyBaseException(Exception):
    def __init__(self, message):
        self.message = message


class FileNotExistException(MyBaseException):
    def __init__(self, message=""):
        MyBaseException.__init__(self, message)


class CustomException(MyBaseException):
    def __init__(self, message=""):
        MyBaseException.__init__(self, message)
