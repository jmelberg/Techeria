$(document).ready(function(){
  $("[id^='reply-']").click(function(){
    var counter = $(this).attr('id').split('-')[1];
    $("[id^='replybox-']").remove();
    $("[id^='reply-']").show();
    $('#replybox').clone().show().attr('id', 'replybox-'+counter).insertAfter('#comment'+counter);
    var margin = $('#comment'+counter).css('margin-left');
    $('#replybox-'+counter).css('margin-left', margin);
    var parent = $(this).val();
    $('#replybox-'+counter).find('#parent').val(parent);
    $(this).hide();
    $('#replybox-'+counter).find('textarea').focus();
  });

  $('#postreplyButton').click(function(){
  });
});