import os
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

KEYCLOAK_PUBLIC_KEY = os.getenv("KEYCLOAK_PUBLIC_KEY")
ALGORITHM = os.getenv("KEYCLOAK_ALGORITHM", "RS256")
AUDIENCE = os.getenv("KEYCLOAK_AUDIENCE")
ISSUER = os.getenv("KEYCLOAK_ISSUER")

security = HTTPBearer()

def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, KEYCLOAK_PUBLIC_KEY, algorithms=[ALGORITHM], audience=AUDIENCE, issuer=ISSUER)
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Token inválido o expirado") 