import os

import google.cloud.functions.context as cloud_context

import util


class EventDataCustomerEncryption:
    def __init__(self, data: dict):
        self.encryptionAlgorithm = util.value_or_default(data, 'encryptionAlgorithm', '')
        self.keySha256 = util.value_or_default(data, 'keySha256', '')


class EventData:
    """
    EventData is an objectified version of the dict we get from a gcs invocation event

    There are a lot of inefficiencies in here, but meh.
    """

    def __init__(self, data: dict):
        self.kind = util.value_or_default(data, 'kind', '')
        self.id = util.value_or_default(data, 'id', '')
        self.selfLink = util.value_or_default(data, 'selfLink', '')
        self.name = util.value_or_default(data, 'name', '')
        self.bucket = util.value_or_default(data, 'bucket', '')
        self.generation = util.value_or_default(data, 'generation', '')
        self.metageneration = util.value_or_default(data, 'metageneration', '')
        self.contentType = util.value_or_default(data, 'contentType', '')
        self.timeCreated = util.value_or_default(data, 'timeCreated', '')
        self.timeCreatedDatetime = util.datetime_or_none(data, 'timeCreated')
        self.updated = util.value_or_default(data, 'updated', '')
        self.updatedDatetime = util.datetime_or_none(data, 'updated')
        self.temporaryHold = util.value_or_default(data, 'temporaryHold', False)
        self.retentionExpirationTime = util.value_or_default(data, 'retentionExpirationTime', '')
        self.retentionExpirationTimeDatetime = util.datetime_or_none(data, 'retentionExpirationTime')
        self.storageClass = util.value_or_default(data, 'storageClass', '')
        self.storageClassUpdated = util.value_or_default(data, 'storageClassUpdated', '')
        self.storageClassUpdatedDatetime = util.datetime_or_none(data, 'storageClassUpdated')
        self.size = util.value_or_default(data, 'size', '')
        self.md5Hash = util.value_or_default(data, 'md5Hash', '')
        self.mediaLink = util.value_or_default(data, 'mediaLink', '')
        self.contentEncoding = util.value_or_default(data, 'contentEncoding', '')
        self.contentDisposition = util.value_or_default(data, 'contentDisposition', '')
        self.cacheControl = util.value_or_default(data, 'cacheControl', '')
        self.metadata = util.value_or_default(data, 'metadata', {})
        self.crc32c = util.value_or_default(data, 'crc32c', '')
        self.componentCount = util.value_or_default(data, 'componentCount', 0)
        self.etag = util.value_or_default(data, 'etag', '')
        self.customerEncryption = EventDataCustomerEncryption(util.value_or_default(data, 'customerEncryption', {}))
        self.kmsKeyName = util.value_or_default(data, 'kmsKeyName', '')
        self.resourceState = util.value_or_default(data, 'resourceState', '')


class ObjectMeta:
    """
    ObjectMeta is used as a container for the values extracted from the event_object_meta
    func.
    """

    def __init__(self, event_data: EventData, ctx: cloud_context.Context):
        split = ctx.resource['name'].split('/')
        self.bucket = split[3]
        self.path = '/'.join(split[5:])
        self.name = os.path.basename(self.path)
        self.created = event_data.timeCreatedDatetime
        self.updated = event_data.updatedDatetime
