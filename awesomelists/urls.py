from django.conf.urls import patterns, include, url
from django.http import HttpResponse

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

HOME_PAGE = '''
<html>
    <head><title>To-Do App</title></head>
</html>'''

def get_home_page(request):
    return HttpResponse(HOME_PAGE)

urlpatterns = patterns('',
    # Examples:
    url(r'^$', get_home_page),
    # url(r'^awesomelists/', include('awesomelists.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
