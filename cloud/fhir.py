import json

_KEY_RESOURCE_TYPE = 'resourceType'
_KEY_RESOURCE_ID = 'id'


class Resource:
    """
    Resource represents a raw decoded FHIR resource
    """

    def __init__(self, json_bytes: bytes):
        """
        :param bytearray json_bytes: Raw bytes of JSON string
        """
        self.raw = json.loads(json_bytes)
        if _KEY_RESOURCE_TYPE in self.raw:
            self.resource_type = self.raw[_KEY_RESOURCE_TYPE]
        else:
            raise ValueError(f'Expected key {_KEY_RESOURCE_TYPE} not found in decoded JSON!')

        if _KEY_RESOURCE_ID in self.raw:
            self.resource_id = self.raw[_KEY_RESOURCE_ID]
        else:
            raise ValueError(f'Expected key {_KEY_RESOURCE_ID} not found in decoded JSON!')
