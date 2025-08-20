import requests
import re

def parse_proxy(proxy_input: str, protocol: str):
    """
    Parses different proxy formats and constructs a valid URL.
    Expected formats:
    - host:port
    - host:port:user:pass
    """
    if not proxy_input:
        return None

    parts = proxy_input.split(':')
    host = parts[0]
    port = parts[1]

    if len(parts) == 4:
        user = parts[2]
        password = parts[3]
        return f"{protocol.lower()}://{user}:{password}@{host}:{port}"
    elif len(parts) == 2:
        return f"{protocol.lower()}://{host}:{port}"
    else:
        raise ValueError("Invalid proxy format. Use host:port or host:port:user:pass")

def get_geo_from_proxy(proxy_input: str, protocol: str):
    """
    Extracts the IP from a proxy string and fetches geolocation data.
    """
    if not proxy_input:
        return None

    host = proxy_input.split(':')[0]
    if not host:
        raise ValueError("Could not extract host from proxy string")

    try:
        # Use a proxy to make the geo API request itself, to test the proxy
        # This is a bit redundant with test_proxy but good for this specific function
        full_proxy_url = parse_proxy(proxy_input, protocol)
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
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to connect to geo API: {e}")

def test_proxy(proxy_input: str, protocol: str):
    """
    Tests if a proxy is working by making a request through it.
    Returns (True, message) on success, (False, message) on failure.
    """
    if not proxy_input:
        return False, "Proxy string is empty."

    try:
        full_proxy_url = parse_proxy(proxy_input, protocol)
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
