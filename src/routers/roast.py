from fastapi import APIRouter

import urllib.parse
import requests

from enum import Enum

import auth
from routers import user
from consts import BASE_URL, DEFAULT_HEADERS

router = APIRouter()

class RoastProfile(str, Enum):
    contest = 'contest'
    advance = 'advance'
    user = 'user'

@router.get("/{profile_type}/profiles/get")
async def get_profiles(profile_type: RoastProfile, token: str):
    profiles_path = f"/api/roast/{profile_type}/profiles/get"
    get_profiles_url = urllib.parse.urljoin(BASE_URL, profiles_path)

    print(get_profiles_url)

    r = requests.post(get_profiles_url, 
                      headers=DEFAULT_HEADERS,
                      verify=False,
                      json={
                          'structVersion': 1,
                          'page': 0,
                          'size': 9999,
                          'model': ''
                      },
                      auth=auth.BearerAuth(token)
                    )
    return {"message": r.json()}

@router.get("/{profile_type}/profile/{profile_id}")
async def get_profile_by_id(profile_type: RoastProfile, profile_id: str, token: str):
    profile_path = f"/api/roast/{profile_type}/profile/{profile_id}"
    get_profile_by_id_url = urllib.parse.urljoin(BASE_URL, profile_path)

    print(get_profile_by_id_url)

    r = requests.get(get_profile_by_id_url, 
                      headers=DEFAULT_HEADERS,
                      verify=False,
                      auth=auth.BearerAuth(token)
                    )
    return {"message": r.json()}

router.include_router(user.router, prefix="/user")
