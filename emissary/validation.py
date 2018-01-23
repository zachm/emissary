import logging

from bs4 import BeautifulSoup
from email_validator import validate_email as _validate_email
from email_validator import EmailNotValidError


class ValidationError(Exception):
    """ Raised when validation fails in some way. """
    pass


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


def validate_payload(request_dict):
    """ Given a dict-like object, make certain all keys are present and valid.
            If they do, return a 6-tuple for convenience.
        :raise: ValidationError if payload is invalid
        :return: the signature of emissary.email.Email otherwise, as a 6-tuple.
    """
    required = ['to', 'to_name', 'from', 'from_name', 'subject', 'body']
    for field in required:
        if not isinstance(request_dict.get(field), str):
            raise ValidationError('The parameter %s is missing from the payload.' % field)

    if not validate_email(request_dict['to']):
        raise ValidationError('The email specified in the \'to\' field is invalid.')
    if not validate_email(request_dict['from']):
        raise ValidationError('The email specified in the \'from\' field is invalid.')

    # Limit is from the RFC spec.
    if len(request_dict['subject']) > 998 or len(request_dict['subject'].splitlines()) > 1:
        raise ValidationError('The \'subject\' field is too long or contained newlines.')

    # Limit is made up.
    if len(request_dict['to_name']) > 256 or len(request_dict['to_name'].splitlines()) > 1:
        raise ValidationError('The \'to_name\' field is too long or contained newlines.')
    if len(request_dict['from_name']) > 256 or len(request_dict['from_name'].splitlines()) > 1:
        raise ValidationError('The \'from_name\' field is too long or contained newlines.')

    return (
            request_dict['from'],
            request_dict['from_name'],
            request_dict['to'],
            request_dict['to_name'],
            request_dict['subject'],
            request_dict['body'],
           )


def clean_html(body):
    """ Use BeautifulSoup to make a passable plain text copy of our HTML.
            Great StackOverflow approach:
            https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
        :param body: string, hopefully HTML.
        :return: plain text string, or the empty string on an exception.
    """
    soup = BeautifulSoup(body)
    return soup  # TODO
