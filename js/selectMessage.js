$(document).ready(function() {
  var key;
  var count = 0;
  // Select Checkbox
  $( "[id^='checkbox']" ).click(function() {
    if($(this).children(':visible').length == 0){
      $( this).children().show( "fast", function() {
        key = $(this).val();
        $("#delete").show("fast");
        count++;
      });
    }
    else {
      $(this).children().hide("fast", function() {
        count--;
        if(count==0){
          $("#delete").hide("fast", function(){});
        }
      });
    }
  });  
  //Delete Selected
  $("#delete").click(function(){
  // Delete function
    var array = []
    $("[id^='checkbox']").each(function(index, key){
      if($(this).children(':visible').length > 0){
        array.push(key.value);
      }
    });
    var json_array = array.toString();
    $.ajax({
      type: "POST",
      url: "/trash",
      data: {'array' : json_array},
    });
    top.location.href = '/messages';
  });                
});
