# coding: UTF-8
"""
Created on 2015/08/21

@author: Yang Wanjun
"""
import datetime
import re
import urllib
import xlrd

from django.http import HttpResponse
from django.contrib import admin
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout
from django.shortcuts import redirect, render_to_response
from django.views.decorators.csrf import csrf_protect
from django.template.context_processors import csrf

from utils import constants, common, errors, loader as file_loader
from .models import Company, Member, Section, Project, ProjectMember, Salesperson
from .forms import UploadFileForm


PAGE_SIZE = 50


def get_company():
    company_list = Company.objects.all()
    if company_list.count() == 0:
        return None
    else:
        return company_list[0]


def index(request):
    company = get_company()
    now = datetime.date.today()
    next_month = common.add_months(now, 1)
    next_2_months = common.add_months(now, 2)
    filter_list = {'now_year': now.year,
                   'now_month': now.month,
                   'next_month_year': next_month.year,
                   'next_month_month': next_month.month,
                   'next_2_months_year': next_2_months.year,
                   'next_2_months_month': next_2_months.month}

    member_count = company.get_all_members(request.user).count()
    working_members = company.get_working_members(request.user)
    waiting_members = company.get_waiting_members(request.user)

    current_month = company.get_release_current_month(request.user)
    next_month = company.get_release_next_month(request.user)
    next_2_month = company.get_release_next_2_month(request.user)

    context = RequestContext(request, {
        'company': company,
        'title': 'Home',
        'filter_list': filter_list,
        'member_count': member_count,
        'working_member_count': len(working_members),
        'waiting_member_count': len(waiting_members),
        'current_month_count': len(current_month),
        'next_month_count': len(next_month),
        'next_2_month_count': len(next_2_month),
    })
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context))


def employee_list(request):
    company = get_company()
    status = request.GET.get('status', None)
    first_name = request.GET.get('first_name', None)
    last_name = request.GET.get('last_name', None)
    business_status = request.GET.get('business_status', None)
    salesperson = request.GET.get('salesperson', None)
    download = request.GET.get('download', None)

    params = ""
    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['first_name', 'section', 'salesperson__first_name'])
    order_list = common.get_ordering_list(o)

    all_members = company.get_all_members(request.user)

    if salesperson:
        salesperson_obj = Salesperson.objects.get(employee_id=salesperson)
        all_members = salesperson_obj.member_set.all()
        params += u"&salesperson=%s" % (salesperson,)
    if first_name:
        all_members = Member.objects.filter(first_name__contains=first_name)
        params += u"&first_name=%s" % (first_name,)
    if last_name:
        all_members = all_members.filter(last_name__contains=last_name)
        params += u"&last_name=%s" % (last_name,)

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

    if download == constants.DOWNLOAD_MEMBER_LIST:
        filename = constants.NAME_MEMBER_LIST
        output = common.generate_member_list(all_members, filename)
        response = HttpResponse(output.read(), content_type="application/ms-excel")
        response['Content-Disposition'] = "filename=" + urllib.quote(filename.encode('utf-8')) + ".xlsx"
        return response
    else:
        paginator = Paginator(all_members, PAGE_SIZE)
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
            'salesperson': Salesperson.objects.all(),
            'paginator': paginator,
            'params': params,
            'dict_order': dict_order,
        })
        template = loader.get_template('employee_list.html')
        return HttpResponse(template.render(context))


def section_members(request, name):
    company = get_company()
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

    paginator = Paginator(all_members, PAGE_SIZE)
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
    company = get_company()
    status = request.GET.get('status', None)
    name = request.GET.get('name', None)
    client = request.GET.get('client', None)
    salesperson = request.GET.get('salesperson', None)
    download = request.GET.get('download', None)
    params = ""
    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['name', 'client__name', 'salesperson__first_name', 'boss__name',
                                              'middleman__name'])
    order_list = common.get_ordering_list(o)

    if download == constants.DOWNLOAD_BUSINESS_PLAN:
        all_projects = Project.objects.filter(status=4)
    else:
        all_projects = Project.objects.all()

    if salesperson:
        salesperson_obj = Salesperson.objects.get(employee_id=salesperson)
        all_projects = salesperson_obj.project_set.all()
        params += "&salesperson=%s" % (salesperson,)
    if status:
        all_projects = Project.objects.filter(status=status)
        params += "&status=%s" % (status,)
    if name:
        all_projects = all_projects.filter(name__contains=name)
        params += "&name=%s" % (name,)

    if order_list:
        all_projects = all_projects.order_by(*order_list)

    if client:
        all_projects = [project for project in all_projects if client in project.client.name]
        params += "&client=%s" % (client,)

    if download == constants.DOWNLOAD_BUSINESS_PLAN:
        filename = constants.NAME_BUSINESS_PLAN % (datetime.date.today().month,)
        output = common.generate_business_plan(all_projects, filename)
        response = HttpResponse(output.read(), content_type="application/ms-excel")
        response['Content-Disposition'] = "filename=" + urllib.quote(filename.encode('utf-8')) + ".xlsx"
        return response
    else:
        paginator = Paginator(all_projects, PAGE_SIZE)
        page = request.GET.get('page')
        try:
            projects = paginator.page(page)
        except PageNotAnInteger:
            projects = paginator.page(1)
        except EmptyPage:
            projects = paginator.page(paginator.num_pages)

        context = RequestContext(request, {
            'company': company,
            'title': u'案件一覧',
            'projects': projects,
            'paginator': paginator,
            'salesperson': Salesperson.objects.all(),
            'params': params,
            'dict_order': dict_order,
        })
        template = loader.get_template('project_list.html')
        return HttpResponse(template.render(context))


def project_detail(request, project_id):
    company = get_company()
    project = Project.objects.get(pk=project_id)
    download = request.GET.get("download", None)

    if download == constants.DOWNLOAD_REQUEST:
        try:
            path = common.generate_request(project, company)
            now = datetime.datetime.now()
            filename = "請求書（%s年%02d月）.xls" % (now.year, now.month)
            response = HttpResponse(open(path, 'rb'), content_type="application/excel")
            response['Content-Disposition'] = "filename=" + urllib.quote(filename)
            return response
        except errors.FileNotExistException, ex:
            return HttpResponse(u"<script>alert('%s');window.close();</script>" % (ex.message,))
    else:
        context = RequestContext(request, {
            'company': company,
            'title': u'%s - 案件詳細' % (project.name,),
            'project': project,
        })
        template = loader.get_template('project_detail.html')
        return HttpResponse(template.render(context))


def project_member_list(request, project_id):
    company = get_company()
    status = request.GET.get('status', None)
    project = Project.objects.get(pk=project_id)
    params = ""
    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['member__first_name',
                                              'member__section', 'start_date', 'end_date', 'price'])
    order_list = common.get_ordering_list(o)

    all_project_members = project.projectmember_set.all()
    if order_list:
        all_project_members = all_project_members.order_by(*order_list)

    if status == "working":
        all_project_members = [member for member in all_project_members if member.member.get_project_end_date()]
        params += u"&status=%s" % (status,)
    elif status == "waiting":
        all_project_members = [member for member in all_project_members if not member.member.get_project_end_date()]
        params += u"&status=%s" % (status,)

    paginator = Paginator(all_project_members, PAGE_SIZE)
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
        'dict_order': dict_order,
    })
    template = loader.get_template('project_members.html')
    return HttpResponse(template.render(context))


def release_list(request):
    company = get_company()
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
    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['member__first_name', 'project__name', 'start_date', 'end_date'])
    order_list = common.get_ordering_list(o)

    if request.user:
        if request.user.is_superuser:
            # 管理員の場合全部見られる
            all_project_members = ProjectMember.objects.filter(end_date__gte=start_date,
                                                               end_date__lt=end_date).order_by('end_date')
        elif common.is_salesperson_director(request.user) and request.user.salesperson.section:
            # 営業部長の場合、部門内すべての社員が見られる
            salesperson_list = request.user.salesperson.section.salesperson_set.all()
            all_project_members = ProjectMember.objects.filter(end_date__gte=start_date,
                                                               end_date__lt=end_date,
                                                               member__salesperson__in=salesperson_list).\
                order_by('end_date')
        elif common.is_salesperson(request.user):
            # 営業員の場合、担当している社員だけ見られる
            all_project_members = ProjectMember.objects.filter(end_date__gte=start_date,
                                                               end_date__lt=end_date,
                                                               member__salesperson=request.user.salesperson).\
                order_by('end_date')
        else:
            all_project_members = ProjectMember.objects.filter(pk=-1)
    else:
        all_project_members = ProjectMember.objects.filter(end_date__gte=start_date,
                                                           end_date__lt=end_date).order_by('end_date')
    if order_list:
        all_project_members = all_project_members.order_by(*order_list)

    filter_list = common.get_release_months(3)

    paginator = Paginator(all_project_members, PAGE_SIZE)
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
        'dict_order': dict_order,
        'filter_list': filter_list,
    })
    template = loader.get_template('release_list.html')
    return HttpResponse(template.render(context))


def member_detail(request, employee_id):
    company = get_company()
    member = Member.objects.get(employee_id=employee_id)

    context = RequestContext(request, {
        'company': company,
        'member': member,
        'title': u'%s の履歴' % (member,),
    })
    template = loader.get_template('member_detail.html')
    return HttpResponse(template.render(context))


def member_project_list(request, employee_id):
    status = request.GET.get('status', None)
    company = get_company()
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
        'title': u'%s の案件一覧' % (member,),
        'project_members': project_members,
    })
    template = loader.get_template('member_project_list.html')
    return HttpResponse(template.render(context))


def recommended_member_list(request, project_id):
    project = Project.objects.get(pk=project_id)
    company = get_company()
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
    company = get_company()
    member = Member.objects.get(employee_id=employee_id)
    skills = member.get_skill_list()
    project_id_list = member.get_recommended_projects()
    projects = Project.objects.filter(pk__in=project_id_list)

    context = RequestContext(request, {
        'company': company,
        'title': u'%s - 推薦される案件' % (member,),
        'member': member,
        'skills': skills,
        'projects': projects,
    })
    template = loader.get_template('recommended_project.html')
    return HttpResponse(template.render(context))


@csrf_protect
def upload_resume(request):
    company = get_company()
    context = {
        'company': company,
        'title': u'履歴書をアップロード',
        'site_header': admin.site.site_header,
        'site_title': admin.site.site_title,
    }
    context.update(csrf(request))

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        context.update({'form': form})
        if form.is_valid():
            input_excel = request.FILES['file']
            member_id = request.POST.get('select', None)
            new_member, finished = file_loader.load_resume(input_excel.read(), member_id)
            if not finished:
                members = Member.objects.raw(u"select * from eb_member"
                                             u" where CONCAT(first_name, last_name) = %s",
                                             [new_member.first_name + new_member.last_name])
                members = list(members)
                if members:
                    # 同じ名前のメンバーが存在する場合
                    context.update({'members': members, 'display': True})
            else:
                pass
    else:
        form = UploadFileForm()
        context.update({'form': form})

    r = render_to_response('upload_file.html', context)
    return HttpResponse(r)


def history(request):
    company = get_company()
    context = RequestContext(request, {
        'company': company,
        'title': u'更新履歴',
    })
    template = loader.get_template('history.html')
    return HttpResponse(template.render(context))


def logout_view(request):
    logout(request)
    return redirect('index')


def sync_db(request):
    message = "成功しました！"
    from utils.syncdb import SyncDb
    sync = SyncDb()
    sync.sync_subcontractor()
    sync.sync_section()
    sync.sync_member()
    sync.sync_client()
    sync.sync_project()
    return HttpResponse(message)