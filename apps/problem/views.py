# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.context_processors import csrf
from django.http import JsonResponse
# import os
import codecs
import math
import json
import hashlib
import traceback

# Create your views here.

class EncrptHelper(object):
    def __init__(self):
        self.method = hashlib.md5()
        
    def hash(self, value):
        self.method.update(value)
        return self.method.hexdigest() # encrpt to hex format


class BaseProblemHelper(object):
    def __init__(self, user):
        self.user = user

    def mapChoice(self):
        prolist = json.load(codecs.open('db/choices.json', encoding='utf-8'))
        return sorted(prolist, key=lambda x: x.get('id'))
    
    def mapToF(self):
        prolist = json.load(codecs.open('db/tofs.json', encoding='utf-8'))
        
        for pro in prolist:
            pro['correct'] = True if pro['correct'] == 'true' else False
        return sorted(prolist, key=lambda x: x.get('id'))
        # return { pro['id']: pro for pro in prolist }
    

class ProblemGenerateHelper(BaseProblemHelper):
    '''
    the selection algorithm description
    for example, we have 'uname', use md5 encrypt to a hex-value called hv,
    assume hv is '4124bc0a9335c27f086f24ba207a4912'
    then add hv with revserse of hv, and get first 40 characters, 
    (4124bc0a9335c27f086f24ba207a4912 + 2194a702ab42f680f72c5339a0cb4214)[:40]
    two hex chars could represent a number, then we have 20 numbers, 
    value range from '00'(0) to 'ff'(255)
    but total count is less than 100, mod each number with total then we get id
    '''
    def __init__(self, user):
        super(ProblemGenerateHelper, self).__init__(user)

    def hexValue(self):
        encrptHelper = EncrptHelper()
        hexval = encrptHelper.hash(self.user.get('username')) # 32 length
        return (hexval + hexval[::-1])[:40] # 40 length

    def problems(self, problemSet):
        total = len(problemSet)
        hexval = self.hexValue()
        pieces = [hexval[i: i + 2] for i in range(0, len(hexval), 2)]
        problemIds = [int(piece, 16) % total for piece in pieces]
        return [problemSet[i] for i in problemIds]

    def choiceProblems(self):
        return self.problems(self.mapChoice())

    def tofProblems(self):
        return self.problems(self.mapToF())


class ProblemCheckHelper(BaseProblemHelper):
    def __init__(self, user):
        super(ProblemCheckHelper, self).__init__(user)

    def getCorrects(self, answers, problemSet):
        corrects = {}
        for pro in answers.get('answers'):
            if not pro: continue
            pid = pro.get('id')
            corrects[pid] = problemSet[pid].get('correct')
        return corrects

    def checkChoice(self):        
        choiceAnswers = self.user.get('choiceAnswers')
        tofAnswers = self.user.get('tofAnswers')
        choiceCorrects = self.getCorrects(choiceAnswers, self.mapChoice())
        tofCorrects = self.getCorrects(tofAnswers, self.mapToF())
        score = 0
        correctNum = 0
        for ans in choiceAnswers.get('answers'):
            if not ans: continue
            pid, selection = ans['id'], ans['selection']
            if choiceCorrects[pid] == selection:
                score += 3
                correctNum += 1
        for ans in tofAnswers.get('answers'):
            if not ans: continue
            pid, selection = ans['id'], ans['selection']
            if tofCorrects[pid] == selection:
                score += 2
                correctNum += 1
        print 'score', score
        return score, correctNum
        


class Quiz(View):
    def get(self, request):
        context = {}
        context['loop'] = range(40)
        user = {}
        user['username'] = 'a'
        user['password'] = 'a'
        user['score'] = 0
        helper = ProblemGenerateHelper(user)
        context['choice_problems'] = helper.choiceProblems()[:3]
        context['tof_problems'] = helper.tofProblems()[:3]
        return render(request, 'problems.html', context)

    def post(self, request):
        user = {}
        user['username'] = 'a'
        user['password'] = 'a'
        score = 0
        user['score'] = score
        try:
            post = json.loads(request.body)
            choiceAnswers = {
                'qtype': 'choice',
                'answers': post.get('choiceAnswers')
            }
            tofAnswers = {
                'qtype': 'tof',
                'answers': post.get('tofAnswers')
            }
            user['tof_answers'] = tofAnswers
            user['choice_answers'] = choiceAnswers
            helper = ProblemCheckHelper(user)
            score, correctNum = helper.checkChoice()
        except Exception, e:
            traceback.print_exc()
        request.session['score'] = score
        context['score'] = score
        context['correct_num'] = correctNum
        return redirect('/achieve/', context)


class Result(View):
    def get(self, request):
        context = {}
        correctNum, score = 4, 76
        context['score'] = score
        context['correct_num'] = correctNum
        context['rate'] = round(float(correctNum) / float(40), 1)
        return render(request, 'achieve.html', context)


