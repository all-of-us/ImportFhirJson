import json, requests

SERVER="https://apps.hdap.gatech.edu/omoponfhir2/fhir/"
# testFile='/home/bcrumpton3-gtri/Documents/AllOfUs/ImportFhirJson/test/folder/1032702/new_patient_smart-1032702.json'
testFile='/home/bcrumpton3-gtri/Documents/AllOfUs/ImportFhirJson/test/afolder/aobservation.json'
# ResourceType="Patient"
ResourceType='Observation'

with open(testFile,'r') as f:
    try:
        tempString=json.load(f)
    except json.JSONDecodeError:
        print("file {} is invalid json".format(jsonFile)) 

# print(tempString)
tempString.pop('id')
tempString.pop('meta')
# print(tempString)

response = requests.post("{}{}".format(SERVER,ResourceType),auth=requests.auth.HTTPBasicAuth('***REMOVED***','***REMOVED***'),json=tempString)
print(response)
print(response.text)
newLocation=response.headers.get('Location')
print(json.loads(requests.get(newLocation,auth=requests.auth.HTTPBasicAuth('***REMOVED***','***REMOVED***')).text))

getresponse = requests.get("{}{}".format(SERVER,ResourceType),auth=requests.auth.HTTPBasicAuth('***REMOVED***','***REMOVED***'))
getjson_response=json.loads(getresponse.text)
print(getjson_response)

response = requests.delete(newLocation,auth=requests.auth.HTTPBasicAuth('***REMOVED***','***REMOVED***'))

getresponse = requests.get("{}{}".format(SERVER,ResourceType),auth=requests.auth.HTTPBasicAuth('***REMOVED***','***REMOVED***'))
getjson_response=json.loads(getresponse.text)
print(getjson_response)