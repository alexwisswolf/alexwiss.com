
#import requests
from google.appengine.api import urlfetch
import base64
import six
from flask import render_template
import urllib

client_id = "b2542a830907411195ef052c11eb39fb"

#token_url = "https://accounts.spotify.com/api/token"
auth_url = "https://accounts.spotify.com/authorize"
redirect_uri = "https://alexwiss-website.appspot.com/spotify"

def request_access(client_id):
	# payload = {
	redirect_uri = 'https://alexwiss-website.appspot.com/spotify'
	scope = 'user-top-read'
	# }
	# print payload
	query_string = urllib.urlencode({'client_id': client_id, 'redirect_uri': redirect_uri, 'scope': scope, 'response_type': 'code'})
	print query_string
	print "%s?%s" % (auth_url, query_string)
	#response = urlfetch.fetch("%s?%s" % (auth_url, query_string))
	
	if response.status_code is not 200:
		print "Error authorizing:"
		raise SystemError("Failed to authorize")
	
	return 
	
	
	#return response.json()['access_token']

# try:
	# token = request_access_token(client_id, client_secret)
# except SystemError as se:
	# print se
	# exit(1)
# token = 'BQByf_OugInFMRS0AovZ5UXGIDTXwll1giSyptrydo7Q8zukZkKmBNcNM2khY3TxOkL3v1D-AYgXnDAy917Ykw'
# token_header = { 'Authorization': 'Bearer %s' % token }
# api_version = "1"
# base_url = "https://api.spotify.com/v%s" % api_version

# top_tracks = requests.get("%s/recommendations" % base_url, headers=token_header)
# print top_tracks.reason
# print top_tracks.text
# print top_tracks

def render():
	return request_access(client_id)
	