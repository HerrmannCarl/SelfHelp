import click
from flask import current_app, g
from flask.cli import with_appcontext
from shutil import copy2

def save_production_db():
    try: 
        copy2("instance/helpr.sqlite","backup/helpr.sqlite")
    except FileNotFoundError:
        print("Cannot backup SQL database - production database missing!")

def load_production_db():
    try:
        copy2("backup/helpr.sqlite","instance/helpr.sqlite")
    except FileNotFoundError:
        print("Cannot load backup SQL Datbase - production database missing!") 
        
def save_production_yamls():
    try: 
        copy2("helpr/data/answers.yml","backup/answers.yml")
        copy2("helpr/data/questions.yml","backup/questions.yml")
    except FileNotFoundError:
        print("Cannot backup yml files - files missing!")

def load_production_yamls():
    try: 
        copy2("backup/answers.yml","helpr/data/answers.yml")
        copy2("backup/questions.yml","helpr/data/questions.yml")
    except FileNotFoundError:
        print("Cannot load backup yml files - files missing!")

@click.command('tooling-save-db')
@with_appcontext
def save_production_db_command():
    """saves a production database."""
    save_production_db()
    click.echo('Production DB saved.')

@click.command('tooling-load-db')
@with_appcontext
def load_production_db_command():
    """Loads a production database."""
    load_production_db()
    click.echo('Database backup loaded')

@click.command('tooling-load-yml')
@with_appcontext
def load_production_yamls_command():
    """Loads a the backup yaml."""
    load_production_yamls()
    click.echo('Yaml backup loaded.')    

@click.command('tooling-save-yml')
@with_appcontext
def save_production_yamls_command():
    """Production yamls saved."""
    save_production_yamls()
    click.echo('Yaml backup saved.')

@click.command("tooling-questions-to-yml")
@with_appcontext
def save_questions_to_yaml_command():
    from helpr.dataPy import save_all_questions
    save_all_questions()
    click.echo("Quesions saved to yaml.")

@click.command("tooling-answers-to-yml")
@with_appcontext
def save_answers_to_yaml_command():
    from helpr.dataPy import save_all_answers
    save_all_answers()
    click.echo("Answers saved to yaml.")
    
@click.command("tooling-init-db")
@with_appcontext
def init_db_command():
    from helpr.db import init_db
    init_db()
    click.echo("Database initialized.")

@click.command("tooling-config-db")
@with_appcontext
def config_db_command():
    from helpr.db import config_db
    config_db()
    click.echo("Database Questions Configured.")

def init_app(app):
    app.cli.add_command(save_production_db_command)
    app.cli.add_command(load_production_db_command)
    app.cli.add_command(save_production_yamls_command)
    app.cli.add_command(load_production_yamls_command)
    app.cli.add_command(save_questions_to_yaml_command)
    app.cli.add_command(save_answers_to_yaml_command)
    app.cli.add_command(init_db_command)
    app.cli.add_command(config_db_command)