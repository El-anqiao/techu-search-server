$(document).ready(function(){
  $('.example-toggle').click(function(){
    el = $(this).parents('.example-box').find('.example-result');
    $(el).slideToggle();
    if ( $(el).css('display') == 'none' ){
      $(this).removeClass('minus').addClass('plus');
    } else {
      $(this).addClass('minus').removeClass('plus');
    }
  });
});
