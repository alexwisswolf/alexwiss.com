"""
BEFORE RUNNING:
---------------
1. If not already done, enable the Google Cloud Resource Manager API
   and check the quota for your project at
   https://console.developers.google.com/apis/api/cloudresourcemanager
2. This sample uses Application Default Credentials for authentication.
   If not already done, install the gcloud CLI from
   https://cloud.google.com/sdk and run
   `gcloud beta auth application-default login`.
   For more information, see
   https://developers.google.com/identity/protocols/application-default-credentials
3. Install the Python client library for Google APIs by running
   `pip install --upgrade google-api-python-client`
"""

def main():
	#from oauth2client.contrib.gce import AppAssertionCredentials
	from oauth2client.contrib.appengine import AppAssertionCredentials
	from googleapiclient import discovery
	#from oauth2client.client import GoogleCredentials

	#credentials = GoogleCredentials.get_application_default()
	credentials = AppAssertionCredentials('https://www.googleapis.com/auth/compute')

	service = discovery.build('compute', 'v1', credentials=credentials)

	# The Project ID (for example, `my-project-123`).
	# Required.
	#scopes = ['https://www.googleapis.com/auth/compute']
	project = 'alexwiss-website'  # TODO: Update placeholder value.
	zone = 'us-central1-f'

	request = service.instances().list(project=project, zone=zone)
	response = request.execute()


	# TODO: Change code below to process the `response` dict:
	#pprint(response)

	for item in response['items']:
		print item['name']