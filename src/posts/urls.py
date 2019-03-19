#from django.conf.urls import url
from django.urls import re_path, path
from django.contrib import admin

from .views import (
	post_list,
	post_create,
	post_detail,
	post_update,
	post_delete,
	PostDetailView
	)

app_name = 'posts'

urlpatterns = [
	path('', post_list, name='list'),
    path('create/', post_create),
    #re_url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    re_path(r'^(?P<slug>[\w-]+)/$', PostDetailView.as_view(), name='detail'), #Django Code Review #3 on joincfe.com/youtube/
    re_path(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    re_path(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
    #path('posts/', "<appname>.views.<function_name>"),
]
