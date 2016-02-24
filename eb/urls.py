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
    url(r'^project_order_member_assign/(?P<project_id>[^,/]+).html$', views.project_order_member_assign,
        name='project_order_member_assign'),
    url(r'^project_members_by_order/(?P<order_id>[^,/]+).html$', views.project_members_by_order,
        name='project_members_by_order'),
    url(r'^release_list.html$', views.release_list, name='release_list'),
    url(r'^member_project_list/(?P<employee_id>[^,/]+).html$', views.member_project_list, name='member_project_list'),
    url(r'^member_detail/(?P<employee_id>[^,/]+).html$', views.member_detail, name='member_detail'),
    url(r'^project/(?P<project_id>[^,/]+)/recommended_member.html$', views.recommended_member_list,
        name='recommended_member'),
    url(r'^project/quotation/(?P<project_id>[^,/]+).html$', views.download_project_quotation,
        name='download_project_quotation'),
    url(r'^client_turnover_month.html$', views.client_turnover_month, name='client_turnover_month'),
    url(r'^client_turnover/(?P<client_id>[0-9]+).html$', views.client_turnover_details, name='client_turnover_details'),
    url(r'^project/client_order/download/$', views.download_client_order, name='download_client_order'),
    url(r'^member/(?P<employee_id>[^,/]+)/recommended_project.html$', views.recommended_project_list,
        name='recommended_project'),
    url(r'^subcontractor_list.html$', views.subcontractor_list, name='subcontractor_list'),
    url(r'^subcontractor_detail/(?P<subcontractor_id>[0-9]+).html$', views.subcontractor_detail,
        name='subcontractor_detail'),
    url(r'^subcontractor_members/(?P<subcontractor_id>[0-9]+).html$', views.subcontractor_members,
        name='subcontractor_members'),
    url(r'^subcontractor_order/(?P<subcontractor_id>[0-9]+).html$', views.download_subcontractor_order,
        name='download_subcontractor_order'),
    url(r'^map_position.html$', views.map_position, name='map_position'),
    url(r'^issue.html$', views.issue, name='issue'),
    url(r'^history.html$', views.history, name='history'),
    url(r"^sync_coordinate.html", views.sync_coordinate, name="sync_coordinate"),
    url(r"^sync_members.html", views.sync_members, name="sync_members"),
    url(r"^syncdb2.html", views.sync_db2, name="syncdb2"),
    url(r"^upload_file.html$", views.upload_resume, name="upload_file"),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
]
