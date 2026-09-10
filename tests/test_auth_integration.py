import os
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

import app as app_module
from db.database import SessionLocal
from db.models import User

pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_INTEGRATION") != "1",
    reason="Set RUN_INTEGRATION=1 to run tests against PostgreSQL",
)


def test_signup_and_login_use_postgres():
    email = f"integration-{uuid4().hex}@example.com"
    password = "StrongPassword123!"

    with TestClient(app_module.app) as client:
        signup_response = client.post(
            "/signup",
            json={"email": email, "password": password},
        )
        login_response = client.post(
            "/login",
            json={"email": email, "password": password},
        )
        invalid_login_response = client.post(
            "/login",
            json={"email": email, "password": "WrongPassword123!"},
        )

    try:
        assert signup_response.status_code == 201
        assert signup_response.json()["email"] == email
        assert "hashed_password" not in signup_response.json()

        assert login_response.status_code == 200
        assert login_response.json()["token_type"] == "bearer"
        assert login_response.json()["access_token"]

        assert invalid_login_response.status_code == 401
    finally:
        with SessionLocal() as db:
            db.execute(delete(User).where(User.email == email))
            db.commit()
