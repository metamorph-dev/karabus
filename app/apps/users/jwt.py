from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer


JSONWebToken = Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer(auto_error=False))]
