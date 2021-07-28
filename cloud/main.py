import google.cloud.functions.context as gcf_context

import config
import database
import gcf
import gcs
import log
import util


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
    log.init(conf=conf, event_data=event_data)

    log.debug('Runtime config', conf=util.obj_to_dict(conf))

    # print for posterity...
    log.debug('Runtime arguments', event_data=event_data, ctx=ctx)
    # determine which object we're interacting with
    object_meta = gcf.ObjectMeta(event_data=event_data, ctx=ctx)
    log.info('Object meta parsed', objec_meta=object_meta.__dict__)

    # init gcs conn
    gcs_conn = gcs.Connection()

    # download FHIR file
    fhir_resource = cloud.gcs.fetch_fhir_gcs_object(object_meta=object_meta, gcs_conn=gcs_conn)
    log.info('FHIR Resource parsed', fhir_resource=fhir_resource)

    # init db connection
    dbm = database.Manager(conf)
    current = cloud.database.fetch_fhir_psql_resource(dbm, fhir_resource.resource_id)
    if current:
        log.info('Resource already exists in DB, moving on...')
        # TODO: at some point may have to do a json value comparison between existing and incoming...
        return

    log.info('Resource does not already exist in DB, inserting...')
    resource_file = cloud.database.create_psql_resource_entity(fhir_resource, object_meta)
    dbm.insert_single_entity(entity=resource_file)
    log.info('New resource successfully inserted!')
