import os
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from .scripts import CANVAS_SPOOFING_SCRIPT

PROFILES_DIR = "profiles"

def launch_browser(profile, start_url=None):
    options = webdriver.ChromeOptions()
    profile_type = profile.get("profile_type", "Desktop")

    # Common options
    profile_path = os.path.join(os.getcwd(), PROFILES_DIR, profile["name"])
    options.add_argument(f"user-data-dir={profile_path}")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Proxy
    if profile.get("proxy"):
        options.add_argument(f"--proxy-server={profile['proxy']}")

    # WebRTC
    if profile.get("disable_webrtc"):
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--disable-webrtc-multiple-routes")
        options.add_argument("--disable-webrtc-encryption")

    # Profile-type specific options
    if profile_type == "Mobile":
        if profile.get("user_agent"):
            mobile_emulation = {
                "deviceMetrics": {
                    "width": profile.get("screen_width", 390),
                    "height": profile.get("screen_height", 844),
                    "pixelRatio": 3.0
                },
                "userAgent": profile.get("user_agent")
            }
            options.add_experimental_option("mobileEmulation", mobile_emulation)
    else: # Desktop
        if profile.get("user_agent"):
            options.add_argument(f"user-agent={profile['user_agent']}")

    # Initialize driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    # Apply stealth only to desktop profiles
    if profile_type == "Desktop":
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

    # Set window size only for desktop profiles
    if profile_type == "Desktop":
        driver.set_window_size(profile["screen_width"], profile["screen_height"])

    # Geolocation and Timezone
    try:
        if profile.get("timezone"):
            driver.execute_cdp_cmd("Emulation.setTimezoneOverride", {"timezoneId": profile["timezone"]})

        if profile.get("latitude") and profile.get("longitude"):
            params = {
                "latitude": float(profile.get("latitude")),
                "longitude": float(profile.get("longitude")),
                "accuracy": 100
            }
            driver.execute_cdp_cmd("Emulation.setGeolocationOverride", params)
    except Exception:
        # Ignore errors if lat/lon are not valid floats
        pass

    # Inject scripts
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": CANVAS_SPOOFING_SCRIPT
    })

    # Navigate to start URL
    if start_url:
        driver.get(start_url)

    return driver
