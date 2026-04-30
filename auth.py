"""Authentication — PBKDF2-HMAC-SHA256, 100,000 iterations, per-user salt.
Same security pattern as SpeakAgain (auth.py)."""

import hashlib
import os
import secrets
import streamlit as st
import db


ITERATIONS = 100_000
HASH_NAME = "sha256"
SALT_BYTES = 16


def _hash(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac(
        HASH_NAME,
        password.encode("utf-8"),
        bytes.fromhex(salt),
        ITERATIONS,
    ).hex()


def _generate_salt() -> str:
    return secrets.token_hex(SALT_BYTES)


def sign_up(username, email, password, primary_condition, gender, age, city):
    if not username or not email or not password:
        return False, "missing_fields"
    if len(password) < 8:
        return False, "password_too_short"
    if "@" not in email:
        return False, "invalid_email"

    salt = _generate_salt()
    password_hash = _hash(password, salt)

    result = db.insert_user(
        username.strip().lower(),
        email.strip().lower(),
        password_hash,
        salt,
        primary_condition,
        gender,
        age,
        city.strip(),
    )
    if isinstance(result, tuple):
        return False, result[1]
    return True, "ok"


def sign_in(username_or_email, password):
    if not username_or_email or not password:
        return None
    user = db.get_user_by_login(username_or_email.strip().lower())
    if not user:
        return None
    if _hash(password, user["salt"]) != user["password_hash"]:
        return None
    return user


def sign_out():
    for k in list(st.session_state.keys()):
        if k != "language":
            del st.session_state[k]


def change_password(user_id, old_password, new_password):
    user = db.get_user_by_id(user_id)
    if not user:
        return False
    if _hash(old_password, user["salt"]) != user["password_hash"]:
        return False
    if len(new_password) < 8:
        return False
    new_salt = _generate_salt()
    new_hash = _hash(new_password, new_salt)
    db.update_password(user_id, new_hash, new_salt)
    return True
