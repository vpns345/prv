# AbdullahBot v3.0 - Professional Anti-Detect Browser

AbdullahBot is a professional-grade anti-detect browser and automation tool built with Python, PyQt6, and Playwright. It is designed to manage multiple browser profiles with unique, spoofed fingerprints to bypass advanced detection systems.

## Core Features

- **Playwright Engine**: The core is built on Playwright with `playwright-stealth` for a more modern and undetectable automation experience compared to Selenium.
- **Isolated Profiles**: Create and manage unlimited browser profiles. Each profile's data (cookies, cache, etc.) is stored in a separate folder, ensuring complete isolation.
- **Advanced Fingerprint Spoofing**: Each profile gets a new, randomized, but consistent fingerprint.
  - **Canvas, AudioContext, WebGL, Fonts**: Intelligent spoofing to prevent tracking.
  - **Hardware & Client Rects**: Spoofing of hardware properties and randomized client rectangle values.
  - **Automation Signatures**: All Playwright automation signatures are removed.
- **Mobile Device Emulation**: Create "Mobile" profiles that use Playwright's built-in mobile emulation.
- **Robust Network Management**:
  - **Reliable Proxies**: Uses Playwright's native proxy API for reliable HTTP and SOCKS5 connections.
  - **Proxy Tester**: A built-in tool to test proxy connectivity before use.
- **Multi-threaded Automation**:
  - Launch multiple browser profiles simultaneously.
  - Specify the number of concurrent threads (up to 1000).
  - Automatically navigate all launched browsers to a target URL.

## Workflow Features

- **Bulk Profile Creation**: Generate hundreds of profiles at once with a given name prefix.
- **Fingerprint Refresh**: Instantly generate a new random fingerprint for any profile with a single click.
- **IP-Based Geolocation**: Enter a proxy IP, and AbdullahBot will automatically fetch and fill in the correct timezone and geolocation data.

## How to Use

### Installation

1.  Clone the repository.
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Install Playwright's browser binaries:
    ```bash
    playwright install
    ```

### Running the Application

```bash
python main.py
```

### Profile Management

- **Create**: Click "Create New Profile", enter a name, and choose a profile type (Desktop or Mobile).
- **Bulk Create**: Click "Bulk Create Profiles" to generate many profiles at once.
- **Configure**: Select a profile and click "Configure".
  - **Proxy**: Enter your proxy and click "Test Proxy" to verify it.
  - **Geolocation**: Click "Fetch from Proxy" to auto-fill location data.
  - **Fingerprint**: Click "Refresh Fingerprint" to generate a new identity.
- **Launch**: Select a profile and click "Launch Selected Profile".

### Automation

1.  Enter a website in the "Target URL" box.
2.  Set the "Number of Threads".
3.  Select one or more profiles from the list (use Ctrl+Click or Shift+Click).
4.  Click "Start Automation".
