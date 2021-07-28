from google.cloud import storage

import fhir
import gcf


class Connection:
    """
    GCS is a small wrapper around the upstream gcs storage client
    """

    def __init__(self):
        self.client = storage.Client()  # "allow" "public" access to upstream client
        self._buckets = {}  # buck dict

    def bucket(self, name: str) -> storage.bucket.Bucket:
        """
        bucket will attempt to return an existing Bucket handle, creating a new handle
        if one was not previously created.

        :param name: Name of bucket to open
        :return: bucket handler
        """
        if name not in self._buckets:
            self._buckets[name] = self.client.bucket(name)
        buck = self._buckets[name]
        return buck


def fetch_fhir_gcs_object(object_meta: gcf.ObjectMeta, gcs_conn: Connection) -> fhir.Resource:
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
