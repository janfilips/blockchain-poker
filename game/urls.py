import os
from django.conf.urls import url

from django.contrib import admin
from django.urls import path

from game.views import home, about, tos, credit
from game.views import reveal_deck

from game.views import ajax_bet

from game.views import tmp_about_desired_look

urlpatterns = [
    # common views
    url(r'^$', home, name='home'),
    url(r'^about$', about, name='about'),
    url(r'^tmp/about/desired/look$', tmp_about_desired_look, name='tmp_about_desired_look'),
    url(r'^deck/(?P<deck_hash>[\w\-\.]+)/$', reveal_deck, name='reveal_deck'),
    url(r'^tos$', tos, name='tos'),
    url(r'^credit$', credit, name='credit'),
    # ajax
    url(r'^ajax/bet_amount/$', ajax_bet, name='ajax_bet'),
]
