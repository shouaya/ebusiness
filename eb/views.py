# coding: utf8
"""
Created on 2015/08/21

@author: Yang Wanjun
"""
import datetime
import re
import urllib
import json
import os

import biz

from django.http import HttpResponse
from django.contrib import admin
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout
from django.shortcuts import redirect, render_to_response
from django.views.decorators.csrf import csrf_protect
from django.template.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.forms.models import modelformset_factory
from django.db.models import Max

from utils import constants, common, errors, loader as file_loader, file_gen
from .models import Member, Section, Project, ProjectMember, Salesperson, \
    MemberAttendance, Subcontractor, BankInfo, ClientOrder, History, Client, BpMemberOrderInfo, Issue
from . import forms


PAGE_SIZE = 50


@login_required(login_url='/admin/login/')
def index(request):
    company = biz.get_company()
    now = datetime.date.today()
    next_month = common.add_months(now, 1)
    next_2_months = common.add_months(now, 2)
    filter_list = {'now_year': now.year,
                   'now_month': now.month,
                   'next_month_year': next_month.year,
                   'next_month_month': next_month.month,
                   'next_2_months_year': next_2_months.year,
                   'next_2_months_month': next_2_months.month}

    member_count = biz.get_all_members(request.user).count()
    working_members = biz.get_working_members(request.user)
    waiting_members = biz.get_waiting_members(request.user)

    is_superuser = False
    salesperson = None
    if request.user.is_superuser:
        is_superuser = True
    else:
        salesperson = request.user.salesperson
    current_month = biz.get_release_current_month(salesperson, is_superuser)
    next_month = biz.get_release_next_month(salesperson, is_superuser)
    next_2_month = biz.get_release_next_2_month(salesperson, is_superuser)

    context = RequestContext(request, {
        'company': company,
        'title': 'Home',
        'filter_list': filter_list,
        'member_count': member_count,
        'working_member_count': working_members.count(),
        'waiting_member_count': waiting_members.count(),
        'current_month_count': current_month.count(),
        'next_month_count': next_month.count(),
        'next_2_month_count': next_2_month.count(),
    })
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/admin/login/')
def employee_list(request):
    company = biz.get_company()
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

    all_members = biz.get_all_members(request.user)

    if salesperson:
        salesperson_obj = Salesperson.objects.get(employee_id=salesperson)
        all_members = salesperson_obj.member_set.public_all()
        params += u"&salesperson=%s" % (salesperson,)
    if first_name:
        all_members = all_members.filter(first_name__contains=first_name)
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
            'salesperson': Salesperson.objects.public_all(),
            'paginator': paginator,
            'params': params,
            'dict_order': dict_order,
        })
        template = loader.get_template('employee_list.html')
        return HttpResponse(template.render(context))


@login_required(login_url='/admin/login/')
def section_members(request, name):
    company = biz.get_company()
    section = Section.objects.get(name=name)
    status = request.GET.get('status', None)
    name = request.GET.get('name', None)
    business_status = request.GET.get('business_status', None)
    salesperson = request.GET.get('salesperson', None)
    params = ""
    if name:
        all_members = Member.objects.public_filter(section=section, name__contains=name)
        params += u"&name=%s" % (name,)
    else:
        all_members = Member.objects.public_filter(section=section)

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


@login_required(login_url='/admin/login/')
def project_list(request):
    company = biz.get_company()
    status = request.GET.get('status', None)
    name = request.GET.get('name', None)
    client = request.GET.get('client', None)
    salesperson = request.GET.get('salesperson', None)
    download = request.GET.get('download', None)
    params = ""
    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['name', 'client__name', 'salesperson__first_name', 'boss__name',
                                              'middleman__name', 'update_date'])
    order_list = common.get_ordering_list(o)

    if download == constants.DOWNLOAD_BUSINESS_PLAN:
        all_projects = Project.objects.public_filter(status=4)
    else:
        all_projects = Project.objects.public_all()

    if salesperson:
        salesperson_obj = Salesperson.objects.get(employee_id=salesperson)
        all_projects = salesperson_obj.project_set.public_all()
        params += "&salesperson=%s" % (salesperson,)
    if status:
        all_projects = Project.objects.public_filter(status=status)
        params += "&status=%s" % (status,)
    if name:
        all_projects = all_projects.filter(name__contains=name)
        params += "&name=%s" % (name,)

    if order_list:
        all_projects = all_projects.order_by(*order_list)

    if client:
        all_projects = all_projects.filter(client__name__contains=client)
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
            'salesperson': Salesperson.objects.public_all(),
            'params': params,
            'orders': "&o=%s" % (o,) if o else "",
            'dict_order': dict_order,
        })
        template = loader.get_template('project_list.html')
        return HttpResponse(template.render(context))


def project_order_list(request):
    company = biz.get_company()
    name = request.GET.get('name', None)
    client = request.GET.get('client', None)
    ym = request.GET.get('ym', None)
    if not ym:
        today = datetime.date.today()
        ym = "%s%02d" % (today.year, today.month)
    o = request.GET.get('o', None)
    params = ""
    dict_order = common.get_ordering_dict(o, ['name', 'client__name'])
    order_list = common.get_ordering_list(o)

    all_projects = Project.objects.public_all()

    if name:
        all_projects = all_projects.filter(name__contains=name)
        params += "&name=%s" % (name,)
    if client:
        all_projects = all_projects.filter(client__name__contains=client)
        params += "&client=%s" % (client,)

    all_project_orders = []
    first_day = common.get_first_day_from_ym(ym)
    last_day = common.get_last_day_by_month(first_day)
    all_projects = all_projects.filter(start_date__lte=last_day, end_date__gte=first_day)
    if order_list:
        all_projects = all_projects.order_by(*order_list)
    for project in all_projects:
        client_order = project.get_order_by_month(ym[:4], ym[4:])
        if not client_order:
            client_order = [None]
        all_project_orders.append((project, project.get_project_request(ym[:4], ym[4:]), client_order))
    params += "&ym=%s" % (ym,)

    paginator = Paginator(all_project_orders, PAGE_SIZE)
    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)

    context = RequestContext(request, {
        'company': company,
        'title': u'現在実施中案件一覧',
        'projects': projects,
        'paginator': paginator,
        'dict_order': dict_order,
        'params': params,
        'orders': "&o=%s" % (o,) if o else "",
        'month_list': common.get_month_list(-1, 1),
        'current_year': str(datetime.date.today().year),
        'current_month': str("%02d" % (datetime.date.today().month,)),
    })
    template = loader.get_template('project_order_list.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/admin/login/')
def project_detail(request, project_id):
    company = biz.get_company()
    project = Project.objects.get(pk=project_id)
    download = request.GET.get("download", None)

    if download == constants.DOWNLOAD_REQUEST:
        try:
            client_order_id = request.GET.get("client_order_id", None)
            request_name = request.GET.get("request_name", None)
            order_no = request.GET.get("order_no", None)
            ym = request.GET.get("ym", None)
            bank_id = request.GET.get('bank', None)
            now = datetime.datetime.now()
            client_order = ClientOrder.objects.get(pk=client_order_id)
            try:
                bank = BankInfo.objects.get(pk=bank_id)
            except ObjectDoesNotExist:
                bank = None
            path, request_no = file_gen.generate_request(project, company, client_order, request_name, order_no, ym, bank)
            filename = "EB請求書_%s_%s_%s.xls" % (str(request_no), project.client.name.encode('UTF-8'), now.strftime("%Y%m%d%H%M%S"))
            response = HttpResponse(open(path, 'rb'), content_type="application/excel")
            response['Content-Disposition'] = "filename=" + urllib.quote(filename)
            # 一時ファイルを削除する。
            common.delete_temp_files(os.path.dirname(path))
            return response
        except errors.FileNotExistException, ex:
            return HttpResponse(u"<script>alert('%s');window.close();</script>" % (ex.message,))
    else:
        context = RequestContext(request, {
            'company': company,
            'title': u'%s - 案件詳細' % (project.name,),
            'project': project,
            'banks': BankInfo.objects.public_all(),
            'order_month_list': project.get_year_month_order_finished(),
            'attendance_month_list': project.get_year_month_attendance_finished(),
        })
        context.update(csrf(request))
        template = loader.get_template('project_detail.html')
        return HttpResponse(template.render(context))


@login_required(login_url='/admin/login/')
def project_order_member_assign(request, project_id):
    pm_list = request.POST.get("pm_list", None)
    order_id = request.POST.get("order_id", None)
    d = dict()
    if pm_list and order_id:
        try:
            client_order = ClientOrder.objects.get(pk=order_id)
            client_order.member_comma_list = pm_list.strip(",")
            client_order.save()
            d['result'] = True
            d['message'] = u"成功しました。"
        except ObjectDoesNotExist:
            d['result'] = False
            d['message'] = u"注文書が削除されました。"
    else:
        d['result'] = False
        d['message'] = u"パラメータは空です。"
    return HttpResponse(json.dumps(d))


@login_required(login_url='/admin/login/')
def project_members_by_order(request, order_id):
    d = dict()
    try:
        client_order = ClientOrder.objects.get(pk=order_id)
        d['pm_list'] = client_order.member_comma_list
    except ObjectDoesNotExist:
        d['pm_list'] = ''
    return HttpResponse(json.dumps(d))


@login_required(login_url='/admin/login/')
def project_attendance_list(request, project_id):
    company = biz.get_company()
    project = Project.objects.get(pk=project_id)
    ym = request.GET.get('ym', None)
    formset = None

    context = {
        'company': company,
        'title': u'%s - 勤怠入力' % (project.name,),
        'project': project,
    }
    context.update(csrf(request))

    if ym:
        str_year = ym[:4]
        str_month = ym[4:]
        date = datetime.date(int(str_year), int(str_month), 1)
        if request.method == 'GET':
            initial_form_count = 0
            try:
                project_members = project.get_project_members_by_month(date)
                dict_initials = []
                for project_member in project_members:
                    attendance = project_member.get_attendance(date.year, date.month)
                    if attendance:
                        initial_form_count += 1
                        d = {'id': attendance.pk,
                             'pk': attendance.pk,
                             'project_member': attendance.project_member,
                             'year': str_year,
                             'month': str_month,
                             'basic_price': attendance.project_member.price,
                             'max_hours': attendance.project_member.max_hours,
                             'min_hours': attendance.project_member.min_hours,
                             'rate': attendance.rate,
                             'total_hours': attendance.total_hours,
                             'extra_hours': attendance.extra_hours,
                             'plus_per_hour': project_member.plus_per_hour,
                             'minus_per_hour': project_member.minus_per_hour,
                             'price': attendance.price,
                             'comment': attendance.comment,
                             }
                    else:
                        d = {'id': u"",
                             'project_member': project_member,
                             'year': str_year,
                             'month': str_month,
                             'basic_price': project_member.price,
                             'max_hours': project_member.max_hours,
                             'min_hours': project_member.min_hours,
                             'plus_per_hour': project_member.plus_per_hour,
                             'minus_per_hour': project_member.minus_per_hour,
                             }
                    dict_initials.append(d)
                AttendanceFormSet = modelformset_factory(MemberAttendance, form=forms.MemberAttendanceFormSet, extra=len(project_members))
                dict_initials.sort(key=lambda item: item['id'])
                formset = AttendanceFormSet(queryset=MemberAttendance.objects.none(), initial=dict_initials)
            except Exception as e:
                print e.message

            context.update({'formset': formset, 'initial_form_count': initial_form_count})

            r = render_to_response('project_attendance_list.html', context)
            return HttpResponse(r)
        else:
            AttendanceFormSet = modelformset_factory(MemberAttendance, form=forms.MemberAttendanceFormSet, extra=0)
            formset = AttendanceFormSet(request.POST)
            if formset.is_valid():
                attendance_list = formset.save(commit=False)
                for i, attendance in enumerate(attendance_list):
                    if not attendance.pk:
                        attendance_id = request.POST.get("form-%s-id" % (i,), None)
                        attendance.pk = int(attendance_id) if attendance_id else None
                    attendance.save()
                return redirect("/eb/project/%s.html#tbl_attendance" % (project.pk,))
            else:
                context.update({'formset': formset})
                r = render_to_response('project_attendance_list.html', context)
                return HttpResponse(r)


@login_required(login_url='/admin/login/')
def project_member_list(request, project_id):
    company = biz.get_company()
    status = request.GET.get('status', None)
    project = Project.objects.get(pk=project_id)
    params = ""
    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['member__first_name',
                                              'member__section', 'start_date', 'end_date', 'price'])
    order_list = common.get_ordering_list(o)

    all_project_members = project.get_project_members()
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


@login_required(login_url='/admin/login/')
def company_turnover_month(request):
    company = biz.get_company()
    ym = request.GET.get('ym', None)
    first_day = common.get_first_day_current_month()
    prev_month = first_day + datetime.timedelta(days=-1)
    if not ym:
        ym = "%s%02d" % (prev_month.year, prev_month.month)

    client_turnovers = biz.company_turnover_month(ym)
    summary = {'price': 0, 'cost': 0, 'profit': 0}
    for turnover in client_turnovers:
        summary['price'] += turnover['price']
        summary['cost'] += turnover['cost']
        summary['profit'] += turnover['profit']

    paginator = Paginator(client_turnovers, PAGE_SIZE)
    page = request.GET.get('page')
    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    context = RequestContext(request, {
        'company': company,
        'title': u'月の売上情報',
        'clients': clients,
        'summary': summary,
        'paginator': paginator,
        'month_list': common.get_month_list(-1, 1),
        'ym': ym,
        'current_year': str(prev_month.year),
        'current_month': str("%02d" % (prev_month.month,)),
    })
    template = loader.get_template('company_turnover_month.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/admin/login/')
def client_turnover_details(request, client_id):
    company = biz.get_company()
    ym = request.GET.get('ym', None)
    if not ym:
        today = datetime.date.today()
        ym = "%s%02d" % (today.year, today.month)

    params = '&ym=' + ym
    first_day = common.get_first_day_from_ym(ym)
    client = Client.objects.get(pk=client_id)
    client_turnovers = client.get_turnover_month_detail(first_day)
    client_turnover = biz.company_turnover_month(ym, client_id)[0]

    summary = {'base_price': 0, 'total_price': 0, 'cost': 0, 'profit': 0}
    for turnover in client_turnovers:
        summary['base_price'] += turnover['base_price']
        summary['total_price'] += turnover['total_price']
        summary['cost'] += turnover['cost']
        summary['profit'] += turnover['profit']

    paginator = Paginator(client_turnovers, PAGE_SIZE)
    page = request.GET.get('page')
    try:
        members = paginator.page(page)
    except PageNotAnInteger:
        members = paginator.page(1)
    except EmptyPage:
        members = paginator.page(paginator.num_pages)

    context = RequestContext(request, {
        'company': company,
        'client': client,
        'title': u'月の売上情報',
        'members': members,
        'summary': summary,
        'client_turnover': client_turnover,
        'paginator': paginator,
        'params': params,
    })
    template = loader.get_template('client_turnover_details.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/admin/login/')
def release_list(request):
    company = biz.get_company()
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
    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['member__first_name', 'project__name', 'start_date', 'end_date'])
    order_list = common.get_ordering_list(o)

    if request.user.is_superuser:
        all_project_members = biz.get_project_members_month(start_date)
    elif hasattr(request.user, 'salesperson'):
        all_project_members = biz.get_release_members_by_month(start_date, request.user.salesperson)
    else:
        all_project_members = biz.get_release_members_by_month(start_date, None)
    if order_list:
        all_project_members = all_project_members.order_by(*order_list)

    filter_list = common.get_month_list()

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


@login_required(login_url='/admin/login/')
def member_detail(request, employee_id):
    company = biz.get_company()
    member = Member.objects.get(employee_id=employee_id)
    download = request.GET.get('download', None)
    member.set_coordinate()

    if download == constants.DOWNLOAD_RESUME:
        date = datetime.date.today().strftime("%Y%m")
        filename = constants.NAME_RESUME % (member.first_name + member.last_name, date)
        output = file_gen.generate_resume(member)
        response = HttpResponse(output.read(), content_type="application/ms-excel")
        response['Content-Disposition'] = "filename=" + urllib.quote(filename.encode('utf-8')) + ".xlsx"
        return response
    else:
        project_count = member.projectmember_set.public_all().count()
        context = RequestContext(request, {
            'company': company,
            'member': member,
            'title': u'%s の履歴' % (member,),
            'project_count': project_count,
            'all_project_count': project_count + member.historyproject_set.public_all().count(),
            'default_project_count': range(1, 14),
        })
        template = loader.get_template('member_detail.html')
        return HttpResponse(template.render(context))


@login_required(login_url='/admin/login/')
def member_project_list(request, employee_id):
    status = request.GET.get('status', None)
    company = biz.get_company()
    member = Member.objects.get(employee_id=employee_id)
    if status and status != '0':
        project_members = ProjectMember.objects.public_filter(member=member, status=status)\
            .order_by('-status', 'end_date')
    else:
        project_members = ProjectMember.objects.public_filter(member=member)\
            .order_by('-status', 'end_date')

    context = RequestContext(request, {
        'company': company,
        'member': member,
        'title': u'%s の案件一覧' % (member,),
        'project_members': project_members,
    })
    template = loader.get_template('member_project_list.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/admin/login/')
def recommended_member_list(request, project_id):
    project = Project.objects.get(pk=project_id)
    company = biz.get_company()
    dict_skills = project.get_recommended_members()

    context = RequestContext(request, {
        'company': company,
        'title': u'%s - 推薦されるメンバーズ' % (project.name,),
        'project': project,
        'dict_skills': dict_skills,
    })
    template = loader.get_template('recommended_member.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/admin/login/')
def recommended_project_list(request, employee_id):
    company = biz.get_company()
    member = Member.objects.get(employee_id=employee_id)
    skills = member.get_skill_list()
    project_id_list = member.get_recommended_projects()
    projects = Project.objects.public_filter(pk__in=project_id_list)

    context = RequestContext(request, {
        'company': company,
        'title': u'%s - 推薦される案件' % (member,),
        'member': member,
        'skills': skills,
        'projects': projects,
    })
    template = loader.get_template('recommended_project.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/admin/login/')
def subcontractor_list(request):
    company = biz.get_company()
    name = request.GET.get('name', None)
    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['name'])
    order_list = common.get_ordering_list(o)
    params = ""

    all_subcontractors = Subcontractor.objects.public_all()
    if name:
        all_subcontractors = all_subcontractors.filter(name__contains=name)
        params += "&name=%s" % (name,)
    if order_list:
        all_subcontractors = all_subcontractors.order_by(*order_list)

    paginator = Paginator(all_subcontractors, PAGE_SIZE)
    page = request.GET.get('page')
    try:
        subcontractors = paginator.page(page)
    except PageNotAnInteger:
        subcontractors = paginator.page(1)
    except EmptyPage:
        subcontractors = paginator.page(paginator.num_pages)

    context = RequestContext(request, {
        'company': company,
        'title': u'協力会社一覧',
        'subcontractors': subcontractors,
        'paginator': paginator,
        'params': params,
        'orders': "&o=%s" % (o,) if o else "",
        'dict_order': dict_order,
        'bp_count': Member.objects.public_filter(subcontractor__isnull=False).count(),
    })
    template = loader.get_template('subcontractor_list.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/admin/login/')
def subcontractor_detail(request, subcontractor_id):
    company = biz.get_company()
    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['first_name'])
    order_list = common.get_ordering_list(o)

    subcontractor = Subcontractor.objects.get(pk=subcontractor_id)
    all_members = subcontractor.member_set.all()
    if order_list:
        all_members = all_members.order_by(*order_list)

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
        'title': u'%s | 協力会社' % (subcontractor.name,),
        'subcontractor': subcontractor,
        'members': members,
        'paginator': paginator,
        'orders': "&o=%s" % (o,) if o else "",
        'dict_order': dict_order,
        'order_month_list': subcontractor.get_year_month_order_finished(),
    })
    template = loader.get_template('subcontractor_detail.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/admin/login/')
def subcontractor_members(request, subcontractor_id):
    company = biz.get_company()
    subcontractor = Subcontractor.objects.get(pk=subcontractor_id)
    ym = request.GET.get('ym', None)

    context = RequestContext(request, {
        'company': company,
        'title': u'注文情報入力 | %s | 協力会社' % (subcontractor.name,),
        'subcontractor': subcontractor,
    })
    context.update(csrf(request))

    if ym:
        str_year = ym[:4]
        str_month = ym[4:]
    else:
        str_year = str(datetime.date.today().year)
        str_month = '%02d' % (datetime.date.today().month,)
        ym = str_year + str_month

    if request.method == 'GET':
        initial_form_count = 0
        first_day = common.get_first_day_from_ym(ym)
        # 現在案件実施中のメンバーを取得する。
        members = subcontractor.get_members_by_month(first_day)
        dict_initials = []
        for member in members:
            bp_member_info = member.get_bp_member_info(first_day)
            if bp_member_info:
                initial_form_count += 1
                d = {'id': bp_member_info.pk,
                     'pk': bp_member_info.pk,
                     'member': bp_member_info.member,
                     'year': bp_member_info.year,
                     'month': bp_member_info.month,
                     'min_hours': bp_member_info.min_hours,
                     'max_hours': bp_member_info.max_hours,
                     'cost': bp_member_info.cost,
                     'plus_per_hour': bp_member_info.plus_per_hour,
                     'minus_per_hour': bp_member_info.minus_per_hour,
                     'comment': bp_member_info.comment,
                     }
            else:
                d = {'id': u"",
                     'member': member,
                     'year': str_year,
                     'month': str_month,
                     'min_hours': 160,
                     'max_hours': 180,
                     'cost': member.cost,
                     'plus_per_hour': member.cost / 180,
                     'minus_per_hour': member.cost / 160,
                     'comment': "",
                     }
            dict_initials.append(d)
        BpOrderInfoFormSet = modelformset_factory(BpMemberOrderInfo, form=forms.BpMemberOrderInfoFormSet,
                                                  extra=len(members))
        dict_initials.sort(key=lambda item: item['id'])
        formset = BpOrderInfoFormSet(queryset=BpMemberOrderInfo.objects.none(), initial=dict_initials)

        context.update({'formset': formset, 'initial_form_count': initial_form_count})

        r = render_to_response('subcontractor_members.html', context)
        return HttpResponse(r)
    else:
        BpOrderInfoFormSet = modelformset_factory(BpMemberOrderInfo, form=forms.BpMemberOrderInfoFormSet, extra=0)
        formset = BpOrderInfoFormSet(request.POST)
        if formset.is_valid():
            bp_member_list = formset.save(commit=False)
            for i, bp_member in enumerate(bp_member_list):
                if not bp_member.pk:
                    bp_member_id = request.POST.get("form-%s-id" % (i,), None)
                    bp_member.pk = int(bp_member_id) if bp_member_id else None
                bp_member.save()
            return redirect("/eb/subcontractor_detail/%s.html" % (subcontractor.pk,))
        else:
            context.update({'formset': formset})
            r = render_to_response('subcontractor_members.html', context)
            return HttpResponse(r)


@login_required(login_url='/admin/login/')
@csrf_protect
def upload_resume(request):
    company = biz.get_company()
    context = {
        'company': company,
        'title': u'履歴書をアップロード',
        'site_header': admin.site.site_header,
        'site_title': admin.site.site_title,
    }
    context.update(csrf(request))

    if request.method == 'POST':
        form = forms.UploadFileForm(request.POST, request.FILES)
        context.update({'form': form})
        if form.is_valid():
            input_excel = request.FILES['file']
            member_id = request.POST.get('select', None)
            new_member, members = file_loader.load_resume(input_excel.read(), int(member_id) if member_id else None)
            if members:
                # 同じ名前のメンバーが存在する場合
                context.update({'members': members, 'display': True})
            else:
                pass
    else:
        form = forms.UploadFileForm()
        context.update({'form': form})

    r = render_to_response('upload_file.html', context)
    return HttpResponse(r)


def download_project_quotation(request, project_id):
    company = biz.get_company()
    project = Project.objects.get(pk=project_id)
    try:
        now = datetime.datetime.now()
        path = file_gen.generate_quotation(project, request.user, company)
        filename = "見積書_%s.xls" % (now.strftime("%Y%m%d%H%M%S"),)
        response = HttpResponse(open(path, 'rb'), content_type="application/excel")
        response['Content-Disposition'] = "filename=" + urllib.quote(filename)
        # 一時ファイルを削除する。
        common.delete_temp_files(os.path.dirname(path))
        return response
    except errors.FileNotExistException, ex:
        return HttpResponse(u"<script>alert('%s');window.close();</script>" % (ex.message,))


def download_client_order(request):
    p = request.GET.get('path', None)
    if p:
        path = os.path.join(settings.MEDIA_ROOT, p.strip('./'))
        if os.path.exists(path):
            filename = os.path.basename(path)
            response = HttpResponse(open(path, 'rb'), content_type="application/excel")
            response['Content-Disposition'] = "filename=" + urllib.quote(filename.encode("utf8"))
            return response


@login_required(login_url='/admin/login/')
def download_subcontractor_order(request, subcontractor_id):
    company = biz.get_company()
    ym = request.GET.get('ym', None)
    subcontractor = Subcontractor.objects.get(pk=subcontractor_id)

    try:
        data = biz.generate_order_data(company, subcontractor, request.user, ym)
        path = file_gen.generate_order(company, data)
        filename = biz.get_order_filename(subcontractor, data['DETAIL']['ORDER_NO'])
        response = HttpResponse(open(path, 'rb'), content_type="application/excel")
        response['Content-Disposition'] = "filename=" + urllib.quote(filename.encode('UTF-8'))
        return response
    except errors.FileNotExistException, ex:
        return HttpResponse(u"<script>alert('%s');window.close();</script>" % (ex.message,))


@login_required(login_url='/admin/login/')
def map_position(request):
    company = biz.get_company()
    members = Member.objects.public_filter(lat__isnull=False, lng__isnull=False).exclude(lat__exact='', lng__exact='')
    context = RequestContext(request, {
        'company': company,
        'title': u'地図情報',
        'members': members,
    })
    template = loader.get_template('map_position.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/admin/login/')
def issue(request):

    issues = Issue.objects.all()

    context = RequestContext(request, {
        'title': u'課題管理票',
        'issues': issues,
    })
    template = loader.get_template('issue.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/admin/login/')
def history(request):
    company = biz.get_company()

    histories = History.objects.all()
    total_hours = 0
    for h in histories:
        total_hours += h.get_hours()

    context = RequestContext(request, {
        'company': company,
        'title': u'更新履歴',
        'histories': histories,
        'total_hours': total_hours,
    })
    template = loader.get_template('history.html')
    return HttpResponse(template.render(context))


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required(login_url='/admin/login/')
def sync_coordinate(request):
    company = biz.get_company()

    if request.method == 'GET':
        members = company.get_members_to_set_coordinate()

        context = {
            'title': u'座標を設定',
            'site_header': admin.site.site_header,
            'site_title': admin.site.site_title,
            'members': members,
            'count': members.count()
        }
        context.update(csrf(request))
        r = render_to_response('sync_coordinate.html', context)
        return HttpResponse(r)
    else:
        lat = request.POST.get('lat', None)
        lng = request.POST.get('lng', None)
        member_id = request.POST.get('member_id', None)
        d = dict()
        if lat and lng and member_id:
            try:
                member = Member.objects.get(pk=member_id)
                member.lat = lat
                member.lng = lng
                member.coordinate_update_date = datetime.datetime.now()
                member.save()
                d['result'] = True
            except ObjectDoesNotExist:
                d['result'] = False
        else:
            d['result'] = False
        return HttpResponse(json.dumps(d))


@login_required(login_url='/admin/login/')
def sync_members(request):
    context = {
        'title': u'社員管理DBのデータを同期する。',
        'site_header': admin.site.site_header,
        'site_title': admin.site.site_title,
    }
    context.update(csrf(request))
    if request.method == 'GET':
        pass
    else:
        message_list = biz.sync_members()
        context.update({
            'messages': [u"完了しました。"],
            'message_list': message_list,
            'show_result': True,
        })

    r = render_to_response('sync_members.html', context)
    return HttpResponse(r)


@login_required(login_url='/admin/login/')
def sync_db2(request):
    context = {
        'title': u'社員管理DBのデータを同期する。',
        'site_header': admin.site.site_header,
        'site_title': admin.site.site_title,
    }
    context.update(csrf(request))
    if request.method == 'GET':
        pass
    else:
        data = request.POST.get('dict_members', None)
        if data:
            dict_members = json.loads(data)
            if dict_members['members']:
                for dict_member in dict_members['members']:
                    company_name = dict_member['company_name']
                    first_name = dict_member['first_name']
                    last_name = dict_member['last_name']
                    cost = dict_member['cost']
                    postcode = dict_member['postcode']
                    address = dict_member['address']
                    tel = dict_member['tel']

                    try:
                        subcontractor = Subcontractor.objects.get(name=company_name)
                    except ObjectDoesNotExist:
                        subcontractor = Subcontractor(name=company_name, post_code=postcode, address1=address, tel=tel)
                        subcontractor.save()

                    if Member.objects.filter(member_type=4, first_name=first_name, last_name=last_name,
                                             subcontractor=subcontractor).count() == 0:
                        member = Member(first_name=first_name, last_name=last_name, member_type=4,
                                        subcontractor=subcontractor, cost=cost)
                        max_employee_id = Member.objects.filter(employee_id__gte=10000).aggregate(Max('employee_id'))
                        member.employee_id = common.get_next_employee_id(max_employee_id.get('employee_id__max'))
                        member.save()
                context.update({
                    'messages': [u"完了しました。"],
                })

    r = render_to_response('syncdb2.html', context)
    return HttpResponse(r)
