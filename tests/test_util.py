import pytest

from emissary.util import MarshalingError
from emissary.util import validate_email
from emissary.util import validate_payload


def test_validate_payload_normal():
    complicated = MarshalingError()
    req_fields = (('hello', int), ('goodbye', str), ('goodnight', MarshalingError))
    req_sample = {'goodbye': 'whoever', 'goodnight': complicated, 'hello': 12}
    assert validate_payload(req_sample, req_fields) == [12, 'whoever', complicated]


def test_validate_payload_wrong_type():
    req_fields = (('hello', int), ('goodbye', str), ('goodnight', int))
    req_sample = {'goodbye': 'whoever', 'goodnight': 'wrong type!', 'hello': 12}
    with pytest.raises(MarshalingError):
        validate_payload(req_sample, req_fields)


def test_validate_payload_missing_field():
    req_fields = (('hello', int), ('goodbye', str), ('goodnight', int))
    req_sample = {'goodnight': 134, 'hello': 12}
    with pytest.raises(MarshalingError):
        validate_payload(req_sample, req_fields)


def test_validate_email():
    assert validate_email('jason@yahoo.co.uk')
    assert validate_email('jennifer@telus.ca')
    assert not validate_email('zach@nonono.yes')
    assert not validate_email('zach')
    assert not validate_email('zach@gma')
    assert not validate_email('zach@baxter.doggy', dns_check=True)
    assert validate_email('zach@baxter.dog', dns_check=False)
