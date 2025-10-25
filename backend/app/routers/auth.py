# This file handles user authentication and JWT token generation.
# All code, comments, and docstrings are in English.

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

# Import the Pydantic models (schemas) defined in step (1.5)
# Use relative import (..) to go up one level from 'routers' to 'app'
from .. import schemas

# --- Configuration ---

# This secret key should be complex and stored securely (e.g., in .env)
# DO NOT hardcode this in production.
SECRET_KEY = "your-super-secret-key-please-change-this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# This is the OAuth2 scheme definition.
# It tells FastAPI which URL to check for the token.
# We will import this `oauth2_scheme` in dependencies.py (2.2)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Router Definition ---

router = APIRouter(
    tags=["Authentication"] # Group this endpoint in the OpenAPI docs
)

# --- Simulated User Database ---

# This is a mock database. In a real application,
# you would fetch this user from your SQLAlchemy models.
# The password for 'admin' is 'adminpass'
FAKE_USER_DB = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "email": "admin@example.com",
        "hashed_password": "$2b$12$T.G.O.Wf.u8xW.1.o.M.P.uvYkSEuI5xT/yypn2sMhE9wp3T/i56O", # This hash is for "adminpass"
        "disabled": False,
    }
}

# --- Helper Functions ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a stored hash.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Generates a bcrypt hash for a given password.
    (Used here to create the hash for the fake DB)
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generates a new JWT access token.

    Args:
        data (dict): The data to encode in the token (e.g., {"sub": username}).
        expires_delta (Optional[timedelta]): Optional expiration time.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Default expiration if not provided
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Simulated Authentication Logic ---

def get_user_from_db(username: str) -> Optional[dict]:
    """
    Simulated function to retrieve a user from the database.
    In a real app, this would be a CRUD call.
    """
    if username in FAKE_USER_DB:
        user_dict = FAKE_USER_DB[username]
        # Here you could map the dict to a Pydantic model or SQLAlchemy model
        return user_dict
    return None

def authenticate_user(username: str, password: str) -> Optional[dict]:
    """
    Authenticates a user by checking username and verifying password.
    Returns the user object (dict) if successful, else None.
    """
    user = get_user_from_db(username)
    if not user:
        return None # User not found

    if not verify_password(password, user["hashed_password"]):
        return None # Invalid password

    if user["disabled"]:
        return None # User account is disabled

    return user

# --- API Endpoint ---

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Provides a JWT access token for a valid user.

    This endpoint implements the OAuth2 password flow.
    The client must send 'username' and 'password'
    in a 'application/x-www-form-urlencoded' body.
    """

    # 1. Authenticate the user
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        # If authentication fails, raise a 401 Unauthorized error
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}, # Standard header for auth errors
        )

    # 2. Create the access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, # 'sub' (subject) is the standard JWT claim for the user
        expires_delta=access_token_expires
    )

    # 3. Return the token in the format defined by schemas.Token
    return {"access_token": access_token, "token_type": "bearer"}

