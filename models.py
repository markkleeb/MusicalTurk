# -*- coding: utf-8 -*-
from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import * # for our custom signup form
from flask.ext.mongoengine.wtf.orm import validators
from flask.ext.mongoengine import *
from datetime import datetime


class Song(mongoengine.Document):

	title = mongoengine.StringField(max_length=120, required=True)
	postedby = mongoengine.StringField(max_length=120, required=True, verbose_name="Your name")
	
	tags = mongoengine.ListField( mongoengine.StringField())

	filename = mongoengine.StringField()

	# Timestamp will record the date and time idea was created.
	timestamp = mongoengine.DateTimeField(default=datetime.now())


song_form = model_form(Song)

# Create a WTForm form for the photo upload.
# This form will inhirit the Photo model above
# It will have all the fields of the Photo model
# We are adding in a separate field for the file upload called 'fileupload'
class song_upload_form(song_form):
	fileupload = FileField('Upload a clip', validators=[])


	

