$(document).ready(function(){
  $('#add_button').click(function(){
    $('#more_skills').show();
    $('#add_button').hide();
  });
  $('#add_skill_submit').click(function(){
    skills = document.getElementById('add_skills').value;
    $.ajax({
        type: "POST",
        url: "/addskill",
        data:{ 'skills': skills,},
        success: function() {
          window.location.reload(true);
        }
      });
  });
});