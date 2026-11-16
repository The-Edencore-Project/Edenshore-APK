# sensors.py
import time
import datetime
import math
import random

try:
    from plyer import accelerometer, battery
    HAS_HARDWARE = True
    try:
        accelerometer.enable()
    except:
        pass
except ImportError:
    HAS_HARDWARE = False

class SensorArray:
    def __init__(self):
        self.light_level = 0.5
        self.motion_mag = 0.0
        self.orientation_tilt = 0.0
        self.audio_amplitude = 0.1 
        self.battery_level = 1.0
        self.is_charging = 0.0
        self.thermal_baseline = 0.5
        self.shakiness = 0.0
        
        self.session_start_time = time.time()
        self.last_tap_time = time.time()
        self.last_tap_interval = 1.0
        self.tap_count_10s = 0
        self.swipe_count_10s = 0
        self.biome_switch_count = 0
        self.feed_count = 0
        self.riddle_wins = 0
        self.riddle_losses = 0
        
        self.walking_factor = 0.0
        self.prev_mag = 9.8
        
        self._fetch_thermal_baseline()

    def _fetch_thermal_baseline(self):
        try:
            from jnius import autoclass
            from android import mActivity
            Context = autoclass('android.content.Context')
            Intent = autoclass('android.content.Intent')
            IntentFilter = autoclass('android.content.IntentFilter')
            BatteryManager = autoclass('android.os.BatteryManager')
            
            intent = mActivity.registerReceiver(None, IntentFilter(Intent.ACTION_BATTERY_CHANGED))
            temp_c = intent.getIntExtra(BatteryManager.EXTRA_TEMPERATURE, 0) / 10.0
            self.thermal_baseline = self._norm(temp_c, 15.0, 40.0)
        except Exception:
            self.thermal_baseline = 0.5 

    def _norm(self, val, min_val, max_val):
        if val <= min_val: return 0.0
        if val >= max_val: return 1.0
        return (val - min_val) / (max_val - min_val)

    def update_hardware(self):
        if not HAS_HARDWARE: return

        try:
            val = accelerometer.acceleration
            if val and val[0] is not None:
                x, y, z = val
                mag = math.sqrt(x**2 + y**2 + z**2)
                movement = abs(mag - 9.8) 
                
                # --- THE DEADZONE FIX ---
                # Ignore phantom vibrations and sensor noise
                if movement < 1.5:
                    movement = 0.0
                
                variance = abs(movement - self.prev_mag)
                if variance < 1.5:
                    variance = 0.0
                
                self.shakiness = self._norm(variance, 0.0, 5.0)
                self.prev_mag = movement
                
                self.motion_mag = self._norm(movement, 0.0, 15.0)
                self.orientation_tilt = self._norm(abs(z), 0.0, 9.8)
                
                if 1.0 < movement < 5.0:
                    self.walking_factor = min(1.0, self.walking_factor + 0.05)
                else:
                    self.walking_factor = max(0.0, self.walking_factor - 0.02)
        except:
            pass

        try:
            bat = battery.status
            if bat:
                self.battery_level = self._norm(bat.get('percentage', 100), 0, 100)
                self.is_charging = 1.0 if bat.get('isCharging', False) else 0.0
        except:
            pass

        hour = datetime.datetime.now().hour
        self.light_level = 0.8 if 6 <= hour <= 18 else 0.2

    def register_tap(self):
        now = time.time()
        interval = now - self.last_tap_time
        self.last_tap_interval = interval
        self.last_tap_time = now
        self.tap_count_10s += 1

    def register_swipe(self):
        self.swipe_count_10s += 1

    def decay_counters(self, dt):
        idle_time = time.time() - self.last_tap_time
        if idle_time > 10.0:
            self.tap_count_10s = max(0, self.tap_count_10s - int(dt * 2))
            self.swipe_count_10s = max(0, self.swipe_count_10s - int(dt * 2))
            
        if idle_time > 3.0:
            self.last_tap_interval = 1.0

    def get_32_params(self, brain_state):
        now = datetime.datetime.now()
        
        v1 = [
            self.light_level,
            self.motion_mag,
            self.orientation_tilt,
            self.audio_amplitude,
            self.battery_level,
            self.is_charging,
            self.thermal_baseline, 
            self.shakiness         
        ]

        absence_sec = time.time() - brain_state.get("last_visit_time", time.time())
        session_sec = time.time() - self.session_start_time
        feed_sec = time.time() - brain_state.get("last_feed_time", time.time())
        riddle_sec = time.time() - brain_state.get("last_riddle_time", time.time())
        
        v2 = [
            self._norm(now.hour, 0, 23),
            self._norm(now.weekday(), 0, 6),
            1.0 if now.weekday() >= 5 else 0.0,
            self._norm(absence_sec, 0, 86400),
            self._norm(session_sec, 0, 3600),
            self._norm(feed_sec, 0, 3600),
            self._norm(riddle_sec, 0, 1800),
            self._norm(now.month, 1, 12)
        ]

        idle_sec = time.time() - self.last_tap_time
        rhythm_score = 1.0 - self._norm(self.last_tap_interval, 0.1, 2.0) if self.tap_count_10s > 0 else 0.0

        v3 = [
            self._norm(self.tap_count_10s, 0, 20),
            self._norm(self.swipe_count_10s, 0, 10),
            self._norm(idle_sec, 0, 300),
            self._norm(brain_state.get("bond_score", 0), 0, 1000),
            self._norm(brain_state.get("heat", 0), 0, 10),
            rhythm_score,          
            self.walking_factor,   
            self._norm(self.riddle_wins, 0, max(1, self.riddle_wins + self.riddle_losses))
        ]

        mood_map = {"NORMAL": 0.25, "SLEEPY": 0.5, "PLAYFUL": 0.75, "CRISIS": 1.0}
        biome_map = {"WATER": 0.0, "FOREST": 0.15, "BEACH": 0.3, "CASTLE": 0.45, 
                     "DESERT": 0.6, "MOUNTAIN": 0.75, "RUINS": 0.9, "VOID": 1.0}
        
        v4 = [
            mood_map.get(brain_state.get("current_mood", "NORMAL"), 0.25),
            self._norm(brain_state.get("cinematic_cooldown", 0), 0, 3600),
            biome_map.get(brain_state.get("current_biome", "WATER"), 0.0),
            self._norm(brain_state.get("weather_intensity", 0), 0, 10),
            self._norm(brain_state.get("bag_exhaustion", 0), 0, 100),
            brain_state.get("active_focus", 0.0),
            brain_state.get("choreo_state", 0.0),
            self._norm(brain_state.get("dialogue_queue_len", 0), 0, 10)
        ]

        return v1 + v2 + v3 + v4