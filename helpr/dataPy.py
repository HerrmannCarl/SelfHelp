import yaml
import datetime
from helpr.db import get_db

import click
from flask import current_app, g
from flask.cli import with_appcontext


def load_questions(file):
    """Loads questions; returns a yaml as a text"""
    filename = file

    with open(filename, 'r') as stream:
        data = yaml.safe_load(stream)
    # print(data)
    return data

def get_questions(faketime=False):
    """Loads questions from the YAML, returns them as a two lists"""
    filename = "helpr/data/questions.yml"
    loaded_data = load_questions(filename)
    # print("loaded_data:",loaded_data)
    tf_questions = loaded_data["Questions"]["True-False"]
    lf_questions = loaded_data["Questions"]["Longform"]

    tf = []
    lf = []
    for q in tf_questions:
        # print("q is: ",q)
        # print("q[currently_active]",q["currently_active"])
        if q["currently_active"]:
            if q["morning"] and is_morning(faketime = faketime):
                d = {"question":q["question"],"id":q["id"]}
                tf.append(d)
            if q["evening"] and is_evening(faketime = faketime):
                d = {"question":q["question"],"id":q["id"]}
                tf.append(d)

    for q in lf_questions:
        # print("q is: ",q)
        # print("q[currently_active]",q["currently_active"])
        if q["currently_active"]:
            if q["morning"] and is_morning(faketime = faketime):
                d = {"question":q["question"],"id":q["id"]}
                lf.append(d)
            if q["evening"] and is_evening(faketime = faketime):
                d = {"question":q["question"],"id":q["id"]}
                lf.append(d)
                
    # print("true-false questions: ",tf)
    # print("longform questions: ",lf)
    return [tf,lf]


def save_all_questions():
    """Saves the questions from the database to a yaml file."""
    db = get_db()
    ans = db.execute("SELECT * FROM question").fetchall()
    tf = []
    lf = []
    for a in ans:
        d = {}
        d["question"] = a["question"]
        d["morning"] = a["active_morning"]
        d["evening"] = a["active_evening"]
        d["created"] = a["created"]
        d["id"] = a["id"]
        d["currently_active"] = 1
        if a["question_type"] == "true-false":tf.append(d)
        if a["question_type"] == "longform":lf.append(d)
    d = {}
    d["schema_version"] = 1
    d["Questions"] = {"True-False":tf,"Longform":lf}

    t_out = yaml.dump(d)
    # print("text_out is: ",t_out)
    with open("helpr/data/questions.yml", "w+") as file_out:
        file_out.write(t_out)       

def save_answer():
    """ Adds one answer to the yaml file. """
    pass

def save_all_answers():
    """ Saves all answers from the sql dtabase to a yaml file """
    db = get_db()
    ans = db.execute("SELECT DISTINCT answer_id FROM answer").fetchall()
    lis = []
    for a in ans: 
        lis.append(a["answer_id"])
    d = {"schema_version":1}
    d["answers"] = []
    
    # print("answer IDs: ",lis)
    for a in lis: 
        # Iterate through the answers.
        
        ans = db.execute("SELECT * FROM answer WHERE answer_id = ?",(str(a)),).fetchall()
        one_ans = {"answer_id":ans[0]["answer_id"]}
        one_ans["timestamp"] =str(ans[0]["created"])

        qs = db.execute("SELECT DISTINCT id,question_id,answer_id from answer WHERE answer_id = ?"
                        " ORDER BY question_id ASC",(a,)).fetchall()
        ql = []
        for q in qs:
            q_id = q["question_id"]
            q_text = db.execute("SELECT id, question FROM question WHERE id = ?",(q_id,)).fetchall()[0]["question"]
            a_text = db.execute("SELECT answer FROM answer WHERE answer_id = ? AND question_id = ?",(str(a),q_id,)).fetchall()[0]["answer"]
            a_id =  db.execute("SELECT id FROM answer WHERE answer_id = ? AND question_id = ?",(str(a),q_id,)).fetchall()[0]["id"]
            q_dict = {"question_id":q_id,"question_text":q_text,"answer":a_text,"instance_id":a_id}
            
            ql.append(q_dict)
        
        # Add the questions list to that answer group
        one_ans["answer"] = ql
        
        # Append the answergroup to the list of answers
        d["answers"].append(one_ans)
        
    # print("*"*10)
    # print(d["answers"])
    # print(d["answers"][0])
    # for e in d["answers"]:
    #     for k in e.keys():
    #         print("e[{}]is: {}".format(k,e[k]))
        
    # turn D in to yaml. 
    t_out = yaml.dump(d)
    with open("helpr/data/answers.yml", "w+") as file_out:
        file_out.write(t_out)          

def is_evening(faketime = False):
    """Tells you if it's evening or not".  Returns True / False"""
    if faketime:
        now = faketime
    else: 
        now = datetime.datetime.now()
    hour = now.hour
    if ((hour > 18) and (hour < 24)) or (hour<4):
        return True
    return False 

def is_morning(faketime = False):
    """Tells you if it's morning or not.  Returns true / false"""
    if faketime:
        now = faketime
    else: 
        now = datetime.datetime.now()
    hour = now.hour
    if (hour > 6) and (hour < 13):
        return True
    return False 

@click.command('save-all-answers')
@with_appcontext
def save_all_answers_command():
    """Save the answers from the database to a yaml."""
    save_all_answers()
    click.echo('Answers Saved.')
    
@click.command('save-all-questions')
@with_appcontext
def save_all_questions_command():
    """Save the questions from the database to a yaml."""
    save_all_questions()
    click.echo('Questions Saved.')


def init_app(app):
    app.cli.add_command(save_all_answers_command)
    app.cli.add_command(save_all_questions_command)