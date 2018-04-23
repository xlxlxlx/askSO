#import os
import json

post_f = "Posts.xml"
output_question_path = "questionsCodeOrigin/"
output_answer_path = "answersCode/"
output_other_answer_path = "answersCode_highscore/"

dict_question_answer = {}
dict_question_answer_highscore = {}

## Ordered by creation time
with open(post_f, encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line.startswith("<row"):
            continue
        
        ## We now have a postid
        post_id = line.split('Id="')[1].split('"')[0]
        
        ## This is a question post with accepted answer, and a code snippet
        if "AcceptedAnswerId" in line and "&lt;code&gt" in line:
            ac_id = line.split('AcceptedAnswerId="')[1].split('"')[0]
            dict_question_answer[post_id] = ac_id
            with open(output_question_path+"post_"+post_id+".xml","w", encoding='utf-8') as outf:
                outf.write(line)
                
        ## This is an answer post with a parent question, within the filtered questions
        elif "ParentId" in line:
            question_id = line.split('ParentId="')[1].split('"')[0]
            if not question_id in dict_question_answer:
                score = int(line.split('Score="')[1].split('"')[0])
                if ("&lt;code&gt" in line) and (score > 50):
                    with open(output_other_answer_path+"post_"+post_id+".xml","w", encoding='utf-8') as outf:
                        outf.write(line)
                    dict_question_answer_highscore[question_id] = post_id
                else:
                    continue
            with open(output_answer_path+"post_"+post_id+".xml","w", encoding='utf-8') as outf:
                outf.write(line)
        

with open("QAmappingCodeQ.json","w") as metaf:        
    metaf.write(json.dumps(dict_question_answer))

with open("QAmappingCodeQ_highscore.json","w") as metaf:        
    metaf.write(json.dumps(dict_question_answer_highscore))

