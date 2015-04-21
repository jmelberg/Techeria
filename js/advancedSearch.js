$(document).ready(function(){

  $('.list-group li').click(function(e) {
        e.preventDefault()
        $that = $(this);
        $('.list-group').find('li').removeClass('active');
        $that.addClass('active');
    });
  // Users Selected
  $('#users').click(function(){
    $('#jobs_list').hide();
    $('#skills_list').hide();
    $('#forums_list').hide();
    $('#employers_list').hide();
    $('#users_list').show();
  });
  // Skills Selected
  $('#skills').click(function(){
    $('#jobs_list').hide();
    $('#users_list').hide();
    $('#forums_list').hide();
    $('#employers_list').hide();
    $('#skills_list').show();
  });
  // Forums Selected
  $('#forums').click(function(){
    $('#jobs_list').hide();
    $('#skills_list').hide();
    $('#users_list').hide();
    $('#employers_list').hide();
    $('#forums_list').show();
  });
  // Employers Selected
  $('#employers').click(function(){
    $('#jobs_list').hide();
    $('#skills_list').hide();
    $('#forums_list').hide();
    $('#users_list').hide();
    $('#employers_list').show();
  });
  // Jobs Selected
  $('#jobs').click(function(){
    $('#users_list').hide();
    $('#skills_list').hide();
    $('#forums_list').hide();
    $('#employers_list').hide();
    $('#jobs_list').show();
  });
}); 