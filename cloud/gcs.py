from google.cloud import storage


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
