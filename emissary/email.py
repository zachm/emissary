from emissary.validation import validate_email


class MailFailureException(Exception):
    """ Raised if any part of the sending process fails. """
    pass


class Email(object):
    """ Base class for email providers. """

    from_addr = None
    from_name = None
    to_addr = None
    to_name = None
    subject = None
    body_html = None

    body_text = None

    def __init__(self, from_addr, from_name, to_addr, to_name, subject, body_html):

        self.from_addr = from_addr
        self.from_name = from_name
        self.to_addr = to_addr
        self.to_name = to_name
        self.subject = subject
        self.body_html = body_html

        self.body_text = body_html  # TODO

    def preprocess(self):
        """ Execute all emissary-level validation and pre-processing steps. """

        if not validate_email(self.from_addr):
            raise MailFailureException('Could not validate: %s' % self.from_addr)
        if not validate_email(self.to_addr):
            raise MailFailureException('Could not validate: %s' % self.to_addr)

    def send(self):
        raise NotImplementedError
