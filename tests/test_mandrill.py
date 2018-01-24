import json
import pytest
from unittest import mock

from emissary import app
from emissary.email import MailFailureException
from emissary.mandrill import Mandrill


app.config['emissary']['providers']['mandrill']['endpoint'] = 'MANDRILL_ENDPOINT'
app.config['emissary']['providers']['mandrill']['key'] = 'MANDRILL_KEY'


def create_email():
    return Mandrill(
                    'foo@bar.com',
                    'F. Bar',
                    'bar@baz.co.uk',
                    'Bar Baz',
                    'Hello old friend',
                    '<h1>Not today!</h1>'
                   ), {
                       'key': 'MANDRILL_KEY',
                       'message': {
                                   'from_email': 'foo@bar.com',
                                   'from_name': 'F. Bar',
                                   'subject': 'Hello old friend',
                                   'html': '<h1>Not today!</h1>',
                                   'text': '',
                                   'to': [{
                                           'name': 'Bar Baz',
                                           'email': 'bar@baz.co.uk',
                                           'type': 'to',
                                          }, ],
                                  },
                      }


@mock.patch('requests.post')
def test_mandrill_happy(post_call):
    mg, post_args = create_email()
    mg.validate = mock.Mock()
    response_mock = mock.Mock()
    response_mock.status_code = 200
    response_mock.text = '[{"status": "queued"}]'
    post_call.return_value = response_mock
    mg.send()
    assert post_call.call_args_list[0][1]['data'] == json.dumps(post_args)
    assert post_call.call_count == 1
    assert mg.validate.call_count == 1


@mock.patch('requests.post')
def test_mandrill_needs_a_hug(post_call):
    mg, post_args = create_email()
    mg.validate = mock.Mock()
    response_mock = mock.Mock()
    response_mock.status_code = 500
    response_mock.text = '{"message": "whoops"}'
    post_call.return_value = response_mock

    with pytest.raises(MailFailureException):
        mg.send()

        assert post_call.call_args_list[0][1]['data'] == json.dumps(post_args)
        assert post_call.call_count == 1
        assert mg.validate.call_count == 1
