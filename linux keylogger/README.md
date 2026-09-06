# Linux Keylogger Project

A comprehensive Linux keylogger for system auditing and security testing.

## 🚀 Features

- **Automatic Keyboard Detection**: Finds keyboard devices automatically
- **Real-time Capture**: Logs keystrokes with timestamps
- **Email Reports**: Sends logs via email at configured intervals
- **Bash Wrapper**: Easy start/stop/status management
- **Comprehensive Testing**: Test suite validates all components
- **Signal Handling**: Graceful shutdown with Ctrl+C

## 📋 Requirements

- Linux operating system
- Python 3.6+
- Root privileges (for hardware access)
- evdev Python module

## 🔧 Installation

```bash
# Clone or download the project
cd linux_keylogger

# Make scripts executable
chmod +x *.sh *.py

# Run installation
sudo ./install.sh
