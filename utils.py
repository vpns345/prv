import requests
import re

def parse_proxy(proxy_input: str, protocol: str):
    """
    Parses different proxy formats and returns a dictionary for Playwright.
    Expected formats:
    - host:port
    - host:port:user:pass
    """
    if not proxy_input:
        return None

    parts = proxy_input.split(':')
    if len(parts) not in [2, 4]:
        raise ValueError("Invalid proxy format. Use host:port or host:port:user:pass")

    host = parts[0]
    port = parts[1]
    server = f"{protocol.lower()}://{host}:{port}"

    if len(parts) == 4:
        return {
            "server": server,
            "username": parts[2],
            "password": parts[3]
        }
    else: # len(parts) == 2
        return {"server": server}

def get_geo_from_proxy(proxy_input: str, protocol: str):
    """
    Extracts the IP from a proxy string and fetches geolocation data.
    """
    if not proxy_input:
        return None

    try:
        # Use a proxy to make the geo API request itself, to test the proxy
        proxy_dict = parse_proxy(proxy_input, protocol)
        # requests library needs a different format than playwright
        full_proxy_url = proxy_dict['server']
        if 'username' in proxy_dict:
            # Rebuild the URL for requests
            proto, url = full_proxy_url.split('://')
            full_proxy_url = f"{proto}://{proxy_dict['username']}:{proxy_dict['password']}@{url}"

        proxies = {"http": full_proxy_url, "https": full_proxy_url}
        response = requests.get("http://ip-api.com/json/", proxies=proxies, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "success":
            return {
                "timezone": data.get("timezone"),
                "latitude": data.get("lat"),
                "longitude": data.get("lon"),
            }
        else:
            raise Exception(f"API Error: {data.get('message')}")
    except (requests.exceptions.RequestException, ValueError) as e:
        raise Exception(f"Failed to connect to geo API: {e}")

def test_proxy(proxy_input: str, protocol: str):
    """
    Tests if a proxy is working by making a request through it.
    Returns (True, message) on success, (False, message) on failure.
    """
    if not proxy_input:
        return False, "Proxy string is empty."

    try:
        proxy_dict = parse_proxy(proxy_input, protocol)
        full_proxy_url = proxy_dict['server']
        if 'username' in proxy_dict:
            proto, url = full_proxy_url.split('://')
            full_proxy_url = f"{proto}://{proxy_dict['username']}:{proxy_dict['password']}@{url}"

        proxies = {
            "http": full_proxy_url,
            "https": full_proxy_url,
        }
        response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=10)
        response.raise_for_status()
        return True, f"Proxy is working. IP: {response.json()['origin']}"
    except ValueError as e:
        return False, str(e)
    except requests.exceptions.ProxyError as e:
        return False, f"Proxy Error: {e}"
    except requests.exceptions.RequestException as e:
        return False, f"Request Failed: {e}"
