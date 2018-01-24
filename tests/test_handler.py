import unittest.mock as mock

from emissary.handler import send_email
from emissary.util import MarshalingError


@mock.patch('emissary.util.validate_payload')
def test_send_email_missing_values(val_pay):
    val_pay.side_effect = MarshalingError('oopsie')
    assert send_email({}) == ('oopsie', 400)


@mock.patch('emissary.util.validate_payload')
@mock.patch('emissary.choice.Choice.choose')
def test_send_email_happy_path(choose, val_pay):
    choose.return_value = mock.Mock()
    assert send_email({}) == ('Mail sent successfully', 200)
