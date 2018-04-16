"""
keywords:
 lda 
topic analy

either answer/question score > 50?

"""

## in both body and tags
keywords = [
" lda ",
"topic analy"
]

## Only in tags
keytags = [
## How to handle the tags
"<lda>", 
"topic-modeling"
]


import os
import json
from shutil import copyfile
from pathlib import Path

output_question_path = "questionsCodeOrigin/"
output_answer_path = "answersCode/"

output_path_Q = "questionsLDA/"
output_path_A = "answersLDA/"

import xml.etree.ElementTree
from bs4 import BeautifulSoup


for post_f in os.listdir(output_question_path):
    qRoot = xml.etree.ElementTree.parse(output_question_path+post_f).getroot()
    post_id = qRoot.get('Id')
    answer_id = qRoot.get('AcceptedAnswerId')
    body = qRoot.get('Body')   
    
    score = qRoot.get('Score')   
    ## handle it later
    code = BeautifulSoup(body, 'lxml').code
    ## ensure enough length of code snippet
    #if len(str(code)) < 100:
    #    continue
    score_flag = False
    ## Either high score Q or A
    if int(score) >= 50:
        score_flag = True
    tags = qRoot.get('Tags')

    ## clean html tags
    body = BeautifulSoup(body, "lxml").text
    
    if any(keyword in body.lower() for keyword in keywords) or any(keytag in tags.lower() for keytag in keytags):        
        answer_file = output_answer_path+"post_"+answer_id+".xml"
        if Path(answer_file).exists():
            aRoot = xml.etree.ElementTree.parse(answer_file).getroot()
            ascore = qRoot.get('Score')
            if int(ascore) >= 50:
                score_flag = True
            
            #if not score_flag:
            #    continue
            copyfile(output_question_path+"post_"+post_id+".xml", output_path_Q+"post_"+post_id+".xml")
            copyfile(answer_file, output_path_A+"post_"+answer_id+".xml")
