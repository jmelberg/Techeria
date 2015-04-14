$(document).ready(function(){
  var key;
  var counter;
  var endorsee = document.getElementById('endorser').innerHTML;
  // Upvote Selected
  $("[id^='up-']").click(function(){
    key = $(this).val();
    alert(key)
    var counter = $(this).attr('id').split('-')[1];
    var number = document.getElementById('upCount'+counter);
    alert(number)
    var voteCount = number.value;
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