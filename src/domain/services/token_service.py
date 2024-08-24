from datetime import datetime, timedelta, timezone

from jose import jwt

from config import Settings


def create_jwt(
    data: dict,
    secret_key: str,
    algorithm: str,
    expires_delta: timedelta | None = None
):
    """
    Create a JWT token with the given data.

    Args:
        data (dict): The data to be encoded in the token.
        secret_key (str): The secret key used to sign the token.
        algorithm (str): The algorithm used to sign the token.
        expires_delta (timedelta | None, optional): The expiration time for the token. Defaults to None, which means the token will expire in 15 minutes.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

# TODO: 여기서부터 이어서 할 거
# 내일 할 일: dependencies 전부, database,


def create_user_tokens(user_id: int) -> dict:
    """
    Create JWT access and refresh tokens for the user.

    Args:
        user_id (int): The user ID.
        secret_key (str): The secret key used to sign the tokens.

    Returns:
        dict: A dictionary containing the access and refresh tokens.
    """
    # Create Access Token
    access_token_expires = timedelta(minutes=Settings().JWT_ACCESS_EXPIRATION_TIME_MINUTES)
    access_token = create_jwt(
        data={"sub": str(user_id)},
        secret_key=Settings().JWT_SECRET_KEY,
        algorithm=Settings().JWT_ALGORITHM,
        expires_delta=access_token_expires
    )

    # Create Refresh Token
    refresh_token_expires = timedelta(minutes=Settings().JWT_REFRESH_EXPIRATION_TIME_MINUTES)
    refresh_token = create_jwt(
        data={"sub": str(user_id)},
        secret_key=Settings().JWT_SECRET_KEY,
        algorithm=Settings().JWT_ALGORITHM,
        expires_delta=refresh_token_expires
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
