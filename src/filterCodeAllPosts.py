#import os
import json

post_f = "Post100.xml"
out_question_path = "questions_code/"
out_answer_path = "answers_code/"

dict_question_answer = {}

with open(post_f, encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line.startswith("<row"):
            continue
        ## With code snippet
        if not "&lt;code&gt" in line:
            continue
        
        ## We now have a postid
        post_id = line.split('Id="')[1].split('"')[0]
        
        ## This is a question post with accepted answer
        if "AcceptedAnswerId" in line:
            ac_id = line.split('AcceptedAnswerId="')[1].split('"')[0]
            dict_question_answer[id] = ac_id
            with open(output_question_path+"post_"+post_id+".xml","w", encoding='utf-8') as outf:
                outf.write(line)
        ## This is an answer post with a parent question
        elif "ParentId" in line:
            question_id = line.split('ParentId="')[1].split('"')[0]
            dict_question_answer[question_id] = post_id
            with open(output_answer_path+"post_"+post_id+".xml","w", encoding='utf-8') as outf:
                outf.write(line)
        


## Dump dict to json            
#with open("commentPost.json","w") as metaf:        
    #metaf.write(json.dumps(dict_comment_post))
with open("postComment.json","w") as metaf:        
    metaf.write(json.dumps(dict_post_comment))

