import datetime
import traceback
import zipfile

from flask import (
	Blueprint, current_app, g, redirect, 
	render_template, request, url_for, 
	make_response, jsonify
)
from werkzeug.exceptions import abort

from ..db import get_db
from .. import utils as u
from ..auth import auth_check_dashboard

from os.path import (basename, splitext, 
						join, dirname, realpath, isfile,
						exists)
from os import remove, makedirs
import shutil


ALLOWED_IMGS_EXT = ['.jpg', '.jpeg', '.JPG', '.JPEG', '.PNG', '.png']

content_dir = "content"
content_bk_dir = "content/prev"

path = join("../static", content_dir)
bk_path = join("../static", content_bk_dir)

file_path = realpath(join(dirname(realpath(__file__)), path))
file_bk_path = realpath(join(dirname(realpath(__file__)), bk_path))

bp = Blueprint('api_content', __name__, url_prefix='/content')

maker_img_fmt = 'ar/barcodes/{:02d}.png'

def objects_get_dict(obj_id = None):
	response = []
	
	db = get_db()
	
	if obj_id is None:
		res = db.execute("SELECT * FROM objects")
		res = res.fetchall()
	
	else:
		res = db.execute("SELECT * FROM objects WHERE id = ?", (obj_id,))
		res = res.fetchall()

	for row in res:
		response.append({k:row[k] for k in row.keys()})
		if response[-1]['model'] == "__default__":
			 response[-1]['model'] = current_app.config['DEF_MODEL']
			 response[-1]['default'] = True
		else:
			 response[-1]['default'] = False

		response[-1]["markerImage"] = url_for('static', filename=maker_img_fmt.format(int(row['marker'])))

	return response


def prepare_folder(slot):
	folder = join(file_path, str(slot))
	dest = join(file_bk_path, str(slot))

	if exists(folder):
		if exists(dest):
			shutil.rmtree(dest)
		shutil.move(folder, file_bk_path)
	
	makedirs(folder)
	
	return folder

def handle_file(data, filename, slot):
	ext = splitext(filename)

	current_app.logger.debug("Handling file %s, ext: %s",filename, ext)

	ret = {"status": "not saved", 
			"file": filename, 
		 	"filetype": None,
			"gltf_file" : None,
			"obj_file" : None,
			"mtl_file" : None,
			"base_url" : None,
		  	"file_urls" : [],
			"textures" : [],
		   	"reason": "not set"}

	if ext[1] in ['.glb', '.zip']:
		dest = prepare_folder(slot)
		ret['base_url'] = url_for("static", filename=join(content_dir, str(slot)))
		current_app.logger.debug("Save to %s",dest)
	else:
		current_app.logger.debug("File not saved, extension not allowed %s",filename)
		ret["reason"] = "File extension not allowed: {}".format(filename)
		return make_response( jsonify(ret),	415 )

	if ext[1] == ".glb":
		dest = join(dest, filename)
		save_file(data, dest)
		ret['status'] = 'ok'
		ret['filetype'] = "GLTF"
		ret['gltf_file'] = filename
		ret['file_urls'] = [url_for("static", filename=join(content_dir, str(slot), filename))]
	elif ext[1] == ".zip":
		status = unzip(data, dest, url_for("static", filename=join(content_dir, str(slot))))
		ret.update(status)

	if ret['status'] == 'ok':
		return jsonify(ret)

	if ret['status'] == 'bad file':
		current_app.logger.debug("Bad file, not saved: {} | reason: {}".format(filename, ret['reason']))
		return make_response(jsonify(ret), 415)

	raise u.Upload_File_Error("Error during file handling")

def inspect_zip(zip_ref, base_url):
	info = []
	urls = []
	gltf_file = None
	obj_file = None
	mtl_file = None
	filetype = None
	textures = []

	for item in zip_ref.infolist():
		# get info
		item_info = item.filename, "{}/{}/{} {}:{}:{}".format(*item.date_time), item.file_size
		d = ">> zip dir" if item.is_dir() else "> zip item"
		info.append("{}: [ {} ] modified: {}, size: {}".format(d, *item_info))
		urls.append(join(base_url,item.filename))
		ext = splitext(item.filename)
		current_app.logger.debug(info[-1])

		#inspect
		if ext[1] in [".glb", ".gltf"]:
			gltf_file = item.filename
		elif ext[1] == ".obj":
			obj_file = item.filename
		elif ext[1] == ".mtl":
			mtl_file = item.filename
		elif ext[1] in ALLOWED_IMGS_EXT:
			textures.append(item.filename)

	if obj_file:
		reason = "OBJ type detected, format not supported"
		filetype = "OBJ"
		return {"status" : "bad file", 'file_urls':urls, "zip_info": info, "reason": reason}

	if gltf_file:
		filetype = "GLTF"

	ret = {"status" : "ok", 'file_urls':urls, "zip_info": info,
			"gltf_file" : gltf_file,
			"obj_file" : obj_file,
			"mtl_file" : mtl_file,
			"filetype" : filetype,
			"textures" : textures
		}

	if not filetype:
		ret["status"] = "bad file"
		ret["reason"] = "No valid 3D file found in zip file"

	return ret


def unzip(file, path, base_url):
	current_app.logger.debug("Extracting zip file: {}".format(file.filename))
	if not zipfile.is_zipfile(file):
		return {"status": "bad file", "reason": "The file is not a zip"}
	
	with zipfile.ZipFile(file, 'r') as zip_ref:
		zip_error = zip_ref.testzip()
		if zip_error:
			return {"status": "bad file", "reason": "Corrupted zip file, errorlist: {}".format(zip_error)}

		ret = inspect_zip(zip_ref, base_url)

		if ret['status'] == 'ok':
			zip_ref.extractall(path)

	return ret


def save_file(file, path):
	data = file.stream.read()

	with open(path, "wb") as f:
		f.write(data)

	current_app.logger.info("Saved file %s",path)

	return path


@bp.route('/file/<slot>', methods=('POST',)) 
@auth_check_dashboard(redirect_to_login=True)
def _file(user=None, slot=None):
	try:
		if 'file' not in request.files:
			return jsonify({"status": "image not saved, file not present in request"})

		file = request.files['file']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			return jsonify({"status": "image not saved, empty file in request"})

		if 'Content-length' not in request.headers:
			raise u.Upload_File_Error("No Content-length header in request")

		if int(request.headers['Content-length']) > current_app.config['MAX_FILE_SIZE']:
			raise u.Upload_File_Error("The file {} is too big, max allowed {}kb".format(file.filename, current_app.config['MAX_FILE_SIZE']/1024))

		return handle_file(file, file.filename, slot)

	except u.Upload_File_Error as e:
		err_id = u.get_error_id()

		int_error = jsonify({"status": "error", "reason": "Content upload error: {}".format(e), "error_id": err_id})
		current_app.logger.error('[ Content Upload error | error_id: %s ] %s\n%s---' % (err_id, e, traceback.format_exc()) )

		return make_response( int_error, 500 )

	except Exception as e:
		err_id = u.get_error_id()

		current_app.logger.error('[ Content upload generic error | error_id: %s ] %s\n%s---' % (err_id, e, traceback.format_exc()) )

		int_error = jsonify({"status": "error", "reason": "internal error", "error_id": err_id})
		return make_response( int_error, 500 )
	
	# it should never get here
	return make_response( jsonify({"status": "unknown", "reason": "The file upload process was not completed"} ), 500 )

@bp.route('/<slot>', methods=('POST',))
@auth_check_dashboard(redirect_to_login=True) 
def populate_msg(user=None, slot=None):
	content = request.get_json()

	try:
		db = get_db()

		query = ''' UPDATE objects
					SET 
					  model = {},
					  modified = CURRENT_TIMESTAMP,
					  marker = ?,
					  info = ?,
					  scale = ?,
					  pos_x = ?,
					  pos_y = ?,
					  pos_z = ?
					WHERE id = ?;'''. format("?" if content["model"] else "model" )

		model_arg = (content["model"],) if content["model"] else tuple()
		query_args = model_arg + (content['marker-barcode'], content['info'], 
					content['scale'], content['px'], content['py'], 
					content["pz"], slot)

		db.execute( query , query_args)
		
		db.commit()

	except Exception as e:
		err_id = u.get_error_id()

		current_app.logger.error('[ Content upload content error | error_id: %s ] %s\n%s---' % (err_id, e, traceback.format_exc()) )

		int_error = jsonify({"status": "error", "reason": "internal error", "error_id": err_id})
		return make_response( int_error, 500 )


	return jsonify({"status": "ok"})




# @bp.route('/', methods=('GET',)) 
# def cards_get():
#     try:
#         db = get_db()
		
#         res = db.execute("SELECT * FROM cards")
#         res = res.fetchall()

#         response = []
#         for row in res:
#             response.append({k:row[k] for k in row.keys()})
		
#     except Exception as e:
#         err_id = u.get_error_id()

#         current_app.logger.error('[ Get cards list error | error_id: %s ] %s\n%s---' % (err_id, e, traceback.format_exc()) )

#         int_error = jsonify({"status": "error", "reason": "internal error", "error_id": err_id})
#         return make_response( int_error, 500 )

#     return jsonify(response)
	



# def old_save_file(file, path):
# 	# ext = splitext(file.filename)

# 	# if ext[1] not in current_app.config['ALLOWED_IMGS_EXT']:
# 	# 	raise Upload_File_Error("The image {} has an invalid extension, allowed: {}".format(file.filename, current_app.config['ALLOWED_IMGS_EXT']))

# 	data = file.stream.read()
# 	# md5_hash = hashlib.md5()
# 	# md5_hash.update(data)
# 	# save_image_name = "{}{}".format(md5_hash.hexdigest(), ext[1])
# 	# save_image_path = join(path, save_image_name)

# 	# file_path = join(dirname(realpath(__file__)), path)
# 	# save_image_as = join(file_path, save_image_name)

# 	# if not isfile(path): #save the image only if it doesnt exists
# 	with open(path, "wb") as f:
# 		f.write(data)

# 	# img_type = imghdr.what(save_image_as)
# 	current_app.logger.info("Saved file %s",path)

# 	# if img_type not in current_app.config['ALLOWED_IMGS_TYPES']:
# 	# 	remove(save_image_as)
# 	# 	current_app.logger.debug("Removed image %s, type: %s", save_image_as, img_type)
# 	# 	raise Upload_File_Error("The image {} has an invalid type, allowed: {}".format(file.filename, current_app.config['ALLOWED_IMGS_TYPES']))

# 	return path