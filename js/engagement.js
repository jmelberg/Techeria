$(document).ready(function(){

  var field;
  var tools;
  var specialty;
  var count = document.getElementById("skill_count").value;
  if( count == 0){
    $('#myModal').modal(); // Instatiates modal
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
  //Business or Engineering
  $('#business').click(function(){
    $('#tech').prop("checked", false);
    $('#role').html("business");
  });
  $('#tech').click(function(){
    $('#business').prop("checked", false);
    $('#role').html("engineering");
  });
  //Do you code?
  $('#yes').click(function(){
    $('#no').prop("checked", false);
    $('#languages-form').show();
  });
  $('#no').click(function(){
    $('#yes').prop("checked", false);
    //programming languages form
    $('#languages-form').hide();
  });

  //What kind of business?
  $('#marketing').click(function(){
    $('#sales').prop("checked", false);
    $('#finance').prop("checked", false);
    //Marketing Tools form
    $('#marketing-form').show();
    $('#finance-form').hide();
    $('#sales-form').hide();
  });
  $('#sales').click(function(){
    $('#marketing').prop("checked", false);
    $('#finance').prop("checked", false);
    //Sales Tools form
    $('#sales-form').show();
    $('#finance-form').hide();
    $('#marketing-form').hide();
  });
  $('#finance').click(function(){
    $('#sales').prop("checked", false);
    $('#marketing').prop("checked", false);
    //Finance Tools form
    $('#finance-form').show();
    $('#marketing-form').hide();
    $('#sales-form').hide();
  });

  // What kind of developer?
  $('#mobile').click(function(){
    $('#system').prop("checked", false);
    $('#web').prop("checked", false);
    $('#embedSystem').prop("checked", false);
    $('#bigdata').prop("checked", false);
    $('#quality').prop("checked", false);
    $('#e_student').prop("checked", false);
  });
  $('#system').click(function(){
    $('#mobile').prop("checked", false);
    $('#web').prop("checked", false);
    $('#embedSystem').prop("checked", false);
    $('#bigdata').prop("checked", false);
    $('#quality').prop("checked", false);
    $('#e_student').prop("checked", false);
  });
  $('#web').click(function(){
    $('#system').prop("checked", false);
    $('#mobile').prop("checked", false);
    $('#embedSystem').prop("checked", false);
    $('#bigdata').prop("checked", false);
    $('#quality').prop("checked", false);
    $('#e_student').prop("checked", false);
  });
  $('#embedSystem').click(function(){
    $('#system').prop("checked", false);
    $('#mobile').prop("checked", false);
    $('#web').prop("checked", false);
    $('#bigdata').prop("checked", false);
    $('#quality').prop("checked", false);
    $('#e_student').prop("checked", false);
  });
  $('#bigdata').click(function(){
    $('#system').prop("checked", false);
    $('#mobile').prop("checked", false);
    $('#embedSystem').prop("checked", false);
    $('#web').prop("checked", false);
    $('#quality').prop("checked", false);
    $('#e_student').prop("checked", false);
  });
  $('#quality').click(function(){
    $('#system').prop("checked", false);
    $('#mobile').prop("checked", false);
    $('#embedSystem').prop("checked", false);
    $('#bigdata').prop("checked", false);
    $('#web').prop("checked", false);
    $('#e_student').prop("checked", false);
  });
  $('#e_student').click(function(){
    $('#system').prop("checked", false);
    $('#mobile').prop("checked", false);
    $('#embedSystem').prop("checked", false);
    $('#bigdata').prop("checked", false);
    $('#quality').prop("checked", false);
    $('#web').prop("checked", false);
  });

//What kind of Marketing?
  $('#online_marketing').click(function(){
    $('#business_marketing').prop("checked", false);
    $('#consumer_marketing').prop("checked", false);
    $('#partner_marketing').prop("checked", false);
    $('#m_student').prop("checked", false);
  });
  $('#busines_marketing').click(function(){
    $('#online_marketing').prop("checked", false);
    $('#consumer_marketing').prop("checked", false);
    $('#partner_marketing').prop("checked", false);
    $('#m_student').prop("checked", false);
  });
  $('#consumer_marketing').click(function(){
    $('#business_marketing').prop("checked", false);
    $('#online_marketing').prop("checked", false);
    $('#partner_marketing').prop("checked", false);
    $('#m_student').prop("checked", false);
  });
  $('#partner_marketing').click(function(){
    $('#business_marketing').prop("checked", false);
    $('#consumer_marketing').prop("checked", false);
    $('#online_marketing').prop("checked", false);
    $('#m_student').prop("checked", false);
  });
  $('#m_student').click(function(){
    $('#business_marketing').prop("checked", false);
    $('#consumer_marketing').prop("checked", false);
    $('#partner_marketing').prop("checked", false);
    $('#online_marketing').prop("checked", false);
  });

  //What kind of Finance
  $('#personal_finance').click(function(){
    $('#corporate_finance').prop("checked", false);
    $('#investment').prop("checked", false);
    $('#f_student').prop("checked", false);
  });
  $('#corporate_finance').click(function(){
    $('#personal_finance').prop("checked", false);
    $('#investment').prop("checked", false);
    $('#f_student').prop("checked", false);
  });
  $('#investment').click(function(){
    $('#corporate_finance').prop("checked", false);
    $('#personal_finance').prop("checked", false);
    $('#f_student').prop("checked", false);
  });
  $('#f_student').click(function(){
    $('#corporate_finance').prop("checked", false);
    $('#investment').prop("checked", false);
    $('#personal_finance').prop("checked", false);
  });

// What kind of sales?
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


  $('ul.setup-panel li.active a').trigger('click');
    //Let other tabs be accessable //
  $('#activate2').on('click', function(e) {
    if(document.getElementById("business").checked == true){
      field = "business";
      $('ul.setup-panel li:eq(1)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step2"]').trigger('click');
      $('#step2t').hide();
      $('#step2b').show();
    }
    else{
      field = "engineering";
      $('ul.setup-panel li:eq(1)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step2"]').trigger('click');
      $('#step2b').hide();
      $('#step2t').show();
    }
    //$(this).remove();
  }); 

  $('#activate3t').on('click', function(e) {
    if(document.getElementById("yes").checked== true){
      tools = document.getElementById("languages").value;
      $('ul.setup-panel li:eq(2)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step3"]').trigger('click');
      $('#step3t').show();
    }
    else{
      alert("No Skills Added");
      $('ul.setup-panel li:eq(2)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step3"]').trigger('click');
      $('#step3t').show();
    }
    //$(this).remove();
  });

  $('#activate3b').on('click', function(e) {
    if(document.getElementById("finance").checked== true){
      tools = document.getElementById("financetools").value;
      $('ul.setup-panel li:eq(2)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step3"]').trigger('click');
      $('#step3f').show();
    }
    if(document.getElementById("marketing").checked== true){
      tools = document.getElementById("marketingtools").value;
      $('ul.setup-panel li:eq(2)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step3"]').trigger('click');
      $('#step3m').show();
    }
    if(document.getElementById("sales").checked== true){
      tools = document.getElementById("salestools").value;
      $('ul.setup-panel li:eq(2)').removeClass('disabled');
      $('ul.setup-panel li a[href="#step3"]').trigger('click');
      $('#step3s').show();
    }
    //$(this).remove();
  });

  $("#done_t").click(function(){
    if(document.getElementById("mobile").checked == true){
      specialty = "mobile developer";
    }
    if(document.getElementById("system").checked == true){
      specialty = "systems developer";
    }
    if(document.getElementById("embedSystem").checked == true){
      specialty = "embedded systems developer";
    }
    if(document.getElementById("bigdata").checked == true){
      specialty = "big data developer";
    } 
    if(document.getElementById("quality").checked == true){
      specialty = "quality assurance developer";
    }
    if(document.getElementById("e_student").checked == true){
      specialty = "software engineering student";
    }           
    $.ajax({
      type:"POST",
      url: "/newskill",
      data:{'field':field, 'specialty':specialty, 'tools':tools}
    });
  });
  $("#done_m").click(function(){
    if(document.getElementById("online_marketing").checked == true){
      specialty = "online marketing";
    }
    if(document.getElementById("business_marketing").checked == true){
      specialty = "business marketing";
    }
    if(document.getElementById("consumer_marketing").checked == true){
      specialty = "consumer marketing";
    }
    if(document.getElementById("partner_marketing").checked == true){
      specialty = "partner marketing";
    } 
    if(document.getElementById("m_student").checked == true){
      specialty = "marketing student";
    } 
    $.ajax({
      type:"POST",
      url: "/newskill",
      data:{'field':field, 'tools':tools, 'specialty':specialty}
    });
  });
  $("#done_f").click(function(){
    if(document.getElementById("personal_finance").checked == true){
      specialty = "personal finance";
    }
    if(document.getElementById("corporate_finance").checked == true){
      specialty = "corporate finance";
    }
    if(document.getElementById("investment").checked == true){
      specialty = "investment";
    }
    if(document.getElementById("f_student").checked == true){
      specialty = "finance student";
    } 
    $.ajax({
      type:"POST",
      url: "/newskill",
      data:{'field':field, 'tools':tools, 'specialty': specialty}
    });
  });
  $("#done_s").click(function(){
  if(document.getElementById("inside_sales").checked == true){
      specialty = "inside sales";
    }
    if(document.getElementById("outside_sales").checked == true){
      specialty = "outside sales";
    }
    if(document.getElementById("support_sales").checked == true){
      specialty = "support sales";
    }
    if(document.getElementById("commission_sales").checked == true){
      specialty = "commission sales";
    } 
    if(document.getElementById("s_sales").checked == true){
      specialty = "sales student";
    }     
    $.ajax({
      type:"POST",
      url: "/newskill",
      data:{'field':field, 'tools':tools, 'specialty':specialty}
    });
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