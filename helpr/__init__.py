import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'helpr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!11!'

    from . import vote
    app.register_blueprint(vote.bp)
    
    from . import answerPy
    @app.route('/answer',methods=('GET', 'POST'))
    def answer():
        return answerPy.answerPage()
    
    @app.route('/answer_submit')
    def answer_submit():
        return answerPy.answerSubmit()

    from . import configPy
    @app.route("/config",methods = ("GET", 'POST'))
    def config():
        return configPy.configPage()
    
    from . import db
    db.init_app(app)

    from . import dataPy
    dataPy.init_app(app)

    from . import tooling
    tooling.init_app(app)

    return app