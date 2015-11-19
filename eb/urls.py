# coding: UTF-8
"""
Created on 2015/08/20

@author: Yang Wanjun
"""

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^employee_list.html$', views.employee_list, name='employee_list'),
    url(r'^project_list.html$', views.project_list, name='project_list'),
    url(r'^project_order_list.html', views.project_order_list, name='project_order_list'),
    url(r'^section/(?P<name>[^,/]+).html$', views.section_members, name='section'),
    url(r'^project/(?P<project_id>[^,/]+).html$', views.project_detail, name='project_detail'),
    url(r'^project/attendance/(?P<project_id>[^,/]+).html$', views.project_attendance_list,
        name='project_attendance_list'),
    url(r'^project_members/(?P<project_id>[^,/]+).html$', views.project_member_list, name='project_members'),
    url(r'^release_list.html$', views.release_list, name='release_list'),
    url(r'^member_project_list/(?P<employee_id>[^,/]+).html$', views.member_project_list, name='member_project_list'),
    url(r'^member_detail/(?P<employee_id>[^,/]+).html$', views.member_detail, name='member_detail'),
    url(r'^project/(?P<project_id>[^,/]+)/recommended_member.html$', views.recommended_member_list,
        name='recommended_member'),
    url(r'^project/client_order/download/$', views.download_client_order, name='download_client_order'),
    url(r'^member/(?P<employee_id>[^,/]+)/recommended_project.html$', views.recommended_project_list,
        name='recommended_project'),
    url(r'^history.html$', views.history, name='history'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r"^syncdb.html", views.sync_db, name="syncdb"),
    url(r"^upload_file.html$", views.upload_resume, name="upload_file"),
]
