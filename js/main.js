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
  $('#how-it-works-diagram-container').height($('#how-it-works-text').height());
});
