$(document).ready(function(){

  var field;
  var role;
  var tools;
  var specialty;
  var count = document.getElementById("skill_count").value;
  if( count == 0){
    // $('#myModal').modal(); // Instatiates modal
    $('#myModal').appendTo("body").modal('show');
  }
  var navListItems = $('ul.setup-panel li a'),
    allWells = $('.setup-content');
  allWells.hide();
  navListItems.click(function(e){ 
    e.preventDefault();
    var $target = $($(this).attr('href')),
      $item = $(this).closest('li');
            
    if (!$item.hasClass('disabled')) {
      navListItems.closest('li').removeClass('active');
      $item.addClass('active');
      allWells.hide();
      $target.show();
    }
  });

  // Click one or the other
  // Student, Recruiter, or Professional
  $('#student').click(function(){
    $('#recruiter').prop("checked", false);
    $('#professional').prop("checked", false);
    $('#job').html("student");
    $('#d_role').html("");
    $('#dlanguages').html("");
    $('#r_role').html("");
    $('#rm_role').html("");
    $('#rf_role').html("");
    $('#rs_role').html("");
  });
  $('#recruiter').click(function(){
    $('#student').prop("checked", false);
    $('#professional').prop("checked", false);
    $('#job').html("recruiter");
    $('#d_role').html(" applicant");
    $('#dlanguages').html(" desired");
    $('#r_role').html(" applicant's desired");
    $('#rm_role').html(" are desired");
    $('#rf_role').html(" are desired");
    $('#rs_role').html(" are desired");
  });
  $('#professional').click(function(){
    $('#student').prop("checked", false);
    $('#recruiter').prop("checked", false);
    $('#job').html("professional");
    $('#d_role').html("");
    $('#dlanguages').html("");
    $('#r_role').html("");
    $('#rm_role').html("");
    $('#rf_role').html("");
    $('#rs_role').html("");


  });
  ///// Business or Engineering on/off switch /////
  $('#business').click(function(){
    $('#tech').prop("checked", false);
    $('#role').html("business");
  });
  $('#tech').click(function(){
    $('#business').prop("checked", false);
    $('#role').html("engineering");
  });

  /////// What kind of business on/off switch ///////
  $('#marketing').click(function(){
    $('#sales').prop("checked", false);
    $('#finance').prop("checked", false);
    $('#b_other').prop("checked", false);
    $('#b_other_text').hide();
  });
  $('#sales').click(function(){
    $('#marketing').prop("checked", false);
    $('#finance').prop("checked", false);
    $('#b_other').prop("checked", false);
    $('#b_other_text').hide();
  });
  $('#finance').click(function(){
    $('#sales').prop("checked", false);
    $('#marketing').prop("checked", false);
    $('#b_other').prop("checked", false);
    $('#b_other_text').hide();
  });
  $('#b_other').click(function(){
    $('#sales').prop("checked", false);
    $('#marketing').prop("checked", false);
    $('#finance').prop("checked", false);
    $('#b_other_text').show();
  });

  //////// What kind of engineering on/off switch? /////
  $('#air').click(function(){
    $('#medical').prop("checked", false);
    $('#civil').prop("checked", false);
    $('#computer').prop("checked", false);
    $('#electrical').prop("checked", false);
    $('#general').prop("checked", false);
    $('#industrial').prop("checked", false);
    $('#mechanical').prop("checked", false);
    $('#software').prop("checked", false);
    $('#other').prop("checked", false);
    $('#other_text').hide();
  });
  $('#medical').click(function(){
    $('#air').prop("checked", false);
    $('#civil').prop("checked", false);
    $('#computer').prop("checked", false);
    $('#electrical').prop("checked", false);
    $('#general').prop("checked", false);
    $('#industrial').prop("checked", false);
    $('#mechanical').prop("checked", false);
    $('#software').prop("checked", false);
    $('#other').prop("checked", false);
    $('#other_text').hide();
  });
  $('#civil').click(function(){
    $('#medical').prop("checked", false);
    $('#air').prop("checked", false);
    $('#computer').prop("checked", false);
    $('#electrical').prop("checked", false);
    $('#general').prop("checked", false);
    $('#industrial').prop("checked", false);
    $('#mechanical').prop("checked", false);
    $('#software').prop("checked", false);
    $('#other').prop("checked", false);
    $('#other_text').hide();
  });
  $('#computer').click(function(){
    $('#medical').prop("checked", false);
    $('#civil').prop("checked", false);
    $('#air').prop("checked", false);
    $('#electrical').prop("checked", false);
    $('#general').prop("checked", false);
    $('#industrial').prop("checked", false);
    $('#mechanical').prop("checked", false);
    $('#software').prop("checked", false);
    $('#other').prop("checked", false);
    $('#other_text').hide();
  });
  $('#electrical').click(function(){
    $('#medical').prop("checked", false);
    $('#civil').prop("checked", false);
    $('#computer').prop("checked", false);
    $('#air').prop("checked", false);
    $('#general').prop("checked", false);
    $('#industrial').prop("checked", false);
    $('#mechanical').prop("checked", false);
    $('#software').prop("checked", false);
    $('#other').prop("checked", false);
    $('#other_text').hide();
  });
  $('#general').click(function(){
    $('#medical').prop("checked", false);
    $('#civil').prop("checked", false);
    $('#computer').prop("checked", false);
    $('#electrical').prop("checked", false);
    $('#air').prop("checked", false);
    $('#industrial').prop("checked", false);
    $('#mechanical').prop("checked", false);
    $('#software').prop("checked", false);
    $('#other').prop("checked", false);
    $('#other_text').hide();
  });
    $('#industrial').click(function(){
    $('#medical').prop("checked", false);
    $('#civil').prop("checked", false);
    $('#computer').prop("checked", false);
    $('#electrical').prop("checked", false);
    $('#general').prop("checked", false);
    $('#air').prop("checked", false);
    $('#mechanical').prop("checked", false);
    $('#software').prop("checked", false);
    $('#other').prop("checked", false);
    $('#other_text').hide();
  });
  $('#mechanical').click(function(){
    $('#medical').prop("checked", false);
    $('#civil').prop("checked", false);
    $('#computer').prop("checked", false);
    $('#electrical').prop("checked", false);
    $('#general').prop("checked", false);
    $('#industrial').prop("checked", false);
    $('#air').prop("checked", false);
    $('#software').prop("checked", false);
    $('#other').prop("checked", false);
    $('#other_text').hide();
  });
  $('#software').click(function(){
    $('#medical').prop("checked", false);
    $('#civil').prop("checked", false);
    $('#computer').prop("checked", false);
    $('#electrical').prop("checked", false);
    $('#general').prop("checked", false);
    $('#industrial').prop("checked", false);
    $('#mechanical').prop("checked", false);
    $('#air').prop("checked", false);
    $('#other').prop("checked", false);
    $('#other_text').hide();
  });
  $('#other').click(function(){
    $('#medical').prop("checked", false);
    $('#civil').prop("checked", false);
    $('#computer').prop("checked", false);
    $('#electrical').prop("checked", false);
    $('#general').prop("checked", false);
    $('#industrial').prop("checked", false);
    $('#mechanical').prop("checked", false);
    $('#air').prop("checked", false);
    $('#software').prop("checked", false);
    $('#other_text').show();
  });  

  //////// What kind of developer on/off switch //////
  $('#mobile').click(function(){
    $('#languages-form').show();
    $('#system').prop("checked", false);
    $('#web').prop("checked", false);
    $('#embedSystem').prop("checked", false);
    $('#bigdata').prop("checked", false);
    $('#quality').prop("checked", false);
    $('#d_other').prop("checked", false);
    $('#d_other_text').hide();
  });
  $('#system').click(function(){
    $('#languages-form').show();
    $('#mobile').prop("checked", false);
    $('#web').prop("checked", false);
    $('#embedSystem').prop("checked", false);
    $('#bigdata').prop("checked", false);
    $('#quality').prop("checked", false);
    $('#d_other').prop("checked", false);
    $('#d_other_text').hide();
  });
  $('#web').click(function(){
    $('#languages-form').show();
    $('#system').prop("checked", false);
    $('#mobile').prop("checked", false);
    $('#embedSystem').prop("checked", false);
    $('#bigdata').prop("checked", false);
    $('#quality').prop("checked", false);
    $('#d_other').prop("checked", false);
    $('#d_other_text').hide();
  });
  $('#embedSystem').click(function(){
    $('#languages-form').show();
    $('#system').prop("checked", false);
    $('#mobile').prop("checked", false);
    $('#web').prop("checked", false);
    $('#bigdata').prop("checked", false);
    $('#quality').prop("checked", false);
    $('#d_other').prop("checked", false);
    $('#d_other_text').hide();
  });
  $('#bigdata').click(function(){
    $('#languages-form').show();
    $('#system').prop("checked", false);
    $('#mobile').prop("checked", false);
    $('#embedSystem').prop("checked", false);
    $('#web').prop("checked", false);
    $('#quality').prop("checked", false);
    $('#d_other').prop("checked", false);
    $('#d_other_text').hide();
  });
  $('#quality').click(function(){
    $('#languages-form').show();
    $('#system').prop("checked", false);
    $('#mobile').prop("checked", false);
    $('#embedSystem').prop("checked", false);
    $('#bigdata').prop("checked", false);
    $('#web').prop("checked", false);
    $('#d_other').prop("checked", false);
    $('#d_other_text').hide();
  });
  $('#d_other').click(function(){
    $('#languages-form').show();
    $('#system').prop("checked", false);
    $('#mobile').prop("checked", false);
    $('#embedSystem').prop("checked", false);
    $('#bigdata').prop("checked", false);
    $('#web').prop("checked", false);
    $('#quality').prop("checked", false);
    $('#d_other_text').show();
  });

//////// What kind of Marketing on/off switch //////
  $('#online_marketing').click(function(){
    $('#business_marketing').prop("checked", false);
    $('#consumer_marketing').prop("checked", false);
    $('#partner_marketing').prop("checked", false);
  });
  $('#busines_marketing').click(function(){
    $('#online_marketing').prop("checked", false);
    $('#consumer_marketing').prop("checked", false);
    $('#partner_marketing').prop("checked", false);
  });
  $('#consumer_marketing').click(function(){
    $('#business_marketing').prop("checked", false);
    $('#online_marketing').prop("checked", false);
    $('#partner_marketing').prop("checked", false);
  });
  $('#partner_marketing').click(function(){
    $('#business_marketing').prop("checked", false);
    $('#consumer_marketing').prop("checked", false);
    $('#online_marketing').prop("checked", false);
  });

  //////// What kind of Finance on/off switch /////
  $('#personal_finance').click(function(){
    $('#corporate_finance').prop("checked", false);
    $('#investment').prop("checked", false);
  });
  $('#corporate_finance').click(function(){
    $('#personal_finance').prop("checked", false);
    $('#investment').prop("checked", false);
  });
  $('#investment').click(function(){
    $('#corporate_finance').prop("checked", false);
    $('#personal_finance').prop("checked", false);
  });


  /////// What kind of sales on/off switch ///////
  $('#inside_sales').click(function(){
    $('#outside_sales').prop("checked", false);
    $('#support_sales').prop("checked", false);
    $('#commission_sales').prop("checked", false);
    $('#s_sales').prop("checked", false);
  });
  $('#outside_sales').click(function(){
    $('#inside_sales').prop("checked", false);
    $('#support_sales').prop("checked", false);
    $('#commission_sales').prop("checked", false);
    $('#s_sales').prop("checked", false);
  });
  $('#support_sales').click(function(){
    $('#outside_sales').prop("checked", false);
    $('#inside_sales').prop("checked", false);
    $('#commission_sales').prop("checked", false);
    $('#s_sales').prop("checked", false);
  });
  $('#commission_sales').click(function(){
    $('#outside_sales').prop("checked", false);
    $('#support_sales').prop("checked", false);
    $('#inside_sales').prop("checked", false);
    $('#s_sales').prop("checked", false);
  });
  $('#s_sales').click(function(){
    $('#outside_sales').prop("checked", false);
    $('#support_sales').prop("checked", false);
    $('#commission_sales').prop("checked", false);
    $('#inside_sales').prop("checked", false);
  });

  //////////                     //////////
  //////////  Main Modal Fields  //////////
  //////////                     //////////
 
  $('ul.setup-panel li.active a').trigger('click');
    //Let other tabs be accessable //

  //////// Gather Account Type //////
  $('#activate1').on('click', function(e) {
    if(document.getElementById("student").checked == true){
      role = "student";
    }
    else if (document.getElementById("recruiter").checked == true){
      role = "recruiter";
    }
    else{
      role = "professional"
    }
    $('ul.setup-panel li:eq(1)').removeClass('disabled');
    $('ul.setup-panel li a[href="#step1"]').trigger('click');
    $('#step1').show();
  }); 

  ///////// Gather Business or Engineering ////// 
  $('#activate2').on('click', function(e) {
    if(document.getElementById("business").checked == true){
      field = "business";
      $('ul.setup-panel li:eq(2)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step2"]').trigger('click');
      $('#step2b').show();
    }
    else{
      field = "engineering";
      $('ul.setup-panel li:eq(2)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step2"]').trigger('click');
      $('#step2e').show();
    }
  }); 

  ///////// Gather Engineering Type ///////
  $('#activate3e').on('click', function(e) {
    if(document.getElementById("air").checked== true){
      specialty = "Aerospace Engineering";
      $('ul.setup-panel li:eq(3)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step3"]').trigger('click');
      $('#step3e').show();
    }
    else if(document.getElementById("medical").checked== true){
      specialty = "Medical Engineering";
      $('ul.setup-panel li:eq(3)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step3"]').trigger('click');
      $('#step3e').show();
    }    
    else if(document.getElementById("civil").checked== true){
      specialty = "Civil Engineering";
      $('ul.setup-panel li:eq(3)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step3"]').trigger('click');
      $('#step3e').show();
    }
    else if(document.getElementById("computer").checked== true){
      specialty = "Computer Engineering";
      $('ul.setup-panel li:eq(3)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step3"]').trigger('click');
      $('#step3e').show();
    }
    else if(document.getElementById("electrical").checked== true){
      specialty = "Electrical Engineering";
      $('ul.setup-panel li:eq(3)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step3"]').trigger('click');
      $('#step3e').show();
    }
    else if(document.getElementById("general").checked== true){
      specialty = "General Engineering";
      $('ul.setup-panel li:eq(3)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step3"]').trigger('click');
      $('#step3e').show();
    }
    else if(document.getElementById("mechanical").checked== true){
      specialty = "Mechanical Engineering";
      $('ul.setup-panel li:eq(3)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step3"]').trigger('click');
      $('#step3e').show();
    }
    else if(document.getElementById("software").checked== true){
      specialty = "Software Engineering";
      $('ul.setup-panel li:eq(3)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step3"]').trigger('click');
      $('#step3se').show();
    }
    else{
      specialty = $('#other_text').val();
      $('ul.setup-panel li:eq(3)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step3"]').trigger('click');
      $('#step3e').show();
    }
  });

  ///////// Gather Business Type ////////
  $('#activate3b').on('click', function(e) {
    if(document.getElementById("finance").checked== true){
      specialty = "Finance";
      $('ul.setup-panel li:eq(3)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step3"]').trigger('click');
      $('#step3f').show();
    }
    else if(document.getElementById("marketing").checked== true){
      specialty = "Marketing";
      $('ul.setup-panel li:eq(3)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step3"]').trigger('click');
      $('#step3m').show();
    }
    else if(document.getElementById("sales").checked== true){
      specialty = "Sales";
      $('ul.setup-panel li:eq(3)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step3"]').trigger('click');
      $('#step3s').show();
    }
    else{
      specialty = $('#b_other_text').val();
      $('ul.setup-panel li:eq(3)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step3"]').trigger('click');
      $('#step3e').show();
    }
  });

  //////// Software Engineer Submit //////
  $("#done_t").click(function(){
    if(document.getElementById("mobile").checked == true){
      specialty = "Mobile Developer";
    }
    else if(document.getElementById("system").checked == true){
      specialty = "Systems Developer";
    }
    else if(document.getElementById("embedSystem").checked == true){
      specialty = "Embedded Systems Developer";
    }
    else if(document.getElementById("bigdata").checked == true){
      specialty = "Big Data Developer";
    } 
    else if(document.getElementById("quality").checked == true){
      specialty = "Quality Assurance Developer";
    }
    else{
      specialty = $('#d_other_text').val();
    }  
    tools = document.getElementById("languages").value;  
    $.ajax({
      type:"POST",
      url: "/newskill",
      data:{'field':field, 'specialty':specialty, 'role':role, 'tools':tools}
    });
    window.location.href = '/';
  });
  //////// Engineer Submit //////
  $("#done_te").click(function(){
    tools = document.getElementById("engineering_skills").value;
    $.ajax({
      type:"POST",
      url: "/newskill",
      data:{'field':field, 'specialty':specialty, 'role':role, 'tools':tools}
    });
    window.location.href = '/';
  });

  //////// Marketing Submit //////
  $("#done_m").click(function(){
    if(document.getElementById("online_marketing").checked == true){
      specialty = "Online Marketing";
    }
    if(document.getElementById("business_marketing").checked == true){
      specialty = "Business Marketing";
    }
    if(document.getElementById("consumer_marketing").checked == true){
      specialty = "Consumer Marketing";
    }
    if(document.getElementById("partner_marketing").checked == true){
      specialty = "Partner Marketing";
    }
    tools = document.getElementById("marketingtools").value; 
    $.ajax({
      type:"POST",
      url: "/newskill",
      data:{'field':field, 'tools':tools, 'role':role, 'specialty':specialty}
    });
    window.location.href = '/';
  });

  //////// Finance Submit //////
  $("#done_f").click(function(){
    if(document.getElementById("personal_finance").checked == true){
      specialty = "Personal Finance";
    }
    if(document.getElementById("corporate_finance").checked == true){
      specialty = "Corporate Finance";
    }
    if(document.getElementById("investment").checked == true){
      specialty = "Investment Finance";
    }
    tools = document.getElementById("financetools").value; 

    $.ajax({
      type:"POST",
      url: "/newskill",
      data:{'field':field, 'tools':tools, 'role':role,  'specialty': specialty}
    });
    window.location.href = '/';
  });

  //////// Sales Submit //////
  $("#done_s").click(function(){
  if(document.getElementById("inside_sales").checked == true){
      specialty = "Inside Sales";
    }
    if(document.getElementById("outside_sales").checked == true){
      specialty = "Outside Sales";
    }
    if(document.getElementById("support_sales").checked == true){
      specialty = "Support Sales";
    }
    if(document.getElementById("commission_sales").checked == true){
      specialty = "Commission Sales";
    } 
    tools = document.getElementById("salestools").value;
    $.ajax({
      type:"POST",
      url: "/newskill",
      data:{'field':field, 'tools':tools, 'role':role, 'specialty':specialty}
    });
    window.location.href = '/';
  });
});

// Edit and Cancel Buttons
$(function () {
  $('#edit').click(function () {
    $('#test').hide();
    $('#editField').show();
  });
  $('#cancel').click(function(){
    $('#test').show();
    $('#editField').hide();
  });
});