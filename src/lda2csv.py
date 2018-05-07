#! usr/bin/python
#coding=utf-8
# -*- coding:cp936 -*-
#import os
from collections import defaultdict

in_f = "../output/ldaSumMed.txt"
out_text_f = "../output/ldaSumMed_text.csv"
out_code_f = "../output/ldaSumMed_code.csv"

post_text_kw = {}
post_code_kw = {}
cat = "text"

def updateDict(post_kw, keywords, post_id):
    if not post_id in post_kw:
        post_kw[post_id] = keywords
    else:
        post_kw[post_id] += keywords
        post_kw[post_id] = list(set(post_kw[post_id]))

with open(in_f, encoding='utf-8') as f:
    for line in f:
        line = line.strip()

        if line.startswith("post"):
            post_id = line.split('_')[1]
        elif line == "title+tags+text":
            cat = "text"
        elif line == "code":
            cat = "code"
        else:
            weights = line.split(" + ")
            keywords = [word.split('*')[1].strip('"') for word in weights]
            if cat == "text":
                updateDict(post_text_kw, keywords, post_id)
            elif cat == "code":
                updateDict(post_code_kw, keywords, post_id)

import csv            
with open(out_text_f, 'w', newline='',encoding='utf-8') as f:  
    f_w = csv.writer(f,delimiter = ',')
    for key in post_text_kw:
        while post_text_kw[key]:
            f_w.writerow([str(key), post_text_kw[key].pop()])

with open(out_code_f, 'w', newline='',encoding='utf-8') as f:  
    f_w = csv.writer(f,delimiter = ',')
    for key in post_code_kw:
        while post_code_kw[key]:
            f_w.writerow([str(key), post_code_kw[key].pop()])
