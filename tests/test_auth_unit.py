from datetime import timedelta

from auth import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_is_hashed_and_verifies():
    password = "StrongPassword123!"
    hashed_password = hash_password(password)

    assert hashed_password != password
    assert verify_password(password, hashed_password)
    assert not verify_password("WrongPassword123!", hashed_password)


def test_access_token_contains_identity_and_expires():
    token = create_access_token(
        {"sub": "user-123", "email": "user@example.com"},
        expires_delta=timedelta(minutes=5),
    )

    claims = decode_access_token(token)

    assert claims is not None
    assert claims["sub"] == "user-123"
    assert claims["email"] == "user@example.com"
    assert "exp" in claims


def test_invalid_access_token_is_rejected():
    assert decode_access_token("not-a-valid-token") is None
