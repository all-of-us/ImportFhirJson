import json, requests, sqlite3, os, argparse, itertools, getpass
from DSTU2libs import *

defaultServer = "https://10.0.1.6/omoponfhir2/fhir/"
# defaultFolder="/home/bcrumpton3-gtri/Documents/AllOfUs/ImportFhirJson/test"
# authTypes=["basic","SSO"]
fhirVersions = ["DSTU2", "STU3", "R4"]


# defaultDB="OmopMapping.db"
# globalAuth=None

# def get_file_list(path):
#     json_files = []
#     for root, dirs, files in os.walk(path):
#         for name in files:
#             if name.endswith((".json")):
#                 full_path = os.path.join(root, name)
#                 json_files.append(full_path)
#     return json_files


def db_setup(conn):
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS IDMap (oldID text, resourceType text, newID text);')
    conn.commit()


def mapping_exists(conn, entity):
    c = conn.cursor()
    # c.execute("SELECT * from IDMap WHERE oldID=?;",(oldID,))
    old_id = entity.get('id')
    resource_type = entity.get('resourceType')
    c.execute("SELECT * from IDMap WHERE oldID='{}' AND resourceType='{}';".format(old_id, resource_type))
    if (c.fetchone()):
        return True
    else:
        return False


# def post_entity(entity, args):
#     global globalAuth
#     # if(entity.get('resourceType')!="Medication"):
#     # return "tempnewID",True
#     entity.pop('id', None)
#     entity.pop('meta', None)
#     response = requests.post("{}{}".format(args.server, entity.get('resourceType')), auth=globalAuth, json=entity)
#     if (response.status_code != 201):
#         # Error code 500 is a backend error, or an import error
#         print(
#             "Entity: {} failed to post with status:{} and text:{}".format(entity, response.status_code, response.text))
#         # there must have been an error
#         return "", "notSuccess"
#     print("Response code:{} Resource URL:{}".format(response.status_code, response.headers.get('Location')))
#     newLocation = response.headers.get('Location').split("/")
#     newID = newLocation[len(newLocation) - 1]
#     return newID, "success"


def process_file(conn, entity, args):
    # This is where I'm going to want to put all of the code to determine what version to be working with
    if (args.fhirversion == "DSTU2"):
        entity, successful = DSTU2fixEntity(conn, entity, args)
    elif (args.fhirversion == "STU3"):
        print("running for STU3")
        successful = False
    else:
        print("running for R4")
        successful = False
    if (successful != "success"):
        return successful
    # TODO: in the event that we don't have an old ID, we should create something so that we don't have DB clashes
    oldID = entity.get('id')
    newID, successful = post_entity(entity, args)
    if (successful != "success"):
        return successful
    resourceType = entity.get('resourceType')
    c = conn.cursor()
    c.execute("INSERT INTO IDMap VALUES('{}','{}','{}');".format(oldID, resourceType, newID))
    conn.commit()
    return successful


def clean_up(conn, args):
    c = conn.cursor()
    c.execute("SELECT * from IDMap ORDER By rowid DESC;")
    rows = c.fetchall()
    for row in rows:
        delete_from_server(row, args)


def delete_from_server(row, args):
    global globalAuth
    response = requests.delete("{}{}/{}".format(args.server, row[1], row[2]), auth=globalAuth)
    print("attempted removal of {}/{} gives status code: {} and text: {}".format(row[1], row[2], response.status_code,
                                                                                 response.text))
    # 204 is successful deletion


def build_entity_list(file_list):
    entity_list = []
    for file in file_list:
        with open(file, 'r') as f:
            try:
                temp_string = json.load(f)
            except json.JSONDecodeError:
                print("file {} is invalid json".format(file))
                continue
        if temp_string.get('resourceType', None) == "Bundle":
            i = 0
            for entity in temp_string.get('entry'):
                temp_dict = {'file': file, 'type': 3, 'index': i}
                entity_list.append(temp_dict)
                i = i + 1
        elif temp_string.get('resource', None):
            # print("format one")
            temp_dict = {'file': file, 'type': 1}
            entity_list.append(temp_dict)
        else:
            # print("format two")
            temp_dict = {'file': file, 'type': 2}
            entity_list.append(temp_dict)

    return entity_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
        This will go through all files in the specified folder ({} by default), and import them to the omoponfhir server provided ({} by default)
        """.format(defaultServer, defaultFolder))
    parser.add_argument("-s", "--server", type=str, default=defaultServer, help="Omop Server URL to import data")
    parser.add_argument("--original-server", type=str, default=defaultServer,
                        help="URL of original server where ingested data came from. Necessary for pulling down documents")
    parser.add_argument("--pull-files", action='store_true',
                        help="attempt to pull down documents, at the url set from original-server")
    parser.add_argument("-f", "--folder", type=str, default=defaultFolder,
                        help="folder location with all JSON files. This can have sub folders")
    parser.add_argument("--auth-type", type=str, choices=authTypes, default="basic",
                        help="what type of authentication the server utilizes")
    parser.add_argument("--fhirversion", type=str, choices=fhirVersions, default="DSTU2",
                        help="what FHIR version are the JSON files stored in")
    parser.add_argument("-d", "--database-name", type=str, default=defaultDB,
                        help="sqlite file name that will hold the ID mapping results")
    parser.add_argument('--clean',
                        help='will go over all mapping objects in the provided database, and remove them from the provided server',
                        action='store_true')
    args = parser.parse_args()

    if args.auth_type == 'basic':
        username = getpass.getpass("Username: ")
        password = getpass.getpass()
        globalAuth = requests.auth.HTTPBasicAuth(username, password)

    conn = sqlite3.connect(args.database_name)
    if args.clean:
        clean_up(conn, args)
        exit()
    file_list = get_file_list(args.folder)
    db_setup(conn)
    iteration = 0
    added_entities = []
    skipped_entities = []
    error_entities = []
    entity_list = build_entity_list(file_list)
    # print(entityList)
    while entity_list:
        max_iterations = len(entity_list) * 2
        file_entity = entity_list[0]
        # print("Checking {}".format(fileEntity))
        if iteration >= max_iterations:
            print("All remaining files have unsuccessfully imported twice each.")
            break
        with open(file_entity['file'], 'r') as f:
            tempString = json.load(f)
        if file_entity['type'] == 3:
            # this comes from a bundle
            entity = tempString.get('entry')[file_entity['index']].get('resource')
        elif file_entity['type'] == 1:
            # print("format one")
            entity = tempString.get('resource')
        else:
            # print("format two")
            entity = tempString
        if mapping_exists(conn, entity):
            print(
                "an entity of this Resource type with this ID has already been imported. skipping this file:{}".format(
                    file_entity))
            # This entity already exists
            skipped_entities.append(file_entity)
            entity_list.pop(0)
            continue
        else:
            result = process_file(conn, entity, args)
            if result == "success":
                # we successfully processed the file
                added_entities.append(file_entity)
                entity_list.pop(0)
                iteration = 0
            elif result == "removeFile":
                # this file cannot be processed at any time. remove it from the list
                print("removing {} for the reason above".format(file_entity['file']))
                error_entities.append(file_entity)
                entity_list.pop(0)
            else:
                # we failed importing, add it back to the list and try again later
                entity_list.append(file_entity)
                entity_list.pop(0)
                iteration = iteration + 1
                continue

    print("entities not imported: ", entity_list, "\n")
    print("entities imported: ", added_entities, "\n")
    print("files skipped as they're already imported: ", skipped_entities, "\n")
    print("entities skipped due to errors: ", error_entities)
