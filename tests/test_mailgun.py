import pytest
from unittest import mock

from emissary.email import MailFailureException
from emissary.mailgun import Mailgun


def create_email():
    return Mailgun(
                   'foo@bar.com',
                   'F. Bar',
                   'bar@baz.co.uk',
                   'Bar Baz',
                   'Hello old friend',
                   '<h1>Not today!</h1>'
                  ), {
                      'from': 'F. Bar <foo@bar.com>',
                      'to': 'Bar Baz <bar@baz.co.uk>',
                      'subject': 'Hello old friend',
                      'html': '<h1>Not today!</h1>',
                      'text': '',
                     }


@mock.patch('requests.post')
def test_mailgun_happy(post_call):
    mg, post_args = create_email()
    mg.validate = mock.Mock()
    response_mock = mock.Mock()
    response_mock.status_code = 200
    response_mock.text = None
    post_call.return_value = response_mock
    mg.send()
    assert post_call.call_args_list[0][1]['data'] == post_args
    assert post_call.call_count == 1
    assert mg.validate.call_count == 1


@mock.patch('requests.post')
def test_mailgun_needs_a_hug(post_call):
    mg, post_args = create_email()
    mg.validate = mock.Mock()
    response_mock = mock.Mock()
    response_mock.status_code = 500
    response_mock.text = '{"message": "whoops"}'
    post_call.return_value = response_mock

    with pytest.raises(MailFailureException):
        mg.send()

        assert post_call.call_args_list[0][1]['data'] == post_args
        assert post_call.call_count == 1
        assert mg.validate.call_count == 1
