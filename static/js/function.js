$( document ).ready(function() {

    $('.card-wrap').click(function() {
      $(this).toggleClass('held');
    });

    $('.type-list .points').click(function() {
      $('.type-list .points').removeClass('active');
      $(this).toggleClass('active');
    });

    var rowselector = 5;
    $('.type-list .points span:nth-child(' + rowselector + ')').addClass( "activeLine" );
    $('.type-list .combination span:nth-child(' + rowselector + ')').addClass( "activeLine" );

});
