# -*- coding: utf-8 -*-
from mongoengine import *
from datetime import datetime


class Loop(Document):

	title = StringField(max_length=120, required=True)
	postedby = StringField(max_length=120, required=True, verbose_name="Your name")
	
	tags = ListField( StringField())

	filename = StringField()

	# Comments is a list of Document type 'Comments' defined above

	# Timestamp will record the date and time idea was created.
	timestamp = DateTimeField(default=datetime.now())


song_form = model_form(Loop)

# Create a WTForm form for the photo upload.
# This form will inhirit the Photo model above
# It will have all the fields of the Photo model
# We are adding in a separate field for the file upload called 'fileupload'
class song_upload_form(song_form):
	fileupload = FileField('Upload a clip', validators=[])


	

