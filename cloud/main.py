import json

import google.cloud.functions.context as gcf_context

import config
import database
import gcs
import util


def main(data, ctx: gcf_context.Context):
    """
    Triggered by a file being uploaded into the source GCS bucket

    :param data:
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
    print(f'Runtime config: {conf.__dict__}')

    # print for posterity...
    print(('Runtime arguments: "{"obj": '
           f'{data}'
           ', "context: "'
           f'{ctx}'
           '"}'))
    # determine which object we're interacting with
    ol = util.extract_object_loc(ctx)
    print(f'Dealin\' with object: {ol.__dict__}')

    # init gcs conn
    gcs_conn = gcs.GCS(conf)

    # download FHIR file
    fhir_resource = util.fetch_fhir_gcs_object(object_location=ol, gcs_conn=gcs_conn)
    print(f'Dealing with resource {json.dumps(fhir_resource.__dict__)}')

    # init db connection
    db_conn = database.Connection(conf)
    if util.resource_exists_in_db(fhir_resource.resource_id, db_conn):
        print('Resource already exists in DB, moving on...')
        return

    print('Resource does not already exist in DB, inserting...')
