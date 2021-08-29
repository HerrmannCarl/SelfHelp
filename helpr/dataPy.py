import yaml
import datetime

def load_questions(file):
    filename = file

    with open(filename, 'r') as stream:
        data = yaml.safe_load(stream)
    # print(data)
    return data

def get_questions(faketime=False):
    filename = "helpr/data/questions.yml"
    loaded_data = load_questions(filename)
    tf_questions = loaded_data["Questions"]["True-False"]
    lf_questions = loaded_data["Questions"]["Longform"]

    tf = []
    lf = []
    for q in tf_questions:
        # print("q is: ",q)
        # print("q[currently_active]",q["currently_active"])
        if q["currently_active"]:
            if q["morning"] and is_morning(faketime = faketime):
                tf.append(q["question"])
            if q["evening"] and is_evening(faketime = faketime):
                tf.append(q["question"])

    for q in lf_questions:
        # print("q is: ",q)
        # print("q[currently_active]",q["currently_active"])
        if q["currently_active"]:
            if q["morning"] and is_morning(faketime = faketime):
                lf.append(q["question"])
            if q["evening"] and is_evening(faketime = faketime):
                lf.append(q["question"])

    # print("true-false questions: ",tf)
    # print("longform questions: ",lf)
    return [tf,lf]

def is_evening(faketime = False):
    if faketime:
        now = faketime
    else: 
        now = datetime.datetime.now()
    hour = now.hour
    if ((hour > 18) and (hour < 24)) or (hour<4):
        return True
    return False 

def is_morning(faketime = False):
    if faketime:
        now = faketime
    else: 
        now = datetime.datetime.now()
    hour = now.hour
    if (hour > 6) and (hour < 13):
        return True
    return False 