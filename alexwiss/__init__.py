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
from flask import current_app, Flask, redirect, url_for, Blueprint, render_template
from jinja2 import TemplateNotFound



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

	# Setup the data model.
	# with app.app_context():
		# model = get_model()
		# model.init_app(app)

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
	
		
	# Add an error handler. This is useful for debugging the live application,
	# however, you should disable the output of the exception for production
	# applications.
	@app.errorhandler(500)
	def server_error(e):
		return """
		An internal error occurred: <pre>{}</pre>
		See logs for full stacktrace.
		""".format(e), 500

	return app


def get_model():
	model_backend = current_app.config['DATA_BACKEND']
	if model_backend == 'cloudsql':
		from . import model_cloudsql
		model = model_cloudsql
	elif model_backend == 'datastore':
		from . import model_datastore
		model = model_datastore
	else:
		raise ValueError(
			"No appropriate databackend configured. "
			"Please specify datastore, or cloudsql")

	return model
