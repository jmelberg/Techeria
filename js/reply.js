$(document).ready(function(){
  $("[id^='reply-']").click(function(){
    var counter = $(this).attr('id').split('-')[1];
    $('#replybox').show().insertAfter('#comment'+counter);
    var parent = $(this).val();
    $('#parent').val(parent);
    $(this).hide();
    $('#replycommentBox').focus();
  });
  
  $('#postreplyButton').click(function(){
  });
});