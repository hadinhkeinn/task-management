import pytest
from datetime import timedelta
from jose import jwt
from fastapi import HTTPException
from app.core.security import hash_password, verify_password, create_access_token, decode_token
from app.core.config import settings

def test_password_hashing():
    password = "secretpassword"
    hashed = hash_password(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

def test_create_and_decode_token():
    data = {"sub": "123", "role": "user"}
    token = create_access_token(data)
    
    decoded = decode_token(token)
    assert decoded["sub"] == "123"
    assert decoded["role"] == "user"
    assert "exp" in decoded

def test_expired_token_raises_exception():
    data = {"sub": "123"}
    token = create_access_token(data, expires_delta=timedelta(minutes=-10))
    
    with pytest.raises(HTTPException) as exc_info:
        decode_token(token)
    
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"
