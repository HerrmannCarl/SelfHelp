import functools
from . import dataPy
import datetime
import json
from copy import deepcopy
from helpr.db import get_db, get_new_answer_id


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

def answerPage():
    """
    This page lets you answer questions.
    """
    faketime = datetime.datetime.now()
    # faketime = faketime.replace(hour = 10)
    print("faketime is: ",faketime)
    [tf,lf]=dataPy.get_questions(faketime)
    
    if request.method == 'POST':
        ans = []
        for answer in request.form:
            ans.append(request.form[answer])
       
        # print("answers are: ",answers)
        # print("answers type: ",type(answers))
        # print("type ans: ",type(ans))
        
        qs = []
        i = 0
        for q in tf:
            d = deepcopy(q)
            d["answer"] = ans[i]
            qs.append(d)
            i+=1
        for q in lf:
            d = deepcopy(q)
            d["answer"] = ans[i]
            qs.append(d)
            i+=1
        questions=json.dumps(qs)
        
        db = get_db()
        
        answer_id = get_new_answer_id()
        print("answer id is: ",answer_id)
        for q in qs: 
            db.execute(
            "INSERT INTO answer (question_id,answer,answer_id) VALUES (?,?,?)",
            (q["id"],q["answer"],answer_id),
            )
        db.commit()
        
        return redirect(url_for('answer_submit',questions=questions))
    return render_template('answer.html',tf = tf,lf = lf)

def answerSubmit():
    """
    This page shows up after you submit your answers
    """
    try: 
        questions=request.args['questions']
    except KeyError:
        questions = "{}"
    # print("questions are: ",questions)
    qs = json.loads(questions)
    # print("questions are: ",qs)
    db = get_db()
    ts = db.execute("SELECT * FROM answer ORDER BY answer_id DESC,question_id ASC").fetchall()
    array_list = []
    warn_string = ""
    
    print("len(ts):",len(ts))
    if len(ts)==0:
        warn_string = "Warning: answers database is empty"
    else:
        ks = ts[0].keys()
        head_list=[]
        for k in ks:
            head_list.append(str(k))

        array_list = [head_list]
        for t in ts:
            test = []
            for k in head_list:
                test.append(t[k])
            array_list.append(test)

    return render_template('answer_submit.html',questions=qs,array_list = array_list,warn_string=warn_string)

