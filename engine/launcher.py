import os
import playwright_stealth
from .async_manager import async_manager
from utils import parse_proxy
from .fingerprint import (
    CANVAS_PATCH_SCRIPT, AUDIO_PATCH_SCRIPT, FONTS_PATCH_SCRIPT,
    HARDWARE_PATCH_SCRIPT, WEBGL_PATCH_SCRIPT, USER_AGENT_DATA_PATCH_SCRIPT
)

PROFILES_DIR = "profiles"

async def launch_browser(profile, start_url=None):
    # Ensure playwright is ready
    await async_manager._playwright_ready

    p = async_manager.playwright
    profile_path = os.path.join(os.getcwd(), PROFILES_DIR, profile["name"])
    if not os.path.exists(profile_path):
        os.makedirs(profile_path)

    proxy_input = profile.get("proxy")
    proxy_protocol = profile.get("proxy_protocol", "HTTP")

    proxy_dict = None
    if proxy_input:
        try:
            proxy_dict = parse_proxy(proxy_input, proxy_protocol)
        except ValueError as e:
            print(f"Skipping invalid proxy for profile {profile['name']}: {e}")

    browser_context = await p.chromium.launch_persistent_context(
        user_data_dir=profile_path,
        headless=False,
        proxy=proxy_dict,
        channel="chrome",
        args=['--disable-blink-features=AutomationControlled'],
        user_agent=profile.get("user_agent"),
        viewport={
            "width": profile.get("screen_width", 1920),
            "height": profile.get("screen_height", 1080)
        },
        timezone_id=profile.get("timezone")
    )

    page = browser_context.pages[0]
    await playwright_stealth.stealth_async(page)

    # Inject all fingerprinting scripts
    fingerprint = profile.get("fingerprint", {})
    if 'user_agent_data' in fingerprint:
        await page.evaluate_on_new_document(USER_AGENT_DATA_PATCH_SCRIPT, fingerprint['user_agent_data'])

    await page.evaluate_on_new_document(CANVAS_PATCH_SCRIPT, fingerprint.get("canvas_seed", 12345))
    await page.evaluate_on_new_document(AUDIO_PATCH_SCRIPT)
    await page.evaluate_on_new_document(FONTS_PATCH_SCRIPT)
    await page.evaluate_on_new_document(
        HARDWARE_PATCH_SCRIPT,
        {"concurrency": fingerprint.get("hardware_concurrency", 8), "memory": fingerprint.get("device_memory", 16)}
    )
    await page.evaluate_on_new_document(
        WEBGL_PATCH_SCRIPT,
        {"vendor": fingerprint.get("webgl_vendor", "Google Inc."), "renderer": fingerprint.get("webgl_renderer", "ANGLE")}
    )

    # Geolocation can still be set via CDP
    try:
        if profile.get("latitude") and profile.get("longitude"):
            await page.context.set_geolocation({
                "latitude": float(profile.get("latitude")),
                "longitude": float(profile.get("longitude"))
            })
    except Exception as e:
        print(f"Could not set geolocation for profile {profile['name']}: {e}")

    print(f"Launching profile {profile['name']}. Target URL: {start_url}")
    if start_url:
        try:
            await page.goto(start_url, timeout=60000)
            print(f"Successfully navigated to {start_url} for profile {profile['name']}")
        except Exception as e:
            print(f"Error navigating to {start_url} for profile {profile['name']}: {e}")

    return browser_context, page
