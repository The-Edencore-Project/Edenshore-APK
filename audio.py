# audio.py
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
import os
import random
import threading

class SoundBank:
    def __init__(self):
        self.current_biome = None
        self.bed_sound = None
        self.music_sound = None
        self.active_sounds = []
        
        # Volume states: 0 = HI, 1 = LO, 2 = MUTE
        self.vol_state = 0 
        self.vol_levels = [0.3, 0.1, 0.0]
        self.music_base_vol = self.vol_levels[self.vol_state]
        self.bed_base_vol = 0.3  # Beds remain untouched
        self.ducked_vol = 0.15
        self.sting_vol = 0.5
        self.feed_vol = 0.6
        
        self.seat_volumes = {
            "Vertex": 0.4, "Solon": 0.3, "Lumen": 0.5, "Prism": 0.4, "Ripple": 0.4   
        }

        self.music_playlist = []
        self.current_track_index = 0
        self.current_mood = "normal"

    def cycle_volume(self):
        self.vol_state = (self.vol_state + 1) % 3
        self.music_base_vol = self.vol_levels[self.vol_state]
        if self.music_sound:
            self.music_sound.volume = self.music_base_vol
        return self.vol_state

    def _get_path(self, subfolder, filename):
        path1 = f"assets/audio/{subfolder}/{filename}"
        path2 = f"audio/{subfolder}/{filename}"
        if os.path.exists(path1): return path1
        if os.path.exists(path2): return path2
        return None

    def _play_and_track(self, sound, volume):
        if not sound: return
        sound.volume = volume
        self.active_sounds.append(sound)
        sound.play()
        Clock.schedule_once(lambda dt: self._cleanup_sound(sound), 5.0)

    def _cleanup_sound(self, sound):
        if sound in self.active_sounds:
            self.active_sounds.remove(sound)
        try:
            sound.stop()
        except: pass

    def start_music(self, mood="normal"):
        if self.music_sound and self.current_mood == mood and self.music_sound.state == 'play':
            return

        self.current_mood = mood
        self._build_playlist(mood)
        
        if self.music_sound:
            self.music_sound.unbind(on_stop=self._on_music_end)
            self.music_sound.stop()
            self.music_sound = None
            
        if not self.music_playlist:
            self._build_playlist("all")
            if not self.music_playlist:
                return
                
        self.current_track_index = 0
        self._play_current_track()

    def _build_playlist(self, mood):
        self.music_playlist = []
        folder = "assets/audio/music" if os.path.exists("assets/audio/music") else "audio/music"
        if not os.path.exists(folder): return
        
        for filename in os.listdir(folder):
            if filename.endswith(".ogg"):
                if mood == "all" or f"_{mood}.ogg" in filename:
                    self.music_playlist.append(os.path.join(folder, filename))
                
        random.shuffle(self.music_playlist)

    def _play_current_track(self):
        if not self.music_playlist: return
        path = self.music_playlist[self.current_track_index]
        
        if self.music_sound:
            self.music_sound.unbind(on_stop=self._on_music_end) 
            self.music_sound.stop()
            self.music_sound = None
            
        def load_thread():
            try:
                new_sound = SoundLoader.load(path)
                if new_sound:
                    new_sound.loop = False
                    new_sound.volume = self.music_base_vol
                    new_sound.bind(on_stop=self._on_music_end)
                    Clock.schedule_once(lambda dt: self._start_loaded_track(new_sound))
            except Exception: pass
            
        threading.Thread(target=load_thread, daemon=True).start()

    def _start_loaded_track(self, new_sound):
        if self.music_sound is None: 
            self.music_sound = new_sound
            self.music_sound.play()

    def _on_music_end(self, instance):
        self.skip_track()

    def skip_track(self):
        if not self.music_playlist: return
        self.current_track_index = (self.current_track_index + 1) % len(self.music_playlist)
        self._play_current_track()

    def play_bed(self, biome_name):
        biome_name = biome_name.lower()
        path = self._get_path("beds", f"{biome_name}_bed.ogg")
        
        if not path or self.current_biome == biome_name: return
        
        if self.bed_sound: 
            self.bed_sound.stop()
            self.bed_sound = None
            
        def load_thread():
            try:
                sound = SoundLoader.load(path)
                if sound:
                    sound.loop = True
                    sound.volume = self.bed_base_vol
                    Clock.schedule_once(lambda dt: self._start_bed(sound, biome_name))
            except Exception: pass
            
        threading.Thread(target=load_thread, daemon=True).start()

    def _start_bed(self, sound, biome_name):
        self.bed_sound = sound
        self.bed_sound.play()
        self.current_biome = biome_name

    def play_sting(self, seat_name):
        path = self._get_path("stings", f"{seat_name.lower()}_sting.ogg")
        if not path: return
        vol = self.seat_volumes.get(seat_name, self.sting_vol)
        
        def load_thread():
            try:
                sound = SoundLoader.load(path)
                if sound:
                    Clock.schedule_once(lambda dt: self._play_and_track(sound, vol))
            except Exception: pass
        threading.Thread(target=load_thread, daemon=True).start()

    def play_feed_splash(self):
        path = self._get_path("stings", "feed_splash.ogg")
        if not path: return
        def load_thread():
            try:
                sound = SoundLoader.load(path)
                if sound:
                    Clock.schedule_once(lambda dt: self._play_and_track(sound, self.feed_vol))
            except Exception: pass
        threading.Thread(target=load_thread, daemon=True).start()

    def duck_volume(self):
        if self.bed_sound: self.bed_sound.volume = self.ducked_vol
        if self.music_sound: self.music_sound.volume = self.ducked_vol

    def restore_volume(self):
        if self.bed_sound: self.bed_sound.volume = self.bed_base_vol
        if self.music_sound: self.music_sound.volume = self.music_base_vol

    def stop_all(self):
        if self.bed_sound: self.bed_sound.stop()
        if self.music_sound: self.music_sound.stop()
        for s in self.active_sounds:
            try: s.stop()
            except: pass
        self.active_sounds.clear()