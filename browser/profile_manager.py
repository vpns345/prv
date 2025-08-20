import json
import os
import shutil

PROFILES_FILE = "profiles/profiles.json"
PROFILES_DIR = "profiles"


def load_profiles():
    if not os.path.exists(PROFILES_FILE):
        return []
    with open(PROFILES_FILE, "r") as f:
        return json.load(f)


def save_profiles(profiles):
    with open(PROFILES_FILE, "w") as f:
        json.dump(profiles, f, indent=4)


def create_profile(profile_name):
    profiles = load_profiles()
    if any(p["name"] == profile_name for p in profiles):
        raise ValueError(f"Profile '{profile_name}' already exists.")

    profile_dir = os.path.join(PROFILES_DIR, profile_name)
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)

    new_profile = {
        "name": profile_name,
        "user_agent": "",
        "screen_width": 1920,
        "screen_height": 1080,
        "timezone": "",
        "latitude": "",
        "longitude": "",
        "proxy": "",
        "disable_webrtc": True,
    }
    profiles.append(new_profile)
    save_profiles(profiles)
    return new_profile


def delete_profile(profile_name):
    profiles = load_profiles()
    profiles = [p for p in profiles if p["name"] != profile_name]
    save_profiles(profiles)

    profile_dir = os.path.join(PROFILES_DIR, profile_name)
    if os.path.exists(profile_dir):
        shutil.rmtree(profile_dir)


def update_profile(updated_profile):
    profiles = load_profiles()
    for i, p in enumerate(profiles):
        if p["name"] == updated_profile["name"]:
            profiles[i] = updated_profile
            break
    save_profiles(profiles)
