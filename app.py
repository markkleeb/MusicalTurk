# -*- coding: utf-8 -*-
import os, datetime, re
from flask import Flask, request, render_template, redirect, abort, jsonify
from werkzeug import secure_filename

# import all of mongoengine
from flask.ext.mongoengine import mongoengine

# import data models
import models


# Amazon AWS library
import boto




app = Flask(__name__)   # create our flask app
app.secret_key = os.environ.get('SECRET_KEY') # put SECRET_KEY variable inside .env file with a random string of alphanumeric characters
app.config['CSRF_ENABLED'] = False
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024 # 16 megabyte file upload

# --------- Database Connection ---------
# MongoDB connection to MongoLab's database
mongoengine.connect('mydata', host=os.environ.get('MONGOLAB_URI'))
app.logger.debug("Connecting to MongoLabs")

ALLOWED_EXTENSIONS = set(['wav', 'mp3', 'aac', 'aif'])


# --------- Routes ----------

# this is our main page
@app.route("/", methods=['GET'])
def index():


		return render_template("main.html")


@app.route("/loops", methods=['GET','POST'])
def loops():



	# get Idea form from models.py
	song_upload_form = models.song_upload_form(request.form)
	
	# if form was submitted and it is valid...
	if request.method == "POST" and song_upload_form.validate():
		
		uploaded_file = request.files['fileupload']
		# app.logger.info(file)
		# app.logger.info(file.mimetype)
		# app.logger.info(dir(file))
		
		# Uploading is fun
		# 1 - Generate a file name with the datetime prefixing filename
		# 2 - Connect to s3
		# 3 - Get the s3 bucket, put the file
		# 4 - After saving to s3, save data to database

		if uploaded_file and allowed_file(uploaded_file.filename):
			# create filename, prefixed with datetime
			now = datetime.datetime.now()
			filename = now.strftime('%Y%m%d%H%M%s') + "-" + secure_filename(uploaded_file.filename)
			# thumb_filename = now.strftime('%Y%m%d%H%M%s') + "-" + secure_filename(uploaded_file.filename)

			# connect to s3
			s3conn = boto.connect_s3(os.environ.get('AWS_ACCESS_KEY_ID'),os.environ.get('AWS_SECRET_ACCESS_KEY'))

			# open s3 bucket, create new Key/file
			# set the mimetype, content and access control
			b = s3conn.get_bucket(os.environ.get('AWS_BUCKET')) # bucket name defined in .env
			k = b.new_key(b)
			k.key = filename
			k.set_metadata("Content-Type", uploaded_file.mimetype)
			k.set_contents_from_string(uploaded_file.stream.read())
			k.make_public()

			# save information to MONGO database
			# did something actually save to S3
			if k and k.size > 0:
				
				submitted_loop = models.Song()
				submitted_loop.title = request.form.get('title')
				submitted_loop.postedby = request.form.get('postedby')
				submitted_loop.tag = 'loops'
				submitted_loop.filename = filename # same filename of s3 bucket file
				submitted_loop.save()


			return redirect('/loops')

		else:
			return "uhoh there was an error " + uploaded_file.filename



	else:
		# get existing images
		songs = models.Song.objects(tag='loops').order_by('-timestamp')
		
		# render the template
		templateData = {
			'songs' : songs,
			'form' : song_upload_form
		}

		return render_template("loops.html", **templateData)

@app.route("/beats", methods=['GET','POST'])
def beats():



	# get Idea form from models.py
	song_upload_form = models.song_upload_form(request.form)
	
	# if form was submitted and it is valid...
	if request.method == "POST" and song_upload_form.validate():
		
		uploaded_file = request.files['fileupload']
		# app.logger.info(file)
		# app.logger.info(file.mimetype)
		# app.logger.info(dir(file))
		
		# Uploading is fun
		# 1 - Generate a file name with the datetime prefixing filename
		# 2 - Connect to s3
		# 3 - Get the s3 bucket, put the file
		# 4 - After saving to s3, save data to database

		if uploaded_file and allowed_file(uploaded_file.filename):
			# create filename, prefixed with datetime
			now = datetime.datetime.now()
			filename = now.strftime('%Y%m%d%H%M%s') + "-" + secure_filename(uploaded_file.filename)
			# thumb_filename = now.strftime('%Y%m%d%H%M%s') + "-" + secure_filename(uploaded_file.filename)

			# connect to s3
			s3conn = boto.connect_s3(os.environ.get('AWS_ACCESS_KEY_ID'),os.environ.get('AWS_SECRET_ACCESS_KEY'))

			# open s3 bucket, create new Key/file
			# set the mimetype, content and access control
			b = s3conn.get_bucket(os.environ.get('AWS_BUCKET')) # bucket name defined in .env
			k = b.new_key(b)
			k.key = filename
			k.set_metadata("Content-Type", uploaded_file.mimetype)
			k.set_contents_from_string(uploaded_file.stream.read())
			k.make_public()

			# save information to MONGO database
			# did something actually save to S3
			if k and k.size > 0:
				
				submitted_loop = models.Song()
				submitted_loop.title = request.form.get('title')
				submitted_loop.postedby = request.form.get('postedby')
				submitted_loop.tag = 'beats'
				submitted_loop.filename = filename # same filename of s3 bucket file
				submitted_loop.save()


			return redirect('/beats')

		else:
			return "uhoh there was an error " + uploaded_file.filename



	else:
		# get existing images
		songs = models.Song.objects(tag='beats').order_by('-timestamp')
		
		# render the template
		templateData = {
			'songs' : songs,
			'form' : song_upload_form
		}

		return render_template("beats.html", **templateData)

@app.route("/atmosphere", methods=['GET','POST'])
def atmosphere():



	# get Idea form from models.py
	song_upload_form = models.song_upload_form(request.form)
	
	# if form was submitted and it is valid...
	if request.method == "POST" and song_upload_form.validate():
		
		uploaded_file = request.files['fileupload']
		# app.logger.info(file)
		# app.logger.info(file.mimetype)
		# app.logger.info(dir(file))
		
		# Uploading is fun
		# 1 - Generate a file name with the datetime prefixing filename
		# 2 - Connect to s3
		# 3 - Get the s3 bucket, put the file
		# 4 - After saving to s3, save data to database

		if uploaded_file and allowed_file(uploaded_file.filename):
			# create filename, prefixed with datetime
			now = datetime.datetime.now()
			filename = now.strftime('%Y%m%d%H%M%s') + "-" + secure_filename(uploaded_file.filename)
			# thumb_filename = now.strftime('%Y%m%d%H%M%s') + "-" + secure_filename(uploaded_file.filename)

			# connect to s3
			s3conn = boto.connect_s3(os.environ.get('AWS_ACCESS_KEY_ID'),os.environ.get('AWS_SECRET_ACCESS_KEY'))

			# open s3 bucket, create new Key/file
			# set the mimetype, content and access control
			b = s3conn.get_bucket(os.environ.get('AWS_BUCKET')) # bucket name defined in .env
			k = b.new_key(b)
			k.key = filename
			k.set_metadata("Content-Type", uploaded_file.mimetype)
			k.set_contents_from_string(uploaded_file.stream.read())
			k.make_public()

			# save information to MONGO database
			# did something actually save to S3
			if k and k.size > 0:
				
				submitted_loop = models.Song()
				submitted_loop.title = request.form.get('title')
				submitted_loop.postedby = request.form.get('postedby')
				submitted_loop.tag = 'atmosphere'
				submitted_loop.filename = filename # same filename of s3 bucket file
				submitted_loop.save()


			return redirect('/atmosphere')

		else:
			return "uhoh there was an error " + uploaded_file.filename



	else:
		# get existing images
		songs = models.Song.objects(tag='atmosphere').order_by('-timestamp')
		
		# render the template
		templateData = {
			'songs' : songs,
			'form' : song_upload_form
		}

		return render_template("atmosphere.html", **templateData)

@app.route("/about")
def about():

	

	return render_template("about.html")

@app.route('/delete/<songid>')
def delete_image(songid):
	
	song = models.Song.objects.get(id=songid)
	if song:

		# delete from s3
	
		# connect to s3
		s3conn = boto.connect_s3(os.environ.get('AWS_ACCESS_KEY_ID'),os.environ.get('AWS_SECRET_ACCESS_KEY'))

		# open s3 bucket, create new Key/file
		# set the mimetype, content and access control
		bucket = s3conn.get_bucket(os.environ.get('AWS_BUCKET')) # bucket name defined in .env
		k = bucket.new_key(bucket)
		k.key = song.filename
		bucket.delete_key(k)

		# delete from Mongo	
		song.delete()

		return redirect('/')

	else:
		return "Unable to find requested image in database."



@app.route('/data/loops')
def data_loops():

	# query for the ideas - return oldest first, limit 10
	loops = models.Song.objects().order_by('-timestamp')

	if loops:

		# list to hold ideas
		public_loops = []

		#prep data for json
		for n in loops:

			tmpLoop = {
				'path' : n.filename,
				'title' : n.title,
				'name' : n.postedby,
				'tag' : n.tag,
				'timestamp' : str( n.timestamp )
				
			}


			# insert idea dictionary into public_ideas list
			public_loops.append( tmpLoop )

		# prepare dictionary for JSON return
		data = {
			'status' : 'OK',
			'loops' : public_loops
		}

		# jsonify (imported from Flask above)
		# will convert 'data' dictionary and set mime type to 'application/json'
		return jsonify(data)

	else:
		error = {
			'status' : 'error',
			'msg' : 'unable to retrieve ideas'
		}
		return jsonify(error)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

def allowed_file(filename):
    return '.' in filename and \
           filename.lower().rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)



	