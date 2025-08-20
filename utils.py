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
