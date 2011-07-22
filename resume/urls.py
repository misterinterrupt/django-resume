# Resume App URLs file
from django.conf.urls.defaults import *

urlpatterns = patterns('resume.views',
    url(r'^$', 'index', name='resume_home'),
)
