import requests
from fastapi.security import HTTPAuthorizationCredentials

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token: HTTPAuthorizationCredentials):
        self.token = str(token)
    def __call__(self, r):
        r.headers["authorization"] = "Token " + self.token
        return r