import os
from django.conf.urls import url

from django.contrib import admin
from django.urls import path

from game.views import home, about, tos, credit
from game.views import reveal_deck

from game.views import ajax_bet, ajax_draw_cards, ajax_autoplay, ajax_deal_cards, ajax_jackpot_stats

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
    url(r'^ajax/deal/cards/$', ajax_deal_cards, name='ajax_deal_cards'),
    url(r'^ajax/change/bet/$', ajax_bet, name='ajax_bet'),
    url(r'^ajax/draw/cards/$', ajax_draw_cards, name='ajax_draw_cards'),
    url(r'^ajax/autoplay/$', ajax_autoplay, name='autoplay'),
    url(r'^ajax/jackpot/stats/$', ajax_jackpot_stats, name='ajax_jackpot_stats'),
]
