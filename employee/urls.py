from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.i18n import javascript_catalog
from eboa.admin import eboa_admin_site
from del_data.admin import del_data_admin_site
from contract.admin import contract_admin_site
from employee import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^eb/', include('eb.urls')),
    url(r'^flow/', include('flow.urls')),
    url(r'^contract/', include('contract.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^jsi18n/$', javascript_catalog, {'packages': 'django.conf'}),
    url(r'push.js', views.get_push_js),
    url(r'notification_data', views.notification_data),
    url(r'update_subscription', views.UpdateSubscription.as_view(), name='update_subscription'),

    url(r'^eboa-admin/', include(eboa_admin_site.urls)),
    url(r'^del-data-admin/', include(del_data_admin_site.urls)),
    url(r'^contract-admin/', include(contract_admin_site.urls)),
]

handler403 = 'eb.views.handler403'
handler404 = 'eb.views.handler404'
