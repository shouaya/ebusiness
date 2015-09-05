from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'employee.views.home', name='home'),
    url(r'^eb/', include('eb.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
