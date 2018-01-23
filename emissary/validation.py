import logging

from email_validator import validate_email as _validate_email
from email_validator import EmailNotValidError


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
