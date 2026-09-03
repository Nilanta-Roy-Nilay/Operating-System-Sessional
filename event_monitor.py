import asyncio
from evdev import InputDevice, ecodes

DEVICE_PATH = '/dev/input/event2'

async def monitor_events(path):
    try:
        device = InputDevice(path)
        print(f"[*] Successfully connected to device: {device.name}")
        print("[*] Monitoring system input events asynchronously...\n")

        async for event in device.async_read_loop():
            print(f"Event Time: {event.timestamp()} | Type: {event.type} | Code: {event.code} | Value: {event.value}")

    except PermissionError:
        print("[!] Error: Access denied. Root standard privileges (sudo) required to access /dev/input devices.")
    except FileNotFoundError:
        print(f"[!] Error: Device at {path} not found.")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")

async def background_status_logger():
    while True:
        print("[System Status] Event loop is running smoothly...")
        await asyncio.sleep(10)

async def main():
    await asyncio.gather(
        monitor_events(DEVICE_PATH),
        background_status_logger()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[*] Program stopped by user.")
