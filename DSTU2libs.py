import json, requests, sqlite3, os, argparse, itertools

def DSTU2fixEntity(conn,entity,args):
    entity,successful=fixEntity(conn,entity)
    if(not successful):
        return entity,False
    return entity,True

def fixEntity(conn,entity):
    c=conn.cursor()
    resourceType=entity.get('resourceType')
    if(resourceType=="Patient"):
        pass
    if(resourceType=="Observation"):
        reference=entity.get('subject').get('reference').split('/')
        referenceType=reference[0]
        referenceID=reference[1]
        c.execute("SELECT * from IDMap WHERE oldID='{}' AND resourceType='{}';".format(referenceID,referenceType))
        result=c.fetchone()
        if(result):
            referenceID=result[2]
            entity['subject']['reference']="{}/{}".format(referenceType,referenceID)
        else:
            return entity,False
    if(resourceType=="Medication"):
        if(entity.get('product')!=None):
            # We have a product, and it may have ingrediants
            if(entity.get('product').get('ingredient')!=None):
                for ingredient in entity.get('product').get('ingredient'):
                    if(ingredient.get('item')!=None):
                        reference=ingredient.get('item').get('reference').split('/')
                        referenceType=reference[0]
                        referenceID=reference[1]
                        c.execute("SELECT * from IDMap WHERE oldID='{}' AND resourceType='{}';".format(referenceID,referenceType))
                        result=c.fetchone()
                        if(result):
                            referenceID=result[2]
                            ingredient['item']['reference']="{}/{}".format(referenceType,referenceID)
                        else:
                            return entity,False
    if(resourceType=="Condition"):
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
                return entity,False
    if(resourceType=="Encounter"):
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
                return entity,False
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
                    return entity,False
    if(resourceType=="Procedure"):
        reference=entity.get('subject').get('reference').split('/')
        referenceType=reference[0]
        referenceID=reference[1]
        c.execute("SELECT * from IDMap WHERE oldID='{}' AND resourceType='{}';".format(referenceID,referenceType))
        result=c.fetchone()
        if(result):
            referenceID=result[2]
            entity['subject']['reference']="{}/{}".format(referenceType,referenceID)
        else:
            return entity,False
    if(resourceType=="MedicationStatement"):
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
                return entity,False
    return entity,True