# AbdullahBot - The Intelligent Automation Browser

AbdullahBot is an advanced anti-detect browser and automation tool built with Python, PyQt6, and Selenium. It allows you to create, manage, and automate multiple browser profiles, each with a unique and customizable fingerprint.

## Features

- **Isolated Profiles**: Create and manage unlimited browser profiles. Each profile's data (cookies, cache, etc.) is stored in a separate folder, ensuring complete isolation.
- **Advanced Fingerprint Spoofing**: Customize a wide range of browser parameters to create a unique fingerprint for each profile:
  - **User-Agent**: Choose from a built-in list of 50+ recent desktop and mobile User-Agents, or randomize it.
  - **Screen Resolution**: Set custom screen dimensions.
  - **Timezone & Geolocation**: Automatically fetched based on the proxy IP address.
  - **WebRTC**: Disabled by default to prevent IP leaks.
  - **Canvas & WebGL**: Protected against fingerprinting.
- **Mobile Device Emulation**: Create "Mobile" profiles that use Selenium's built-in mobile emulation for realistic device spoofing.
- **IP-Based Configuration**: Enter a proxy IP, and AbdullahBot will automatically fetch and fill in the correct timezone and geolocation data for that IP.
- **Multi-threaded Automation**:
  - Launch multiple browser profiles simultaneously.
  - Specify the number of concurrent threads.
  - Automatically navigate all launched browsers to a target URL.

## How to Use

### Installation

1.  Clone the repository.
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

```bash
python main.py
```

### Profile Management

- **Create**: Click "Create New Profile", enter a name, and choose a profile type (Desktop or Mobile).
- **Configure**: Select a profile and click "Configure Selected Profile".
  - **User-Agent**: Select a User-Agent from the dropdown or click "Randomize".
  - **Proxy**: Enter your proxy in the format `http://user:pass@host:port` or `socks5://user:pass@host:port`.
  - **Geolocation**: Click "Fetch from Proxy" to automatically populate timezone and geolocation data from your proxy's IP.
- **Launch**: Select a profile and click "Launch Selected Profile" to open a single browser instance.
- **Delete**: Select a profile and click "Delete Selected Profile".

### Automation

1.  Enter a website in the "Target URL" box.
2.  Set the "Number of Threads" for concurrent browser sessions.
3.  Select one or more profiles from the list (use Ctrl+Click or Shift+Click for multiple selections).
4.  Click "Start Automation". The selected browsers will launch concurrently and navigate to the target URL.
