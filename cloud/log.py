import inspect
import json

import config
import gcf

_LEVEL_DEBUG = 'DBG'
_LEVEL_INFO = 'INF'
_LEVEL_WARN = 'WRN'
_LEVEL_ERROR = 'ERR'

_FIELD_MESSAGE = 'message'
_FIELD_LEVEL = 'level'

_PRIVATE_FIELDS = [_FIELD_LEVEL, _FIELD_MESSAGE]

_base_dict = {}


def init(conf: config.Config, event_data: gcf.EventData) -> None:
    """
    init initializes our cloud func logger

    :param conf: this runtime's configuration
    :param event_data: this runtime's event metadata
    :return:
    """
    global _base_dict
    _base_dict['function_name'] = conf.gcf.functionName
    _base_dict['function_version'] = conf.gcf.functionVersion
    _base_dict['gcs_bucket'] = event_data.bucket
    _base_dict['gcs_object_etag'] = event_data.etag


def _format_field_value(v):
    """
    _format_field_value attempts to return a json-dumpable value from the input

    :param v: whatever value needs to be dumped
    :return: somethin' dumpable
    """
    if inspect.isclass(v):
        out = {}
        for k, vv in v.__dict_.items():
            out[k] = _format_field_value(vv)
        return out
    elif type(v) == bool:
        return 'true' if v else 'false'
    else:
        return str(v)


def _do_log(lvl: str, msg: str, fields: dict) -> None:
    """
    _do_log do's the logging.

    :param lvl: level of this message
    :param msg: free text message of the message
    :param fields: structured fields of the message.  these cannot and will not override "private" fields.
    :return: nothin'
    """
    # build base output dict
    out = _base_dict.copy()
    out[_FIELD_LEVEL] = lvl
    out[_FIELD_MESSAGE] = msg

    # build log field map
    if fields:
        # build temp dict for field storage
        tmp = {}

        # loop over each provided field, preventing setting of "private" fields
        for _, (k, v) in enumerate(fields.items()):
            if k not in _PRIVATE_FIELDS:
                tmp[k] = _format_field_value(v)

        # if there was at least 1 non-private field defined, add them to "out"
        if len(tmp) > 0:
            out = {**tmp, **out}

    # json encode and print to stdout
    print(json.dumps(out, default=lambda o: o.__dict__))


def debug(msg: str, **kwargs) -> None:
    """
    debug prints a debug-level message

    :param msg: the message
    :param kwargs: the fields
    :return: nothin'
    """
    _do_log(lvl=_LEVEL_DEBUG, msg=msg, fields=kwargs)


def info(msg: str, **kwargs) -> None:
    """
    info prints an info-level message

    :param msg: the message
    :param kwargs: the fields
    :return: nothin'
    """
    _do_log(lvl=_LEVEL_INFO, msg=msg, fields=kwargs)


def warn(msg: str, **kwargs) -> None:
    """
    warn prints a warn-level message

    :param msg: the message
    :param kwargs: the fields
    :return: nothin'
    """
    _do_log(lvl=_LEVEL_WARN, msg=msg, fields=kwargs)


def error(msg: str, **kwargs) -> None:
    """
    error prints an error-level message

    :param msg: the message
    :param kwargs: the fields
    :return: nothin'
    """
    _do_log(lvl=_LEVEL_ERROR, msg=msg, fields=kwargs)
