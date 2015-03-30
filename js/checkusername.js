  $(function () {
    $('#username').focus();
    $('#username').keyup(function () {
      if($(this).val().length != 0){
        checkUsername($(this).val().toLowerCase());
      }
      else{
        $("#available").hide();
      }
    });
    $('#c_password').keyup(function () {
      if($(this).val() != $('#password').val()){
        $('#passwords_match').show();
        $('#signup').prop('disabled', true);
      }
      else{
        $('#passwords_match').hide();
        $('#signup').prop('disabled', false);
      }
    });             
  });
  function checkUsername(username) {
    $.ajax({
      url: "/checkusername",
      cache: false,
      data:{'username' : username},
      success: function(result){
      $("#available").text(result);
      if(result == 'Username is available'){
        $("#available").attr('class', 'label label-success pull-right');
        $("#available").show();
        $("#signup").prop('disabled', false);
      }
      else {
        $("#available").attr('class', 'label label-danger pull-right');
        $("#available").show();
        $("#signup").prop('disabled', true);
      }
    }});
  }
