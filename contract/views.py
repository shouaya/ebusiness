from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from . import biz, models, forms
from eb import biz_config
from eb import models as sales_models
from utils import constants
import operator

# Create your views here.


@method_decorator(login_required(login_url=constants.LOGIN_IN_URL), name='dispatch')
class BaseView(View, ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        kwargs.update({
            'request': request
        })
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        pass


class BaseTemplateView(TemplateResponseMixin, BaseView):
    pass


class IndexView(BaseTemplateView):
    template_name = 'members.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        request = kwargs.get('request')
        q = request.GET.get('q', None)

        all_members = biz.get_members()
        if q:
            orm_lookups = ['first_name__icontains', 'last_name__icontains', 'id_from_api']
            for bit in q.split():
                or_queries = [Q(**{orm_lookup: bit}) for orm_lookup in orm_lookups]
                all_members = all_members.filter(reduce(operator.or_, or_queries))

        paginator = Paginator(all_members, biz_config.get_page_size())
        page = request.GET.get('page')
        try:
            members = paginator.page(page)
        except PageNotAnInteger:
            members = paginator.page(1)
        except EmptyPage:
            members = paginator.page(paginator.num_pages)
        context.update({
            'members': members,
            'paginator': paginator,
        })
        return context


class ContractView(BaseTemplateView):
    template_name = 'contract.html'

    def get_context_data(self, **kwargs):
        context = super(ContractView, self).get_context_data(**kwargs)
        request = kwargs.get('request')
        api_id = kwargs.get('api_id')
        member = get_object_or_404(sales_models.Member, id_from_api=api_id)
        contract_set = biz.get_latest_contract(member)

        ver = request.GET.get('ver', None)
        if ver:
            contract = contract_set.get(contract_no=ver)
        elif contract_set.count() > 0:
            contract = contract_set[0]
        else:
            contract = models.Contract(member=member)
        form = forms.ContractForm(instance=contract)
        context.update({
            'member': member,
            'contract_set': contract_set,
            'contract': contract,
            'form': form,
        })
        return context

    def get(self, request, *args, **kwargs):
        kwargs.update({
            'request': request
        })
        context = self.get_context_data(**kwargs)
        contract = context.get('contract')
        form = forms.ContractForm(instance=contract)
        context.update({
            'form': form,
        })
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        kwargs.update({
            'request': request
        })
        context = self.get_context_data(**kwargs)
        # contract = context.get('contract')
        form = forms.ContractForm(request.POST)
        context.update({
            'form': form,
        })
        if form.is_valid():
            pass

        return self.render_to_response(context)
