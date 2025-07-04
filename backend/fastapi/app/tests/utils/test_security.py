from datetime import timedelta, datetime, timezone
import pytest

from jose import jwt, JWTError

from app.utils.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)
from app.schemas.token import TokenData
from fastapi import HTTPException


def test_password_hashing_and_verification():
    password = "testpassword123"
    hashed_password = get_password_hash(password)
    assert hashed_password is not None
    assert password != hashed_password
    assert verify_password(password, hashed_password) is True
    assert verify_password("wrongpassword", hashed_password) is False


def test_create_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    assert token is not None
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "testuser"
    assert "exp" in payload


def test_create_access_token_with_expiry():
    data = {"sub": "testuser_expiry"}
    expires_delta = timedelta(minutes=15)
    token = create_access_token(data, expires_delta=expires_delta)
    assert token is not None
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "testuser_expiry"
    assert "exp" in payload
    # Check if expiry is roughly correct (within a small tolerance for execution time)
    expected_expiry_timestamp = (datetime.now(timezone.utc) + expires_delta).timestamp()
    assert abs(payload["exp"] - expected_expiry_timestamp) < 5  # 5 seconds tolerance


def test_decode_access_token_valid():
    username = "testdecodeuser"
    token = create_access_token({"sub": username})
    token_data = decode_access_token(token)
    assert token_data is not None
    assert token_data.username == username


def test_decode_access_token_invalid_signature():
    # Create a token with a different key
    invalid_secret_key = SECRET_KEY + "_invalid"
    data = {"sub": "testuser_invalid_sig"}
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    invalid_token = jwt.encode(to_encode, invalid_secret_key, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        decode_access_token(invalid_token)
    assert excinfo.value.status_code == 401
    assert "Could not validate credentials" in excinfo.value.detail


def test_decode_access_token_expired():
    data = {"sub": "testuser_expired"}
    # Create a token that expired 1 minute ago
    expires_delta = timedelta(minutes=-1)
    expired_token = create_access_token(data, expires_delta=expires_delta)

    with pytest.raises(HTTPException) as excinfo:
        decode_access_token(expired_token)
    assert excinfo.value.status_code == 401
    assert "Could not validate credentials" in excinfo.value.detail # Due to JWTError (ExpiredSignatureError)


def test_decode_access_token_no_sub():
    # Create a token without the 'sub' field
    to_encode = {"exp": (datetime.now(timezone.utc) + timedelta(minutes=15)).timestamp()}
    malformed_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        decode_access_token(malformed_token)
    assert excinfo.value.status_code == 401
    assert "Could not validate credentials" in excinfo.value.detail


def test_decode_access_token_invalid_token_format():
    invalid_token = "this.is.not.a.jwt"
    with pytest.raises(HTTPException) as excinfo:
        decode_access_token(invalid_token)
    assert excinfo.value.status_code == 401
    assert "Could not validate credentials" in excinfo.value.detail
