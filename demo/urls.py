from django.conf.urls import url
from demo.views import *

urlpatterns= [
    url(r'upload_stats/$', upload_stats, name="upload_stats"),
    url(r'sync/$', sync, name="sync"),
    url(r'say_yes/$', say_yes, name="say_yes"),
    url(r'statistics/$', statistcs, name="statistics"),
    url(r'test_share/(?P<email>\w*)/$', test_mail, name="test_mail"),
    url(r'test_mail/$', test_mail, name="test_mail"),
]