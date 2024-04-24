import pytest

from dundie.utils.email import check_valid_email, send_email


@pytest.mark.unit
@pytest.mark.parametrize(
    "address", ["bruno@rocha.com", "joe@doe.com", "a@b.pt"]
)
def test_positive_check_valid_email(address):
    """Ensure email is valid."""
    assert check_valid_email(address) is True


@pytest.mark.unit
@pytest.mark.parametrize("address", ["bruno@.com", "@doe.com", "a@b"])
def test_negative_check_valid_email(address):
    """Ensure email is invalid."""
    assert check_valid_email(address) is False


@pytest.mark.unit
def test_send_email(mocker):
    mock_SMTP = mocker.MagicMock(name="dundie.utils.email.smtplib.SMTP")
    mocker.patch("dundie.utils.email.smtplib.SMTP", new=mock_SMTP)

    from_email = "from@example.com"
    to_emails = ["to1@example.com", "to2@example.com"]
    subject = "Test Subject"
    text = "Test Email Body"

    send_email(from_email, to_emails, subject, text)
