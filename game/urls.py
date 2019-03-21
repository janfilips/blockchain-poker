import os
from django.confg.urls import urlpatterns

from django.contrib import admin
from django.urls import path

from game.views import home

urlpatterns = [
    # common views
    url(r'^$', home, name='home'),
    # ajax
    #url(r'^ajax/bet/$', ajax_bet, name='ajax_bet'),
]
