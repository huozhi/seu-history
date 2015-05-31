"use strict";
var timer = {
  second: 60,
  init: function () {
    timer.second = 60;
  },
  start: function () {
    timer.second--;
    $('#timer').text(parseInt(timer.second / 60) + ' : ' + timer.second);
    if (timer.second === 0) {
      // times up  
    }
    else
      setTimeout(timer.start, 1000);
  }
};

var utils = {
  getQIdByAnswer: function (element) {
    return $(element).parent().parent().attr('id');
  },
  getQIdByMark: function (element) {
    return $(element).next('.question').attr('id');
  },
  getQIndex: function (element) {
    var idx = $(element)
      .parent().parent()
      .prevAll('.qorder')
      .text().match(/\d+/)[0];
    return parseInt(idx);
  },
  getQType: function (qid) {
    return qid.match(/(choice)|(tof)/)[0];
  },
  getQNumber: function (qid) {
    return parseInt(qid.match(/\d+/)[0]);
  },
  getQAnswer: function (element) {
    return $(element).attr('answer');
  }
};

var answer = {
  choiceAnswers: new Array(20),
  tofAnswers: new Array(20),
  init: function () {
    $('.answer')
      .click(answer.select)
      .click(progresser.highlight);
    $('.qmark')
      .click(answer.mark)
      .click(progresser.mark);  
    $('#submit').click(answer.submit);
  },
  // bind answer button with answer list
  select: function () {
    var self = $(this);
    var choice = utils.getQAnswer(self),
        qid = utils.getQIdByAnswer(self),
        index = utils.getQIndex(self),
        type = utils.getQType(qid),
        num = utils.getQNumber(qid);
    answer.set(type, index, {
      id: num,
      selection: choice
    });
  },
  set: function (type, num, choice) {
    if (type === 'choice') {
      answer.choiceAnswers[num] = choice;
    } else {
      choice.selection = Boolean(choice.selection);
      answer.tofAnswers[num] = choice;
    }
  },
  mark: function () {
    var self = $(this);
    var qid = utils.getQIdByMark(self),
        type = utils.getQType(qid),
        num = utils.getQNumber(qid);
    console.log(qid, type, num)
    if (type === 'choice') {
      answer.choiceAnswers[num] = null;
    } else {
      answer.tofAnswers[num] = null;
    }
  },
  submit: function () {
    console.log(answer.choiceAnswers);
    console.log(answer.tofAnswers);
    $.postJSON('/problems/', {
        choiceAnswers: answer.choiceAnswers,
        tofAnswers: answer.tofAnswers
      },
      function (data) {
        console.log(data);
        if (data.sucess) {
          window.location.href = '/achieve/';
        }
      }, 'json');
  }
};

var progresser = {
  init: function () {

  },
  highlight: function () {
    var self = $(this),
        qid = utils.getQIdByAnswer(self),
        type = utils.getQType(qid),
        index = utils.getQIndex(self),
        progressId = type + index + 'Progresser';
    $('#' + progressId).addClass('highlight');
  },
  mark: function () {
    var self = $(this),
        qid = utils.getQIdByMark(self),
        progressId = qid + 'Progresser';
    $('#' + progressId).removeClass('highlight');
  }
};


$(document).ready(function() {
  answer.init();
  timer.init();
  timer.start();
  
});