$.postJSON = function(url, data, callback, dataType) {
  var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
  var opts = {
    url: url,
    type: 'post',
    data: JSON.stringify(data),
    success: callback,
    error: function (err) {
      console.log(err);
    }
  };  
  if (dataType) {
    opts.dataType = dataType;
  }
  $.ajax(opts);
};
