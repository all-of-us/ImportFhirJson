import os, json

paths=[]
paths.append("/home/bcrumpton3-gtri/Documents/AllOfUs/ImportFhirJson/test")
jsonFiles=[]

for rootdir in paths:
    for root, dirs, files in os.walk(rootdir):
        for name in files:
            if name.endswith((".json")):
                print(name)
                full_path = os.path.join(root, name)
                jsonFiles.append(full_path)

print(jsonFiles)
jsonStrings=[]
for jsonFile in jsonFiles:
    with open(jsonFile,'r') as f:
        try:
            tempString=json.load(f)
            jsonStrings.append(tempString)
        except json.JSONDecodeError:
            print("file {} is invalid json".format(jsonFile)) 

for jsonString in jsonStrings:
    if(jsonString.get('resource',None)):
        print("format one")
        print(jsonString.get('resource'))
    else:
        print("format two")
        print(jsonString)
