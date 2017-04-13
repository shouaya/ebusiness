# coding: UTF-8
"""
Created on 2015/08/20

@author: Yang Wanjun
"""

from django.conf.urls import url, include

from . import views
from eboa import views as eboa_views

member_patterns = [
    url(r'^list.html$', views.MemberListView.as_view(), name='employee_list'),
    url(r'^detail/(?P<employee_id>[^,/]+).html$', views.MemberDetailView.as_view(), name='member_detail'),
    url(r'^(?P<employee_id>[^,/]+)/recommended_project.html$', views.RecommendedProjectsView.as_view(),
        name='recommended_project'),
    url(r'^list/in_coming.html$', views.MembersComingView.as_view(), name='members_in_coming'),
    url(r'^list/subcontractor.html$', views.MembersSubcontractorView.as_view(), name='members_subcontractor'),
    url(r'^change_list.html$', views.MemberChangeListView.as_view(), name='change_list'),
    url(r'^project_list/(?P<employee_id>[^,/]+).html$', views.MemberProjectsView.as_view(),
        name='member_project_list'),
]

section_patterns = [
    url(r'^sections.html$', views.SectionListView.as_view(), name='section_list'),
    url(r'^(?P<section_id>[0-9]+).html$', views.SectionDetailView.as_view(), name='section_detail'),
    url(r'^(?P<section_id>[0-9]+)/attendance.html$', views.section_attendance, name='section_attendance'),
]

download_patterns = [
    url(r'^project_request/(?P<project_id>[0-9]+).html$', views.DownloadProjectRequestView.as_view(),
        name='download_project_request'),
    url(r'^subcontractor_order/(?P<subcontractor_id>[0-9]+).html$', views.DownloadSubcontractorOrderView.as_view(),
        name='download_subcontractor_order'),
    url(r'^project_client_order/$', views.DownloadClientOrderView.as_view(), name='download_client_order'),
    url(r'^project_quotation/(?P<project_id>[0-9]+).html$', views.DownloadProjectQuotationView.as_view(),
        name='download_project_quotation'),
    url(r'^resume/(?P<member_id>[0-9]+).html$', views.DownloadResumeView.as_view(), name='download_resume'),
    url(r'^section/(?P<section_id>[0-9]+)/attendance/(?P<year>[0-9]{4})/(?P<month>[0-9]{2}).html$',
        views.DownloadSectionAttendance.as_view(),
        name='download_section_attendance'),
    url(r'^member/list/eboa_info.html$', eboa_views.download_eboa_members, name='download_eboa_members'),
]

turnover_patterns = [
    url(r'^company_yearly.html$', views.TurnoverCompanyYearlyView.as_view(), name="turnover_company_yearly"),
    url(r'^company_monthly.html$', views.TurnoverCompanyMonthlyView.as_view(), name="turnover_company_monthly"),
    url(r'^charts/(?P<ym>[0-9]{6}).html$', views.TurnoverChartsMonthlyView.as_view(),
        name='turnover_charts_monthly'),
    url(r'^members/(?P<ym>[0-9]{6}).html$', views.TurnoverMembersMonthlyView.as_view(),
        name='turnover_members_monthly'),
    url(r'^clients/(?P<year>[0-9]{4}).html$', views.TurnoverClientsYearlyView.as_view(),
        name='turnover_clients_yearly'),
    url(r'^clients/(?P<ym>[0-9]{6}).html$', views.TurnoverClientsMonthlyView.as_view(),
        name='turnover_clients_monthly'),
    url(r'^client/(?P<client_id>[0-9]+)/(?P<ym>[0-9]{6}).html$', views.TurnoverClientMonthlyView.as_view(),
        name='turnover_client_monthly'),
]

subcontractor_patterns = [
    url(r'^list.html$', views.SubcontractorListView.as_view(), name='subcontractor_list'),
    url(r'^detail/(?P<subcontractor_id>[0-9]+).html$', views.SubcontractorDetailView.as_view(),
        name='subcontractor_detail'),
    url(r'^members/(?P<subcontractor_id>[0-9]+).html$', views.SubcontractorMembersView.as_view(),
        name='subcontractor_members'),
]

project_patterns = [
    url(r'^list.html$', views.ProjectListView.as_view(), name='project_list'),
    url(r'^order_list.html', views.ProjectOrdersView.as_view(), name='project_order_list'),
    url(r'^(?P<project_id>[0-9]+).html$', views.ProjectDetailView.as_view(), name='project_detail'),
    url(r'^members/(?P<project_id>[0-9]+).html$', views.ProjectMembersView.as_view(), name='project_members'),
    url(r'^end/(?P<project_id>[0-9]+).html$', views.ProjectEndView.as_view(), name='project_end'),
    url(r'^attendance/(?P<project_id>[0-9]+).html$', views.ProjectAttendanceView.as_view(),
        name='project_attendance_list'),
    url(r'^request_view/(?P<request_id>[0-9]+).html$', views.ProjectRequestView.as_view(),
        name='view_project_request'),
    url(r'^(?P<project_id>[0-9]+)/recommended_member.html$', views.RecommendedMembersView.as_view(),
        name='recommended_member'),
    url(r'^order_member_assign/(?P<project_id>[0-9]+).html$', views.ProjectOrderMemberAssignView.as_view(),
        name='project_order_member_assign'),
    url(r'^members_by_order/(?P<order_id>[0-9]+).html$', views.ProjectMembersByOrderView.as_view(),
        name='project_members_by_order'),
]

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^member/', include(member_patterns)),
    url(r'^section/', include(section_patterns)),
    url(r'^project/', include(project_patterns)),
    url(r'^release_list.html$', views.ReleaseListCurrentView.as_view(), name='release_list_current'),
    url(r'^release_list/(?P<ym>[0-9]{6}).html$', views.ReleaseListView.as_view(), name='release_list'),
    url(r'^subcontractor/', include(subcontractor_patterns)),
    url(r'^turnover/', include(turnover_patterns)),
    url(r'^download/', include(download_patterns)),
    url(r'^issues.html$', views.IssueListView.as_view(), name='issues'),
    url(r'^issue/(?P<issue_id>[0-9]+).html$', views.IssueDetailView.as_view(), name='issue_detail'),
    url(r'^history.html$', views.HistoryView.as_view(), name='history'),
    url(r"^batch_list.html", views.BatchListView.as_view(), name="batch_list"),
    url(r"^batch/(?P<name>[A-Za-z0-9_-]+).log$", views.BatchLogView.as_view(), name="batch_log"),
    url(r"^upload_file.html$", views.upload_resume, name="upload_file"),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^accounts/password/change/$', views.password_change, name='password_change'),
]
