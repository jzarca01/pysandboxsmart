import requests
import json

from settings import USERNAME, PASSWORD

def get_access_token(username: str, password: str) -> str:
    r = requests.post("http://localhost:8000/auth/login", 
        auth=(username, password),
        verify=False
    )
    response = r.json()
    return response["access_token"]

def get_profiles(profile_type: str, access_token: str):
    r = requests.get(f"http://localhost:8000/roast/{profile_type}/profiles/get", 
        verify=False,
        params={
            "token":access_token
        }
    )
    return r.json()

def get_profile(profile_type: str, profile_id: str, access_token: str):
    r = requests.get(f"http://localhost:8000/roast/{profile_type}/profile/{profile_id}", 
        verify=False,
        params={
            "token":access_token
        }
    )
    return r.json()

def get_filename(profile_type: str, profile) -> str:
    locale_name = profile['profile']['localeDictionary']['profileName']['en_US']
    return f"{profile_type} {locale_name}"

def print_to_file(filename: str, content):
    with open(f'{filename}.json', 'w') as f:
        json.dump(content, file=f, ensure_ascii=False, indent=4)

def extract_all_profiles():
    access_token = get_access_token(USERNAME, PASSWORD)
    profiles_types = ['contest', 'advance']

    all_profiles = []
    for type in profiles_types:
        response = get_profiles(type, access_token)
        profiles = response['profiles']['content']

        for item in profiles:
            profile_id = item["profileId"]
            profile_info = get_profile(type, profile_id, access_token)
            filename = get_filename(type, profile_info)
            # print_to_file(filename, profile_info)
            all_profiles.append({**profile_info, "profile_type": type, "filename": filename})
    print_to_file('all_profiles', all_profiles)

def create_profile_files():
    with open('all_profiles.json', 'r') as file:
        data = json.load(file)
        for item in data["items"]:
            filename = item["filename"]
            print_to_file(filename, item)
        

if __name__ == '__main__':
    # extract_all_profiles()
    # create_profile_files()
    print('main thread')