var done = 0;
var items = getUrlParameter('q')
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
        updateFeed(count, items);
        $('#loading').show();
        count++;
        done = 1;
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
$('#commentsNav').click(function() {
  updateFeed(0);
  $('#postsNav').removeAttr("class");
  $('#commentsNav').attr("class", "active");
}); 
$('#postsNav').click(function() {
  updateFeed(0);
  $('#commentsNav').removeAttr("class");
  $('#postsNav').attr("class", "active");
}); 
  
function updateFeed(page, items) {
  $.ajax({
    url: "/feedlist",
    cache: false,
    async: true,
    data: {'page': page,'items': items},
    success: function(frag){
      $("#feedlist").append(frag);
      $('#loading').hide();
      var id = "#more-" + page;
      done = 0;
      if(parseInt($(id).text()) < 10){
        done = 1;
      }
    }
  });
}

function getUrlParameter(sParam)
{
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) 
    {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) 
        {
            return sParameterName[1];
        }
    }
}
if(items == 'posts'){
  $('#commentDiv').hide();
  $('#commentsNav').removeAttr("class");
  $('#postsNav').attr("class", "active");
}
else{
  $('#commentDiv').show();
  $('#postsNav').removeAttr("class");
  $('#commentsNav').attr("class", "active");
}
updateFeed(0, items);