$(document).ready(function(){
  var key;
  var counter;
  var endorsee = document.getElementById('endorser').innerHTML;
  // Upvote Selected
  $("[id^='up-']").click(function(){
    key = $(this).val();
    var counter = $(this).attr('id').split('-')[1];
    var number = document.getElementById(counter);
    var voteCount = number.innerHTML;
    if($('#up-'+ counter).is(":enabled")){
      voteCount++;
    }
    number.innerHTML = voteCount;
    $(this).prop('disabled', true);

    $.ajax({
      type: "POST",
      url: "/endorse",
      data: {'key' : key, 'endorsee': endorsee},
    });
  });
}); 