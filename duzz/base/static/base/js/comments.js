$('#id_text').on('keyup', function() {
  $('#id_submit').attr('disabled', 'disabled');
  if ($(this).val().length > 0) {
    $('#id_submit').removeAttr('disabled');
  }
});


$('#id_submit').on('click', function(event){
  event.preventDefault();
  $.post('add/', $("#comment-form").serialize())
    .done(function() {
        $('#comment-form').each (function(){
            this.reset();
        });
    })
    .fail(function() {
    })
});


function fetch_updates() {
    var last = $('.tc-item:last');
  var url = '?after=' + last.data('id');
  $.ajax({url: url}).done(function(data) {
    last.after(data);
  });
  setTimeout(fetch_updates, 2000);
}


$(document).ready(function() {
  setTimeout(fetch_updates, 2000);
});

var isCtrl = false;
$(document).keyup(function (e) {
  if(e.which == 17) isCtrl=false;
});


$(document).keydown(function (e) {
  if(e.which == 17) isCtrl=true;
  if(e.which == 13 && isCtrl == true) {
    $('#id_submit').click();
  }
});
