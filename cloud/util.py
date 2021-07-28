import datetime
import json
from typing import Optional

from sqlalchemy.orm import Query

import database
import fhir
import gcf
import gcs

RFC3339_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


def gosh_python_is_good_at_time(time_string: str) -> datetime.datetime:
    """
    python is really good at time and does a good job and i'm not bitter at all.

    :param time_string: Raw RFC3339-formatted time string
    :return: timezone aware datetime instance.
    """
    return datetime.datetime.strptime(time_string, RFC3339_FORMAT).replace(tzinfo=datetime.timezone.utc)


def value_or_default(src: dict, key: str, default):
    """
    value_or_default attempts to locate a value within a dict, returning the provided default should it not be found

    :param src: source dictionary
    :param key: dictionary key name
    :param default: value to return should the key not be found in the src dict
    :return:
    """
    if key in src:
        return src[key]
    else:
        return default


def datetime_or_none(src: dict, key: str) -> Optional[datetime.datetime]:
    """
    datetime_or_none attempts to locate and parse an RFC3339 datetime value from a dictionary, returning None if the
    key is not found in the provided dict

    :param src: source dictionary
    :param key: key containing RFC3339 datetime value
    :return:
    """
    if key in src:
        return gosh_python_is_good_at_time(src[key])
    else:
        return None


def obj_to_dict(obj: object) -> dict:
    """
    obj_to_dict recursively turns an object into a set of dictionaries

    :param obj: source object
    :return:
    """
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))


def create_psql_resource_entity(fhir_resource: fhir.Resource, object_meta: gcf.ObjectMeta) -> database.ResourceFile:
    """
    create_psql_resource_entity constructs a new ResourceFile entity, ready to be persisted into postgres

    :param fhir_resource: Source resource file
    :param object_meta: Object location metadata
    :return: Constructed ResourceFile instance
    """

    # construct new ResourceFile
    resource_file = database.ResourceFile()

    # populate
    resource_file.resource_id = fhir_resource.resource_id
    resource_file.resource_type = fhir_resource.resource_type
    resource_file.object_path = object_meta.path
    resource_file.uploaded = object_meta.created
    resource_file.inserted = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    resource_file.meta = fhir_resource.raw
    # dumb pythonic ways are dumb.
    resource_file.bucket = object_meta.bucket

    return resource_file


def fetch_fhir_gcs_object(object_meta: gcf.ObjectMeta, gcs_conn: gcs.Connection) -> fhir.Resource:
    """
    fetch_fhir_gcs_object attempts to fetch the raw bytes for a given FHIR object in GCS,
    then attempts to decode it into fhir.Resource type

    :param ObjectLocation object_meta: object of interest
    :param gcs_conn: exiting GCS connection
    :return: fhir.Resource instance
    """
    buck = gcs_conn.bucket(object_meta.bucket)
    obj = buck.get_blob(object_meta.path)
    b = obj.download_as_bytes()
    return fhir.Resource(b)


def fetch_fhir_psql_resource(dbm: database.Manager, resource_id: str) -> Optional[database.ResourceFile]:
    """
    fetch_fhir_psql_resource returns true if a row is found in the DB with a given Resource ID

    :param dbm: Existing database connection
    :param resource_id: ID of resource to attempt to fetch from PSQL
    :return: returns ResourceFile or None if one was not found
    """
    db_sess = dbm.open_session()
    db_query = db_sess.query(database.ResourceFile) \
        .filter_by(resource_id=resource_id) \
        .order_by(database.ResourceFile.inserted.desc())  # type: Query
    res = db_query.one_or_none()
    db_sess.close()
    return res
