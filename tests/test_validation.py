from emissary.validation import validate_email


def test_validate_email():
    assert validate_email('jason@yahoo.co.uk')
    assert validate_email('jennifer@telus.ca')
    assert not validate_email('zach@nonono.yes')
    assert not validate_email('zach')
    assert not validate_email('zach@gma')
    assert not validate_email('zach@baxter.doggy', dns_check=True)
    assert validate_email('zach@baxter.dog', dns_check=False)
