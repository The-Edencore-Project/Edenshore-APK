# iot.py

class SmartHomeBridge:
    def __init__(self):
        self.lights_on = True
        self.music_on = True
        
    def send_signal(self, device, action):
        # This is where the future Bluetooth/Wi-Fi code will go.
        print(f"[IoT BRIDGE] -> Sending signal to SMART HUB: {device} = {action}")