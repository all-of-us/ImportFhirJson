import datetime

import google.cloud.functions.context as gcf_context

from cloud.common import config, database, fhir, gcf, gcs, log


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
    resource_file.processed = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    resource_file.meta = fhir_resource.raw
    resource_file.bucket = object_meta.bucket

    return resource_file


def main(event_data, ctx: gcf_context.Context):
    """
    Triggered by a file being uploaded into the source GCS bucket

    :param event_data:
        {
            kind                        : string
            id                          : string
            selfLink                    : string
            name                        : string
            bucket                      : string
            generation                  : string
            metageneration              : string
            contentType                 : string
            timeCreated                 : string (RFC3339)
            updated                     : string (RFC3339)
            temporaryHold               : bool
            retentionExpirationTime     : string (RFC3339)
            storageClass                : string
            timeStorageClassUpdated     : string (RFC3339)
            size                        : string
            md5Hash                     : string
            mediaLink                   : string
            contentEncoding             : string
            contentDisposition          : string
            cacheControl                : string
            metadata                    : dict
            crc32c                      : string
            componentCount              : int
            etag                        : string
            customerEncryption          : {
                encryptionAlgorithm : string
                keySha256           : string
            }
            kmsKeyName                  : string
            resourceState               : string
        }
    :param google.cloud.functions.context.Context ctx:
        {
            event_id        : int
            timestamp       : string (RFC3339)  -> timestamp of event itself
            event_type      : string            -> one of https://cloud.google.com/functions/docs/calling/storage#event_types
            resource:       : {
                service : string    -> name of service in this case "storage.googleapis.com"
                name    : string    -> actual path to object, i.e. "projects/_/buckets/{bucket_name}/objects/{object_name}"
                type    : string    -> type of object, in this case interested in "storage#object"
            }
        }
    """

    # init config
    conf = config.Config()

    # construct our event data object
    event_data = gcf.EventData(event_data)
    log.init(function_name=conf.gcf.functionName,
             function_version=conf.gcf.functionVersion,
             gcs_bucket=event_data.bucket,
             gcs_object_etag=event_data.etag)

    log.debug('Runtime config', conf=conf)

    # print for posterity...
    log.debug('Runtime arguments', event_data=event_data, ctx=ctx)
    # determine which object we're interacting with
    object_meta = gcf.ObjectMeta(event_data=event_data, ctx=ctx)
    log.info('Object meta parsed', object_meta=object_meta)

    # init gcs conn
    gcs_conn = gcs.Connection()

    # download FHIR file
    fhir_resource = fetch_fhir_gcs_object(object_meta=object_meta, gcs_conn=gcs_conn)
    log.info('FHIR Resource parsed', fhir_resource=fhir_resource)

    # init db connection
    dbm = database.Manager(conf)
    current = database.fetch_fhir_psql_resource(dbm, fhir_resource.resource_id)
    if current:
        log.info('Resource already exists in DB, moving on...')
        # TODO: at some point may have to do a json value comparison between existing and incoming...
        return

    log.info('Resource does not already exist in DB, inserting...')
    resource_file = create_psql_resource_entity(fhir_resource, object_meta)
    dbm.insert_single_entity(entity=resource_file)
    dbm.close()
    log.info('New resource successfully inserted!')
