
import random
import traceback

from flask import (
	Blueprint, current_app, g, redirect, 
	render_template, request, url_for, 
	make_response, jsonify, session, flash
)
from werkzeug.exceptions import abort
from os.path import join

from . import utils as u
from .dashboard.api import objects_get_dict

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/', methods=('GET',)) 
def index():
	try:
		data = objects_get_dict()
		print(data)
	except Exception as e:
		err_id = u.get_error_id()

		current_app.logger.error('[ Get objects list error (home)| error_id: %s ] %s\n%s---' % (err_id, e, traceback.format_exc()) )

		int_error = jsonify({"status": "error", "reason": "internal error", "error_id": err_id})
		return make_response( int_error, 500 )

	return render_template('home.html', data=data)

@bp.route('/minimal', methods=('GET',)) 
def minimal():
	return render_template('viewer_minimal.html', data={})

# MAX_CARDS = 10

# @bp.route('/end', methods=('GET',)) 
# def end():
# 	return render_template('cards/end.html')


# @bp.route('/continue', methods=('GET',)) 
# def card_continue():
# 	card_id = request.args.get('card_id')
# 	c_uid = session.get('_ar_user_id', None)

# 	# render templates in case the request is not valid
# 	if not c_uid:
# 		return redirect(url_for("cards.index"))

# 	if not card_id:
# 		return redirect(url_for("cards.index"))

# 	#convert card_id to int
# 	try:
# 		card_id = int(card_id)
# 	except Exception as e:
# 		flash("card_id should be an integer")
# 		return render_template('cards/home.html')


# 	map_image = "map_not_found.jpg"
# 	map_image =  url_for('static', filename=map_image)
 
# 	try:
# 		card_data = api.objects_get_dict(card_id)
# 		map_image = card_data[0]["mapimage"]
# 	except Exception as e:
# 		pass

# 	return render_template('cards/continue.html', first_card=request.path+"?card_id=0", map_image= map_image)	





# enigma_keys = ["enigma{}".format(i) for i in range(10)]

# @bp.route('/badges', methods=('GET', 'POST')) 
# def badges():
# 	card_id = request.args.get('card_id', None)

# 	c_uid = session.get('_ar_user_id', None)
# 	if not c_uid:
# 		return render_template('cards/init.html', first_card=request.host_url+"?card_id=0")		

# 	if card_id is not None:
# 		try:
# 			card_id = int(card_id)
# 		except Exception as e:
# 			flash("card_id should be an integer")
# 			return render_template('cards/home.html')

# 	new_badge = -1
# 	if request.method == 'POST':
# 		if not card_id is not None:
# 			flash("A card_id is required to POST a new badge")
# 			return render_template('cards/home.html')

# 		play_time = request.form.get('play_time')
		
# 		enigma_key = None
# 		try:
# 			enigma_key = enigma_keys[card_id]
# 		except (KeyError, IndexError):
# 			flash("Card not found: {}".format(card_id))
# 			return render_template('cards/home.html')

# 		db = get_db()
# 		db.execute('''UPDATE users SET 
# 					lastseen = CURRENT_TIMESTAMP,
# 					firstanswer = case when firstanswer then
# 									firstanswer
# 								   else
# 									CURRENT_TIMESTAMP
# 								   end,
# 					playtime = playtime + ?,
# 					{} = ?
# 					WHERE id = ?;'''.format(enigma_key), (play_time, 1, c_uid))
# 		db.commit()	
# 		new_badge = card_id


# 		tempres = db.execute("SELECT playtime from users WHERE id = ?", (c_uid,)).fetchone()

# 	user_data = user.user_get_dict(c_uid)
# 	if not user_data:
# 		return render_template('cards/init.html', first_card=request.host_url+"?card_id=0")

# 	user_badges = [user_data["enigma0"], user_data["enigma1"], user_data["enigma2"],
# 					user_data["enigma3"], user_data["enigma4"], user_data["enigma5"],
# 					user_data["enigma6"], user_data["enigma7"], user_data["enigma8"],
# 					user_data["enigma9"]]
	
# 	map_image = "map_not_found.jpg"
# 	map_image =  url_for('static', filename=map_image)
 
# 	if card_id is not None:
# 		try:
# 			card_data = api.objects_get_dict(card_id)
# 			map_image = card_data[0]["mapimage"]
# 		except Exception as e:
# 			err_id = u.get_error_id()
# 			current_app.logger.error('[ Get cards list error (api /badges) | error_id: %s ] %s\n%s---' % (err_id, e, traceback.format_exc()) )
# 			int_error = jsonify({"status": "error", "reason": "internal error", "error_id": err_id})
# 			return make_response( int_error, 500 )
	
# 		back_to_card = request.host_url+"?card_id={}".format(card_id)
# 		scan = request.host_url+"continue?card_id={}".format(card_id)

# 	else:
# 		map_image = None
# 		back_to_card = None
# 		scan = None
# 		card_data = [{"postdata":""}]

# 	return render_template('cards/badge.html',
# 							back_to_card = back_to_card, 
# 							new_badge= new_badge, 
# 							user_badges= user_badges,
# 							map_image= map_image,
# 							postdata = card_data[0]["postdata"],
# 							scan = scan)