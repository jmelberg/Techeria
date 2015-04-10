$(document).ready(function(){
  var key;
  var counter;
  var voter = document.getElementById('voter').innerHTML;

  // Upvote Selected
  $("[id^='upVote-']").click(function(){
    this.style.backgroundColor = 'orange';
    key = $(this).val();
    change = 1;
    var counter = $(this).attr('id').split('-')[1];
    $('#downVote-' + counter).removeAttr("style");
    var number = document.getElementById('voteCount'+counter);
    var voteCount = number.innerHTML;
    if ($('#downVote-' + counter).is(":disabled")){
      voteCount++;
    }
    if($('#upVote-'+ counter).is(":enabled")){
      voteCount++;
    }
    number.innerHTML = voteCount;
    $(this).prop('disabled', true);

    $('#downVote-' + counter).prop('disabled', false);
    $.ajax({
      type: "POST",
      url: "/vote",
      data: {'key' : key, 'change': change, 'voter': voter},
    });
  });

  // Downvote Selected
  $("[id^='downVote-']").click(function(){
    this.style.backgroundColor = '4682B4  ';
    key = $(this).val();
    change = -1;
    var voter = document.getElementById('voter').innerHTML;
    var counter = $(this).attr('id').split('-')[1];
    $('#upVote-' + counter).removeAttr("style");
    var number = document.getElementById('voteCount'+counter);
    var voteCount = number.innerHTML;
    if ($('#upVote-' + counter).is(":disabled")){
      voteCount--;
    }
    if($('#downVote-'+ counter).is(":enabled")){
      voteCount--;
    }
    number.innerHTML = voteCount;
    $(this).prop('disabled', true);
    $('#upVote-' + counter).prop('disabled', false);
    $.ajax({
      type: "POST",
      url: "/vote",
      data: {'key' : key, 'change': change, 'voter': voter},
    });
  });
}); 