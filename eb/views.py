# coding: utf8
"""
Created on 2015/08/21

@author: Yang Wanjun
"""
import datetime
import json
import os
import urllib

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Max
from django.forms.models import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command

from eb import biz, biz_batch, biz_turnover
from utils import constants, common, errors, loader as file_loader, file_gen
from . import forms
from .models import Member, Section, Project, ProjectMember, Salesperson, \
    MemberAttendance, Subcontractor, BankInfo, ClientOrder, History, BpMemberOrderInfo, Issue, \
    ProjectRequest, Client, EmployeeExpenses, BatchManage

PAGE_SIZE = 50


@login_required(login_url='/eb/login/')
def index(request):
    company = biz.get_company()
    now = datetime.date.today()
    next_month = common.add_months(now, 1)
    next_2_months = common.add_months(now, 2)
    filter_list = {'current_ym': now.strftime('%Y%m'),
                   'next_ym': next_month.strftime('%Y%m'),
                   'next_2_ym': next_2_months.strftime('%Y%m')}

    member_count = biz.get_sales_members().count()
    working_members = biz.get_working_members()
    waiting_members = biz.get_waiting_members()
    member_in_coming = biz.get_members_in_coming()
    off_sales_members_count = biz.get_off_sales_members().count()

    current_month = biz.get_release_current_month()
    next_month = biz.get_release_next_month()
    next_2_month = biz.get_release_next_2_month()

    subcontractor_sales_member_count = biz.get_subcontractor_sales_members().count()
    subcontractor_working_member_count = biz.get_subcontractor_working_members().count()
    subcontractor_waiting_member_count = subcontractor_sales_member_count - subcontractor_working_member_count
    subcontractor_off_sales_member_count = biz.get_subcontractor_off_sales_members().count()

    subcontractor_release_current_month = biz.get_subcontractor_release_current_month().count()
    subcontractor_release_next_month = biz.get_subcontractor_release_next_month().count()
    subcontractor_release_next_2_month = biz.get_subcontractor_release_next_2_month().count()

    activities = biz.get_activities_incoming()

    context = RequestContext(request, {
        'company': company,
        'title': 'Home',
        'filter_list': filter_list,
        'member_count': member_count,
        'working_member_count': working_members.count(),
        'waiting_member_count': waiting_members.count(),
        'members_in_coming_count': member_in_coming.count(),
        'off_sales_members_count': off_sales_members_count,
        'current_month_count': current_month.count(),
        'next_month_count': next_month.count(),
        'next_2_month_count': next_2_month.count(),
        'subcontractor_sales_member_count': subcontractor_sales_member_count,
        'subcontractor_working_member_count': subcontractor_working_member_count,
        'subcontractor_waiting_member_count': subcontractor_waiting_member_count,
        'subcontractor_off_sales_member_count': subcontractor_off_sales_member_count,
        'subcontractor_release_current_month': subcontractor_release_current_month,
        'subcontractor_release_next_month': subcontractor_release_next_month,
        'subcontractor_release_next_2_month': subcontractor_release_next_2_month,
        'activities': activities,
    })
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/eb/login/')
def employee_list(request):
    company = biz.get_company()
    status = request.GET.get('status', None)
    section_id = request.GET.get('section', None)
    salesperson_id = request.GET.get('salesperson', None)
    if status == "sales":
        all_members = biz.get_sales_members()
    elif status == "working":
        all_members = biz.get_working_members()
    elif status == "waiting":
        all_members = biz.get_waiting_members()
    elif status == "off_sales":
        all_members = biz.get_off_sales_members()
    else:
        all_members = biz.get_all_members()

    param_list = common.get_request_params(request.GET)
    params = "&".join(["%s=%s" % (key, value) for key, value in param_list.items()]) if param_list else ""
    if 'status' in param_list:
        del param_list['status']
    if 'section' in param_list:
        del param_list['section']
    if 'salesperson' in param_list:
        del param_list['salesperson']
    if param_list:
        all_members = all_members.filter(**param_list)

    if section_id:
        all_members = biz.get_members_by_section(all_members, section_id)
    if salesperson_id:
        all_members = biz.get_members_by_salesperson(all_members, salesperson_id)
    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['first_name', 'section', 'subcontractor__name',
                                              'salesperson__first_name'])
    order_list = common.get_ordering_list(o)

    if order_list:
        all_members = all_members.order_by(*order_list)

    # if business_status:
    #     all_members = [member for member in all_members if member.get_business_status() == business_status]
    #     params += u"&business_status=%s" % (business_status,)
    #
    # if download == constants.DOWNLOAD_MEMBER_LIST:
    #     filename = constants.NAME_MEMBER_LIST
    #     output = common.generate_member_list(all_members, filename)
    #     response = HttpResponse(output.read(), content_type="application/ms-excel")
    #     response['Content-Disposition'] = "filename=" + urllib.quote(filename.encode('utf-8')) + ".xlsx"
    #     return response
    # else:
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
        'sections': Section.objects.public_filter(is_on_sales=True),
        'salesperson': Salesperson.objects.public_all(),
        'paginator': paginator,
        'params': "&" + params if params else "",
        'dict_order': dict_order,
        'page_type': "off_sales" if status == "off_sales" else None,
    })
    template = loader.get_template('employee_list.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/eb/login/')
def members_in_coming(request):
    company = biz.get_company()
    param_list = common.get_request_params(request.GET)
    params = "&".join(["%s=%s" % (key, value) for key, value in param_list.items()]) if param_list else ""

    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['first_name', 'section', 'subcontractor__name',
                                              'salesperson__first_name'])
    order_list = common.get_ordering_list(o)

    all_members = biz.get_members_in_coming()
    if param_list:
        all_members = all_members.filter(**param_list)
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
        'title': u'協力社員一覧',
        'members': members,
        'sections': Section.objects.public_filter(is_on_sales=True),
        'salesperson': Salesperson.objects.public_all(),
        'paginator': paginator,
        'params': "&" + params if params else "",
        'dict_order': dict_order,
        'page_type': "members_in_coming",
    })
    template = loader.get_template('employee_list.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/eb/login/')
def members_subcontractor(request):
    company = biz.get_company()
    status = request.GET.get('status', None)
    if status == "sales":
        all_members = biz.get_subcontractor_sales_members()
    elif status == "working":
        all_members = biz.get_subcontractor_working_members()
    elif status == "waiting":
        all_members = biz.get_subcontractor_waiting_members()
    elif status == "off_sales":
        all_members = biz.get_subcontractor_off_sales_members()
    else:
        all_members = biz.get_subcontractor_all_members()

    param_list = common.get_request_params(request.GET)
    params = "&".join(["%s=%s" % (key, value) for key, value in param_list.items()]) if param_list else ""
    if 'status' in param_list:
        del param_list['status']
    if param_list:
        all_members = all_members.filter(**param_list)

    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['first_name', 'section', 'subcontractor__name',
                                              'salesperson__first_name'])
    order_list = common.get_ordering_list(o)

    if order_list:
        all_members = all_members.order_by(*order_list)

    # if business_status:
    #     all_members = [member for member in all_members if member.get_business_status() == business_status]
    #     params += u"&business_status=%s" % (business_status,)
    #
    # if download == constants.DOWNLOAD_MEMBER_LIST:
    #     filename = constants.NAME_MEMBER_LIST
    #     output = common.generate_member_list(all_members, filename)
    #     response = HttpResponse(output.read(), content_type="application/ms-excel")
    #     response['Content-Disposition'] = "filename=" + urllib.quote(filename.encode('utf-8')) + ".xlsx"
    #     return response
    # else:
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
        'title': u'協力社員一覧',
        'members': members,
        'sections': Section.objects.public_filter(is_on_sales=True),
        'salesperson': Salesperson.objects.public_all(),
        'paginator': paginator,
        'params': "&" + params if params else "",
        'dict_order': dict_order,
        'page_type': "off_sales" if status == "off_sales" else None,
    })
    template = loader.get_template('employee_list.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/eb/login/')
def change_list(request):
    company = biz.get_company()
    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['first_name', 'section__name', 'salesperson__first_name'])
    order_list = common.get_ordering_list(o)

    all_members = biz.get_next_change_list()
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
        'title': u'リリース状況一覧',
        'members': members,
        'paginator': paginator,
        'dict_order': dict_order,
    })
    template = loader.get_template('member_change_list.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/eb/login/')
def member_expanses_update(request, member_id, year, month):
    advance_amount = request.POST.get("advance_amount", 0)
    member = get_object_or_404(Member, pk=member_id)
    try:
        member_expanses = EmployeeExpenses.objects.get(member=member, year=year, month=month)
    except ObjectDoesNotExist:
        member_expanses = EmployeeExpenses(member=member, year=year, month=month)
    member_expanses.advance_amount = advance_amount

    try:
        member_expanses.save()
        d = {'ret': 0, 'message': None}
    except Exception as e:
        d = {'ret': 1, 'message': e.message}
    return HttpResponse(json.dumps(d))


@login_required(login_url='/eb/login/')
def project_list(request):
    company = biz.get_company()
    param_list = common.get_request_params(request.GET)
    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['name', 'client__name', 'salesperson__first_name', 'boss__name',
                                              'middleman__name', 'update_date'])
    order_list = common.get_ordering_list(o)
    all_projects = biz.get_projects(q=param_list, o=order_list)

    params = "&".join(["%s=%s" % (key, value) for key, value in param_list.items()]) if param_list else ""

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
        'params': "&" + params if params else "",
        'orders': "&o=%s" % (o,) if o else "",
        'dict_order': dict_order,
    })
    template = loader.get_template('project_list.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/eb/login/')
def project_end(request, project_id):
    params = ""
    for p, v in dict(request.GET).items():
        params += "&%s=%s" % (p, v[0])
    params = params[1:] if params else ""

    try:
        project = Project.objects.get(pk=project_id)
        project.status = 5
        project.save()
    except ObjectDoesNotExist:
        pass

    return redirect(reverse(project_list) + "?" + params)


@login_required(login_url='/eb/login/')
def project_order_list(request):
    company = biz.get_company()
    param_list = common.get_request_params(request.GET)
    ym = request.GET.get('ym', None)
    if not ym:
        today = common.add_months(datetime.date.today(), -1)
        ym = "%s%02d" % (today.year, today.month)
    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['project__name', 'project__client__name',
                                              'clientorder__order_no', 'project__projectrequest__request_no'])
    order_list = common.get_ordering_list(o)

    all_project_orders = biz.get_projects_orders(ym, q=param_list, o=order_list)

    params = "&".join(["%s=%s" % (key, value) for key, value in param_list.items()]) if param_list else ""
    params = "%s&ym=%s" % ("&" + params if params else "", ym,)

    paginator = Paginator(all_project_orders, PAGE_SIZE)
    page = request.GET.get('page')
    try:
        project_orders = paginator.page(page)
    except PageNotAnInteger:
        project_orders = paginator.page(1)
    except EmptyPage:
        project_orders = paginator.page(paginator.num_pages)

    context = RequestContext(request, {
        'company': company,
        'title': u'%s年%s月の注文情報一覧' % (ym[:4], ym[4:]),
        'project_orders': project_orders,
        'paginator': paginator,
        'dict_order': dict_order,
        'params': params,
        'orders': "&o=%s" % (o,) if o else "",
        'month_list': common.get_month_list(-1, 1),
        'current_year': ym[:4],
        'current_month': ym[4:],
        'ym': ym,
    })
    template = loader.get_template('project_order_list.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/eb/login/')
def project_detail(request, project_id):
    company = biz.get_company()
    project = Project.objects.get(pk=project_id)

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


@login_required(login_url='/eb/login/')
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


@login_required(login_url='/eb/login/')
def project_members_by_order(request, order_id):
    d = dict()
    try:
        client_order = ClientOrder.objects.get(pk=order_id)
        d['pm_list'] = client_order.member_comma_list
    except ObjectDoesNotExist:
        d['pm_list'] = ''
    return HttpResponse(json.dumps(d))


@login_required(login_url='/eb/login/')
@permission_required('eb.input_attendance', raise_exception=True)
def project_attendance_list(request, project_id):
    company = biz.get_company()
    project = Project.objects.get(pk=project_id)
    ym = request.GET.get('ym', None)

    context = RequestContext(request, {
        'company': company,
        'title': u'%s - 勤怠入力' % (project.name,),
        'project': project,
    })
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
                    # 既に入力済みの場合、DBから取得する。
                    attendance = project_member.get_attendance(date.year, date.month)
                    if attendance:
                        initial_form_count += 1
                        if project.is_hourly_pay:
                            d = {'id': attendance.pk,
                                 'pk': attendance.pk,
                                 'project_member': attendance.project_member,
                                 'year': str_year,
                                 'month': str_month,
                                 'total_hours': attendance.total_hours,
                                 'extra_hours': attendance.extra_hours,
                                 'price': attendance.price,
                                 'comment': attendance.comment,
                                 'hourly_pay': project_member.hourly_pay
                                 }
                        else:
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
                        # まだ入力してない場合、EBOAの出勤情報から取得する。
                        total_hours = biz.get_attendance_time_from_eboa(project_member, date.year, date.month)
                        if project.is_hourly_pay:
                            d = {'id': u"",
                                 'project_member': project_member,
                                 'year': str_year,
                                 'month': str_month,
                                 'total_hours': total_hours,
                                 'hourly_pay': project_member.hourly_pay
                                 }
                        else:
                            total_price = 0
                            if total_hours > project_member.max_hours:
                                extra_hours = total_hours - float(project_member.max_hours)
                                total_price = project_member.price + (extra_hours * project_member.plus_per_hour)
                            elif total_hours < project_member.min_hours and total_hours > 0:
                                extra_hours = total_hours - float(project_member.min_hours)
                                total_price = project_member.price + (extra_hours * project_member.minus_per_hour)
                            elif total_hours > 0:
                                extra_hours = 0
                                total_price = project_member.price
                            else:
                                extra_hours = 0
                            d = {'id': u"",
                                 'project_member': project_member,
                                 'year': str_year,
                                 'month': str_month,
                                 'basic_price': project_member.price,
                                 'total_hours': total_hours,
                                 'extra_hours': extra_hours,
                                 'max_hours': project_member.max_hours,
                                 'min_hours': project_member.min_hours,
                                 'plus_per_hour': project_member.plus_per_hour,
                                 'minus_per_hour': project_member.minus_per_hour,
                                 'price': total_price,
                                 }
                    dict_initials.append(d)
                if project.is_hourly_pay:
                    AttendanceFormSet = modelformset_factory(MemberAttendance,
                                                             form=forms.MemberAttendanceFormSetHourlyPay,
                                                             extra=len(project_members))
                else:
                    AttendanceFormSet = modelformset_factory(MemberAttendance,
                                                             form=forms.MemberAttendanceFormSet,
                                                             extra=len(project_members))
                dict_initials.sort(key=lambda item: item['id'])
                context['formset'] = AttendanceFormSet(queryset=MemberAttendance.objects.none(), initial=dict_initials)
            except Exception as e:
                context['formset'] = None
                print e.message

            context['initial_form_count'] = initial_form_count

            r = render_to_response('project_attendance_list.html', context)
            return HttpResponse(r)
        else:
            if project.is_hourly_pay:
                AttendanceFormSet = modelformset_factory(MemberAttendance, form=forms.MemberAttendanceFormSetHourlyPay,
                                                         extra=0)
            else:
                AttendanceFormSet = modelformset_factory(MemberAttendance, form=forms.MemberAttendanceFormSet, extra=0)
            formset = AttendanceFormSet(request.POST)
            if formset.is_valid():
                attendance_list = formset.save(commit=False)
                for i, attendance in enumerate(attendance_list):
                    if not attendance.pk:
                        attendance_id = request.POST.get("form-%s-id" % (i,), None)
                        attendance.pk = int(attendance_id) if attendance_id else None
                    action_flag = CHANGE if attendance.pk else ADDITION
                    attendance.save()
                    if action_flag == ADDITION:
                        LogEntry.objects.log_action(request.user.id,
                                                    ContentType.objects.get_for_model(attendance).pk,
                                                    attendance.pk,
                                                    unicode(attendance),
                                                    action_flag)
                return redirect(reverse("project_detail", args=(project.pk,)))
            else:
                context.update({'formset': formset})
                r = render_to_response('project_attendance_list.html', context)
                return HttpResponse(r)


@login_required(login_url='/eb/login/')
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


@login_required(login_url='/eb/login/')
def section_list(request):
    sections = biz.get_on_sales_section()
    section_count_list = []
    total_count = 0
    for section in sections:
        count = biz.get_members_section(section).count()
        total_count += count
        section_count_list.append((section, count))

    context = RequestContext(request, {
        'title': u'部署情報一覧',
        'sections': section_count_list,
        'total_count': total_count,
    })
    template = loader.get_template('section_list.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/eb/login/')
def section_detail(request, section_id):
    company = biz.get_company()
    section = get_object_or_404(Section, pk=section_id)
    all_members = biz.get_members_section(section)

    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['first_name', 'projectmember__project__name'])
    order_list = common.get_ordering_list(o)

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
        'title': u'%s | 部署' % (section.name,),
        'section': section,
        'members': members,
        'dict_order': dict_order,
        'paginator': paginator,
        'year_list': biz.get_year_list()
    })
    template = loader.get_template('section_detail.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/eb/login/')
def section_attendance(request, section_id):
    company = biz.get_company()
    section = get_object_or_404(Section, pk=section_id)
    today = datetime.date.today()
    year = request.GET.get('year', today.year)
    month = request.GET.get('month', today.month)

    param_list = common.get_request_params(request.GET)
    params = "&".join(["%s=%s" % (key, value) for key, value in param_list.items()]) if param_list else ""

    project_members = biz.get_project_members_month_section(section, datetime.date(int(year), int(month), 20))

    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['member__first_name', 'member__employee_id',
                                              'member__subcontractor__name', 'project__name',
                                              'project__client__name', 'member__member_type'])
    order_list = common.get_ordering_list(o)

    if order_list:
        project_members = project_members.order_by(*order_list)

    context = RequestContext(request, {
        'company': company,
        'title': u'%s | %s年%s月 | 出勤' % (section.name, year, month),
        'section': section,
        'project_members': project_members,
        'dict_order': dict_order,
        'params': "&" + params if params else "",
        'year': year,
        'month': month,
    })
    template = loader.get_template('section_attendance.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/eb/login/')
def view_project_request(request, request_id):
    company = biz.get_company()
    project_request = get_object_or_404(ProjectRequest, pk=request_id)
    if hasattr(project_request, 'projectrequestheading'):
        request_heading = project_request.projectrequestheading
    else:
        request_heading = None
    request_details = list(project_request.projectrequestdetail_set.all())
    project_members = [detail.project_member for detail in request_details]
    detail_expenses, expenses_amount = biz.get_request_expenses_list(project_request.project,
                                                                     project_request.year,
                                                                     project_request.month,
                                                                     project_members)
    if len(request_details) < 20:
        request_details.extend([None] * (20 - len(request_details)))

    context = RequestContext(request, {
        'company': company,
        'title': u'請求書 | %s | %s年%s月' % (project_request.project.name, project_request.year, project_request.month),
        'project_request': project_request,
        'request_heading': request_heading,
        'request_details': request_details,
        'detail_expenses': detail_expenses,
    })
    template = loader.get_template('project_request.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/eb/login/')
def turnover_company_monthly(request):
    company = biz.get_company()
    company_turnover = biz_turnover.turnover_company_monthly()
    month_list = [str(item['ym']) for item in company_turnover]
    turnover_amount_list = [item['turnover_amount'] for item in company_turnover]
    context = RequestContext(request, {
        'company': company,
        'title': u'売上情報',
        'company_turnover': company_turnover,
        'month_list': month_list,
        'turnover_amount_list': turnover_amount_list,
    })
    template = loader.get_template('turnover_company_monthly.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/eb/login/')
def turnover_charts_monthly(request, ym):
    company = biz.get_company()
    sections_turnover = biz_turnover.sections_turnover_monthly(ym)
    section_attendance_amount_list = [item['attendance_amount'] for item in sections_turnover]
    section_attendance_tex_list = [item['attendance_tex'] for item in sections_turnover]
    section_expenses_amount_list = [item['expenses_amount'] for item in sections_turnover]
    section_name_list = ["'" + item['section'].name + "'" for item in sections_turnover]

    salesperson_turnover = biz_turnover.salesperson_turnover_monthly(ym)
    salesperson_attendance_amount_list = [item['attendance_amount'] for item in salesperson_turnover]
    salesperson_attendance_tex_list = [item['attendance_tex'] for item in salesperson_turnover]
    salesperson_expenses_amount_list = [item['expenses_amount'] for item in salesperson_turnover]
    salesperson_name_list = ["'" + item['salesperson'].__unicode__() + "'" for item in salesperson_turnover]

    clients_turnover = biz_turnover.clients_turnover_monthly(ym)
    clients_attendance_amount_list = [item['attendance_amount'] for item in clients_turnover]
    clients_attendance_tex_list = [item['attendance_tex'] for item in clients_turnover]
    clients_expenses_amount_list = [item['expenses_amount'] for item in clients_turnover]
    clients_name_list = ["'" + item['client'].name + "'" for item in clients_turnover]

    context = RequestContext(request, {
        'company': company,
        'title': u'%s - 売上情報' % (ym,),
        'sections_turnover': sections_turnover,
        'section_name_list': ",".join(section_name_list),
        'section_attendance_amount_list': section_attendance_amount_list,
        'section_attendance_tex_list': section_attendance_tex_list,
        'section_expenses_amount_list': section_expenses_amount_list,
        'salesperson_turnover': salesperson_turnover,
        'salesperson_name_list': ",".join(salesperson_name_list),
        'salesperson_attendance_amount_list': salesperson_attendance_amount_list,
        'salesperson_attendance_tex_list': salesperson_attendance_tex_list,
        'salesperson_expenses_amount_list': salesperson_expenses_amount_list,
        'clients_turnover': clients_turnover,
        'clients_name_list': ",".join(clients_name_list),
        'clients_attendance_amount_list': clients_attendance_amount_list,
        'clients_attendance_tex_list': clients_attendance_tex_list,
        'clients_expenses_amount_list': clients_expenses_amount_list,
        'ym': ym,
    })
    template = loader.get_template('turnover_charts_monthly.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/eb/login/')
def turnover_members_monthly(request, ym):
    company = biz.get_company()
    param_list = common.get_request_params(request.GET)
    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['project_member__member__first_name',
                                              'project_member__member__section__name',
                                              'project_request__project__name',
                                              'project_request__projectrequestheading__client__name'])
    order_list = common.get_ordering_list(o)
    params = "&".join(["%s=%s" % (key, value) for key, value in param_list.items()]) if param_list else ""

    sections = biz_turnover.get_turnover_sections(ym)
    all_turnover_details = biz_turnover.members_turnover_monthly(ym, param_list, order_list)
    summary = {'attendance_amount': 0, 'expenses_amount': 0,
               'attendance_tex': 0, 'all_amount': 0,
               'cost_amount': 0}
    for item in all_turnover_details:
        summary['attendance_amount'] += item.total_price
        summary['attendance_tex'] += item.get_tax_price()
        summary['expenses_amount'] += item.expenses_price
        summary['all_amount'] += item.total_price + item.get_tax_price() + item.expenses_price
        summary['cost_amount'] += item.cost
    summary['attendance_tex'] = int(round(summary['attendance_tex']))
    summary['all_amount'] = int(round(summary['all_amount']))
    paginator = Paginator(all_turnover_details, PAGE_SIZE)
    page = request.GET.get('page')
    try:
        turnover_details = paginator.page(page)
    except PageNotAnInteger:
        turnover_details = paginator.page(1)
    except EmptyPage:
        turnover_details = paginator.page(paginator.num_pages)

    context = RequestContext(request, {
        'company': company,
        'title': u'%s年%s月の売上詳細情報' % (ym[:4], ym[4:]),
        'sections': sections,
        'salesperson': Salesperson.objects.public_all(),
        'turnover_details': turnover_details,
        'summary': summary,
        'paginator': paginator,
        'dict_order': dict_order,
        'orders': "&o=%s" % (o,) if o else "",
        'params': "&" + params if params else "",
        'ym': ym,
    })
    template = loader.get_template('turnover_members_monthly.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/eb/login/')
def turnover_clients_monthly(request, ym):
    company = biz.get_company()
    clients_turnover = biz_turnover.clients_turnover_monthly(ym)

    summary = {'attendance_amount': 0, 'expenses_amount': 0,
               'attendance_tex': 0, 'all_amount': 0}
    for item in clients_turnover:
        summary['attendance_amount'] += item['attendance_amount']
        summary['attendance_tex'] += item['attendance_tex']
        summary['expenses_amount'] += item['expenses_amount']
        summary['all_amount'] += item['attendance_amount'] + item['attendance_tex'] + item['expenses_amount']

    context = RequestContext(request, {
        'company': company,
        'title': u'%s年%s月のお客様別売上情報' % (ym[:4], ym[4:]),
        'clients_turnover': clients_turnover,
        'ym': ym,
        'summary': summary,
    })
    template = loader.get_template('turnover_clients_monthly.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/eb/login/')
def turnover_client_monthly(request, client_id, ym):
    company = biz.get_company()
    client = get_object_or_404(Client, pk=client_id)
    turnover_details = biz_turnover.turnover_client_monthly(client_id, ym)

    summary = {'attendance_amount': 0, 'expenses_amount': 0,
               'tax_amount': 0, 'all_amount': 0}
    for item in turnover_details:
        summary['attendance_amount'] += item['attendance_amount']
        summary['tax_amount'] += item['tax_amount']
        summary['expenses_amount'] += item['expenses_amount']
        summary['all_amount'] += item['all_amount']

    context = RequestContext(request, {
        'company': company,
        'title': u'%s年%s月　%sの案件別売上情報' % (ym[:4], ym[4:], client.__unicode__()),
        'client': client,
        'turnover_details': turnover_details,
        'ym': ym,
        'summary': summary,
    })
    template = loader.get_template('turnover_projects_monthly.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/eb/login/')
def release_list_current(request):
    now = datetime.date.today()
    return release_list(request, now.strftime('%Y%m'))


@login_required(login_url='/eb/login/')
def release_list(request, ym):
    company = biz.get_company()
    param_list = common.get_request_params(request.GET)
    year = int(ym[0:4])
    month = int(ym[-2:])
    start_date = datetime.datetime(year, month, 1)
    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['member__first_name', 'member__subcontractor__name', 'member__section__name',
                                              'project__name', 'start_date', 'member__salesperson'])
    order_list = common.get_ordering_list(o)

    all_project_members = biz.get_release_members_by_month(start_date, param_list)
    if order_list:
        all_project_members = all_project_members.order_by(*order_list)

    sections = Section.objects.public_filter(is_on_sales=True)
    salesperson = Salesperson.objects.public_all()

    params = "&".join(["%s=%s" % (key, value) for key, value in param_list.items()]) if param_list else ""
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
        'params': "&" + params if params else "",
        'dict_order': dict_order,
        'ym': ym,
        'sections': sections,
        'salesperson': salesperson,
    })
    template = loader.get_template('release_list.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/eb/login/')
def member_detail(request, employee_id):
    company = biz.get_company()
    member = Member.objects.get(employee_id=employee_id)
    member.set_coordinate()

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


@login_required(login_url='/eb/login/')
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


@login_required(login_url='/eb/login/')
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


@login_required(login_url='/eb/login/')
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


@login_required(login_url='/eb/login/')
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


@login_required(login_url='/eb/login/')
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


@login_required(login_url='/eb/login/')
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


@login_required(login_url='/eb/login/')
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


@login_required(login_url='/eb/login/')
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


@login_required(login_url='/eb/login/')
def download_client_order(request):
    p = request.GET.get('path', None)
    if p:
        path = os.path.join(settings.MEDIA_ROOT, p.strip('./'))
        if os.path.exists(path):
            filename = os.path.basename(path)
            response = HttpResponse(open(path, 'rb'), content_type="application/excel")
            response['Content-Disposition'] = "filename=" + urllib.quote(filename.encode("utf8"))
            return response


@login_required(login_url='/eb/login/')
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


@login_required(login_url='/eb/login/')
@permission_required('eb.generate_request', raise_exception=True)
def download_project_request(request, project_id):
    company = biz.get_company()
    project = get_object_or_404(Project, pk=project_id)
    try:
        client_order_id = request.GET.get("client_order_id", None)
        client_order = ClientOrder.objects.get(pk=client_order_id)
        ym = request.GET.get("ym", None)
        first_day = common.get_first_day_from_ym(ym)
        project_request = project.get_project_request(ym[:4], ym[4:], client_order)
        overwrite = request.GET.get("overwrite", None)
        if overwrite:
            path = os.path.join(settings.GENERATED_FILES_ROOT, "project_request", str(ym), project_request.filename)
            if not os.path.exists(path):
                # ファイルが存在しない場合、エラーとする。
                raise errors.FileNotExistException(constants.ERROR_REQUEST_FILE_NOT_EXISTS)
            filename = project_request.filename
        else:
            if common.add_months(first_day, 1) < common.get_first_day_current_month() and project_request.filename:
                # ２ヶ月前の請求書は生成できないようにする。
                raise errors.CustomException(constants.ERROR_CANNOT_GENERATE_2MONTH_BEFORE)
            request_name = request.GET.get("request_name", None)
            bank_id = request.GET.get('bank', None)
            try:
                bank = BankInfo.objects.get(pk=bank_id)
            except ObjectDoesNotExist:
                bank = None
            project_request.request_name = request_name if request_name else project.name
            data = biz.generate_request_data(company, project, client_order, bank, ym, project_request)
            path = file_gen.generate_request(company, project, data, project_request.request_no, ym)
            filename = os.path.basename(path)
            project_request.filename = filename
            project_request.created_user = request.user if not project_request.pk else project_request.created_user
            project_request.updated_user = request.user
            # 請求履歴を保存する。
            action_flag = CHANGE if project_request.pk else ADDITION
            project_request.save(data=data)
            LogEntry.objects.log_action(request.user.id,
                                        ContentType.objects.get_for_model(project_request).pk,
                                        project_request.pk,
                                        unicode(project_request),
                                        action_flag,
                                        '' if action_flag == ADDITION else u'再作成しました。')

        response = HttpResponse(open(path, 'rb'), content_type="application/excel")
        response['Content-Disposition'] = "filename=" + urllib.quote(filename.encode('UTF-8'))
        return response
    except errors.MyBaseException, ex:
        return HttpResponse(u"<script>alert('%s');window.close();</script>" % (ex.message,))


@login_required(login_url='/eb/login/')
def download_resume(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    date = datetime.date.today().strftime("%Y%m")
    filename = constants.NAME_RESUME % (member.first_name + member.last_name, date)
    output = file_gen.generate_resume(member)
    response = HttpResponse(output.read(), content_type="application/ms-excel")
    response['Content-Disposition'] = "filename=" + urllib.quote(filename.encode('utf-8')) + ".xlsx"
    return response


@login_required(login_url='/eb/login/')
def download_section_attendance(request, section_id, year, month):
    section = get_object_or_404(Section, pk=section_id)
    batch = biz.get_batch_manage(constants.BATCH_SEND_ATTENDANCE_FORMAT)
    project_members = biz.get_project_members_month_section(section, datetime.date(int(year), int(month), 20))
    filename = constants.NAME_SECTION_ATTENDANCE % (section.name, int(year), int(month))
    output = file_gen.generate_attendance_format(batch.attachment1.path, project_members, datetime.date(int(year), int(month), 20))
    response = HttpResponse(output, content_type="application/ms-excel")
    response['Content-Disposition'] = "filename=" + urllib.quote(filename.encode('utf-8'))
    return response


@login_required(login_url='/eb/login/')
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


@login_required(login_url='/eb/login/')
def issues(request):

    issue_list = Issue.objects.all()

    context = RequestContext(request, {
        'title': u'課題管理票一覧',
        'issues': issue_list,
    })
    template = loader.get_template('issue_list.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/eb/login/')
def issue_detail(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    context = RequestContext(request, {
        'title': u'課題管理票 - %s' % (issue.title,),
        'issue': issue,
    })
    template = loader.get_template('issue.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/eb/login/')
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


@login_required(login_url='/eb/login/')
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


@login_required(login_url='/eb/login/')
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
        message_list = biz_batch.sync_members()
        context.update({
            'messages': [u"完了しました。"],
            'message_list': message_list,
            'show_result': True,
        })

    r = render_to_response('sync_members.html', context)
    return HttpResponse(r)


@login_required(login_url='/eb/login/')
def batch_list(request):
    context = {
        'title': u'バッチ一覧',
        'site_header': admin.site.site_header,
        'site_title': admin.site.site_title,
    }
    context.update(csrf(request))
    batches = BatchManage.objects.public_all()
    context.update({
        'batches': batches,
    })
    if request.method == 'GET':
        pass
    else:
        batch_name = request.POST.get('batch_name', None)
        call_command(batch_name)

    r = render_to_response('batch_list.html', context)
    return HttpResponse(r)


@login_required(login_url='/eb/login/')
def batch_log(request, name):
    log_file = os.path.join(settings.BASE_DIR, 'log/batch', name + '.log')
    if os.path.exists(log_file):
        f = open(log_file, 'r')
        log = u"<pre>" + f.read().decode('utf-8') + u"</pre>"
        f.close()
    else:
        log = u"ログファイル「%s」が存在しません。" % (log_file,)
    return HttpResponse(log)


@login_required(login_url='/eb/login/')
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


def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('index')

    return render_to_response('login.html', context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    return redirect('index')
