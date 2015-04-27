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
      });
      setTimeout(function(){ // Refresh after 1 second
      window.location.href = '/';
    }, 200);
  });
});