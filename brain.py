# brain.py
import random
import json
import os
import time
import datetime
import hashlib

import crosstalk
from dialogue.biome import BIOME_REACTIONS
import neural
import sensors
import iot

class ShuffleBag:
    def __init__(self, name, items, is_permanent=False):
        self.name = name
        self.items = list(items)
        self.is_permanent = is_permanent
        self.item_hashes = {self._get_hash(item): item for item in self.items}
        self.drawn_hashes = []
        self.recent_hashes = [] 

    def _get_hash(self, item):
        return hashlib.md5(str(item).encode('utf-8')).hexdigest()

    def draw(self):
        if not self.items: return None
        available_hashes = [h for h in self.item_hashes.keys() if h not in self.drawn_hashes]
        if not available_hashes:
            if self.is_permanent:
                self.recent_hashes.extend(self.drawn_hashes[-20:])
                if len(self.recent_hashes) > 50: self.recent_hashes = self.recent_hashes[-50:]
                self.drawn_hashes = [] 
                available_hashes = [h for h in self.item_hashes.keys() if h not in self.recent_hashes]
                if not available_hashes: available_hashes = list(self.item_hashes.keys())
            else:
                # THE FIX: Remember the last 20 draws instead of 3
                self.recent_hashes.extend(self.drawn_hashes)
                if len(self.recent_hashes) > 20: self.recent_hashes = self.recent_hashes[-20:]
                self.drawn_hashes = []
                available_hashes = [h for h in self.item_hashes.keys() if h not in self.recent_hashes]
                if not available_hashes: available_hashes = list(self.item_hashes.keys())

        chosen_hash = random.choice(available_hashes)
        self.drawn_hashes.append(chosen_hash)
        return self.item_hashes[chosen_hash]

    def get_state(self): return {"drawn": self.drawn_hashes, "recent": self.recent_hashes}
    def set_state(self, saved_state):
        if isinstance(saved_state, dict):
            self.drawn_hashes = saved_state.get("drawn", [])
            self.recent_hashes = saved_state.get("recent", [])

class EtiquetteEngine:
    def __init__(self):
        self.cooldown = 5.0 
        self.has_greeted = False
        self.greet_delay = 0.5 
        self.forced_scene = None 
        
        self.save_file = "bond_save.json"
        self.save_version = "4.2_THEATRE" 
        self.bond_score = 0
        self.next_milestone = 50 
        self.bond_timer = 0.0
        self.bond_interval = 300.0 
        self.user_name = "Guest"
        
        self.heat = 0
        self.heat_cool_timer = 0.0
        self.heat_cool_threshold = 5.0 
        self.max_heat_seen = 0

        self.biome_cooldown = 0.0
        self.current_biome = "LAGOON" 

        self.listening_for_request = False
        self.tap_count = 0
        self.tap_timer = 0.0
        self.last_interaction_time = time.time()

        self.game_state = "normal" 
        self.riddle_timer = 0.0
        self.current_riddle = None
        
        self.riddle_bag = ShuffleBag("riddles", crosstalk.get_bank("riddles"), is_permanent=True)

        self.arbiter = neural.Arbiter()
        self.sensor_array = sensors.SensorArray()
        self.current_mood = "NORMAL"
        self.brain_activity = [0.0] * 8
        
        self.last_visit_time = time.time()
        self.last_feed_time = time.time()
        self.last_riddle_time = time.time()
        
        self.trigger_cinematic = False
        self.cinematic_cooldown = 3600.0

        self.pending_absence = False
        self.vibe_journal = []
        self.pending_dream = None
        
        self.iot = iot.SmartHomeBridge() 
        
        self.save_timer = 0.0
        self.save_interval = 30.0
        self.needs_save = False

        self.sleep_state = "AWAKE" 
        self.sleep_timer = 0.0
        self.sleep_dialogue_queued = False
        self.idle_threshold = 300.0 
        self.waking_leader = None
        self.waking_nudge_queued = False
        
        self.feeding_state_timer = 0.0

        self.bags = {
            "jokes": ShuffleBag("jokes", crosstalk.get_bank("jokes"), is_permanent=True),
            "stories": ShuffleBag("stories", crosstalk.get_bank("stories"), is_permanent=True),
            "facts": ShuffleBag("facts", crosstalk.get_bank("facts"), is_permanent=True),
            "poetry": ShuffleBag("poetry", crosstalk.get_bank("poetry"), is_permanent=True),
            "lyrics": ShuffleBag("lyrics", crosstalk.get_bank("lyrics"), is_permanent=True),
            "requests": ShuffleBag("requests", crosstalk.get_bank("requests"), is_permanent=True),
            "wisdom": ShuffleBag("wisdom", crosstalk.get_bank("wisdom"), is_permanent=True),
            "ambient": ShuffleBag("ambient", crosstalk.get_bank("ambient"), is_permanent=False),
            "council": ShuffleBag("council", crosstalk.get_bank("council"), is_permanent=False),
            "visitor": ShuffleBag("visitor", crosstalk.get_bank("visitor"), is_permanent=False),
            "greetings": ShuffleBag("greetings", crosstalk.get_bank("greetings"), is_permanent=False),
            "peering_eyes": ShuffleBag("peering_eyes", crosstalk.get_bank("peering_eyes"), is_permanent=False),
            "tap_reactions": ShuffleBag("tap_reactions", crosstalk.get_bank("tap_reactions"), is_permanent=False),
            "feed_reactions": ShuffleBag("feed_reactions", crosstalk.get_bank("feed_reactions"), is_permanent=False),
            "tap_grunts": ShuffleBag("tap_grunts", crosstalk.get_bank("tap_grunts"), is_permanent=False),
            "feed_grunts": ShuffleBag("feed_grunts", crosstalk.get_bank("feed_grunts"), is_permanent=False),
            "interjections": ShuffleBag("interjections", crosstalk.get_bank("interjections"), is_permanent=False),
            "huddle": ShuffleBag("huddle", crosstalk.get_bank("huddle"), is_permanent=False),
            "dream_nightmare": ShuffleBag("dream_nightmare", crosstalk.get_bank("dream_nightmare"), is_permanent=False),
            "dream_peaceful": ShuffleBag("dream_peaceful", crosstalk.get_bank("dream_peaceful"), is_permanent=False),
            "dream_playful": ShuffleBag("dream_playful", crosstalk.get_bank("dream_playful"), is_permanent=False),
            "dream_absence": ShuffleBag("dream_absence", crosstalk.get_bank("dream_absence"), is_permanent=False),
            "daily_morning": ShuffleBag("daily_morning", crosstalk.get_bank("daily_morning"), is_permanent=False),
            "daily_evening": ShuffleBag("daily_evening", crosstalk.get_bank("daily_evening"), is_permanent=False),
            "daily_night": ShuffleBag("daily_night", crosstalk.get_bank("daily_night"), is_permanent=False),
            "daily_absence": ShuffleBag("daily_absence", crosstalk.get_bank("daily_absence"), is_permanent=False),
            "daily_stress": ShuffleBag("daily_stress", crosstalk.get_bank("daily_stress"), is_permanent=False),
            "daily_busy": ShuffleBag("daily_busy", crosstalk.get_bank("daily_busy"), is_permanent=False),
            "daily_weather": ShuffleBag("daily_weather", crosstalk.get_bank("daily_weather"), is_permanent=False),
            "biome_LAGOON": ShuffleBag("biome_LAGOON", BIOME_REACTIONS.get("LAGOON", []), is_permanent=True),
            "biome_SHORE": ShuffleBag("biome_SHORE", BIOME_REACTIONS.get("SHORE", []), is_permanent=True),
            "biome_TWILIGHT": ShuffleBag("biome_TWILIGHT", BIOME_REACTIONS.get("TWILIGHT", []), is_permanent=True),
            "biome_DEEP": ShuffleBag("biome_DEEP", BIOME_REACTIONS.get("DEEP", []), is_permanent=True),
            "bedtime_resistance": ShuffleBag("bedtime_resistance", crosstalk.get_bank("bedtime_resistance"), is_permanent=False),
            "waking_nudge": ShuffleBag("waking_nudge", crosstalk.get_bank("waking_nudge"), is_permanent=False),
            "waking_others": ShuffleBag("waking_others", crosstalk.get_bank("waking_others"), is_permanent=False)
        }
        self.load_memory()

    def set_user_name(self, name):
        if name and name.strip():
            self.user_name = name.strip()
            self.save_memory(force=True)

    def load_memory(self):
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, "r") as f:
                    data = json.load(f)
                    self.bond_score = data.get("bond_score", 0)
                    self.next_milestone = data.get("next_milestone", 50)
                    self.user_name = data.get("user_name", "Guest")
                    self.vibe_journal = data.get("vibe_journal", [])
                    saved_time = data.get("last_visit_time", time.time())
                    time_diff = time.time() - saved_time
                    if time_diff > 28800: self.pending_absence = True
                    elif time_diff > 60: 
                        if self.vibe_journal:
                            last_entry = self.vibe_journal[-1]
                            if last_entry.get("max_heat", 0) > 10: self.pending_dream = self.bags["dream_nightmare"].draw()
                            elif self.pending_absence: self.pending_dream = self.bags["dream_absence"].draw()
                            elif last_entry.get("mood") == "PLAYFUL": self.pending_dream = self.bags["dream_playful"].draw()
                            else: self.pending_dream = self.bags["dream_peaceful"].draw()
                    saved_bags = data.get("bags", {})
                    for name, bag_obj in self.bags.items():
                        if name in saved_bags: bag_obj.set_state(saved_bags[name])
        except Exception: pass

    def save_memory(self, force=False):
        if not force and not self.needs_save: return
        try:
            session_log = {"timestamp": time.time(), "max_heat": self.max_heat_seen, "mood": self.current_mood, "bond": self.bond_score}
            if not self.vibe_journal or (time.time() - self.vibe_journal[-1]["timestamp"]) > 10:
                self.vibe_journal.append(session_log)
                if len(self.vibe_journal) > 7: self.vibe_journal.pop(0)
            data = {
                "version": self.save_version, "bond_score": self.bond_score, "next_milestone": self.next_milestone,
                "user_name": self.user_name, "last_visit_time": time.time(), "vibe_journal": self.vibe_journal, 
                "bags": {name: bag.get_state() for name, bag in self.bags.items()}
            }
            with open(self.save_file, "w") as f: json.dump(data, f)
            self.needs_save = False
            self.save_timer = 0.0
        except Exception: pass

    def add_bond(self, amount=1, reason=""):
        self.bond_score += amount
        self.needs_save = True
        if self.bond_score >= self.next_milestone:
            self.next_milestone += 50
            self.save_memory(force=True)
            return True
        return False

    def toggle_lights(self, state=None, by_council=False):
        if state is not None: self.iot.lights_on = state
        else: self.iot.lights_on = not self.iot.lights_on
        self.iot.send_signal("LIGHTS", "ON" if self.iot.lights_on else "OFF")
        if not self.iot.lights_on:
            if not by_council: self.forced_scene = [("Solon", "Finally. Darkness.")]
        else:
            if not by_council: self.forced_scene = [("Vertex", "The light is back!")]
        if not by_council: self.cooldown = 4.0

    def trigger_sleep(self):
        if self.sleep_state == "AWAKE":
            self.sleep_state = "RESISTING"
            self.sleep_timer = 15.0 
            self.sleep_dialogue_queued = False
            self.last_interaction_time = time.time()
            self.feeding_state_timer = 0.0 

    def wake_up(self):
        if self.sleep_state in ["SLEEPING", "RESISTING"]:
            self.sleep_state = "WAKING"
            self.sleep_timer = 12.0 
            self.waking_nudge_queued = False
            self.waking_leader = random.choices(
                ["Ripple", "Prism", "Solon", "Lumen"], 
                weights=[0.4, 0.3, 0.2, 0.1], k=1
            )[0]
            self.last_interaction_time = time.time()
            self.sensor_array.last_tap_time = time.time() 

    def on_biome_switch(self, biome_name):
        self.current_biome = biome_name
        self.add_bond(1, "biome")
        self.heat += 1
        self.max_heat_seen = max(self.max_heat_seen, self.heat)
        self.heat_cool_timer = 0.0
        self.sensor_array.biome_switch_count += 1
        self.last_interaction_time = time.time()
        if self.biome_cooldown <= 0:
            biome_key = f"biome_{biome_name}"
            if biome_key in self.bags:
                scene = self.bags[biome_key].draw()
                if scene: self.forced_scene = [scene]
            self.cooldown = 4.0
            self.biome_cooldown = 6.0 

    def on_guest_tap(self):
        if not self.has_greeted: return
        if self.game_state == "riddle_wait": return
        if self.sleep_state != "AWAKE": return 

        self.sensor_array.register_tap()
        self.last_interaction_time = time.time()
        
        if self.listening_for_request:
            self.tap_count += 1
            self.tap_timer = 0.4 
            if self.tap_count >= 5: self.resolve_request()
            return
            
        self.heat += 1
        self.max_heat_seen = max(self.max_heat_seen, self.heat)
        self.heat_cool_timer = 0.0
        
        if self.heat >= 6:
            self.cooldown = 0.0
            stress_scene = self.bags["huddle"].draw()
            if stress_scene: self.forced_scene = stress_scene
            self.needs_save = True
            return
        
        if self.heat == 1:
            reaction = self.bags["tap_reactions"].draw()
            if reaction:
                pivot_cat = random.choice(["ambient", "council"])
                pivot = self.bags[pivot_cat].draw()
                if pivot: self.forced_scene = reaction + pivot
                self.cooldown = 5.0
                self.needs_save = True
        elif self.heat == 2:
            grunt = self.bags["tap_grunts"].draw()
            if grunt: self.forced_scene = grunt
            self.cooldown = 4.0
            self.needs_save = True

    def on_creature_tap(self, creature_name):
        self.last_interaction_time = time.time()
        if self.game_state != "riddle_wait": return
        self.game_state = "normal"
        self.riddle_timer = 0.0
        if creature_name == self.current_riddle["correct_speaker"]:
            self.add_bond(5, "riddle_win")
            self.sensor_array.riddle_wins += 1
            self.forced_scene = self.current_riddle["correct_reply"]
        else:
            self.sensor_array.riddle_losses += 1
            self.forced_scene = self.current_riddle["wrong_reply"]
        self.cooldown = 8.0
        self.save_memory(force=True)

    def resolve_request(self):
        self.listening_for_request = False
        count = self.tap_count
        self.tap_count = 0
        category = "ambient"
        if count == 1: category = "lyrics"
        elif count == 2: self.start_riddle(); return
        elif count == 3: category = "jokes"
        elif count == 4: category = "facts"
        elif count >= 5: category = "stories"
        scene = self.bags[category].draw()
        if not scene and category in ["lyrics", "jokes", "facts", "stories"]:
            category = random.choice(["ambient", "council"])
            scene = self.bags[category].draw()
        if scene:
            self.forced_scene = scene
            self.cooldown = random.uniform(5.0, 8.0)
            self.save_memory(force=True)

    def start_riddle(self):
        self.last_riddle_time = time.time()
        riddle = self.riddle_bag.draw()
        if not riddle:
            self.forced_scene = [("Solon", "My mind is blank. No more riddles today.")]
            self.cooldown = 8.0
            return
        self.current_riddle = riddle
        self.game_state = "riddle_setup"
        self.forced_scene = riddle["setup"]
        self.cooldown = 15.0 

    def get_mood_weights(self):
        if self.current_mood == "CRISIS":
            categories = ["huddle", "daily_stress", "wisdom"]
            weights = [0.6, 0.3, 0.1]
        elif self.current_mood == "SLEEPY":
            categories = ["ambient", "lyrics", "facts", "daily_night"]
            weights = [0.4, 0.2, 0.2, 0.2]
        elif self.current_mood == "PLAYFUL":
            categories = ["jokes", "stories", "council", "wisdom", "lyrics"]
            weights = [0.30, 0.30, 0.15, 0.15, 0.10]
        else:
            hour = datetime.datetime.now().hour
            if 6 <= hour < 11:
                categories = ["ambient", "council", "jokes", "facts", "daily_morning"]
                weights = [0.3, 0.2, 0.2, 0.1, 0.2]
            elif 18 <= hour < 23:
                categories = ["ambient", "council", "stories", "daily_evening"]
                weights = [0.3, 0.3, 0.2, 0.2]
            else:
                categories = ["ambient", "council", "jokes", "facts", "stories", "wisdom", "lyrics"]
                weights = [0.35, 0.20, 0.10, 0.10, 0.10, 0.10, 0.05]
        return categories, weights

    def update(self, dt, bond_level):
        idle_sec = time.time() - self.sensor_array.last_tap_time
        
        if self.feeding_state_timer > 0:
            self.feeding_state_timer -= dt
            
        if self.sleep_state == "AWAKE":
            if idle_sec > self.idle_threshold and self.feeding_state_timer <= 0:
                self.sleep_state = "SLEEPING"
                self.sleep_timer = 0.0
                self.forced_scene = None
        elif self.sleep_state == "RESISTING":
            self.sleep_timer -= dt
            if not self.sleep_dialogue_queued:
                scene = self.bags["bedtime_resistance"].draw()
                if scene: self.forced_scene = scene 
                self.sleep_dialogue_queued = True
            if self.sleep_timer <= 0:
                self.sleep_state = "SLEEPING"
                self.forced_scene = None
        elif self.sleep_state == "SLEEPING":
            self.current_mood = "SLEEPY"
            return None
        elif self.sleep_state == "WAKING":
            self.sleep_timer -= dt
            if self.sleep_timer <= 7.0 and not self.waking_nudge_queued:
                scene = self.bags["waking_nudge"].draw()
                if scene: self.forced_scene = scene
                self.waking_nudge_queued = True
            self.current_mood = "SLEEPY"
            if self.sleep_timer <= 0:
                self.sleep_state = "AWAKE"
                self.last_interaction_time = time.time()
        
        if self.sleep_state in ["RESISTING", "SLEEPING", "WAKING"]:
            self.current_mood = "SLEEPY"

        self.save_timer += dt
        if self.save_timer >= self.save_interval:
            self.needs_save = True
            self.save_memory()

        if self.has_greeted and (time.time() - self.last_interaction_time > 300):
            self.has_greeted = False
            self.greet_delay = 1.0 

        self.sensor_array.update_hardware()
        self.sensor_array.decay_counters(dt)

        if idle_sec > 2.0:
            self.heat = 0
            if self.current_mood == "CRISIS":
                self.current_mood = "NORMAL" 
                self.cooldown = 2.0 

        brain_state = {
            "last_visit_time": self.last_visit_time, "last_feed_time": self.last_feed_time,
            "last_riddle_time": self.last_riddle_time, "bond_score": self.bond_score, "heat": self.heat,
            "current_mood": self.current_mood, "cinematic_cooldown": self.cinematic_cooldown,
            "current_biome": self.current_biome, "weather_intensity": 0, "bag_exhaustion": 0,    
            "active_focus": 0.0, "choreo_state": 0.0, "dialogue_queue_len": 0 
        }
        
        params = self.sensor_array.get_32_params(brain_state)
        new_mood = self.arbiter.get_mood(params)
        self.brain_activity = self.arbiter.get_activity()
        
        if self.sleep_state == "AWAKE" and self.feeding_state_timer <= 0:
            self.current_mood = new_mood
        
        if self.cinematic_cooldown > 0:
            self.cinematic_cooldown -= dt
        elif self.cinematic_cooldown <= 0 and self.game_state == "normal" and not self.listening_for_request and self.sleep_state == "AWAKE" and self.feeding_state_timer <= 0:
            self.cinematic_cooldown = 3600.0 
            self.trigger_cinematic = True
            self.forced_scene = self.bags["peering_eyes"].draw()
            self.cooldown = 20.0 

        if self.game_state == "riddle_wait":
            self.riddle_timer -= dt
            if self.riddle_timer <= 0:
                self.game_state = "normal"
                self.forced_scene = [("Solon", "Too slow. The moment has passed.")]
                self.cooldown = 8.0
            return None

        if self.listening_for_request:
            if self.tap_timer > 0:
                self.tap_timer -= dt
                if self.tap_timer <= 0: self.resolve_request()
            return None 

        self.heat_cool_timer += dt
        if self.heat_cool_timer >= self.heat_cool_threshold:
            self.heat = max(0, self.heat - 1)
            self.heat_cool_timer = 0.0

        if self.biome_cooldown > 0: self.biome_cooldown -= dt

        self.bond_timer += dt
        if self.bond_timer >= self.bond_interval:
            self.add_bond(1, "time")
            self.bond_timer -= self.bond_interval

        if not self.has_greeted:
            self.greet_delay -= dt
            if self.greet_delay <= 0:
                self.has_greeted = True
                self.last_interaction_time = time.time()
                self.cooldown = 8.0 
                
                if self.pending_dream:
                    dream_scene = self.pending_dream
                    self.pending_dream = None
                    return dream_scene
                
                if self.pending_absence:
                    self.pending_absence = False
                    self.forced_scene = self.bags["daily_absence"].draw()
                    self.save_memory(force=True)
                    return self.bags["greetings"].draw()
                    
                greeting_scene = self.bags["greetings"].draw()
                if greeting_scene:
                    if self.user_name and self.user_name != "Guest":
                        dynamic_scene = [("Vertex", f"Hi {self.user_name}! You're back!")]
                    else:
                        dynamic_scene = [("Vertex", "Hi! You're back!")]
                    for spk, txt in greeting_scene:
                        if spk != "Vertex": dynamic_scene.append((spk, txt))
                    greeting_scene = dynamic_scene
                
                self.needs_save = True
                return greeting_scene
            return None

        if self.forced_scene:
            scene = self.forced_scene
            self.forced_scene = None
            if self.game_state == "riddle_setup":
                self.game_state = "riddle_wait"
                self.riddle_timer = 10.0 
            return scene

        if self.cooldown > 0:
            self.cooldown -= dt
            return None
        
        if self.sleep_state != "AWAKE" or self.feeding_state_timer > 0:
            return None

        if random.random() < 0.02:
            prompt = self.bags["requests"].draw()
            if prompt:
                self.listening_for_request = True
                self.tap_count = 0
                self.tap_timer = 0.0
                self.save_memory(force=True)
                return prompt

        if random.random() < 0.35:
            scene = self.bags["interjections"].draw()
            if scene:
                self.cooldown = random.uniform(2.0, 3.5) 
                return scene

        categories, weights = self.get_mood_weights()
        chosen_category = random.choices(categories, weights=weights, k=1)[0]
        scene = self.bags[chosen_category].draw()
        
        if not scene and chosen_category in ["jokes", "stories", "facts", "poetry", "lyrics", "wisdom"]:
            chosen_category = random.choice(["ambient", "council"])
            scene = self.bags[chosen_category].draw()

        if scene:
            self.cooldown = random.uniform(3.0, 6.0) 
            actual_day = datetime.datetime.now().strftime("%A")
            fixed_scene = []
            
            display_name = self.user_name if self.user_name and self.user_name != "Guest" else "friend"
            
            for spk, txt in scene:
                if "Monday" in txt: txt = txt.replace("Monday", actual_day)
                if "{name}" in txt: txt = txt.replace("{name}", display_name)
                fixed_scene.append((spk, txt))
                
            scene = fixed_scene
            self.needs_save = True
            return scene
        return None
        
    def on_feed(self):
        if self.listening_for_request or self.game_state != "normal" or self.sleep_state != "AWAKE": return None 
        self.last_feed_time = time.time()
        self.last_interaction_time = time.time()
        self.sensor_array.feed_count += 1
        self.heat += 1
        self.max_heat_seen = max(self.max_heat_seen, self.heat)
        self.heat_cool_timer = 0.0
        
        self.feeding_state_timer = 10.0 
        
        if self.heat == 1:
            reaction = self.bags["feed_reactions"].draw()
            if reaction:
                pivot_cat = random.choice(["ambient", "council"])
                pivot = self.bags[pivot_cat].draw()
                if pivot: self.forced_scene = reaction + pivot
                self.cooldown = 5.0
            self.save_memory(force=True)
            return self.bags["visitor"].draw()
        elif self.heat == 2:
            grunt = self.bags["feed_grunts"].draw()
            if grunt:
                self.forced_scene = grunt
                self.cooldown = 4.0
                self.save_memory(force=True)
        return None

engine = EtiquetteEngine()

def get_status():
    score = engine.bond_score
    if score <= 10: tier = "Stranger"
    elif score <= 50: tier = "Acquaintance"
    elif score <= 100: tier = "Friend"
    elif score <= 500: tier = "Companion"
    else: tier = "Family"
    return f"BOND: {score} - {tier}"