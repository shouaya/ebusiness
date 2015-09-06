# coding: UTF-8
"""
Created on 2015/08/21

@author: Yang Wanjun
"""
import datetime
import re

import common

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Company, Member, Section, Project, ProjectMember, ProjectStatus


try:
    company = Company.objects.all()[0]
except:
    company = None


def index(request):
    project_status_list = []
    for i, status in enumerate(ProjectStatus.objects.all()):
        rtn = False if i == 0 else (i % 3 == 0)
        project_status_list.append((status.name, {'cnt': Project.objects.filter(status=status).count(), 'rtn': rtn}))
    now = datetime.date.today()
    next_month = common.add_months(now, 1)
    next_2_months = common.add_months(now, 2)
    filter_list = {'now_year': now.year,
                   'now_month': now.month,
                   'next_month_year': next_month.year,
                   'next_month_month': next_month.month,
                   'next_2_months_year': next_2_months.year,
                   'next_2_months_month': next_2_months.month}

    context = RequestContext(request, {
        'company': company,
        'title': 'Home',
        'project_status_list': project_status_list,
        'filter_list': filter_list,
    })
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context))


def employee_list(request):
    status = request.GET.get('status', None)
    name = request.GET.get('name', None)
    business_status = request.GET.get('business_status', None)
    salesperson = request.GET.get('salesperson', None)
    params = ""
    if name:
        all_members = Member.objects.filter(name__contains=name)
        params += u"&name=%s" % (name,)
    else:
        all_members = Member.objects.all()

    if status == "working":
        all_members = [member for member in all_members if member.get_project_end_date()]
        params += u"&status=%s" % (status,)
    elif status == "waiting":
        all_members = [member for member in all_members if not member.get_project_end_date()]
        params += u"&status=%s" % (status,)

    if business_status:
        all_members = [member for member in all_members if member.get_business_status() == business_status]
        params += u"&business_status=%s" % (business_status,)

    if salesperson:
        all_members = [member for member in all_members
                       if member.salesperson and salesperson in member.salesperson.name]
        params += u"&salesperson=%s" % (salesperson,)

    paginator = Paginator(all_members, company.display_count)
    page = request.GET.get('page')
    try:
        members = paginator.page(page)
    except PageNotAnInteger:
        members = paginator.page(1)
    except EmptyPage:
        members = paginator.page(paginator.num_pages)

    context = RequestContext(request, {
        'company': company,
        'title': u'要員一覧',
        'members': members,
        'paginator': paginator,
        'params': params,
    })
    template = loader.get_template('employee_list.html')
    return HttpResponse(template.render(context))


def section_members(request, name):
    section = Section.objects.get(name=name)
    status = request.GET.get('status', None)
    name = request.GET.get('name', None)
    business_status = request.GET.get('business_status', None)
    salesperson = request.GET.get('salesperson', None)
    params = ""
    if name:
        all_members = Member.objects.filter(section=section, name__contains=name)
        params += u"&name=%s" % (name,)
    else:
        all_members = Member.objects.filter(section=section)

    if status == "working":
        all_members = [member for member in all_members if member.get_project_end_date()]
    elif status == "waiting":
        all_members = [member for member in all_members if not member.get_project_end_date()]

    if business_status:
        all_members = [member for member in all_members if member.get_business_status() == business_status]
        params += u"&business_status=%s" % (business_status,)

    if salesperson:
        all_members = [member for member in all_members
                       if member.salesperson and salesperson in member.salesperson.name]
        params += u"&salesperson=%s" % (salesperson,)

    paginator = Paginator(all_members, company.display_count)
    page = request.GET.get('page')
    try:
        members = paginator.page(page)
    except PageNotAnInteger:
        members = paginator.page(1)
    except EmptyPage:
        members = paginator.page(paginator.num_pages)

    context = RequestContext(request, {
        'company': company,
        'title': u'%s 部署の要員一覧' % (section.name,),
        'members': members,
        'paginator': paginator,
        'params': params
    })
    template = loader.get_template('employee_list.html')
    return HttpResponse(template.render(context))


def project_list(request):
    status = request.GET.get('status', None)
    name = request.GET.get('name', None)
    client = request.GET.get('client', None)
    salesperson = request.GET.get('salesperson', None)
    if status:
        projects = Project.objects.filter(status__name=status)
    else:
        projects = Project.objects.all()
    if name:
        projects = projects.filter(name__contains=name)
    if client:
        projects = [project for project in projects if client in project.client.name]
    if salesperson:
        projects = [project for project in projects if project.salesperson and salesperson in project.salesperson.name]

    project_status = ProjectStatus.objects.all()

    context = RequestContext(request, {
        'company': company,
        'title': u'案件一覧',
        'projects': projects,
        'project_status': project_status,
    })
    template = loader.get_template('project_list.html')
    return HttpResponse(template.render(context))


def project_detail(request, project_id):
    project = Project.objects.get(project_id=project_id)
    dict_skills = project.get_recommended_members()

    context = RequestContext(request, {
        'company': company,
        'title': u'%s - 案件詳細' % (project.name,),
        'project': project,
        'dict_skills': dict_skills,
    })
    template = loader.get_template('project_detail.html')
    return HttpResponse(template.render(context))


def project_member_list(request, project_id):
    status = request.GET.get('status', None)
    project = Project.objects.get(project_id=project_id)
    all_project_members = project.projectmember_set.all()
    params = ""
    if status == "working":
        all_project_members = [member for member in all_project_members if member.member.get_project_end_date()]
        params += u"&status=%s" % (status,)
    elif status == "waiting":
        all_project_members = [member for member in all_project_members if not member.member.get_project_end_date()]
        params += u"&status=%s" % (status,)

    paginator = Paginator(all_project_members, company.display_count)
    page = request.GET.get('page')
    try:
        project_members = paginator.page(page)
    except PageNotAnInteger:
        project_members = paginator.page(1)
    except EmptyPage:
        project_members = paginator.page(paginator.num_pages)

    context = RequestContext(request, {
        'company': company,
        'title': u'%s - 案件参加者一覧' % (project.name,),
        'project': project,
        'project_members': project_members,
        'paginator': paginator,
        'params': params,
    })
    template = loader.get_template('project_members.html')
    return HttpResponse(template.render(context))


def release_list(request):
    period = request.GET.get('period', None)
    params = ""
    if period and re.match(r'[12][0-9]{5}', period):
        year = int(period[0:4])
        month = int(period[-2:])
        params = u"&period=%s" % (period,)
    else:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
    start_date = datetime.datetime(year, month, 1)
    end_date = common.add_months(start_date, 1)

    all_project_members = ProjectMember.objects.filter(end_date__gte=start_date,
                                                       end_date__lt=end_date).order_by('end_date')
    filter_list = common.get_release_months(company.release_month_count)

    paginator = Paginator(all_project_members, company.display_count)
    page = request.GET.get('page')
    try:
        project_members = paginator.page(page)
    except PageNotAnInteger:
        project_members = paginator.page(1)
    except EmptyPage:
        project_members = paginator.page(paginator.num_pages)

    context = RequestContext(request, {
        'company': company,
        'title': u'リリース状況一覧',
        'project_members': project_members,
        'paginator': paginator,
        'params': params,
        'filter_list': filter_list,
    })
    template = loader.get_template('release_list.html')
    return HttpResponse(template.render(context))


def member_project_list(request, employee_id):
    status = request.GET.get('status', None)
    member = Member.objects.get(employee_id=employee_id)
    if status and status != '0':
        project_members = ProjectMember.objects.filter(member=member, status=status)\
            .order_by('-status', 'end_date')
    else:
        project_members = ProjectMember.objects.filter(member=member)\
            .order_by('-status', 'end_date')

    context = RequestContext(request, {
        'company': company,
        'member': member,
        'title': u'%s の案件一覧' % (member.name,),
        'project_members': project_members,
    })
    template = loader.get_template('member_project_list.html')
    return HttpResponse(template.render(context))


def history(request):
    context = RequestContext(request, {
        'company': company,
        'title': u'更新履歴',
    })
    template = loader.get_template('history.html')
    return HttpResponse(template.render(context))


@login_required
def export_data(request):
    pass


@login_required
def import_data(request):
    pass