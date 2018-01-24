from emissary.util import validate_email


class MailFailureException(Exception):
    """ Raised if any part of the sending process fails. """
    pass


class ValidationError(Exception):
    """ Raised when validation fails in some way. """
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
        """ Create an email from the requisite components. All are strings.
            :param from_addr: Address the email is from, like example@domain.com
            :param from_name: A name the email is from: John Smith, or WidgetCorp
            :param to_addr: Address the email hopes to reach, like bugsbunny@wb.com
            :param subject: A subject line for the message, no longer than 998 characters.
            :param body_html: The HTML body of the message, as a string.
        """

        self.from_addr = from_addr
        self.from_name = from_name
        self.to_addr = to_addr
        self.to_name = to_name
        self.subject = subject
        self.body_html = body_html

        self.body_text = body_html  # TODO

    def validate(self):
        """ Execute all emissary-level validation and pre-processing steps.
            :raise ValidationError: If validation failed somehow.
        """

        if not validate_email(self.from_addr):
            raise ValidationError('Could not validate: %s' % self.from_addr)
        if not validate_email(self.to_addr):
            raise ValidationError('Could not validate: %s' % self.to_addr)

        # Limit is from the RFC spec.
        if len(self.subject) > 998 or len(self.subject.splitlines()) > 1:
            raise ValidationError('The \'subject\' field is too long or contained newlines.')

        # Limit is made up.
        if len(self.to_name) > 256 or len(self.to_name.splitlines()) > 1:
            raise ValidationError('The \'to_name\' field is too long or contained newlines.')
        if len(self.from_name) > 256 or len(self.from_name.splitlines()) > 1:
            raise ValidationError('The \'from_name\' field is too long or contained newlines.')

        return True

    def send(self):
        """ Implement this in provider-specific classes that inherit from this one. """
        raise NotImplementedError
