import logging

from flask import request

from emissary import app
from emissary import choice
from emissary import email
from emissary import util


EMAIL_MODEL = (
               ('to', str),
               ('to_name', str),
               ('from', str),
               ('from_name', str),
               ('subject', str),
               ('body', str),
              )


def send_email(input_dict):
    """ Guts of the /email handler.
        :param input_dict: dict-like (keyable) object containing all the request's payload.
        :return: 2-tuple, (string reason, int HTTP_response_code)
    """
    try:
        email_parms = util.validate_payload(input_dict, EMAIL_MODEL)
        logging.info('Validated! %s' % str(email_parms))

        # choice.Choice().choose() returns a reference to an *actual* Python class.
        # Invocation with *email_parms (splat operator) expands the 6-tuple parameters.
        # These parameters instantiate the child class of email.Email.
        # And send() actually does the heavy lifting.
        chosen_provider = choice.Choice().choose()
        logging.info('Chose to use %s' % str(chosen_provider))
        chosen_provider(*email_parms).send()

    except util.MarshalingError as e:
        return (str(e), 400)
    except email.ValidationError as e:
        return (str(e), 400)
    except email.MailFailureException as e:
        return (str(e), 500)

    return ("Mail sent successfully", 200)


@app.route('/email', methods=['POST'])
def handle_email():
    return send_email(request.form)
