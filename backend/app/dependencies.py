# This file defines reusable dependencies for the API,
# primarily for handling authentication.
# All code, comments, and docstrings are in English.

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

# Use relative import (.) for sibling modules
from . import schemas
# Use relative import (.) to access the 'routers' package, then 'auth'
from .routers.auth import SECRET_KEY, ALGORITHM, oauth2_scheme

# Note: oauth2_scheme is defined in routers/auth.py and imported here.
# It uses tokenUrl="token", pointing to the /token endpoint in auth.py.


def get_current_user(token: str = Depends(oauth2_scheme)) -> schemas.TokenData:
    """
    Dependency to get the current user from a JWT token.

    This function is used to protect endpoints. It decodes the token,
    validates its signature and expiration, and extracts the user identity.

    Args:
        token (str): The OAuth2 Bearer token provided in the Authorization header.

    Raises:
        HTTPException (401): If the token is invalid, expired, or
                              the signature is incorrect.

    Returns:
        schemas.TokenData: An object containing the username (from the 'sub' claim).
    """

    # This is the standard exception to raise for any authentication failure
    # It includes the "Bearer" challenge in the WWW-Authenticate header.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # The 'sub' (subject) claim is used to store the user's identity (username)
        username: str = payload.get("sub")

        if username is None:
            # If the 'sub' claim is missing
            raise credentials_exception

        # We validate the data using our Pydantic schema
        token_data = schemas.TokenData(username=username)

    except JWTError:
        # This catches invalid signatures, expired tokens, etc.
        raise credentials_exception

    # In a real app, you might also fetch the full user object from the DB
    # using this username to check if they are active, etc.
    # For this project, returning the TokenData is sufficient for authorization.

    return token_data

