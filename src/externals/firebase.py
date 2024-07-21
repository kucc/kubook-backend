"""
참고:
- https://gist.github.com/billydh/734e5cc4d78d46e497b4f0589bc34ac0
- https://firebase.google.com/docs/reference/rest/auth?hl=ko#section-sign-in-email-password
"""

import argparse
import json
import os
import requests
import pprint

from fastapi import HTTPException, status

from config import Settings

FIREBASE_WEB_API_KEY = Settings().FIREBASE_WEB_API_KEY
rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"


async def sign_in_with_email_and_password(email: str, password: str, return_secure_token: bool = True):
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": return_secure_token
    })

    r = requests.post(rest_api_url,
                      params={"key": FIREBASE_WEB_API_KEY},
                      data=payload)
    response = r.json()

    try:
        local_id = None
        local_id = response["localId"]
        if local_id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except:
        error_message = response["error"]["message"]
        if error_message == "EMAIL_NOT_FOUND":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        elif error_message == "INVALID_PASSWORD":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
        elif error_message == "USER_DISABLED":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User disabled")

    return response
