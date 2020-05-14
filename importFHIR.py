import json, requests, sqlite3, os, argparse, itertools
from DSTU2libs import *

defaultServer="https://apps.hdap.gatech.edu/omoponfhir2/fhir/"
defaultFolder="/home/bcrumpton3-gtri/Documents/AllOfUs/ImportFhirJson/test"
authTypes=["basic","SSO"]
fhirVersions=["DSTU2","STU3","R4"]
defaultDB="OmopMapping.db"

def getFileList(path):
    jsonFiles=[]
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith((".json")):
                print(name)
                full_path = os.path.join(root, name)
                jsonFiles.append(full_path)
    return jsonFiles

def DBSetup(conn):
    c=conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS IDMap (oldID text, resourceType text, newID text);')
    conn.commit()

def mappingExists(conn,entity):
    c=conn.cursor()
    # c.execute("SELECT * from IDMap WHERE oldID=?;",(oldID,))
    oldID=entity.get('id')
    resourceType=entity.get('resourceType')
    c.execute("SELECT * from IDMap WHERE oldID='{}' AND resourceType='{}';".format(oldID,resourceType))
    if(c.fetchone()):
        return True
    else:
        return False
        

def postEntity(entity,args):
    # if(entity.get('resourceType')!="Medication"):
    #     return "tempnewID",True
    entity.pop('id')
    entity.pop('meta',None)
    response = requests.post("{}{}".format(args.server,entity.get('resourceType')),auth=requests.auth.HTTPBasicAuth('***REMOVED***','***REMOVED***'),json=entity)
    if(response.status_code!=201):
        # Error code 500 is a backend error, or an import error
        print(entity)
        print(response.status_code)
        print(response.text)
        # there must have been an error
        return "",False
    print(response.status_code)
    newLocation=response.headers.get('Location').split("/")
    print(newLocation)
    newID=newLocation[len(newLocation)-1]
    return newID,True

def processFile(conn,entity,args):
    # This is where I'm going to want to put all of the code to determine what version to be working with
    if(args.fhirversion=="DSTU2"):
        entity,successful=DSTU2fixEntity(conn,entity,args)
    elif(args.fhirversion=="STU3"):
        print("running for STU3")
        successful=False
    else:
        print("running for R4")
        successful=False
    if(not successful):
        return False
    oldID=entity.get('id')
    newID,successful=postEntity(entity,args)
    if(not successful):
        return False
    resourceType=entity.get('resourceType')
    c=conn.cursor()
    c.execute("INSERT INTO IDMap VALUES('{}','{}','{}');".format(oldID,resourceType,newID))
    conn.commit()
    return True

def cleanUp(conn,args):
    c=conn.cursor()
    c.execute("SELECT * from IDMap ORDER By rowid DESC;")
    rows=c.fetchall()
    for row in rows:
        deleteFromServer(row,args)

def deleteFromServer(row,args):
    print(row)
    response = requests.delete("{}{}/{}".format(args.server,row[1],row[2]),auth=requests.auth.HTTPBasicAuth('***REMOVED***','***REMOVED***'))
    print(response.status_code)
    # 204 is successful deletion
    print(response.text)

def buildEntityList(fileList):
    entityList=[]
    for file in fileList:
        with open(file,'r') as f:
            try:
                tempString=json.load(f)
            except json.JSONDecodeError:
                print("file {} is invalid json".format(file))
                continue
        if(tempString.get('resourceType',None)=="Medication"):
            print("we don't handle medications, skipping file {}".format(file))
            continue
        if(tempString.get('resourceType',None)=="Bundle"):
            i=0
            for entity in tempString.get('entry'):
                if(entity.get('resourceType',None)=="Medication"):
                    print("we don't handle medications, skipping file {} entity:{}".format(file,i))
                    continue
                tempDict={}
                tempDict['file']=file
                tempDict['type']=3
                tempDict['index']=i
                entityList.append(tempDict)
                i=i+1
        elif(tempString.get('resource',None)):
            # print("format one")
            tempDict={}
            tempDict['file']=file
            tempDict['type']=1
            entityList.append(tempDict)
        else:
            # print("format two")
            tempDict={}
            tempDict['file']=file
            tempDict['type']=2
            entityList.append(tempDict)

    return entityList

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
        This will go through all files in the specified folder ({} by default), and import them to the omoponfhir server provided ({} by default)
        """.format(defaultServer,defaultFolder))
    parser.add_argument("-s","--server",type=str,default=defaultServer,help="Omop Server URL to import data")
    parser.add_argument("-f","--folder",type=str,default=defaultFolder,help="folder location with all JSON files. This can have sub folders")
    parser.add_argument("--auth-type",type=str,choices=authTypes,help="what type of authentication the server utilizes")
    parser.add_argument("--fhirversion",type=str,choices=fhirVersions,default="DSTU2",help="what FHIR version are the JSON files stored in")
    parser.add_argument("-d","--database-name",type=str,default=defaultDB,help="sqlite file name that will hold the ID mapping results")
    parser.add_argument('--clean',help='will go over all mapping objects in the provided database, and remove them from the provided server',action='store_true')
    args=parser.parse_args()

    conn=sqlite3.connect(args.database_name)
    if(args.clean):
        cleanUp(conn,args)
        exit()
    fileList=getFileList(args.folder)
    DBSetup(conn)
    print(len(fileList))
    # print(fileList)
    iteration=0
    addedEntities=[]
    skippedEntities=[]
    
    entityList=buildEntityList(fileList)
    # print(entityList)
    while entityList:
        maxIterations=len(entityList)*2
        fileEntity=entityList[0]
        if(iteration>=maxIterations):
            print("we have a problem file. ")
            print("exiting")
            break
        print(fileEntity)
        with open(fileEntity['file'],'r') as f:
            tempString=json.load(f)
        if(fileEntity['type']==3):
            entity=tempString.get('entry')[fileEntity['index']].get('resource')
        elif(fileEntity['type']==1):
            # print("format one")
            entity=tempString.get('resource')
        else:
            # print("format two")
            entity=tempString
        if(mappingExists(conn,entity)):
            # This entity already exists
            skippedEntities.append(fileEntity)
            entityList.pop(0)
            iteration=0
            # print("popping entity, ",entity)
            continue
        else:
            if(processFile(conn,entity,args)):
                # we successfully processed the file
                addedEntities.append(fileEntity)
                entityList.pop(0)
                iteration=0
            else:
                # we failed importing
                entityList.append(fileEntity)
                entityList.pop(0)
                iteration=iteration+1
                continue
        
    print("entities not imported: ",entityList)
    print(addedEntities)
    print("files skipped as they're already imported: ",skippedEntities)