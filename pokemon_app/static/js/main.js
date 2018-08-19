$(function() {
  $('.pokemon-like-form').submit(function(e) {
    var $form = $(this)
    e.preventDefault();
    $.ajax({
      context: this,
      type: $form.attr('method'),
      url: $form.attr('action'),
      data: $form.serialize(),
      dataType: 'json',
      success: function (data) {
        $(this).siblings('.pokemon-likes-total').find('.total-likes').text(data.pokemon_likes)
        $(this).siblings('.liked-confirmation').show()
        $(this).find('.pokemon-like').prop('disabled', true);
      },
  	})
  })
})