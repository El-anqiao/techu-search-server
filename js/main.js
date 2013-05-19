$(document).ready(function(){
  $('.example-toggle').click(function(){
    el = $(this).parents('.example-box').find('.example-result');
    if ( $(el).css('display') != 'none' ){
      $(this).removeClass('minus').addClass('plus');
    } else {
      $(this).addClass('minus').removeClass('plus');
    }
    $(el).slideToggle('slow', function(){ $(el).perfectScrollbar('update').scrollTop(0).perfectScrollbar('update'); });
  });
  $('#how-it-works-text-container').perfectScrollbar({
    wheelSpeed: 20,
    wheelPropagation: true
  });
  $('#search-json').perfectScrollbar({
    wheelSpeed: 20,
    wheelPropagation: true
  });
  $('#searchd-options-setup-json').perfectScrollbar({
    wheelSpeed: 20,
    wheelPropagation: true
  });
  $('#index-options-setup-json').perfectScrollbar({
    wheelSpeed: 20,
    wheelPropagation: true
  });
});
