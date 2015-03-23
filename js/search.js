$(function () {
  $('#seachBox').data('holder', $('#searchBox').attr('placeholder'));
  $('#searchBox').focusin(function () {
    $(this).attr('placeholder', '');
  });
  $('#searchBox').focusout(function () {
    if($(this).val().length == 0){
      $(this).attr('placeholder', "Search");
    }
  });
});