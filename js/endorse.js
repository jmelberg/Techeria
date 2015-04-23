$(document).ready(function(){
  var key;
  var counter;
  var endorsee = document.getElementById('endorser').innerHTML;
  var activate = "yes";
  var textDetail = "no";
  // Upvote Selected
  $("[id^='up-']").click(function(){
    $('#comment_selected').click(function(){
      $('#endorse_comment').show();
      textDetail = "yes";
    });
    key = $(this).val();
    $('#endorseModal').modal();
    var modal = $(this)
    $("#endorsementMade").click(function(){
      activate = "no"
      var text = $('#endorse-text').val();

      if(textDetail == "yes"){
        $.ajax({
        type: "POST",
        url: "/endorse",
        data: {'key' : key, 'endorsee': endorsee, 'text':text,},
      });
      }
      else{
        text = "empty"
        $.ajax({
        type: "POST",
        url: "/endorse",
        data: {'key' : key, 'endorsee': endorsee, 'text':text,},
      });
      }
      $('#endorseModal').modal('hide');
      setTimeout(function(){ // Refresh after 1 second
      window.location.href = window.location.href;
    }, 500);
    });
    var counter = $(this).attr('id').split('-')[1];
    var number = document.getElementById(counter);
    var voteCount = number.innerHTML;
    var currentEndorsement = $('#up-' + counter);
    if($('#up-'+ counter).is(":enabled")){
      voteCount++;
    }
    if(activate == "no"){
      currentEndorsement.prop('disabled', true);
      number.innerHTML = voteCount;
    }
  });
}); 