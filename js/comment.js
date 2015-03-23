$(function () {
  $('#commentBox').data('holder', $('#commentBox').attr('placeholder'));
  $('#commentBox').focusin(function () {
   $(this).attr('placeholder', '');
   $(this).attr('rows', 2);
   $("#postButton").show("fast");
 });
  $('#commentBox').focusout(function () {
    if($(this).val().length == 0){
      $(this).attr('placeholder', "Leave {{user.first_name}} a comment.");
      $(this).attr('rows', 1);
      $("#postButton").hide("fast");
    }
  });
});