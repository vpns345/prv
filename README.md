# AbdullahBot v5.0 - Bulk Operations Suite

This is the final, most comprehensive version of AbdullahBot, a professional-grade anti-detect browser and automation tool built with Python, PyQt6, and Playwright.

**Version 5.0 introduces a full suite of Bulk Operation features to make managing large numbers of profiles fast and efficient.** It also includes all the critical bug fixes and elite stealth upgrades from v4.0.

## Core Features

- **Playwright Engine**: The core is built on Playwright with `playwright-stealth` for a more modern and undetectable automation experience.
- **Advanced Fingerprint Spoofing**: Each profile gets a new, randomized, but consistent fingerprint to bypass advanced detection systems.
- **Robust Network Management**: Reliable proxy handling (HTTP/SOCKS5) with a built-in tester and DNS leak protection.
- **Multi-threaded Automation**: Launch hundreds of browser profiles simultaneously and navigate them to a target URL.

## v5.0 - The Bulk Operations Suite

- **Multi-Select**: The main profile list now supports selecting multiple profiles (using Ctrl+Click or Shift+Click).
- **Bulk Delete**: Select multiple profiles and delete them all with a single confirmation.
- **Bulk Proxy Assignment**: Paste a list of proxies into a dialog to have them automatically assigned to all selected profiles.
- **Bulk Fingerprint Randomization**: Instantly generate new, unique fingerprints for all selected profiles with one click.
- **Bulk Session Control**: A "Stop All" button allows you to immediately and gracefully close all running browser sessions launched by the application.

## How to Use

### Installation

1.  Clone the repository.
2.  Install the required dependencies: `pip install -r requirements.txt`
3.  Install Playwright's browser binaries: `playwright install`

### Running the Application

`python main.py`

### Bulk Operations

1.  **Select Profiles**: Hold Ctrl or Shift and click to select multiple profiles in the list.
2.  **Choose Action**:
    - Click **"Bulk Delete"** to delete all selected profiles.
    - Click **"Bulk Set Proxies"** to open a dialog and paste a list of proxies to assign.
    - Click **"Bulk Randomize Fingerprints"** to assign new identities to all selected profiles.
3.  **Control Automation**:
    - Click **"Start Automation"** to launch all selected profiles.
    - Click **"Stop All"** to close all running sessions.
