jQuery(document).ready(function() {
  $('#subscribeButton').click(function () {
    $(this).hide();
    var forum = $('#forumName').val()
    $.ajax({
    type: "POST",
    url: "/subscribe",
    data: {'forum_name': forum}
  });
  });


});