$(document).ready(function() {
  item = $('#active-menu-item').data('item');
  $('#' + item).addClass('active');
});
