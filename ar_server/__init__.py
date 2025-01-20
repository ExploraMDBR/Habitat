import os
import traceback

from flask import Flask, jsonify, make_response, redirect, url_for
from flask.cli import with_appcontext

from werkzeug.exceptions import NotFound

import firebase_admin
from . import utils as u

import click

import configparser

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, static_url_path='/static')

    app.config.from_mapping(
        SECRET_KEY='deva',
        DATABASE=os.path.join(app.instance_path, 'ar_db.sqlite'),
        FIREBASE_CONF=os.path.join(app.instance_path, 'explora-ar-firebase-adminsdk-uu9o5-5279556646.json'),
        MAX_FILE_SIZE = 20 * 1024 * 1024, # 20Mb
        MARKER_NUM = 15,
        DEF_MODEL = "/static/ar/models/Explora_default_AR_model.glb"
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    msgs = configparser.ConfigParser()
    try:
        msgs.read(os.path.join(app.instance_path, 'messages.ini'))
        app.config['MESSAGES'] = msgs['MESSAGES']
        
    except Exception as e:
        pass


    # a simple page that report status
    @app.route('/status')
    def hello():
        resp = {'message': 'running'}
        if app.config['DEBUG']:
            resp["env"] = "dev"
        return jsonify(resp) 

    from . import db
    db.init_app(app)


    from . import home
    app.register_blueprint(home.bp)

    from . import user
    app.register_blueprint(user.bp)

    from . import dashboard
    dashboard.register_blueprints(app)

    @app.errorhandler(Exception)
    def _(error):
        if isinstance(error, NotFound):
            return make_response( "not found", 404 )
            # return redirect(url_for('not_found'))

        err_id = u.get_error_id()

        app.logger.error('[ Generic error | error_id: %s ] %s\n%s---' % (err_id, error, traceback.format_exc()) )

        int_error = jsonify({"status": "error", "reason": "internal error", "error_id": err_id})
        return make_response( int_error, 500 )


    return app
