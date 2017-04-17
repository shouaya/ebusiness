# coding: UTF-8
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from . import models
# Register your models here.


class BaseAdmin(admin.ModelAdmin):
    pass


class NodeInline(admin.TabularInline):
    model = models.Node
    extra = 1


class WorkflowAdmin(BaseAdmin):
    list_display = ('name',)
    inlines = (NodeInline,)

    def get_form(self, request, obj=None, **kwargs):
        form = super(WorkflowAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['content_type'].queryset = ContentType.objects.filter(app_label='eb')
        return form


admin.site.register(models.Workflow, WorkflowAdmin)
