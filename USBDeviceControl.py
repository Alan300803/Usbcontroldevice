import pyudev
import subprocess
import time

class USBControlTool:
    def __init__(self):
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='usb')
        self.blocked_devices = set()

    def start_monitoring(self):
        observer = pyudev.MonitorObserver(self.monitor, callback=self.handle_usb_event, name='usb-monitor')
        observer.start()

        try:
            print("USB Device Control Tool is running. Press Ctrl+C to exit.")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            observer.stop()
            observer.join()

    def handle_usb_event(self, device):
        if device.action == 'add' and device not in self.blocked_devices:
            print(f"USB Device Connected: {device}")
            # Check if the connected device should be blocked
            if self.is_device_blocked(device):
                print(f"Blocking USB Device: {device}")
                self.block_device(device)

        elif device.action == 'remove' and device in self.blocked_devices:
            print(f"USB Device Disconnected: {device}")
            self.unblock_device(device)

    def is_device_blocked(self, device):
        # Add your custom logic to determine if the device should be blocked
        # For example, check against a list of authorized devices
        return True

    def block_device(self, device):
        # Add your custom logic to block the USB device
        # For example, you can disable the USB port using platform-specific commands
        self.blocked_devices.add(device)
        # On Linux, you can use the following command to disable the USB port
        subprocess.run(['sudo', 'echo', '0', '>', f'/sys{device.sys_path}/authorized'])

    def unblock_device(self, device):
        # Add your custom logic to unblock the USB device
        # For example, you can enable the USB port using platform-specific commands
        self.blocked_devices.remove(device)
        # On Linux, you can use the following command to enable the USB port
        subprocess.run(['sudo', 'echo', '1', '>', f'/sys{device.sys_path}/authorized'])

def main():
    usb_tool = USBControlTool()
    usb_tool.start_monitoring()

if __name__ == '__main__':
    main()