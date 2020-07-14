import json, requests, sqlite3, os, argparse, itertools

def DSTU2fixEntity(conn,entity,args):
    entity,successful=fixEntity(conn,entity,args)
    return entity,successful

def fixEntity(conn,entity,args):
    c=conn.cursor()
    resourceType=entity.get('resourceType')
    successful="success"
    if(resourceType=="Patient"):
        pass
    elif(resourceType=="Observation"):
        reference=entity.get('subject').get('reference').split('/')
        referenceType=reference[0]
        referenceID=reference[1]
        c.execute("SELECT * from IDMap WHERE oldID='{}' AND resourceType='{}';".format(referenceID,referenceType))
        result=c.fetchone()
        if(result):
            referenceID=result[2]
            entity['subject']['reference']="{}/{}".format(referenceType,referenceID)
        else:
            successful="notSuccess"
    elif(resourceType=="Medication"):
        print("we don't handle medications")
        successful="removeFile"
        # if(entity.get('product')!=None):
        #     # We have a product, and it may have ingrediants
        #     if(entity.get('product').get('ingredient')!=None):
        #         for ingredient in entity.get('product').get('ingredient'):
        #             if(ingredient.get('item')!=None):
        #                 reference=ingredient.get('item').get('reference').split('/')
        #                 referenceType=reference[0]
        #                 referenceID=reference[1]
        #                 c.execute("SELECT * from IDMap WHERE oldID='{}' AND resourceType='{}';".format(referenceID,referenceType))
        #                 result=c.fetchone()
        #                 if(result):
        #                     referenceID=result[2]
        #                     ingredient['item']['reference']="{}/{}".format(referenceType,referenceID)
        #                 else:
        #                     successful="notSuccess"
        #                     break
    elif(resourceType=="Condition"):
        if(entity.get('patient')!=None):
            reference=entity.get('patient').get('reference').split('/')
            referenceType=reference[0]
            referenceID=reference[1]
            c.execute("SELECT * from IDMap WHERE oldID='{}' AND resourceType='{}';".format(referenceID,referenceType))
            result=c.fetchone()
            if(result):
                referenceID=result[2]
                entity['patient']['reference']="{}/{}".format(referenceType,referenceID)
            else:
                successful="notSuccess"
    elif(resourceType=="Encounter"):
        if(entity.get('patient')!=None):
            reference=entity.get('patient').get('reference').split('/')
            referenceType=reference[0]
            referenceID=reference[1]
            c.execute("SELECT * from IDMap WHERE oldID='{}' AND resourceType='{}';".format(referenceID,referenceType))
            result=c.fetchone()
            if(result):
                referenceID=result[2]
                entity['patient']['reference']="{}/{}".format(referenceType,referenceID)
            else:
                successful="notSuccess"
        if(entity.get('indication')!=None):
            for indication in entity.get('indication'):
                reference=indication.get('reference').split('/')
                referenceType=reference[0]
                referenceID=reference[1]
                c.execute("SELECT * from IDMap WHERE oldID='{}' AND resourceType='{}';".format(referenceID,referenceType))
                result=c.fetchone()
                if(result):
                    referenceID=result[2]
                    indication['reference']="{}/{}".format(referenceType,referenceID)
                else:
                    successful="notSuccess"
                    break
    elif(resourceType=="Procedure"):
        if(entity.get('performedDateTime')==None):
            print("Cannot import this file, needs performedDateTime")
            successful="removeFile"
            pass
        reference=entity.get('subject').get('reference').split('/')
        referenceType=reference[0]
        referenceID=reference[1]
        c.execute("SELECT * from IDMap WHERE oldID='{}' AND resourceType='{}';".format(referenceID,referenceType))
        result=c.fetchone()
        if(result):
            referenceID=result[2]
            entity['subject']['reference']="{}/{}".format(referenceType,referenceID)
        else:
            successful="notSuccess"
    elif(resourceType=="MedicationStatement"):
        if(entity.get('patient')!=None):
            reference=entity.get('patient').get('reference').split('/')
            referenceType=reference[0]
            referenceID=reference[1]
            c.execute("SELECT * from IDMap WHERE oldID='{}' AND resourceType='{}';".format(referenceID,referenceType))
            result=c.fetchone()
            if(result):
                referenceID=result[2]
                entity['patient']['reference']="{}/{}".format(referenceType,referenceID)
            else:
                successful="notSuccess"
    elif(resourceType=="Practitioner"):
        if(entity.get('practitionerRole'!=None)):
            print("need to implement")
        if(entity.get('qualification'!=None)):
            print("need to convert qualification")
    elif(resourceType=="MedicationOrder"):
        if(entity.get('dateWritten')==None):
            print("Cannot import this file, needs dateWritten")
            successful="removeFile"
            pass
        if(entity.get('dateEnded')==None):
            entity['dateEnded']=entity.get('dateWritten')
        if(entity.get('patient')!=None):
            reference=entity.get('patient').get('reference').split('/')
            referenceType=reference[0]
            referenceID=reference[1]
            c.execute("SELECT * from IDMap WHERE oldID='{}' AND resourceType='{}';".format(referenceID,referenceType))
            result=c.fetchone()
            if(result):
                referenceID=result[2]
                entity['patient']['reference']="{}/{}".format(referenceType,referenceID)
            else:
                successful="notSuccess"
    elif(resourceType=="Device"):
        print("we don't allow posting of Devices currently")
        successful="removeFile"
        # if(entity.get('patient')!=None):
        #     reference=entity.get('patient').get('reference').split('/')
        #     referenceType=reference[0]
        #     referenceID=reference[1]
        #     c.execute("SELECT * from IDMap WHERE oldID='{}' AND resourceType='{}';".format(referenceID,referenceType))
        #     result=c.fetchone()
        #     if(result):
        #         referenceID=result[2]
        #         entity['patient']['reference']="{}/{}".format(referenceType,referenceID)
        #     else:
        #         successful="notSuccess"
        # if(entity.get('owner')!=None):
        #     print("need to implement owner in Device")
        #     successful="removeFile"
        #     pass
        # if(entity.get('location')!=None):
        #     print("need to implement location in Device")
        #     successful="removeFile"
        #     pass
    elif(resourceType=="DeviceUseStatement"):
        print("we don't allow posting of DeviceUseStatement currently")
        successful="removeFile"
        pass
        # reference=entity.get('subject').get('reference').split('/')
        # referenceType=reference[0]
        # referenceID=reference[1]
        # c.execute("SELECT * from IDMap WHERE oldID='{}' AND resourceType='{}';".format(referenceID,referenceType))
        # result=c.fetchone()
        # if(result):
        #     referenceID=result[2]
        #     entity['subject']['reference']="{}/{}".format(referenceType,referenceID)
        # else:
        #     successful="notSuccess"
    elif(resourceType=="DocumentReference"):
        if(entity.get('subject')!=None):
            reference=entity.get('subject').get('reference').split('/')
            referenceType=reference[0]
            referenceID=reference[1]
            c.execute("SELECT * from IDMap WHERE oldID='{}' AND resourceType='{}';".format(referenceID,referenceType))
            result=c.fetchone()
            if(result):
                referenceID=result[2]
                entity['subject']['reference']="{}/{}".format(referenceType,referenceID)
            else:
                successful="notSuccess"
        if(entity.get('author')!=None):
            for author in entity.get('author'):
                reference=author.get('reference').split('/')
                referenceType=reference[0]
                referenceID=reference[1]
                c.execute("SELECT * from IDMap WHERE oldID='{}' AND resourceType='{}';".format(referenceID,referenceType))
                result=c.fetchone()
                if(result):
                    referenceID=result[2]
                    author['reference']="{}/{}".format(referenceType,referenceID)
                else:
                    successful="notSuccess"
                    break
        if(entity.get('content')!=None):
            for content in entity.get('content'):
                if(content.get('attachment')!=None):
                    if(content['attachment'].get('contentType')=='application/pdf'):
                        print("{}{}".format(args.originalserver,content['attachment'].get('url')))
                        response=requests.get("{}{}".format(args.originalserver,content['attachment'].get('url')))
                        filename=content['attachment'].get('url').split("/")
                        print(filename)
                        with open(filename[2], 'wb') as f:
                            f.write(response.content)


    else:
        print("we don't know how to handle {} files yet".format(resourceType))
        successful="removeFile"
        pass
    return entity,successful