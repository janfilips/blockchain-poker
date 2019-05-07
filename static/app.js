$(document).ready(() => {
    app.init();
});

function formatMoney(n, c, d, t) {
    var c = isNaN(c = Math.abs(c)) ? 2 : c,
        d = d == undefined ? "." : d,
        t = t == undefined ? "," : t,
        s = n < 0 ? "-" : "",
        i = String(parseInt(n = Math.abs(Number(n) || 0).toFixed(c))),
        j = (j = i.length) > 3 ? j % 3 : 0;

    return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
};

var app = function() {
    return {
        inited: false,
        init: function() {
            if (this.inited === false) {
                this.inited = true;
                this._load_megaloolah();
                setInterval(app._load_megaloolah, 30000);
                if($.cookie('game_already_played')){
                    this.first_draw();
                }
            }
        },
        evaluated_hand_text: (a) => {
            var o = '';
            if (a == "One-pair.")
                o = 'One pair';
            if (a == "Royal-flush.")
                o = 'Royal flush';
            if (a == "Straight-flush.")
                o = 'Straight flush';
            if (a == "Four-of-a-kind.")
                o = 'Four of a kind';
            if (a == "Full-house.")
                o = 'Full house';
            if (a == "Flush.")
                o = 'Flush';
            if (a == "Straight.")
                o = 'Straight';
            if (a == "Three-of-a-kind.")
                o = 'Three of a kind';
            if (a == "Two-pair.")
                o = 'Two pairs';
            if (a == "Jacks-or-better.")
                o = 'Jacks or better';

            return o;
        },
        row_selector: (a) => {
            var o = 0;
            if (a == "Nothing.")
                o = 0;
            if (a == "One-pair.")
                o = 0;
            if (a == "Royal-flush.")
                o = 1;
            if (a == "Straight-flush.")
                o = 2;
            if (a == "Four-of-a-kind.")
                o = 3;
            if (a == "Full-house.")
                o = 4;
            if (a == "Flush.")
                o = 5;
            if (a == "Straight.")
                o = 6;
            if (a == "Three-of-a-kind.")
                o = 7;
            if (a == "Two-pair.")
                o = 8;
            if (a == "Jacks-or-better.")
                o = 9;

            return o;
        },
        _load_megaloolah: () => {
            $.ajax({
                type: "POST",
                url: '/ajax/jackpot/stats/',
                headers: {
                    'X-CSRFToken': csrf_token
                },
                data: {
                    player_session_key: session_key
                },
                success: (r) => {
                    $('header.main-head .mega>span:nth(1)').text('$' + formatMoney(r.super));
                    $('header.main-head .major>span:nth(1)').text('$' + formatMoney(r.mega));
                    $('header.main-head .minor>span:nth(1)').text('$' + formatMoney(r.major));
                    $('header.main-head .mini>span:nth(1)').text('$' + formatMoney(r.minor));
                }
            });
        },
        first_draw: () => {
            $('a.draw-first-action').replaceWith('<a class="btn-action deal-action" href="#">Draw</a><a class="btn-action draw-action" href="#">Deal</a>');
            let b = parseInt($('.points.active').attr('data-base'));
            if(b > user_credit){
                app.bet_max(app._ajax_deal_cards);
            }
            else{
                app._ajax_deal_cards();
            }

        },
        _ajax_deal_cards: () => {
            // odpocitame virtualne kredit
            var b = parseInt($('.points.active').attr('data-base'));
            $('.credit').html('Credit $' + (user_credit - b));

            $.ajax({
                type: "POST",
                url: '/ajax/deal/cards/',
                headers: {
                    'X-CSRFToken': csrf_token
                },
                data: {
                    player_session_key: session_key,
                },
                success: (r) => {
                    var o = JSON.parse(r);
                    var html = '<section class="cards">';
                    $.each(o.hand, (i, e) => {
                        html += '<div class="card-wrap ' + (o.sugested_hand.includes(e) ? 'preselect' : '') + '">\n\
                          <div class="indicator">Held</div>\n\
                          <div class="flip-card-inner">\n\
                            <div class="flip-card-front"><img src="static/cards/card-back.png" /></div>\n\
                            <div class="flip-card-back">\n\
                              <img src="static/cards/' + e + '.png" />\n\
                            </div></div></div>';
                    });
                    html += '</section>';
                    $('div.cards-back.show-backs').replaceWith(html);
                    $('.card-wrap').each(function(i) {
                        var cardflip = $(this);
                        setTimeout(function() {
                            cardflip.toggleClass('flipit', !cardflip.hasClass('flipit'));
                        }, 200 * i);
                    });
                    if (autoplay == true ) {
                        setTimeout(function() {
                            $('.preselect').addClass('held');
                        }, 1800);
                    }

                    $('.stats-line .bet-amaunt').remove();
                    $('.stats-line .win').after('<div class="bet-amaunt">' + app.evaluated_hand_text(o.evaluated_hand) + '</div>');

                    $('.type-list .points span:nth-child(' + app.row_selector(o.evaluated_hand) + ')').addClass("activeLine");
                    $('.type-list .combination span:nth-child(' + app.row_selector(o.evaluated_hand) + ')').addClass("activeLine");
                }
            });
        },
        held_all: () => {
            $('.card-wrap').removeClass('held');
        },
        bet_max: (c) => {
            if (user_credit >= 10) {
                app.change_bet(10, c);
            } else if (user_credit >= 5) {
                app.change_bet(5, c);
            } else if (user_credit >= 3) {
                app.change_bet(3, c);
            } else if (user_credit >= 2) {
                app.change_bet(2, c);
            } else {
                app.change_bet(1, c);
            }
        },
        change_bet: (a, c) => {
            var can_change = false;
            if($('.show-backs').length == 1 || $('.game-done').length == 1){
                can_change = true;
            }
            if(can_change){
                b = a;
                if(a == 5){
                    b = 4;
                } else if(a == 10){
                    b = 5;
                }
                $('.type-list .points').removeClass('active');
                $('.points.point-' + b).addClass('active');
                $('.stats-line .win').text('BET $' + a);
                $('.coin.btn-action>span').text('$' + a);

                $.ajax({
                    type: "POST",
                    url: '/ajax/change/bet/',
                    headers: {
                        'X-CSRFToken': csrf_token
                    },
                    data: {
                        player_session_key: session_key,
                        bet_amount: a
                    },
                    success: function(){
                        "function" == typeof c && c();
                    }
                });
            }
            else{
                console.log('change bet is not allowed');
            }
        }
    }
}();