# coding: UTF-8
"""
Created on 2015/08/20

@author: Yang Wanjun
"""

from django.conf.urls import url, include

from . import views
from eboa import views as eboa_views

member_patterns = [
    url(r'^list.html$', views.employee_list, name='employee_list'),
    url(r'^detail/(?P<employee_id>[^,/]+).html$', views.member_detail, name='member_detail'),
    url(r'^(?P<employee_id>[^,/]+)/recommended_project.html$', views.recommended_project_list,
        name='recommended_project'),
    url(r'^list/in_coming.html$', views.members_in_coming, name='members_in_coming'),
    url(r'^list/subcontractor.html$', views.members_subcontractor, name='members_subcontractor'),
    url(r'^change_list.html$', views.change_list, name='change_list'),
    url(r'^project_list/(?P<employee_id>[^,/]+).html$', views.member_project_list, name='member_project_list'),
    url(r'^attendance_list.html$', eboa_views.attendance_list_monthly, name='attendance_list_monthly'),
    url(r'^(?P<member_id>[0-9]+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/expanses.html$', views.member_expanses_update,
        name='member_expanses_update'),
]

section_patterns = [
    url(r'^sections.html$', views.section_list, name='section_list'),
    url(r'^(?P<section_id>[0-9]+).html$', views.section_detail, name='section_detail'),
    url(r'^(?P<section_id>[0-9]+)/attendance.html$', views.section_attendance, name='section_attendance'),
]

download_patterns = [
    url(r'^project_request/(?P<project_id>[0-9]+).html$', views.download_project_request,
        name='download_project_request'),
    url(r'^subcontractor_order/(?P<subcontractor_id>[0-9]+).html$', views.download_subcontractor_order,
        name='download_subcontractor_order'),
    url(r'^project_client_order/$', views.download_client_order, name='download_client_order'),
    url(r'^project_quotation/(?P<project_id>[0-9]+).html$', views.download_project_quotation,
        name='download_project_quotation'),
    url(r'^resume/(?P<member_id>[0-9]+).html$', views.download_resume, name='download_resume'),
    url(r'^attendance_list/(?P<year>[0-9]{4})/(?P<month>[0-9]{2}).html$', eboa_views.download_attendance_list,
        name='download_attendance_list'),
    url(r'^section/(?P<section_id>[0-9]+)/attendance/(?P<year>[0-9]{4})/(?P<month>[0-9]{2}).html$', views.download_section_attendance,
        name='download_section_attendance'),
]

turnover_patterns = [
    url(r'^company_monthly.html$', views.turnover_company_monthly, name="turnover_company_monthly"),
    url(r'^charts/(?P<ym>[0-9]{6}).html$', views.turnover_charts_monthly, name='turnover_charts_monthly'),
    url(r'^members/(?P<ym>[0-9]{6}).html$', views.turnover_members_monthly, name='turnover_members_monthly'),
    url(r'^clients/(?P<ym>[0-9]{6}).html$', views.turnover_clients_monthly, name='turnover_clients_monthly'),
    url(r'^client/(?P<client_id>[0-9]+)/(?P<ym>[0-9]{6}).html$', views.turnover_client_monthly,
        name='turnover_client_monthly'),
]

subcontractor_patterns = [
    url(r'^list.html$', views.subcontractor_list, name='subcontractor_list'),
    url(r'^detail/(?P<subcontractor_id>[0-9]+).html$', views.subcontractor_detail,
        name='subcontractor_detail'),
    url(r'^members/(?P<subcontractor_id>[0-9]+).html$', views.subcontractor_members,
        name='subcontractor_members'),
]

project_patterns = [
    url(r'^list.html$', views.project_list, name='project_list'),
    url(r'^order_list.html', views.project_order_list, name='project_order_list'),
    url(r'^(?P<project_id>[0-9]+).html$', views.project_detail, name='project_detail'),
    url(r'^members/(?P<project_id>[0-9]+).html$', views.project_member_list, name='project_members'),
    url(r'^end/(?P<project_id>[0-9]+).html$', views.project_end, name='project_end'),
    url(r'^attendance/(?P<project_id>[0-9]+).html$', views.project_attendance_list,
        name='project_attendance_list'),
    url(r'^request_view/(?P<request_id>[0-9]+).html$', views.view_project_request, name='view_project_request'),
    url(r'^(?P<project_id>[0-9]+)/recommended_member.html$', views.recommended_member_list,
        name='recommended_member'),
    url(r'^order_member_assign/(?P<project_id>[0-9]+).html$', views.project_order_member_assign,
        name='project_order_member_assign'),
    url(r'^members_by_order/(?P<order_id>[0-9]+).html$', views.project_members_by_order,
        name='project_members_by_order'),
]

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^member/', include(member_patterns)),
    url(r'^section/', include(section_patterns)),
    url(r'^project/', include(project_patterns)),
    url(r'^release_list.html$', views.release_list_current, name='release_list_current'),
    url(r'^release_list/(?P<ym>[0-9]{6}).html$', views.release_list, name='release_list'),
    url(r'^subcontractor/', include(subcontractor_patterns)),
    url(r'^turnover/', include(turnover_patterns)),
    url(r'^download/', include(download_patterns)),
    url(r'^map_position.html$', views.map_position, name='map_position'),
    url(r'^issues.html$', views.issues, name='issues'),
    url(r'^issue/(?P<issue_id>[0-9]+).html$', views.issue_detail, name='issue_detail'),
    url(r'^history.html$', views.history, name='history'),
    url(r"^sync_coordinate.html", views.sync_coordinate, name="sync_coordinate"),
    url(r"^sync_members.html", views.sync_members, name="sync_members"),
    url(r"^batch_list.html", views.batch_list, name="batch_list"),
    url(r"^batch/(?P<name>[A-Za-z0-9_-]+).log$", views.batch_log, name="batch_log"),
    url(r"^syncdb2.html", views.sync_db2, name="syncdb2"),
    url(r"^upload_file.html$", views.upload_resume, name="upload_file"),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
]
