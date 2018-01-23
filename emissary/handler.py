import logging

from flask import request

from emissary import app
from emissary import choice
from emissary import email
from emissary import validation


@app.route('/', methods=['GET'])
def handle_root():
    return ('Root of emissary service', 200)


@app.route('/email', methods=['POST'])
def handle_email():

    try:
        email_parms = validation.validate_payload(request.form)
        logging.info('Validated! %s' % str(email_parms))

        # This sectionrequires some unpacking. Like so:
        # choice.Choice().choose() returns a reference to an *actual* Python class.
        # Invocation with *email_parms (splat operator) expands the 6-tuple parameters.
        # These parameters instantiate the child class of email.Email.
        # And send() actually does the heavy lifting.
        chosen_provider = choice.Choice().choose()
        logging.info('Chose to use %s' % str(chosen_provider))
        chosen_provider(*email_parms).send()

    except validation.ValidationError as e:
        return (str(e), 400)
    except email.MailFailureException as e:
        return (str(e), 400)

    return ("Mail sent successfully", 200)
