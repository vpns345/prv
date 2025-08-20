import requests
import re

def get_geo_from_proxy(proxy_str):
    """
    Extracts the IP from a proxy string and fetches geolocation data.
    Proxy format: http://user:pass@host:port or socks5://user:pass@host:port or ip:port
    """
    if not proxy_str:
        return None

    # Extract host from the proxy string
    match = re.search(r'@?([^:]+):\d+', proxy_str)
    host = match.group(1) if match else None
    if not host:
        # Fallback for ip:port format
        match = re.search(r'([^:]+):\d+', proxy_str)
        host = match.group(1) if match else None

    if not host:
        raise ValueError("Could not extract host from proxy string")

    try:
        response = requests.get(f"http://ip-api.com/json/{host}")
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

def test_proxy(proxy_str):
    """
    Tests if a proxy is working by making a request through it.
    Returns (True, message) on success, (False, message) on failure.
    """
    if not proxy_str:
        return False, "Proxy string is empty."

    proxies = {
        "http": proxy_str,
        "https": proxy_str,
    }

    try:
        response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=10)
        response.raise_for_status()
        # The response from httpbin.org/ip will contain the proxy's IP if successful
        return True, f"Proxy is working. IP: {response.json()['origin']}"
    except requests.exceptions.ProxyError as e:
        return False, f"Proxy Error: {e}"
    except requests.exceptions.RequestException as e:
        return False, f"Request Failed: {e}"
