import os
from django.conf.urls import url

from django.contrib import admin
from django.urls import path

from game.views import home, about, tos, credit
from game.views import reveal_deck

urlpatterns = [
    # common views
    url(r'^$', home, name='home'),
    url(r'^about$', about, name='about'),
    url(r'^deck/(?P<deck_hash>[\w\-\.]+)/$', reveal_deck, name='reveal_deck'),
    url(r'^tos$', tos, name='tos'),
    url(r'^credit$', credit, name='credit'),
    # ajax
    #url(r'^ajax/bet$', ajax_bet, name='ajax_bet'),
]
