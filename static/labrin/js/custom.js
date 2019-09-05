function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(function (e) {
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  // SHARE TASK
  $(document).on("click", ".share-task", function (e) {
    e.preventDefault();
    var todo_id = $(this).attr('todo-id');
    if ($('#shareAllowComment-'+todo_id).is(':checked')) {
      var allowComment = 'checked'
    }
    var form = new FormData();
    // var text = $('.comment-text').val();
    form.append("todo_id", todo_id);
    form.append("user", $('#inputShareUser-'+todo_id).val());
    form.append("allow_comment", allowComment);
    $.ajax({
      url: window.share_task,
      type: "POST",
      processData: false,
      contentType: false,
      data: form,
      success: function (data) {
        if (data) {
          if (data.msg) {
            alert(data.msg);
          }
          else {
            window.location.href = window.index;
          }
        }
      },
      error: function (xhr, errmsg, err) {
        console.log(xhr, errmsg, err);
      }
    });
  })
});
