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


import random
import json

def generate_fingerprint(profile_type="Desktop"):
    with open("user_agents.json", "r") as f:
        user_agents = json.load(f)

    ua_list = []
    if profile_type.lower() in user_agents:
        for platform in user_agents[profile_type.lower()]:
            ua_list.extend(user_agents[profile_type.lower()][platform])

    return {
        "user_agent": random.choice(ua_list) if ua_list else "",
        "screen_width": random.choice([1920, 1680, 1440]) if profile_type == "Desktop" else random.choice([390, 414, 375]),
        "screen_height": random.choice([1080, 1050, 900]) if profile_type == "Desktop" else random.choice([844, 896, 812]),
        "hardware_concurrency": random.choice([4, 6, 8, 12, 16]),
        "device_memory": random.choice([8, 16]),
        "webgl_vendor": "Google Inc. (NVIDIA)",
        "webgl_renderer": "ANGLE (NVIDIA, NVIDIA GeForce GTX 1080 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "canvas_seed": random.randint(10000, 99999),
    }

def create_profile(profile_name, profile_type="Desktop"):
    profiles = load_profiles()
    if any(p["name"] == profile_name for p in profiles):
        raise ValueError(f"Profile '{profile_name}' already exists.")

    profile_dir = os.path.join(PROFILES_DIR, profile_name)
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)

    fingerprint = generate_fingerprint(profile_type)

    new_profile = {
        "name": profile_name,
        "profile_type": profile_type,
        "user_agent": fingerprint["user_agent"],
        "screen_width": fingerprint["screen_width"],
        "screen_height": fingerprint["screen_height"],
        "timezone": "",
        "latitude": "",
        "longitude": "",
        "proxy": "",
        "disable_webrtc": True,
        "fingerprint": fingerprint
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
