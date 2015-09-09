# coding: UTF-8
"""
Created on 2015/08/21

@author: Yang Wanjun
"""
import datetime
import re
import io
import xlwt

import common

from django.http import HttpResponse
from django.template import RequestContext, loader
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
    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['name', 'section', 'salesperson__name'])
    order_list = common.get_ordering_list(o)

    if name:
        all_members = Member.objects.filter(name__contains=name)
        params += u"&name=%s" % (name,)
    else:
        all_members = Member.objects.all()
    if order_list:
        all_members = all_members.order_by(*order_list)

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
        'dict_order': dict_order,
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
    download = request.GET.get('download', None)
    params = ""
    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['name', 'client__name', 'salesperson__name', 'boss__name',
                                              'middleman__name'])
    order_list = common.get_ordering_list(o)

    if status:
        projects = Project.objects.filter(status__name=status)
        params += "&status=%s" % (status,)
    else:
        projects = Project.objects.all()
    if name:
        projects = projects.filter(name__contains=name)
        params += "&name=%s" % (name,)

    if order_list:
        projects = projects.order_by(*order_list)

    if client:
        projects = [project for project in projects if client in project.client.name]
        params += "&client=%s" % (client,)
    if salesperson:
        projects = [project for project in projects if project.salesperson and salesperson in project.salesperson.name]
        params += "&salesperson=%s" % (salesperson,)

    if download == "download":
        output = io.BytesIO()
        wb = xlwt.Workbook()
        is_save = False
        for project in projects:
            project_members = project.projectmember_set.all()  # start_date__lte=now, end_date__gte=now
            if project_members.count() > 0:
                is_save = True
                ws = wb.add_sheet(project.name)
                ws.write(2, 1, u"案件名称")
                ws.write(2, 2, project.name)
                ws.write(2, 3, u"関連会社")
                ws.write(2, 4, project.client.name)
                ws.write(3, 1, u"営業員")
                ws.write(3, 2, project.salesperson.name)
                ws.write(4, 1, u"顧客責任者")
                ws.write(4, 2, project.boss.name)
                ws.write(4, 3, u"顧客連絡者")
                ws.write(4, 4, project.middleman.name)
                ws.write(5, 1, u"案件概要")
                ws.write(5, 2, project.description)

                # テーブル構造
                ws.write(9, 1, u"名前")
                ws.write(9, 2, u"開始日")
                ws.write(9, 3, u"終了日")
                ws.write(9, 4, u"単価")
                for i, project_member in enumerate(project_members):
                    ws.write(i + 10, 1, project_member.member.name)
                    if project_member.start_date:
                        ws.write(i + 10, 2, project_member.start_date.strftime("%Y-%m-%d"))
                    if project_member.end_date:
                        ws.write(i + 10, 3, project_member.end_date.strftime("%Y-%m-%d"))
                    ws.write(i + 10, 4, project_member.price)
        if is_save:
            wb.save(output)

        filename = "案件情報_%s.xls" % (datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),)
        response = HttpResponse(output.getvalue(), content_type="application/excel")
        response['Content-Disposition'] = "filename=" + filename
        return response
    else:
        project_status = ProjectStatus.objects.all()

        context = RequestContext(request, {
            'company': company,
            'title': u'案件一覧',
            'projects': projects,
            'params': params,
            'dict_order': dict_order,
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


def recommended_member_list(request, project_id):
    project = Project.objects.get(project_id=project_id)
    dict_skills = project.get_recommended_members()

    context = RequestContext(request, {
        'company': company,
        'title': u'%s - 推薦されるメンバーズ' % (project.name,),
        'project': project,
        'dict_skills': dict_skills,
    })
    template = loader.get_template('recommended_member.html')
    return HttpResponse(template.render(context))


def recommended_project_list(request, employee_id):
    member = Member.objects.get(employee_id=employee_id)
    skills = member.get_skill_list()
    project_id_list = member.get_recommended_projects()
    projects = Project.objects.filter(pk__in=project_id_list)

    context = RequestContext(request, {
        'company': company,
        'title': u'%s - 推薦される案件' % (member.name,),
        'member': member,
        'skills': skills,
        'projects': projects,
    })
    template = loader.get_template('recommended_project.html')
    return HttpResponse(template.render(context))


def history(request):
    context = RequestContext(request, {
        'company': company,
        'title': u'更新履歴',
    })
    template = loader.get_template('history.html')
    return HttpResponse(template.render(context))