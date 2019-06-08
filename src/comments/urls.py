#from django.conf.urls import url
from django.urls import re_path, path
from django.contrib import admin

from .views import (
	comment_thread,
	)

app_name = 'comments'

urlpatterns = [
    re_path(r'^(?P<id>\d+)/$', comment_thread, name='comment_thread'),
    #re_path(r'^(?P<id>\w+)/delete/$', comment_delete),
]
