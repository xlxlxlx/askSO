#! usr/bin/python
#coding=utf-8
# -*- coding:cp936 -*-
import os

post_path = "../output/questionsMLLow/"

code_path = post_path+"code/"

out_file = '../output/codeGuessSumLow_Q.txt'



for code_f in os.listdir(code_path):
    
    if not code_f.endswith("txt"):
        continue
    cmd = 'echo %s >> %s' 
    cmd = cmd %(code_f, out_file)
    os.system(cmd)
    
    guesslang_cmd = 'guesslang -i %s%s >> %s' 
    cmd = guesslang_cmd % (code_path, code_f, out_file)
    os.system(cmd)
    
    cmd = 'echo -e "\n" >> %s'
    cmd = cmd %(out_file)
    os.system(cmd)
    