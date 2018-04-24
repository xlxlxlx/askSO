"""
either answer/question score < 0

"""


import os
import json
from shutil import copyfile
from pathlib import Path

post_path = "../output/questionsMLLow/"

#post_path = "E:/tmp/output/questionsMLHigh/"

code_path = post_path+"code/"
#text_path = post_path+"text/"


score_thre = 0

import xml.etree.ElementTree
from bs4 import BeautifulSoup


for post_f in os.listdir(post_path):
    if not post_f.endswith(".xml"):
        continue
    qRoot = xml.etree.ElementTree.parse(post_path+post_f).getroot()
    post_id = qRoot.get('Id')
    body = qRoot.get('Body')   
    
    
    codeFinder = BeautifulSoup(body, 'lxml').findAll('code')
    
    if not codeFinder:
        continue
    
    code = "\n".join(str(tag).replace('&gt;','>').replace('&lt;','<') for tag in codeFinder)
    

    
    with open(code_path+"post_"+post_id+"_code.txt","w", encoding='utf-8') as outf:
        outf.write(code)
    
    