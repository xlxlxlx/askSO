"""
either answer/question score < 0

"""


import os
import json
from shutil import copyfile
from pathlib import Path


ref_path = "../output/questionsMLHigh/"

output_question_path = "../output/questionsPositive/"
output_answer_path = "../output/answersPositive/"

output_path_Q = "../output/questionsMLMed/"
output_path_A = "../output/answersMLMed/"

score_thre = 0

import xml.etree.ElementTree
from bs4 import BeautifulSoup


for post_f in os.listdir(output_question_path):
    
    the_file = ref_path+post_f
       
    if Path(the_file).exists():
        continue
        
    qRoot = xml.etree.ElementTree.parse(output_question_path+post_f).getroot()
    post_id = qRoot.get('Id')
    answer_id = qRoot.get('AcceptedAnswerId')
    
       
    answer_file = output_answer_path+"post_"+answer_id+".xml"
    if Path(answer_file).exists():
        copyfile(output_question_path+"post_"+post_id+".xml", output_path_Q+"post_"+post_id+".xml")
        copyfile(answer_file, output_path_A+"post_"+answer_id+".xml")
