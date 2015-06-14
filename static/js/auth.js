var user = {
  ICCard: null,
  stuentId: null,
  captcha: null,
  bind: function () {
    $('#login').click(user.login);
  },
  set: function () {
    user.ICCard = $('#icCard').val();
    user.studentId = $('#studentId').val();
    user.captcha = $('#captcha').val();
  },
  data: function () {
    return {
      username: user.ICCard,
      password: user.studentId,
      captcha: user.captcha,
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