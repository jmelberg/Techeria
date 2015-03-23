$(function () {
  // Text Forum Post
  $('#textPost').click(function () {
    $('#url').hide();
    $('#linkPost').removeAttr("class");
    $('#urlInput').val('');
    $('#textPost').attr("class", "active");
  });
  // Link Forum Post
  $('#linkPost').click(function () {
    $('#url').show();
    $('#linkPost').attr("class", "active"); 
    $('#textPost').removeAttr("class");                                           
  }); 
});