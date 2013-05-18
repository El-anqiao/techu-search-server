$(document).ready(function(){
  $('.example-toggle').click(function(){
    el = $(this).parents('.example-box').find('.example-result');
    if ( $(el).css('display') != 'none' ){
      $(this).removeClass('minus').addClass('plus');
    } else {
      $(this).addClass('minus').removeClass('plus');
    }
    $(el).slideToggle();
  });
  $('#how-it-works-text-container').perfectScrollbar({
    wheelSpeed: 20,
    wheelPropagation: true
  });
});
