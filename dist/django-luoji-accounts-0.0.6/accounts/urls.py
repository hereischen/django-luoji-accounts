# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .api import transfer_detail


urlpatterns = patterns(
    'accounts.views',
    url(r'^api/transfer_detail/(?P<user_id>\d+)/', transfer_detail),
)
