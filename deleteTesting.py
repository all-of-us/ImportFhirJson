import json, requests

SERVER="https://apps.hdap.gatech.edu/omoponfhir2/fhir/"

getresponse = requests.get("{}{}".format(SERVER,"Patient"),auth=requests.auth.HTTPBasicAuth('***REMOVED***','***REMOVED***'))
getjson_response=json.loads(getresponse.text)
print(getjson_response)

response = requests.delete("{}{}/{}".format(SERVER,"Patient","17"),auth=requests.auth.HTTPBasicAuth('***REMOVED***','***REMOVED***'))

getresponse = requests.get("{}{}".format(SERVER,"Patient"),auth=requests.auth.HTTPBasicAuth('***REMOVED***','***REMOVED***'))
getjson_response=json.loads(getresponse.text)
print(getjson_response)