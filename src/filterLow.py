"""
either answer/question score < 0

"""


import os
import json
from shutil import copyfile
from pathlib import Path

output_question_path = "../output/questionsML/"
output_answer_path = "../output/answersML/"

output_path_Q = "../output/questionsMLLow/"
output_path_A = "../output/answersMLLow/"

score_thre = 0

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
    if len(str(code)) < 100:
        continue
    score_flag = False
    ## Either high score Q or A
    if int(score) < score_thre:
        score_flag = True
    tags = qRoot.get('Tags')

    ## clean html tags
    body = BeautifulSoup(body, "lxml").text
    
       
    answer_file = output_answer_path+"post_"+answer_id+".xml"
    if Path(answer_file).exists():
        aRoot = xml.etree.ElementTree.parse(answer_file).getroot()
        ascore = qRoot.get('Score')
        if int(ascore) < score_thre:
            score_flag = True
        
        if not score_flag:
            continue
        copyfile(output_question_path+"post_"+post_id+".xml", output_path_Q+"post_"+post_id+".xml")
        copyfile(answer_file, output_path_A+"post_"+answer_id+".xml")
