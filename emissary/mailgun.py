import json
import logging

import requests

from emissary import app
from emissary.email import Email, MailFailureException


class Mailgun(Email):

    def send(self):
        self.validate()

        url = app.config['emissary']['providers']['mailgun']['endpoint']
        key = app.config['emissary']['providers']['mailgun']['key']

        authorize = requests.auth.HTTPBasicAuth('api', key)

        payload = {
            'from': '%s <%s>' % (self.from_name, self.from_addr),
            'to': '%s <%s>' % (self.to_name, self.to_addr),
            'subject': self.subject,
            'html': self.body_html,
            'text': self.body_text,
        }
        try:
            response = requests.post(url, data=payload, auth=authorize)

            if response.status_code != 200:
                logging.error('Mailgun returned HTTP %s' % response.status_code)
                try:
                    response_payload = json.loads(response.text).get('message', 'no message')
                except Exception:
                    response_payload = response.text
                logging.error(str(response_payload))
                raise MailFailureException('Mailgun returned HTTP %s: %s' %
                                           (response.status_code, response_payload))

        except requests.exceptions.RequestException as e:
            raise MailFailureException('Could not POST to Mailgun: %s' % e.message)
        except MailFailureException as e:
            raise e
