import sqlite3

import click
import yaml
from flask import current_app, g
from flask.cli import with_appcontext
from . import dataPy

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def config_db():
    db = get_db()

    filename = "helpr/data/questions.yml"
    loaded_data = dataPy.load_questions(filename)
    tf_questions = loaded_data["Questions"]["True-False"]
    lf_questions = loaded_data["Questions"]["Longform"]
    for q in tf_questions:
        q["type"]="true-false"
    for q in lf_questions:
        q["type"]="longform"

    qs = []
    qs.extend(tf_questions)
    qs.extend(lf_questions)
    
    # print("configuring the DB")
    # print("qs: ",qs)

    for q in qs:
        # a = q["morning"]*1
        # print("a is:",a)
        db.execute(
        "INSERT INTO question (question, id, question_type,active_morning,active_evening) VALUES (?,?, ?,?,?)",
        (q["question"], q["id"], q["type"],q["morning"]*1,q["evening"]*1),
        )
    db.commit()

def load_answers():
    """Clears the answers database, and answers from the yaml to the database."""
    filename = "helpr/data/answers.yml"
    db = get_db()
    
    db.execute("DELETE FROM answer")
    db.commit()

    with open(filename, 'r') as stream:
        data = yaml.safe_load(stream)
    
    # print("data is:",data)
    # print("*"*5)
    # print("data['answers'][0]\n",data['answers'][0])
    for ans in data["answers"]:
        a_id = ans["answer_id"]
        a_ts = ans["timestamp"]
        # print("a_id:",a_id)
        # print("a_ts",a_ts)
        for q in ans["answer"]:
            # print("q is:")
            # print(q,"\n")
            q_id = int(q["question_id"])
            q_ans = q["answer"]
            # i_id = q["instance_id"]
        # print("-",ans["answer"],"\n")
            db.execute("INSERT INTO answer (answer_id,question_id,created,answer) VALUES (?,?,?,?)",(a_id,q_id,a_ts,q_ans),)
    db.commit()

def get_questions():
    db = get_db()
    questions = db.execute(
        'SELECT * FROM question ORDER BY id DESC'
    ).fetchall()
    return questions

def get_answers():
    db = get_db()
    answers = db.execute('SELECT * FROM answer ORDER BY id DESC').fetchall()
    return answers

def get_new_answer_id():
    db = get_db()
    answer = db.execute('SELECT max(answer_id) FROM answer').fetchone()
    # print("answer is: ",answer)
    a = answer["max(answer_id)"]
    # print("answer['max(answer_id)'] is:",a)
    # if not a: print ("None evaluates to false!")
    # for k in answer.keys():
    #     print("k: {}\t answer:{}".format(k,answer[k]))
    if not a: 
        return 1
    else:
        return answer[0]+1

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('config-db')
@with_appcontext
def config_db_command():
    """Configure the DB question with info from the YAML files."""
    config_db()
    click.echo('Configured the database.')

@click.command('db-show-questions')
@with_appcontext
def show_questions_command():
    """Show what questions the database is configured to ask."""
    qs= get_questions()
    ks = qs[0].keys()
    l = ""
    for k in ks:
        l+= "{:17}".format(str(k))
    l+= "\n"

    for q in qs:
        for k in ks:
            l+= "-" + "{:15}".format(str(q[k]))[0:15] + " "
        l+="\n"
    click.echo("Conifigured Questions (vales may be truncated):")
    click.echo(l)
    
@click.command('db-seed-answers')
@with_appcontext
def seed_answers_command():
    """Seed the "answers" database with some data, for testing."""
    db = get_db()
    a1 = {"question_id":1,"text":"yes","answer_id":1}
    a2 = {"question_id":2,"text":"no","answer_id":1}
    a3 = {"question_id":101,"text":"WHY IS EVERYTHING SO PAINFUL?","answer_id":1}
    a4 = {"question_id":1,"text":"yes","answer_id":2}
    a5 = {"question_id":2,"text":"yes","answer_id":2}
    ans = [a1,a2,a3,a4,a5]
    for a in ans: 
        db.execute(
        "INSERT INTO answer (question_id,answer,answer_id) VALUES (?,?,?)",
        (a["question_id"],a["text"],a["answer_id"]),
        )
    db.commit()
    click.echo("Data seeeded.")

@click.command('db-show-answers')
@with_appcontext
def show_answers_command():
    """Show the content of the "answers" database."""
    ans = get_answers()
    click.echo("Answers (values maybe truncated): ")
    
    ks = ans[0].keys()
    l = ""
    for k in ks:
        l+= "{:17}".format(str(k))
    l+= "\n"

    for a in ans:
        for k in ks:
            l+= "-" + "{:15}".format(str(a[k]))[0:15] + " "
        l+="\n"
    click.echo(l)

@click.command('db-load-answers')
@with_appcontext
def load_answers_command():
    """Loads answers from the yaml to the database."""
    load_answers()
    click.echo('Answers loaded to database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(config_db_command)
    app.cli.add_command(show_questions_command)
    app.cli.add_command(seed_answers_command)
    app.cli.add_command(show_answers_command)
    app.cli.add_command(load_answers_command)