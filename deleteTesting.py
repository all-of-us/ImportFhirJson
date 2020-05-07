import json, requests

SERVER="https://apps.hdap.gatech.edu/omoponfhir2/fhir/"
resourceType="Observation"
resourceID="113"

getresponse = requests.get("{}{}".format(SERVER,resourceType),auth=requests.auth.HTTPBasicAuth('***REMOVED***','***REMOVED***'))
getjson_response=json.loads(getresponse.text)
print(getjson_response)

response = requests.delete("{}{}/{}".format(SERVER,resourceType,resourceID),auth=requests.auth.HTTPBasicAuth('***REMOVED***','***REMOVED***'))
print(response)
print(response.status_code)
print(response.text)

getresponse = requests.get("{}{}".format(SERVER,resourceType),auth=requests.auth.HTTPBasicAuth('***REMOVED***','***REMOVED***'))
getjson_response=json.loads(getresponse.text)
print(getjson_response)