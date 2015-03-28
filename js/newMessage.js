$(document).ready(function(){
  $('#messageModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var recipient = button.data('recipient')
    var modal = $(this)
    modal.find('.modal-title').text('New message to ' + recipient)
    modal.find('.modal-body #recipient').val(recipient)
    $("#sendMessage").click(function(){
      var sender = document.getElementById("viewer").innerHTML;
      var subject = $('#message-subject').val();
      var text = $('#message-text').val();
      $.ajax({
        type:"POST",
        url: "/compose",
        data:{'recipient':recipient, 'text':text, 'sender':sender,
        'subject':subject},
      });
      $('#messageModal').modal('hide');
    });
  });
});

