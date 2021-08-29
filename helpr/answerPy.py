import functools
from . import dataPy
import datetime
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

def answerPage():
    """
    This page lets you answer questions.
    """
    faketime = datetime.datetime.now()
    faketime = faketime.replace(hour = 10)
    print("faketime is: ",faketime)
    [tf,lf]=dataPy.get_questions(faketime)
    
    if request.method == 'POST':
        ans = []
        for answer in request.form:
            ans.append(request.form[answer])
        answers=json.dumps(ans)
        
        qs = []
        for q in tf:
            qs.append(q)
        for q in lf:
            qs.append(q)
        questions=json.dumps(qs)
        
        return redirect(url_for('answer_submit',questions=questions,answers=answers))
    return render_template('answer.html',tf = tf,lf = lf)

def answerSubmit():
    """
    This page shows up after you submit your answers
    """
    answers=request.args['answers']
    questions=request.args['questions']
    ans = json.loads(answers)
    qs = json.loads(questions)
    return render_template('answer_submit.html',questions=qs,answers = ans)

