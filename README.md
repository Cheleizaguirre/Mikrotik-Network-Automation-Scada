# MikroTik Automation & SCADA GUI

A Python-based desktop application for real-time management of MikroTik routers via SSH.
The system includes IP management, DHCP server provisioning, routing configuration, network monitoring in SCADA style, and hardware signaling via Arduino over serial communication. Built with ttkbootstrap for a modern dark-themed GUI.

---

## 🎯 Purpose

1. **Automate** routine MikroTik router tasks without using the CLI.
2. **Provide** a graphical interface for network configuration and monitoring.
3. **Monitor** host availability and send real-time status to external hardware (Arduino).
4. **Integrate** SCADA-style visual feedback for network health.
5. **Enable** quick DHCP, routing, and IP management from a single application.

---

## ✨ Key Features

- Router Identity Management: View and update router name.
- IP Management: Add, delete, and view IP addresses.
- DHCP Server Configuration: Create pools, assign servers, and configure networks.
- Routing Configuration: Add static routes.
- SCADA Network Monitoring: Visual indicators (ON/OFF) for network status.
- Ping Monitoring: Automatic background host availability checks.
- Arduino Integration: Sends 'G' (green) or 'R' (red) signals via serial to control relays and pilot lights.
- Dark-Themed GUI: Built with ttkbootstrap for modern styling.
- SSH-Based Operations: Directly execute MikroTik commands without temporary scripts.

---

## 🛠️ Stack

| Layer                |	Technology                                            |
|----------------------|--------------------------------------------------------|
| Language             |	Python 3.11                                           |
| GUI Framework        |	Tkinter + ttkbootstrap (dark theme)                   |
| Network Automation   |	SSH commands via sshpass and subprocess               |
| Serial Communication |	Arduino MEGA via USB (/dev/ttyUSB0, 9600 8N1)         |
| Image/Graphics       |	Tkinter PhotoImage (ethernetON.gif / ethernetOFF.gif) |
| Utilities            |	threading, subprocess, ScrolledText                   |

---

## ⚙️ Local Installation (Developers)

```bash
# 1. Clone repository
$ git clone https://github.com/yourusername/mikrotik-gui.git
$ cd mikrotik-gui

# 2. Create virtual environment (recommended)
$ python -m venv venv
$ source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
$ pip install -r requirements.txt
```

> **Note:**: Requirements include: ttkbootstrap, pyserial and standard Python libraries.

```bash
# 4. Run the application
$ python mikrotik_tool_gui.py
```

> **Note:**: Make sure your computer has SSH access to the MikroTik device and, optionally, an Arduino connected at /dev/ttyUSB0.

---

## 🧠 How It Works

1. SSH Communication: run_ssh(cmd: str) executes RouterOS commands via SSH and returns results.
2. Router Management: GUI fields allow the user to update router identity, IP addresses, and comments.
3. DHCP Server & Routing: Secondary windows provide forms to create DHCP pools, assign servers, and add static routes.
4. SCADA Monitoring:
- Ping checks to a host every 5 seconds.
- GUI shows ON/OFF indicators and sends signals to Arduino to control relays/pilot lights.
5. Arduino Integration:
- Receives 'G' (green) or 'R' (red) from Python script via serial.
- Controls relays to switch a pilot light series connected to 110VAC.
6. Background Tasks: hilo_ping() thread monitors connectivity without blocking GUI updates.

---

## 🚀 Future Improvements

- Multi-host monitoring with separate SCADA indicators.
- Logging and historical network state visualization.
- Customizable dashboards with live charts.
- Cross-platform support (Windows/Linux/Mac) with automatic serial port detection.
- Enhanced security with SSH keys instead of plaintext passwords.

---

## 🤝 Contributing

1. Fork the repository and create a feature branch:

```bash
git checkout -b feature/YourFeature
```

2. Make changes with clear commit messages.
3. Open a Pull Request explaining your additions or improvements.

---
