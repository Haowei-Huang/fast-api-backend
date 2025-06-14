# from starlette.middleware.base import BaseHTTPMiddleware
# from typing import Annotated
# from fastapi import FastAPI, Request, Header
# from fastapi.responses import JSONResponse
# from config.auth.auth_settings import AuthSettings
# from auth import AuthUtils
# from exceptions.custom_exception import TokenNotFoundError
# import jwt
# import logging


# class AuthMiddleware(BaseHTTPMiddleware):
#     def __init__(self, app, auth_settings: AuthSettings):
#         super().__init__(app)
#         self.auth_settings = auth_settings

#     async def dispatch(self, request: Request, call_next):
#         try:
#             token = (
#                 request.headers.get("authorization", "").split(" ")[-1]
#                 if request.headers.get("authorization")
#                 else None
#             )

#             if not token:
#                 raise TokenNotFoundError("Access denied, no access token provided")

#             if AuthUtils.verify_token(
#                 token, self.auth_settings.access_token_public_key
#             ):
#                 response = await call_next(request)
#                 return response
#         except (TokenNotFoundError, jwt.InvalidTokenError) as e:
#             logging.error(f"Token validation error: {str(e)}")
#             raise e
#         except Exception as e:
#             logging.error(f"Authentication error: {str(e)}")
#             raise e
