import os
from django.conf.urls import url

from django.contrib import admin
from django.urls import path

from game.views import home, about, reveal_deck

urlpatterns = [
    # common views
    url(r'^$', home, name='home'),
    url(r'^about$', about, name='about'),
    url(r'^deck/(?P<deck_hash>[\w\-\.]+)/$', reveal_deck, name='reveal_deck'),
    # ajax
    #url(r'^ajax/bet$', ajax_bet, name='ajax_bet'),
]
