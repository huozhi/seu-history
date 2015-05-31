var user = {
  ICCard: null,
  stuentId: null,
  bind: function () {
    $('#login').click(user.login);
  },
  set: function () {
    user.ICCard = $('#icCard').val();
    user.studentId = $('#studentId').val();
  },
  data: function () {
    return {
      username: user.ICCard,
      password: user.studentId,
    };
  },
  login: function () {
    user.set();
    
    $.postJSON('/',
      user.data(),
      function (data) {
        if (data.login) {
          window.location.href = "/statement/";
        }
      }, 'json');
  }
}

$(function () {
  user.bind();
});