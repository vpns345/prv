# AbdullahBot v6.0 - Final Version

AbdullahBot is a professional-grade anti-detect browser and automation tool built with Python, PyQt6, and Playwright. It is designed to manage multiple browser profiles with unique, spoofed fingerprints to bypass advanced detection systems like BrowserScan and iphey.com.

**Version 6.0 is the final, polished version, focusing on critical bug fixes and elite-level stealth.**

## Core Features

- **Playwright Engine**: The core is built on Playwright with `playwright-stealth` for a modern and undetectable automation experience.
- **Elite Fingerprint Spoofing**: Each profile gets a new, randomized, and consistent fingerprint.
  - **Client Hints (`userAgentData`)**: Full spoofing of `navigator.userAgentData` to ensure perfect consistency with the User-Agent string, a critical feature for passing modern detection sites.
  - **Canvas, AudioContext, WebGL, Fonts**: Intelligent spoofing to prevent tracking.
  - **Hardware & Geolocation**: Spoofing of hardware, timezone, and location properties.
- **Robust Network Management**:
  - **Authenticated Proxy Support**: Native handling of authenticated proxies (`user:pass`) without annoying OS popups.
  - **Protocol Selector**: UI dropdown to easily select between HTTP and SOCKS5 proxies.
  - **DNS Leak Protection**: All DNS requests are routed through the SOCKS5 proxy.
  - **Proxy Tester**: A built-in tool to test proxy connectivity before use.
- **Multi-threaded Automation**:
  - Launch hundreds of browser profiles simultaneously.
  - A "Stop All" button to gracefully close all running sessions.

## Workflow Features

- **User-Agent Based Resolution**: Screen resolution is now automatically set to a realistic value based on the selected User-Agent's device type.
- **Bulk Operations**: A full suite of tools for managing profiles at scale.
  - **Multi-Select**: Select and manage multiple profiles at once.
  - **Bulk Create, Delete, Proxy Assignment, and Fingerprint Randomization**.

## How to Use

### Installation

1.  Clone the repository.
2.  Install the required dependencies: `pip install -r requirements.txt`
3.  Install Playwright's browser binaries: `playwright install`

### Running the Application

`python main.py`

### Profile Management

- **Create**: Click "Create New Profile", enter a name, and choose a profile type (Desktop or Mobile).
- **Configure**: Select a profile and click "Configure".
  - **Proxy**: Select the protocol (HTTP/SOCKS5), enter your proxy (`host:port` or `host:port:user:pass`), and click "Test Proxy" to verify it.
  - **Geolocation**: Click "Fetch from Proxy" to auto-fill location data based on the proxy's IP.
  - **Fingerprint**: Click "Refresh Fingerprint" to generate a new identity. The User-Agent and screen resolution will update automatically.
- **Launch**: Select one or more profiles and click "Start Automation" to launch them.
