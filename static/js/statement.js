"use strict";
var statement = {
  shown: true,
  content: $('#statementCollapse'),
  toggle: function () {
    statement.shown = !statement.shown;
    if (statement.shown) {
      $(this).text('收起');
    }
    else {
      $(this).text('展开规则');
    }
    statement.content.slideToggle();
  }
};

$(function () {
  $('#rules').click(statement.toggle);
});