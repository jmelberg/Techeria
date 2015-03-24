$('#messageModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var recipient = button.data('recipient')
        var modal = $(this)
        modal.find('.modal-title').text('New message to ' + recipient)
        modal.find('.modal-body input').val(recipient)
      });
$("#sendMessage").click(function(){
  var sender = document.getElementById("viewer").innerHTML;
  var subject = document.getElementById("message-subject").innerHTML;
  var text = document.getElementById("message-text").innerHTML;
  $.ajax({
    type:"POST",
    url: "/compose?recipient={{user.username}}",
    data:{'recipient':recipient, 'text':text, 'sender':sender,
          'subject':subject},
  });
});
