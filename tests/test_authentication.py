from app.services import authentication


def test_token_validation(mocker, monkeypatch):
    fake_settings = mocker.MagicMock()
    fake_settings.api_token = "fake_test_token"

    monkeypatch.setattr(authentication, "get_settings", lambda: fake_settings)
    assert authentication.validate_token(fake_settings.api_token) is True
