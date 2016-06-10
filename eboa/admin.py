# coding: UTF-8
from django.contrib import admin, messages

# Register your models here.
from . import models, forms


class EboaAdmin(admin.ModelAdmin):
    using = 'bpm_eboa'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        # obj.save(using=self.using)
        pass

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(EboaAdmin, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(EboaAdmin, self).formfield_for_foreignkey(db_field, request=request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(EboaAdmin, self).formfield_for_manytomany(db_field, request=request, using=self.using, **kwargs)

    def get_actions(self, request):
        actions = super(EboaAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class SysUserAdmin(EboaAdmin):
    form = forms.MemberForm
    list_display = ['fullname', 'email']
    search_fields = ['fullname']


admin.site.register(models.SysUser, SysUserAdmin)
