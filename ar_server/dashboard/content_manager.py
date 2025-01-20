import datetime
import traceback
import json

from .api import objects_get_dict
from urllib.parse import urlparse, urljoin

from flask import (
	Blueprint, current_app, g, redirect, 
	render_template, request, url_for, 
	make_response, jsonify, session, flash, 
	current_app
)
from werkzeug.exceptions import abort
from functools import wraps

from ..db import get_db, sqlite3
from ..auth import auth_check_dashboard, User

bp = Blueprint('content_manager', __name__, url_prefix='/dashboard/content')



@bp.route('/', methods=('GET',)) 
@auth_check_dashboard(redirect_to_login=True)
def index(user=None):
	try:
		data = objects_get_dict()
	except Exception as e:
		err_id = u.get_error_id()

		current_app.logger.error('[ Get objects list error (content_manager)| error_id: %s ] %s\n%s---' % (err_id, e, traceback.format_exc()) )

		int_error = jsonify({"status": "error", "reason": "internal error", "error_id": err_id})
		return make_response( int_error, 500 )
	
	MARKER_NUM = current_app.config['MARKER_NUM']
	markers = {ob['marker'] for ob in data}
	free_markers = [n for n in range(MARKER_NUM) if n not in markers]

	return render_template('dashboard/content_manager.html', data=data, 
										free_markers = free_markers, 
										marker_num = MARKER_NUM,
										show_slot =int(request.args.get('show_slot', -1)),
										message = request.args.get('msg', ""))
