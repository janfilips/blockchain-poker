import os
from django.conf.urls import url

from django.contrib import admin
from django.urls import path

from game.views import home, about

urlpatterns = [
    # common views
    url(r'^$', home, name='home'),
    url(r'^about$', about, name='about'),
    # ajax
    #url(r'^ajax/bet$', ajax_bet, name='ajax_bet'),
]
