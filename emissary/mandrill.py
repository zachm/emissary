import json
import logging

import requests

from emissary import app
from emissary.email import Email, MailFailureException


class Mandrill(Email):

    def send(self):
        self.validate()

        url = app.config['emissary']['providers']['mandrill']['endpoint']
        key = app.config['emissary']['providers']['mandrill']['key']

        payload = {
            'key': key,
            'message': {
                'from_email': self.from_addr,
                'from_name': self.from_name,
                'subject': self.subject,
                'html': self.body_html,
                'text': self.body_text,
                'to': [{
                    'name': self.to_name,
                    'email': self.to_addr,
                    'type': 'to',
                }, ],
                # TODO auto_text !!!
            },
        }

        try:
            response = requests.post(url, data=json.dumps(payload))
            try:
                response_payload = json.loads(response.text)
            except Exception:
                raise MailFailureException('Mandrill response is malformed: %s' % response.text)

            if response.status_code != 200:
                logging.error('Mandrill returned HTTP %s: %s' %
                              (response.status_code, response_payload.get('message')))
                raise MailFailureException('Mandrill returned HTTP %s: %s' %
                                           (response.status_code, response_payload.get('message')))

            if response_payload[0]['status'] not in ['sent', 'queued']:
                raise MailFailureException('Mandrill bad response: message was %s' %
                                           response_payload[0]['status'])

        except requests.exceptions.RequestException as e:
            raise MailFailureException('Could not POST to Mandrill: %s' % e.message)
        except MailFailureException as e:
            raise e
