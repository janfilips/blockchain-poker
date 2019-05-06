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
        init:function(){
            if(this.inited === false){
                this.inited = true;
                setInterval(app._load_megaloolah, 3000);
            }
        },
        _load_megaloolah: () => {
            $('header.main-head .mega>span:nth(1)').text('$' + formatMoney(Math.random() * 1000000 + 10));
            $('header.main-head .major>span:nth(1)').text('$' + formatMoney(Math.random() * 100000 + 10));
            $('header.main-head .minor>span:nth(1)').text('$' + formatMoney(Math.random() * 50000 + 10));
            $('header.main-head .mini>span:nth(1)').text('$' + formatMoney(Math.random() * 10000 + 10));

            // $.ajax({
            //     type: "POST",
            //     url: '/ajax/get/megaloolah/',
            //     headers: {
            //         'X-CSRFToken': csrf_token
            //     },
            //     data: {
            //       player_session_key: session_key,
            //     },
            //     success: (r) => {
            //       console.log(r);
            //       $('header.main-head .mega>span:nth(1)').text('$' + formatMoney(r.mega)));
            //       $('header.main-head .major>span:nth(1)').text('$' + formatMoney(r.major));
            //       $('header.main-head .minor>span:nth(1)').text('$' + formatMoney(r.minor));
            //       $('header.main-head .mini>span:nth(1)').text('$' + formatMoney(r.mini));
            //     },
            //     error:  () => {
            //       console.log("megaloolah error!!!");
            //     }
            // });
        },
        first_draw:() => {
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
                  console.log(r);
                  // $('header.main-head .mega>span:nth(1)').text('$' + formatMoney(r.mega)));
                  // $('header.main-head .major>span:nth(1)').text('$' + formatMoney(r.major));
                  // $('header.main-head .minor>span:nth(1)').text('$' + formatMoney(r.minor));
                  // $('header.main-head .mini>span:nth(1)').text('$' + formatMoney(r.mini));
                }
            });
        },
        held_all: () => {
            $('.card-wrap').removeClass('held');
        },
        bet_max: () => {
            if(user_credit >= 10){
                $('.points.point-5').click();
            } else if(user_credit >= 5){
                $('.points.point-4').click();
            } else if(user_credit >= 3){
                $('.points.point-3').click();
            } else if(user_credit >= 2){
                $('.points.point-2').click();
            } else{
                $('.points.point-1').click();
            }
        }
    }
}();
