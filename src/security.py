from fastapi.security import HTTPBasic, HTTPBearer

security = HTTPBasic()
bearer_token = HTTPBearer()