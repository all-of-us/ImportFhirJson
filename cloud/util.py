import json
import os

import google.cloud.functions.context as cloud_context
from sqlalchemy.orm import Query

import database
import fhir
import gcs


class ObjectLocation:
    """
    ObjectLocation is used as a container for the values extracted from the extract_object_loc
    func.
    """

    def __init__(self, bucket: str, path: str, name: str):
        self.bucket = bucket
        self.path = path
        self.name = name


def extract_object_loc(ctx: cloud_context.Context) -> ObjectLocation:
    """
    extracts the name of the object that spawned the triggering event
    :param ctx: context provided at runtime
    :return: parsed object location meta obj
    """
    # projects/_/_buckets/{bucket_name}/objects/{object_name}
    split = ctx.resource['name'].split('/')
    bucket = split[3]
    obj_path = '/'.join(split[5:])
    obj_name = os.path.basename(obj_path)
    return ObjectLocation(bucket, obj_path, obj_name)


def fetch_fhir_gcs_object(object_location: ObjectLocation, gcs_conn: gcs.GCS) -> fhir.Resource:
    """
    build_fhir_resource attempts to fetch the raw bytes for a given FHIR object in GCS,
    then attempts to decode it into fhir.Resource type

    :param ObjectLocation object_location: object of interest
    :param gcs_conn: exiting GCS connection
    :return: fhir.Resource instance
    """
    buck = gcs_conn.bucket(object_location.bucket)
    obj = buck.get_blob(object_location.path)
    b = obj.download_as_bytes()
    return fhir.Resource(b)


def resource_exists_in_db(resource_id: str, db_conn: database.Connection) -> bool:
    """
    resource_exists_in_db returns true if a row is found in the DB with a given Resource ID
    :param resource_id:
    :param db_conn:
    :return:
    """
    db_sess = db_conn.open_session()
    db_query = db_sess.query(database.ResourceFile).filter_by(resource_id=resource_id)  # type: Query
    db_sess.close()
    return db_query.count() > 0


def obj_to_dict(obj: object) -> dict:
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))
