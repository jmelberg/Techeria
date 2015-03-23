var done = 0;
jQuery(document).ready(function() {
  var count = 1;
  var multiplier = 0.5;
  var bodyheight = $('body').height();
  $(window).scroll(function(){
    if ($(window).scrollTop() > 100) {
      $('.scroll-top-wrapper').addClass('show');
    } else {
      $('.scroll-top-wrapper').removeClass('show');
    }
    if($(window).scrollTop() + bodyheight >= .75*$('body').height()) {
      if(done == 0){
        updateFeed(count);
        $('#loading').show();
        count++;
      }
    }
  });
});

$('#commentBox').data('holder', $('#commentBox').attr('placeholder'));
$('#commentBox').focusin(function () {
  $(this).attr('placeholder', '');
  $(this).attr('rows', 2);
  $("#postButton").show("fast");
});

$('#commentBox').focusout(function () {
  if($(this).val().length == 0){
    $(this).attr('placeholder', "What's New?");
    $(this).attr('rows', 1);
    $("#postButton").hide("fast");
  }
});

$('#postButton').click(function() {
  updateFeed(0);
}); 
  
function updateFeed(page) {
  $.ajax({
    url: "/feedlist",
    cache: false,
    data: {'page': page},
    success: function(frag){
      $("#feedlist").append(frag);
      $('#loading').hide();
      var id = "#more-" + page;
      if(parseInt($(id).text()) < 10){
        done = 1;
      }
    }
  });
}

updateFeed(0);