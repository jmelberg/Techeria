$(document).ready(function(){
  $('#myModal').modal(); // Instatiates modal
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
  $('#business').click(function(){
    $('#tech').prop("checked", false);
    $('#role').html("business");
  });
  $('#tech').click(function(){
    $('#business').prop("checked", false);
    $('#role').html("engineering");
  });
  $('#yes').click(function(){
    $('#no').prop("checked", false);
  });
  $('#no').click(function(){
    $('#yes').prop("checked", false);
  });

  $('ul.setup-panel li.active a').trigger('click');
    //Let other tabs be accessable //
  $('#activate2').on('click', function(e) {
    if(document.getElementById("business").checked == true){
      alert("Moving to Business");
    }
    else{
      alert("Moving to Tech");
    }
    $('ul.setup-panel li:eq(1)').removeClass('disabled');
    $('ul.setup-panel li a[href="#step2"]').trigger('click');
    $(this).remove();
  });   
  $('#activate3').on('click', function(e) {
    if(document.getElementById("yes").checked== true){
      alert("Coder!");
    }
    else{
      alert("Non-coder");
    }
    $('ul.setup-panel li:eq(2)').removeClass('disabled');
    $('ul.setup-panel li a[href="#step3"]').trigger('click');
    $(this).remove();
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