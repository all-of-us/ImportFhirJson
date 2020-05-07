import json, requests

SERVER="https://apps.hdap.gatech.edu/omoponfhir2/fhir/"

response = requests.get("{}{}".format(SERVER,"Patient"),auth=requests.auth.HTTPBasicAuth('***REMOVED***','***REMOVED***'))
# print(response)
# print(response.text)
json_response=json.loads(response.text)
# print(json_response)
for entry in json_response.get('entry'):
	print("Type:{} id:{} url:{}".format(entry.get('resource').get('resourceType'),entry.get('resource').get('id'),entry.get('fullUrl')))