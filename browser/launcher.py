import os
import time
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from .scripts import CANVAS_SPOOFING_SCRIPT

PROFILES_DIR = "profiles"


def launch_browser(profile):
    options = webdriver.ChromeOptions()

    # Profile path
    profile_path = os.path.join(os.getcwd(), PROFILES_DIR, profile["name"])
    options.add_argument(f"user-data-dir={profile_path}")

    # User-Agent
    if profile.get("user_agent"):
        options.add_argument(f"user-agent={profile['user_agent']}")

    # Proxy
    if profile.get("proxy"):
        options.add_argument(f"--proxy-server={profile['proxy']}")

    # Disable WebRTC
    if profile.get("disable_webrtc"):
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--disable-webrtc-multiple-routes")
        options.add_argument("--disable-webrtc-encryption")

    # Headless or not
    # options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    # Screen Resolution
    if profile.get("screen_width") and profile.get("screen_height"):
        driver.set_window_size(profile["screen_width"], profile["screen_height"])

    # Geolocation and Timezone
    params = {
        "timezoneId": profile.get("timezone"),
        "latitude": float(profile.get("latitude", 0)),
        "longitude": float(profile.get("longitude", 0)),
        "accuracy": 100
    }
    if params["timezoneId"]:
        driver.execute_cdp_cmd("Emulation.setTimezoneOverride", {"timezoneId": params["timezoneId"]})
    if params["latitude"] and params["longitude"]:
        driver.execute_cdp_cmd("Emulation.setGeolocationOverride", params)

    # Canvas and WebGL spoofing will be done via injected script.
    # For now, we will just launch the browser.
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": CANVAS_SPOOFING_SCRIPT
    })

    return driver
