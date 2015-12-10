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
import urllib2

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
from .models import Company, Member, Section, Project, ProjectMember, Salesperson, \
    MemberAttendance, Subcontractor, BankInfo
from . import forms


PAGE_SIZE = 50


def get_company():
    company_list = Company.objects.all()
    if company_list.count() == 0:
        return None
    else:
        return company_list[0]


@login_required(login_url='/admin/login/')
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


@login_required(login_url='/admin/login/')
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
    company = get_company()
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
            'salesperson': Salesperson.objects.public_all(),
            'params': params,
            'dict_order': dict_order,
        })
        template = loader.get_template('project_list.html')
        return HttpResponse(template.render(context))


def project_order_list(request):
    company = get_company()
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

    all_projects = Project.objects.public_filter(status=4)

    if order_list:
        all_projects = all_projects.order_by(*order_list)

    if name:
        all_projects = all_projects.filter(name__contains=name)
        params += "&name=%s" % (name,)
    if client:
        all_projects = [project for project in all_projects if client in project.client.name]
        params += "&client=%s" % (client,)

    all_project_orders = []
    for project in all_projects:
        client_order = project.get_order_by_month(ym[:4], ym[4:])
        all_project_orders.append((project, client_order))

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
        'month_list': common.get_month_list(-1, 1),
        'current_year': str(datetime.date.today().year),
        'current_month': str("%02d" % (datetime.date.today().month,)),
    })
    template = loader.get_template('project_order_list.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/admin/login/')
def project_detail(request, project_id):
    company = get_company()
    project = Project.objects.get(pk=project_id)
    download = request.GET.get("download", None)

    if download == constants.DOWNLOAD_REQUEST:
        try:
            request_name = request.GET.get("request_name", None)
            order_no = request.GET.get("order_no", None)
            ym = request.GET.get("ym", None)
            bank_id = request.GET.get('bank', None)
            now = datetime.datetime.now()
            try:
                bank = BankInfo.objects.get(pk=bank_id)
            except ObjectDoesNotExist:
                bank = None
            path, request_no = file_gen.generate_request(project, company, request_name, order_no, ym, bank)
            filename = "EB請求書_%s_%s.xls" % (str(request_no), now.strftime("%Y%m%d%H%M%S"))
            response = HttpResponse(open(path, 'rb'), content_type="application/excel")
            response['Content-Disposition'] = "filename=" + urllib.quote(filename)
            # 一時ファイルを削除する。
            common.delete_temp_files(os.path.dirname(path))
            return response
        except errors.FileNotExistException, ex:
            return HttpResponse(u"<script>alert('%s');window.close();</script>" % (ex.message,))
    elif download == constants.DOWNLOAD_QUOTATION:
        try:
            pass
        except errors.FileNotExistException, ex:
            pass
    else:
        context = RequestContext(request, {
            'company': company,
            'title': u'%s - 案件詳細' % (project.name,),
            'project': project,
            'banks': BankInfo.objects.public_all(),
            'order_month_list': project.get_year_month_order_finished(),
            'attendance_month_list': project.get_year_month_attendance_finished(),
        })
        template = loader.get_template('project_detail.html')
        return HttpResponse(template.render(context))


@login_required(login_url='/admin/login/')
def project_attendance_list(request, project_id):
    company = get_company()
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
            try:
                project_members = project.get_project_members_by_month(date)
                dict_initials = []
                for project_member in project_members:
                    attendance = project_member.get_attendance(date.year, date.month)
                    if attendance:
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
                        d = {'project_member': project_member,
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
                formset = AttendanceFormSet(queryset=MemberAttendance.objects.none(), initial=dict_initials)
            except Exception as e:
                print e.message

            context.update({'formset': formset})

            r = render_to_response('project_attendance_list.html', context)
            return HttpResponse(r)
        else:
            AttendanceFormSet = modelformset_factory(MemberAttendance, form=forms.MemberAttendanceForm, extra=0)
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
    company = get_company()
    status = request.GET.get('status', None)
    project = Project.objects.get(pk=project_id)
    params = ""
    o = request.GET.get('o', None)
    dict_order = common.get_ordering_dict(o, ['member__first_name',
                                              'member__section', 'start_date', 'end_date', 'price'])
    order_list = common.get_ordering_list(o)

    all_project_members = project.projectmember_set.public_all()
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
            all_project_members = ProjectMember.objects.public_filter(end_date__gte=start_date,
                                                                      end_date__lt=end_date).order_by('end_date')
        elif common.is_salesperson_director(request.user) and request.user.salesperson.section:
            # 営業部長の場合、部門内すべての社員が見られる
            salesperson_list = request.user.salesperson.section.salesperson_set.public_all()
            all_project_members = ProjectMember.objects.public_filter(end_date__gte=start_date,
                                                                      end_date__lt=end_date,
                                                                      member__salesperson__in=salesperson_list).\
                order_by('end_date')
        elif common.is_salesperson(request.user):
            # 営業員の場合、担当している社員だけ見られる
            all_project_members = ProjectMember.objects.public_filter(end_date__gte=start_date,
                                                                      end_date__lt=end_date,
                                                                      member__salesperson=request.user.salesperson).\
                order_by('end_date')
        else:
            all_project_members = ProjectMember.objects.public_filter(pk=-1)
    else:
        all_project_members = ProjectMember.objects.public_filter(end_date__gte=start_date,
                                                                  end_date__lt=end_date).order_by('end_date')
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
    company = get_company()
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
    company = get_company()
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


@login_required(login_url='/admin/login/')
def recommended_project_list(request, employee_id):
    company = get_company()
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
def map_position(request):
    company = get_company()
    members = Member.objects.public_filter(lat__isnull=False, lng__isnull=False).exclude(lat__exact='', lng__exact='')
    context = RequestContext(request, {
        'company': company,
        'title': u'地図情報',
        'members': members,
    })
    template = loader.get_template('map_position.html')
    return HttpResponse(template.render(context))


@login_required(login_url='/admin/login/')
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


@login_required(login_url='/admin/login/')
def sync_coordinate(request):
    company = get_company()

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
def sync_db(request):
    context = {
        'title': u'社員管理DBのデータを同期する。',
        'site_header': admin.site.site_header,
        'site_title': admin.site.site_title,
    }
    context.update(csrf(request))
    if request.method == 'GET':
        pass
    else:
        url = request.POST.get("url", None)
        if not url:
            pass
        else:
            response = urllib2.urlopen(url)
            html = response.read()
            dict_data = json.loads(html.replace("\r", "").replace("\n", ""))
            message_list = []
            if 'employeeList' in dict_data:
                company = get_company()
                for data in dict_data.get("employeeList"):
                    employee_code = data.get("id", None)
                    name = data.get("name", None)
                    birthday = data.get("birthDate", None)
                    address = data.get("address", None)
                    department_name = data.get("department", None)
                    eb_mail = data.get("ebMailAddress", None)
                    introduction = data.get("introduction", None)
                    join_date = data.get("joinDate", None)
                    name_jp = data.get("kana", None)
                    private_mail = data.get("mailAddress", None)
                    phone = data.get("phone", None)
                    postcode = data.get("postcode", None)
                    sex = data.get("sex", None)
                    station = data.get("station", None)
                    if employee_code:
                        if department_name == u"営業部" or employee_code in ('0126', '0198', '0150'):
                            # 0150 孫雲釵
                            # 0198 劉 暢
                            # 0126 丁 玲
                            if Salesperson.objects.filter(employee_id=employee_code).count() == 0:
                                member = Salesperson(employee_id=employee_code)
                            else:
                                # message_list.append(("WARN", name, birthday, address, u"既に存在しているレコードです。"))
                                continue
                        else:
                            if Member.objects.filter(employee_id=employee_code).count() == 0:
                                member = Member(employee_id=employee_code)
                            else:
                                # message_list.append(("WARN", name, birthday, address, u"既に存在しているレコードです。"))
                                continue

                        try:
                            # コストを取得する。
                            member.first_name = common.get_first_last_name(name)[0]
                            member.last_name = common.get_first_last_name(name)[1]
                            if name_jp:
                                lst = common.get_first_last_ja_name(name_jp)
                                if len(lst) == 2 and lst[0]:
                                    member.first_name_ja = common.get_first_last_ja_name(name_jp)[0]
                                    member.last_name_ja = common.get_first_last_ja_name(name_jp)[1]
                                elif len(lst) == 1:
                                    member.first_name_ja = common.get_first_last_ja_name(name_jp)[0]
                            if birthday:
                                try:
                                    member.birthday = common.parse_date_from_string(birthday)
                                except:
                                    member.birthday = None
                            else:
                                member.birthday = datetime.date.today()
                            member.address1 = address
                            if department_name:
                                try:
                                    section = Section.objects.get(name=department_name)
                                except ObjectDoesNotExist:
                                    section = Section(name=department_name)
                                    section.company = get_company()
                                    section.save()
                                member.section = section
                            member.email = eb_mail
                            member.private_email = private_mail
                            member.comment = introduction
                            if join_date:
                                member.join_date = common.parse_date_from_string(join_date)
                            if phone:
                                member.phone = phone.replace("-", "")
                            if postcode:
                                member.post_code = postcode.strip().replace("/", "").replace("-", "").strip()
                                if len(member.post_code.strip()) == 8:
                                    member.post_code = member.post_code[3:] + member.post_code[4:]
                                if len(member.post_code) != 7:
                                    member.post_code = None
                            member.nearest_station = station
                            member.sex = "2" if sex == "0" else "1"
                            member.cost = get_cost(employee_code)
                            member.company = company
                            member.save()
                            message_list.append(("INFO", name, birthday, address, u"完了"))
                        except Exception as e:
                            message_list.append(("ERROR", name, birthday, address, u"エラー：" + e.message))
                context.update({
                    'messages': [u"完了しました。"],
                    'message_list': message_list,
                    'show_result': True,
                })
            else:
                pass

    r = render_to_response('syncdb.html', context)
    return HttpResponse(r)


def is_retired(code):
    if code:
        url = "http://service.e-business.co.jp:8080/ContractManagement/api/newContract?uid=%s" % (code,)
        response = urllib2.urlopen(url)
        html = response.read()
        data = json.loads(html.replace("\r", "").replace("\n", ""))
        period_list = []
        for item in data['contractList']:
            period_list.append(item['EMPLOYMENT_PERIOD_END'])
        if period_list:
            latest_period = max(period_list)
            period_end = common.parse_date_from_string(latest_period, split1=u"-", split2=u"-")
            if period_end and period_end < datetime.date.today():
                return True
    return False


def get_cost(code):
    if code:
        url = "http://service.e-business.co.jp:8080/ContractManagement/api/newContract?uid=%s" % (code,)
        response = urllib2.urlopen(url)
        html = response.read()
        data = json.loads(html.replace("\r", "").replace("\n", ""))
        period_list = []
        for item in data['contractList']:
            period_list.append(item['EMPLOYMENT_PERIOD_END'])
        latest_period = None
        if period_list:
            latest_period = max(period_list)
        for item in data['contractList']:
            if latest_period and item['EMPLOYER_NO'] == code and item['EMPLOYMENT_PERIOD_END'] == latest_period:
                if item['ALLOWANLE_COST'] != "-":
                    return item['ALLOWANLE_COST']
        for item in data['contractList']:
            if item['EMPLOYER_NO'] == code:
                return item['ALLOWANLE_COST'] if item['ALLOWANLE_COST'] != "-" else 0
    return 0


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
