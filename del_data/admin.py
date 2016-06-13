# coding: UTF-8

from django.contrib import admin
from . import models
# Register your models here.


def get_full_name(obj):
    return "%s %s" % (obj.first_name, obj.last_name)
get_full_name.short_description = u"名前"
get_full_name.admin_order_field = "first_name"


def is_user_created(obj):
    return obj.user is not None
is_user_created.short_description = u"ユーザ作成"
is_user_created.admin_order_field = "user"
is_user_created.boolean = True


class BaseAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        return super(BaseAdmin,self).get_queryset(request).filter(is_deleted=True)

    def has_add_permission(self, request):
        return False


class MemberAdmin(BaseAdmin):
    list_display = ['employee_id', get_full_name, 'section', 'subcontractor', 'salesperson',
                    is_user_created, 'is_retired', 'is_deleted']


class SalespersonAdmin(BaseAdmin):
    list_display = ['employee_id', get_full_name, 'email', 'section', 'member_type',
                    is_user_created, 'is_retired', 'is_deleted']


class SectionAdmin(BaseAdmin):
    list_display = ['name', 'is_on_sales', 'is_deleted']


admin.site.register(models.EbMember, MemberAdmin)
admin.site.register(models.EbSalesperson, SalespersonAdmin)
admin.site.register(models.EbSection, SectionAdmin)
