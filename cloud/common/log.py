from abc import ABC, abstractmethod

import jsonpickle

import chrono

# google cloud logging severity level values.
_GCL_SEVERITY_DEFAULT = 0
_GCL_SEVERITY_DEBUG = 100
_GCL_SEVERITY_INFO = 200
_GCL_SEVERITY_NOTICE = 300
_GCL_SEVERITY_WARNING = 400
_GCL_SEVERITY_ERROR = 500
_GCL_SEVERITY_CRITICAL = 600
_GCL_SEVERITY_ALERT = 700
_GCL_SEVERITY_EMERGENCY = 800

# these are the levels we actually care about
_LEVEL_DEBUG = "DEBUG"
_LEVEL_INFO = "INFO"
_LEVEL_WARN = "WARNING"
_LEVEL_ERROR = "ERROR"

# _LEVEL_DEBUG = logging.DEBUG
# _LEVEL_INFO = logging.INFO
# _LEVEL_WARN = logging.WARN
# _LEVEL_ERROR = logging.ERROR

# _LEVEL_DEBUG = _GCL_SEVERITY_DEBUG
# _LEVEL_INFO = _GCL_SEVERITY_INFO
# _LEVEL_WARN = _GCL_SEVERITY_WARNING
# _LEVEL_ERROR = _GCL_SEVERITY_ERROR

# these are private fields that incoming logging structures cannot overwrite
_FIELD_MESSAGE = 'message'
_FIELD_SEVERITY = 'severity'
_FIELD_TIMESTAMP = 'timestamp'  # must be datetime.datetime instance

_PRIVATE_FIELDS = {_FIELD_SEVERITY, _FIELD_MESSAGE, _FIELD_TIMESTAMP}

# contains our base logging fields
_base_fields = {}


class LoggableObject(ABC):
    @abstractmethod
    def to_loggable_dict(self) -> dict:
        """
        Must be implemented by child classes to print their contents to a structured log file
        :return:
        """
        pass


class LoggableObjectPickleHandler(jsonpickle.handlers.BaseHandler):
    def restore(self, obj):
        """
        restore is purposefully not implemented as we do not unserialize into from json
        into these types

        :param obj:
        :return:
        """
        raise NotImplementedError('Restore functionality is purposefully not implemented')

    def flatten(self, obj: LoggableObject, data):
        """
        flatten looks for classes that extend the LoggableObject class to filter the
        logged fields of that object

        :param obj: some kinda object
        :param data: jsonpickle metadata
        :return:
        """
        return obj.to_loggable_dict()


def init(function_name: str, function_version: int, gcs_bucket: str, gcs_object_etag: str) -> None:
    """
    init initializes our cloud func logger

    :param function_name: name of function
    :param function_version: version of function at runtime
    :param gcs_bucket: name of bucket containing object that triggered this runtime
    :param gcs_object_etag: etag of object
    :return:
    """
    global _base_fields

    # init base dict
    _base_fields['function_name'] = function_name
    _base_fields['function_version'] = function_version
    _base_fields['gcs_bucket'] = gcs_bucket
    _base_fields['gcs_object_etag'] = gcs_object_etag

    # register custom jsonpickle handler
    jsonpickle.handlers.register(cls=LoggableObject,
                                 handler=LoggableObjectPickleHandler,
                                 base=True)


def _do_log(severity: str, msg: str, fields: dict) -> None:
    """
    _do_log do's the logging.

    :param severity: level of this message
    :param msg: free text message of the message
    :param fields: structured fields of the message.  these cannot and will not override "private" fields.
    :return: nothin'
    """

    # build base output dict
    out = _base_fields.copy()

    out[_FIELD_SEVERITY] = severity
    out[_FIELD_MESSAGE] = msg
    out[_FIELD_TIMESTAMP] = chrono.now_str()

    # build log field map
    if len(fields) > 0:
        # build temp dict for field storage
        tmp = {}

        # loop over each provided field, preventing setting of "private" fields
        for k, v in fields.items():
            if k not in _PRIVATE_FIELDS:
                tmp[k] = v

        # if there was at least 1 non-private field defined, add them to "out"
        if len(tmp) > 0:
            out = {**tmp, **out}

    # json encode and print to stdout
    print(jsonpickle.dumps(value=out,
                           unpicklable=False,
                           indent=None))


def debug(msg: str, **kwargs) -> None:
    """
    debug prints a debug-level message

    :param msg: the message
    :param kwargs: the fields
    :return: nothin'
    """
    _do_log(severity=_LEVEL_DEBUG, msg=msg, fields=kwargs)


def info(msg: str, **kwargs) -> None:
    """
    info prints an info-level message

    :param msg: the message
    :param kwargs: the fields
    :return: nothin'
    """
    _do_log(severity=_LEVEL_INFO, msg=msg, fields=kwargs)


def warn(msg: str, **kwargs) -> None:
    """
    warn prints a warn-level message

    :param msg: the message
    :param kwargs: the fields
    :return: nothin'
    """
    _do_log(severity=_LEVEL_WARN, msg=msg, fields=kwargs)


def error(msg: str, **kwargs) -> None:
    """
    error prints an error-level message

    :param msg: the message
    :param kwargs: the fields
    :return: nothin'
    """
    _do_log(severity=_LEVEL_ERROR, msg=msg, fields=kwargs)
