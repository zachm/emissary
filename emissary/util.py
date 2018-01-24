import logging

from email_validator import validate_email as _validate_email
from email_validator import EmailNotValidError


class MarshalingError(Exception):
    """ Raised when a MultiDict payload is missing required values, or they are of the wrong type. """
    pass


def validate_payload(request_dict, required_fields):
    """ Given a dict-like object, make certain all keys are present and valid.
            Custom to match the implementation of email.Email
            Return them back to the caller as an N-tuple so they can be used elsewhere.
        :param request_dict: Something behaving like a Python dict. Often a Werkzeug MultiDict.
        :param required_fields: N-tuple of 2-tuples, str=>type. Maps name of field to Python type/class.
        :raise: MarshalingError if payload is invalid.
        :return: An N-ary list containing the values.
    """
    retval = []
    for field, required_type in required_fields:
        if not isinstance(request_dict.get(field), required_type):
            raise MarshalingError('The parameter %s is missing or of incorrect type.' % field)
        retval.append(request_dict.get(field))
    return retval


def validate_email(address, dns_check=True):
    """ Email validation is a known hard problem, so we're outsourcing it.
            Pretty commonly used implementation; available on PyPI.
            This returns a lot of
            https://github.com/JoshData/python-email-validator
        :param address: string, possible email address
        :param dns_check: True/False, defaults True, whether to do a deliverability check
        :return: True or False
    """
    try:
        _validate_email(address, check_deliverability=dns_check)
        return True
    except EmailNotValidError as e:
        logging.warn('Email not valid: %s' % address)
        return False
