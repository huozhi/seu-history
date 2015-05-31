# -*- coding: utf-8 -*-
import codecs
import json
from collections import OrderedDict

f = codecs.open('./problems.txt', encoding='utf-8')
problems = []
cnt = 1
for each_line in f.readlines():
    line_text = each_line.strip()
    if line_text.startswith('order'):
        trash, order = line_text.split(' ', 1)
        curr = OrderedDict()
        curr['id'] = cnt
        cnt += 1
    elif line_text.startswith('desc'):
        trash, desc = line_text.split(' ', 1)
        curr['description'] = desc
    elif line_text.startswith('correct'):
        trash, correct = line_text.split(' ', 1)
        curr['correct'] = correct
    elif line_text.startswith('answer'):
        select, answer = line_text.split(' ', 1)
        curr[select] = answer
        print answer
        if select == 'answerD':
            problems.append(curr)


for each in problems:
    for key in each:
        print key, each[key]

out = codecs.open('problems.json', 'w', encoding='utf-8')
json.dump(problems, out)
