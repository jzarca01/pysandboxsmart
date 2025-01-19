from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import Literal, List, Optional

import urllib.parse
import requests
from requests.exceptions import HTTPError

import auth
from consts import BASE_URL, DEFAULT_HEADERS

router = APIRouter()

class DataPoint(BaseModel):
    doorAngle: int
    continuousTime: int = Field(ge=0)
    timeline: int
    heatPower: int = Field(100, ge=0, le=100)
    temperature: Optional[int] = Field(0, ge=0, le=250)
    fanSpeed: int = Field(100, ge=0, le=100)
    drumSpeed: int = Field(100, ge=0, le=100)

class PreHeat(BaseModel):
    continuousTime: int = Field(ge=0)
    temperature: int = Field(ge=0)

class ExpectedResult(BaseModel):
    roastDegreeShell: int
    roastDegreeKernel: int

class CoffeeRawBean(BaseModel):
    process: Literal['GA', 'Washed', 'Natural', 'Honey', 'Anaerobic', 'Others']
    region: Literal['GA', 'AF', 'AM', 'CA', 'SA', 'AS']
    country: Literal['GA', 'MW', 'KY', 'YE', 'ET', 'PE', 'HN', 'PG', 'SV', 'ID', 'GT', 'BR', 'CR', 'CO', 'Others', 'PM', 'RW']
    altitude: Optional[Literal['EXTREMEHIGH']] = 'EXTREMEHIGH'
    variety: Optional[Literal['Original']] = 'Original'
    level: Optional[Literal['G1']] = 'G1',
    flavor: Optional[Literal['GA', 'Tasty', '#Tasty']] = 'GA',

class Data(BaseModel):
    plannedHeats: List[DataPoint]
    crackConfig: DataPoint
    crackConfig2: DataPoint
    preHeat: PreHeat
    relativeHumidity: int = Field(gt=0, le=100)
    roomTemperature: int
    beanWeight: int
    isFavorite: Optional[bool] = False
    isLastUsed: Optional[bool] = False

class Profile(BaseModel):
    rawBeanWeight: int
    supportVoltage: Literal['GA', 'AC110', 'AC220']
    supportModel: Literal['R1','R2']
    profileRole: str = 'User'
    profileName: str = Field(..., max_length=25)
    profileId: str
    structType: str = "Roast"
    structVersion: int = 1
    revision: int = 0

    expectedResult: ExpectedResult
    coffeeRawBean: CoffeeRawBean
    data: Data

@router.post("/create")
async def create_profile(profile: Profile, token: str):
    profile_path = f"/api/roast/user/profile/post"
    create_profile_url = urllib.parse.urljoin(BASE_URL, profile_path)

    try:
        r = requests.post(create_profile_url, 
                        headers=DEFAULT_HEADERS,
                        verify=False,
                        json=jsonable_encoder(profile),
                        auth=auth.BearerAuth(token)
                        )
        if r.ok:
            response = r.json()
            return response['resultBody']
        raise r.raise_for_status()
    except HTTPError as err:
       raise HTTPException(err)

@router.patch("/edit/{profile_id}")
async def edit_profile_by_id(profile_id: str, profile: Profile, token: str):
    profile_path = f"/api/roast/user/profile/patch/{profile_id}"
    edit_profile_by_id_url = urllib.parse.urljoin(BASE_URL, profile_path)

    try:
        r = requests.patch(edit_profile_by_id_url, 
                      headers=DEFAULT_HEADERS,
                      verify=False,
                      json=jsonable_encoder(profile),
                      auth=auth.BearerAuth(token)
                    )
        if r.ok:
            response = r.json()
            return response['resultBody']
        raise r.raise_for_status()
    except HTTPError as err:
       raise HTTPException(err)

@router.get("/results")
async def get_results(token: str):
    results_path = f"/api/roast/results/get"
    results_url = urllib.parse.urljoin(BASE_URL, results_path)

    results_filters = {
        "lowOfRawBeanWeight": 0,
        "structVersion": 1,
        "structType": "Roast",
        "beanProcessSet": ["GA", "Washed", "Natural", "Honey", "Anaerobic", "Others"],
        "beanRegion": "",
        "size": 100,
        "timePeriod": "",
        "model": "",
        "sortMap": {
            "createDate": "DESC"
        },
        "upperOfRawBeanWeight": 550,
        "page": 0
    }

    try:
        r = requests.post(results_url, 
                      headers=DEFAULT_HEADERS,
                      verify=False,
                      json=jsonable_encoder(results_filters),
                      auth=auth.BearerAuth(token)
                    )
        if r.ok:
            response = r.json()
            return response['resultBody']
        raise r.raise_for_status()
    except HTTPError as err:
       raise HTTPException(err)

@router.get("/results/{result_id}")
async def get_result_by_id(result_id: str, token: str):
    results_path = f"/api/roast/result/get/{result_id}"
    results_url = urllib.parse.urljoin(BASE_URL, results_path)

    try:
        r = requests.post(results_url, 
                      headers=DEFAULT_HEADERS,
                      verify=False,
                      auth=auth.BearerAuth(token)
                    )
        if r.ok:
            response = r.json()
            return response['resultBody']
        raise r.raise_for_status()
    except HTTPError as err:
       raise HTTPException(err)
    
@router.post("/results/share/{result_id}")
async def share_result_by_id(result_id: str, profile: Profile, email: str, token: str):
    results_path = f"/api/roast/result/share"
    results_url = urllib.parse.urljoin(BASE_URL, results_path)

    share_result = {
        "resultId": result_id,
        "profileName": profile.profileName,
        "email": email
    }

    try:
        r = requests.post(results_url, 
                      headers=DEFAULT_HEADERS,
                      json=jsonable_encoder(share_result),
                      verify=False,
                      auth=auth.BearerAuth(token)
                    )
        if r.ok:
            response = r.json()
            return response['resultBody']
        raise r.raise_for_status()
    except HTTPError as err:
       raise HTTPException(err)
    
@router.patch("/results/{result_id}")
async def edit_result_by_id(result_id: str, profile: Profile, token: str):
    results_path = f"/api/roast/result/patch/v2/{result_id}"
    results_url = urllib.parse.urljoin(BASE_URL, results_path)

    try:
        r = requests.patch(results_url, 
                      headers=DEFAULT_HEADERS,
                      verify=False,
                      json=jsonable_encoder(profile),
                      auth=auth.BearerAuth(token)
                    )
        if r.ok:
            response = r.json()
            return response['resultBody']
        raise r.raise_for_status()
    except HTTPError as err:
       raise HTTPException(err)