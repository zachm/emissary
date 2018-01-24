import pytest

from emissary.email import Email
from emissary.email import ValidationError


def create_email():
    return Email(
                 'foo@bar.com',
                 'F. Bar',
                 'bar@baz.co.uk',
                 'Bar Baz',
                 'Hello old friend',
                 '<h1>Not today!</h1>'
                )


def test_happy_path():
    em = create_email()
    assert em.validate() is True
    assert '# Not today!' in em.body_text


def test_missing_addresses():

    with pytest.raises(ValidationError):
        em = create_email()
        em.from_addr = 'fizzbuzz'
        em.validate()

    with pytest.raises(ValidationError):
        em = create_email()
        em.to_addr = '123345'
        em.validate()

    with pytest.raises(ValidationError):
        em = create_email()
        em.to_name = 'a' * 512
        em.validate()

    with pytest.raises(ValidationError):
        em = create_email()
        em.from_name = 'multi\nline'
        em.validate()


def test_missing_subject_body():

    with pytest.raises(ValidationError):
        em = create_email()
        em.subject = 'z' * 1024
        em.validate()
