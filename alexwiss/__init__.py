# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
#import countdown
from flask import current_app, Flask, redirect, url_for, Blueprint, render_template, request
from jinja2 import TemplateNotFound
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from googleapiclient import discovery
from httplib2 import Http
import urllib
import base64
import json
import os
import uuid

client_id = "b2542a830907411195ef052c11eb39fb"
client_secret = "85182bd06df14b259fb41749128d2c3b"
auth_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"
	
available_instances = [
	{"name":"f1-micro", "timeout":"20"},
	{"name":"g1-small", "timeout":"20"}
]

# Get credentials - different if in production or local dev environment
if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
	# Production
	redirect_uri = "https://alexwiss-website.appspot.com/callback"
	
else:
	# Local development server
	#from oauth2client.client import GoogleCredentials
	#credentials = GoogleCredentials.get_application_default()
	# from oauth2client.service_account import ServiceAccountCredentials
	# scopes = ['https://www.googleapis.com/auth/compute']
	# cred_file = "./alexwiss-07e55c19e381.json"
	# credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scopes=scopes)
	redirect_uri = "http://localhost:8888/callback"

	
#from oauth2client.contrib.gce import AppAssertionCredentials
from oauth2client.contrib.appengine import AppAssertionCredentials
#from oauth2client.client import GoogleCredentials

#credentials = GoogleCredentials.get_application_default()
credentials = AppAssertionCredentials('https://www.googleapis.com/auth/compute')
http_auth = credentials.authorize(Http())
service = discovery.build('compute', 'v1', credentials=credentials)
project = 'alexwiss-website'  # TODO: Update placeholder value.
zone = 'us-central1-f'
user = "testuser"
class Instance(ndb.Model):
	user = ndb.StringProperty(indexed=True)
	name = ndb.StringProperty(indexed=False)
	expire_dttm = ndb.DateTimeProperty(auto_now_add=False)

def create_app(config, debug=False, testing=False, config_overrides=None):
	app = Flask(__name__)
	app.config.from_object(config)

	app.debug = debug
	app.testing = testing

	if config_overrides:
		app.config.update(config_overrides)

	# Configure logging
	if not app.testing:
		logging.basicConfig(level=logging.INFO)

	# # Register the blueprint
	# bp = Blueprint("main", __name__)
	# app.register_blueprint(bp, url_prefix="/")
	
	# # Add a default root route.
	# @bp.route("/", defaults={"page", "base"})
	# @bp.route("/<page>")
	# def show(page):
		# try:
			# return render_template("base.html")
		# except TemplateNotFound:
			# abort(404)
			
	@app.route("/")
	def index():
		return render_template("index.html")
	
	@app.route("/resume")
	def resume():
		return render_template("resume.html")
		
	@app.route("/projects")
	def projects():
		return render_template("projects.html")
	
	@app.route("/spotify")
	def spotify():
		scope = 'user-top-read'
		query_string = urllib.urlencode({'client_id': client_id, 'redirect_uri': redirect_uri, 'scope': scope, 'response_type': 'code'})
		return redirect("%s?%s" % (auth_url, query_string))
	
	@app.route("/callback")
	def callback():
		try:
			code = request.args.get("code")
		except:
			code = "Code not found"
		
		#payload = {
		#	"grant_type": "authorization_code",
		#	"code": str(code),
		#	"redirect_uri": redirect_uri
		#}
		payload = urllib.urlencode({
			"grant_type": "authorization_code",
			"code": str(code),
			"redirect_uri": redirect_uri
		})
		
		base64encoded = base64.b64encode("%s:%s" % (client_id, client_secret))
		headers = {"Authorization": "Basic %s" % str(base64encoded)}
		
		response = urlfetch.fetch(
			token_url,
			payload=payload,
			headers=headers,
			method=urlfetch.POST
		)
		
		response_json = json.loads(response.content)
		access_token = response_json['access_token']
		token_type = response_json['token_type']
		expires_in = response_json['expires_in']
		refresh_token = response_json['refresh_token']
		
		auth_header = {"Authorization": "Bearer %s" % access_token}
		top = urlfetch.fetch("https://api.spotify.com/v1/me/top/tracks?limit=10", headers=auth_header)
		top_json = json.loads(top.content)
		return render_template("spotify.html", code=response.content, test="Hello!", songs=top_json['items'])
		#return render_template("spotify.html", code="test")
	
	# Add an error handler. This is useful for debugging the live application,
	# however, you should disable the output of the exception for production
	# applications.
	@app.errorhandler(500)
	def server_error(e):
		return """
		An internal error occurred: <pre>{}</pre>
		See logs for full stacktrace.
		""".format(e), 500
	
	@app.errorhandler(404)
	def not_found(e):
		return render_template("notfound.html")
		
	
	return app

