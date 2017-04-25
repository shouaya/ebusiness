from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, get_object_or_404

from . import models
from utils import constants

# Create your views here.


@method_decorator(login_required(login_url=constants.LOGIN_IN_URL), name='dispatch')
class BaseView(View, ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        context.update({
            'workfows': models.Workflow.objects.all()
        })
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        pass


class BaseTemplateView(TemplateResponseMixin, BaseView):
    pass


class IndexView(BaseTemplateView):
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)


class NewWorkflowView(BaseTemplateView):
    template_name = 'new_workflow.html'

    def get(self, request, *args, **kwargs):
        workflow_id = kwargs.get('workflow_id', 0)
        workflow = get_object_or_404(models.Workflow, pk=workflow_id)
        context = self.get_context_data()
        context.update({
            'workflow': workflow,
        })
        return self.render_to_response(context)
