from datetime import datetime

from django.core.exceptions import SuspiciousOperation
import dateutil.parser


def get_boolean_parameter(parameters, field, required=False, default=False):
    parameter = parameters.get(field)
    if parameter is None and required:
        raise SuspiciousOperation('Parameter "{}" is required'.format(field))
    if parameter is None:
        return default
    if not isinstance(parameter, bool):
        raise SuspiciousOperation('Parameter "{}" is not a valid boolean'.format(field))
    return parameter


def get_string_parameter(parameters, field, required=False, default=''):
    parameter = parameters.get(field)
    if not parameter and required:
        raise SuspiciousOperation('Parameter "{}" is required'.format(field))
    if not parameter and not required:
        return default
    return str(parameter)


def get_enum_parameter(parameters, field, options, required=False, default=None):
    parameter = str(parameters.get(field) or '')
    if parameter and parameter not in options and required:
        raise SuspiciousOperation('Parameter "{}" is required'.format(field))
    if not parameter and not required:
        return default
    if parameter not in options:
        raise SuspiciousOperation('Value {} for parameter "{}" is not supported'.format(parameter, field))
    return parameter


def get_number_parameter(parameters, field, type=int, required=False, default=-1):
    try:
        parameter = parameters.get(field, None)
        if parameter is None and required:
            raise SuspiciousOperation('Parameter "{}" is required'.format(field))
        if parameter is None:
            return default
        return type(parameter)
    except Exception:
        raise SuspiciousOperation('Parameter "{}" is invalid'.format(field))


def get_datetime_parameter(parameters, field, required=False):
    try:
        parameter = parameters.get(field, None)
        if parameter is None and required:
            raise SuspiciousOperation('Parameter "{}" is required'.format(field))
        if parameter is None:
            return None
        return datetime.strptime(parameter, "%Y-%m-%dT%H:%M:%S.%fZ")
    except Exception:
        raise SuspiciousOperation('Parameter "{}" is an invalid datetime string'.format(field))