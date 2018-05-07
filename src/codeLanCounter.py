#! usr/bin/python
#coding=utf-8
# -*- coding:cp936 -*-
import os
import json

item = "Low_Q"

out_file = '../output/codeGuessSum'+item+'.txt'

stack = []
lanDict = {}

with open(out_file) as code_f:
    for line in code_f:
        line = line.strip()
        if line.endswith('.txt'):
            postID = line.split('_')[1].split('_')[0]
            stack.append(postID)
        elif "guesslang" in line:
            lan = line.split("The source code is written in ")[1]
            postID = stack.pop()
            if not lan in lanDict:
                lanDict[lan] = [postID]
            else:
                lanDict[lan].append(postID)

lanDict['"Unknown"'] = stack
                
with open("../postLanML"+item+".json","w") as metaf:        
    metaf.write(json.dumps(lanDict))


for item in lanDict:
    print(item, len(lanDict[item]))