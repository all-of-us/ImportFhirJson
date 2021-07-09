import requests


def main(gcs_obj, context):
    """
    Triggered by a file being uploaded into the souce GCS bucket

    file fields:
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
    """
    print(f'gcs_obj={gcs_obj}')
    print(f'context={context}')

# def hello_gcs(event, context):
#     """Triggered by a change to a Cloud Storage bucket.
#     Args:
#          event (dict): Event payload.
#          context (google.cloud.functions.Context): Metadata for the event.
#     """
#     file = event
#     print(f"Processing file: {file['name']}.")

#     requests.get('http://10.0.1.6:31337', params={'filename':file['name']})
