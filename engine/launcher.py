import os
from playwright_stealth import stealth_async
from .async_manager import async_manager
from .fingerprint import (
    CANVAS_SPOOFING_SCRIPT, AUDIO_SPOOFING_SCRIPT, FONTS_SPOOFING_SCRIPT,
    HARDWARE_SPOOFING_SCRIPT, WEBGL_SPOOFING_SCRIPT
)

PROFILES_DIR = "profiles"

async def launch_browser(profile, start_url=None):
    # Ensure playwright is ready
    await async_manager._playwright_ready

    p = async_manager.playwright
    profile_path = os.path.join(os.getcwd(), PROFILES_DIR, profile["name"])
    if not os.path.exists(profile_path):
        os.makedirs(profile_path)

    proxy_server = profile.get("proxy")
    proxy_dict = {"server": proxy_server} if proxy_server else None

    browser_context = await p.chromium.launch_persistent_context(
        user_data_dir=profile_path,
        headless=False,
        proxy=proxy_dict,
        args=['--disable-blink-features=AutomationControlled'],
        user_agent=profile.get("user_agent"),
        viewport={
            "width": profile.get("screen_width", 1920),
            "height": profile.get("screen_height", 1080)
        }
    )

    page = browser_context.pages[0]
    await stealth_async(page)

    # Inject all fingerprinting scripts
    fingerprint = profile.get("fingerprint", {})
    await page.evaluate_on_new_document(CANVAS_SPOOFING_SCRIPT, fingerprint.get("canvas_seed", 12345))
    await page.evaluate_on_new_document(AUDIO_SPOOFING_SCRIPT)
    await page.evaluate_on_new_document(FONTS_SPOOFING_SCRIPT)
    await page.evaluate_on_new_document(
        HARDWARE_SPOOFING_SCRIPT,
        {"concurrency": fingerprint.get("hardware_concurrency", 8), "memory": fingerprint.get("device_memory", 16)}
    )
    await page.evaluate_on_new_document(
        WEBGL_SPOOFING_SCRIPT,
        {"vendor": fingerprint.get("webgl_vendor", "Google Inc."), "renderer": fingerprint.get("webgl_renderer", "ANGLE")}
    )

    if start_url:
        await page.goto(start_url)

    return browser_context, page
