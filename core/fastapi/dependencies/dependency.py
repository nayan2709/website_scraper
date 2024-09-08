from fastapi import Request, HTTPException, status
from core.config import config


class IsAuthenticated:
    def __init__(self):
        self.static_token = config.AUTH_TOKEN

    async def __call__(self, request: Request):
        # Get the Authorization header
        authorization: str = request.headers.get("Authorization")

        if not authorization or not authorization.startswith("Bearer "):
            # If no authorization header or it doesn't start with 'Bearer', deny access
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization token not provided or invalid",
            )

        # Extract the token from the Authorization header
        token = authorization.split(" ")[1]

        # Compare the token with your static token
        if token != self.static_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )
        return True
