import functools
from . import dataPy
import datetime
import json
from copy import deepcopy
from helpr.db import get_db, get_new_answer_id


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

def configPage():
    """
    This page lets you configure the questions that get asked.
    """
    # if request.method == 'POST':
    #     pass
    db = get_db()
    
    output = db.execute("SELECT * FROM question").fetchall()
    keys = output[0].keys()
    
    return render_template('config.html',fields = keys,questions = output)
