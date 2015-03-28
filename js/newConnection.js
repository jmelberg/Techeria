$(document).ready(function(){
  $('#connectModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var requestee = button.data('requestee')
    var modal = $(this)
    modal.find('.modal-title').text('Connection Request to ' + requestee)
    modal.find('.modal-body #requestee').val(requestee)
    $("#connectRequest").click(function(){
      var sender = document.getElementById("viewer").innerHTML;
      var text = $('#connection-text').val();
      $.ajax({
        type:"POST",
        url: "/connect",
        data:{'requestee':requestee, 'text':text, 'sender':sender,},
      });
      $('#connectModal').modal('hide');
    });
  });
});