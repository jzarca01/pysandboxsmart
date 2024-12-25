from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import HTTPBasicCredentials
from typing import Annotated

import urllib.parse
import requests
from requests.exceptions import HTTPError

import auth
from consts import BASE_URL, DEFAULT_HEADERS
from security import security

router = APIRouter()

@router.post("/login")
async def login(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    login_url = urllib.parse.urljoin(BASE_URL, '/api/authn/signInByEmail/v3')
    
    try:
      r = requests.post(login_url, 
                        json={
                              "password": credentials.password,
                              "userName": credentials.username,
                              "email": credentials.username
                          },
                        headers=DEFAULT_HEADERS,
                        verify=False
                      )
      if r.ok:
        response = r.json()
        return { **response['resultBody'], "access_token": response['resultBody']['user']['tokenid'], "token_type": "bearer" }
      raise r.raise_for_status()
    except HTTPError as err:
       raise HTTPException(err)
       

@router.post("/user/token")
async def get_token(token: str):
    get_token_url = urllib.parse.urljoin(BASE_URL, '/api/authn/user/token')

    try: 
      r = requests.post(get_token_url, 
                      headers=DEFAULT_HEADERS,
                      verify=False,
                      auth=auth.BearerAuth(token)
                    )
      if r.ok:
        response = r.json()
        return { **response['resultBody'], "access_token": response['resultBody']['user']['tokenid'], "token_type": "bearer" }
      raise r.raise_for_status()
    except HTTPError as err:
       raise HTTPException(err)
