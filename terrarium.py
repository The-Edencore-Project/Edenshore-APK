# =====================================================================
# EDENCORE PROJECT - V4.4 (THE TALKING FIX)
# =====================================================================
# CONSTITUTION & LOCKED VALUES FOR FUTURE INSTANCES:
# 1. DO NOT REINTRODUCE ROTATE MATRICES for sprites. It causes ANR 
#    freezes on the Kirin 710A. Use the frame-swapping method.
# 2. DO NOT CHANGE THE 512 MATH. Sprites are 512x512. The scale_factor
#    must remain size_w / 512.0.
# 3. DO NOT SEPARATE SOLON'S FLIPPERS FROM HIS BODY in the Z-order. 
#    They are grouped in Section 3 to prevent floating fins.
# 4. DO NOT CALL sound.unload() in audio.py. It causes weakref crashes.
# 5. KIVY IS STATEFUL. If you draw a black shadow, the next image will
#    inherit that color unless you explicitly set Color(1,1,1,1).
# 6. GHOST BUBBLES: Kivy caches geometry. Set alpha to 0 AND size to
#    (0,0) to flush the canvas. Do not just set size to (0,0).
# 7. TALK PRIORITY: talk_timer must be checked before is_blinking, or
#    the creatures will stop talking mid-sentence to blink.
# =====================================================================

# =====================================================================
# SECTION 1: IMPORTS, CONSTANTS, AND GLOBALS
# =====================================================================
import os
import sys

# --- FORCE PYDROID TO FIND THE ROOT FOLDER ---
ROOT_DIR = "/storage/emulated/0/Edenshore5"
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
# ---------------------------------------------

# Force Android graphics drivers
os.environ['KIVY_WINDOW'] = 'sdl2'
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
os.environ['KIVY_INPUT'] = 'sdl2'
os.environ['KIVY_AUDIO'] = 'sdl2'

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse, Line, Rotate, PushMatrix, PopMatrix
from kivy.core.text import Label as CoreLabel
from kivy.graphics.texture import Texture
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image as KivyImage
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import math
import random

import brain
import audio
import choreography 
import atmosphere 
import cinematics 

try:
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.VIBRATE])
except Exception:
    pass

SHOW_DEBUG = True  

def do_vibrate(ms=50):
    try:
        from plyer import vibrator
        vibrator.vibrate(ms / 1000.0)
        return
    except Exception:
        pass 
    try:
        from jnius import autoclass
        from android import mActivity
        Context = autoclass('android.content.Context')
        vibrator_service = mActivity.getSystemService(Context.VIBRATOR_SERVICE)
        if vibrator_service:
            vibrator_service.vibrate(ms)
            return
    except Exception:
        pass

# --- BIOME PALETTES ---
BIOME_PALETTES = {
    "LAGOON": ["#021a30", "#043060", "#106080", "#20a0a0", "#105060", "#020a10"],
    "SHORE": ["#2a1a40", "#a04060", "#e07050", "#f0a060", "#f0d090", "#f0e0b0"],
    "TWILIGHT": ["#0a0510", "#1a1028", "#2a1838", "#3a2048", "#1a0820", "#050205"],
    "DEEP": ["#000000", "#050010", "#0a0020", "#100030", "#050010", "#000000"]
}

SAND_TINTS = {
    "LAGOON": (0.2, 0.4, 0.5, 1.0), 
    "SHORE": (1.0, 1.0, 1.0, 1.0), 
    "TWILIGHT": (0.3, 0.3, 0.4, 1.0),
    "DEEP": (0.1, 0.1, 0.2, 1.0)
}

# --- UI COLORS ---
NEON_GREEN = (0.0, 1.0, 0.0, 1.0)
NEON_RED = (1.0, 0.12, 0.12, 1.0)
NEON_ORANGE = (1.0, 0.5, 0.0, 1.0)
NEON_BLUE = (0.0, 0.8, 1.0, 1.0)
GOLD = (1.0, 0.8, 0.0, 1.0)
DIM_GREY = (0.4, 0.4, 0.4, 1.0)

SEAT_COLORS = {
    "Solon": (0.0, 1.0, 0.0, 1.0), "Prism": (1.0, 0.85, 0.2, 1.0),
    "Vertex": (1.0, 0.1, 0.1, 1.0), "Lumen": (1.0, 0.4, 0.8, 1.0), 
    "Ripple": (0.2, 0.8, 1.0, 1.0)
}

TEXT_COLORS = {
    "Vertex": (1.0, 0.45, 0.4, 1.0), "Solon": (0.55, 0.85, 0.55, 1.0), 
    "Lumen": (1.0, 0.6, 0.8, 1.0), "Ripple": (0.5, 0.8, 1.0, 1.0),   
    "Prism": (1.0, 0.85, 0.5, 1.0)    
}

PARTICLE_COLORS = {
    "LAGOON": ["#80ffe0", "#ffffff"], 
    "SHORE": ["#ffffff", "#f0d090"], 
    "TWILIGHT": ["#ff8080", "#c0c0ff"],
    "DEEP": ["#ffffff", "#a0c0ff"]
}

# --- CHARACTERS ---
# DO NOT CHANGE the file names or base scales without testing.
CHARACTERS = [
    {"name": "Solon",  "file": "assets/images/solon_body.png",  "x_rel": 0.30, "y_rel": 0.55, "scale": 0.20},
    {"name": "Prism",  "file": "assets/images/prism.png",       "x_rel": 0.70, "y_rel": 0.55, "scale": 0.26},
    {"name": "Lumen",  "file": "assets/images/lumen.png",       "x_rel": 0.20, "y_rel": 0.35, "scale": 0.18}, 
    {"name": "Ripple", "file": "assets/images/ripple.png",      "x_rel": 0.75, "y_rel": 0.35, "scale": 0.36}, 
    {"name": "Vertex", "file": "assets/images/vertex.png",      "x_rel": 0.50, "y_rel": 0.15, "scale": 0.24}
]

def lerp(c1, c2, t):
    h1=c1.lstrip("#"); h2=c2.lstrip("#")
    r1=int(h1[0:2],16); g1=int(h1[2:4],16); b1=int(h1[4:6],16)
    r2=int(h2[0:2],16); g2=int(h2[2:4],16); b2=int(h2[4:6],16)
    t=max(0.0,min(1.0,t))
    return "#%02x%02x%02x"%(int(r1+(r2-r1)*t),int(g1+(g2-g1)*t),int(b1+(b2-b1)*t))

# =====================================================================
# SECTION 2: THE MAIN TERRARIUM CLASS & INITIALIZATION
# =====================================================================
class Terrarium(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        
        self.time_elapsed = 0
        self.base_scroll = 0.0
        self.current_biome = "LAGOON" 
        self.bond = 0
        self.feeding_timer = 0.0
        self.title_timer = 3.0
        self.vertex_greeting_timer = 0.0
        self.has_vertex_greeted = False
        self.milestone_timer = 0.0
        self.debug_timer = 0.0
        self.name_prompt_shown = False
        
        self.last_lights_on = None
        self.last_vol_state = None
        self.last_sleep_state = "AWAKE"

        self.weather = atmosphere.WeatherEngine()
        self.cinematic = cinematics.CinematicEngine() 

        self.sound_bank = audio.SoundBank()
        self.sound_bank.play_bed(self.current_biome.lower())
        self.sound_bank.start_music("normal")

        # --- TEXTURE LOADING ---
        self.textures = {}
        for c in CHARACTERS:
            try:
                base_path = c["file"]
                blink_path = c["file"].replace(".png", "_blink.png")
                talk_path = c["file"].replace(".png", "_talk.png")
                half_path = c["file"].replace(".png", "_half.png")
                
                if c["name"] == "Solon":
                    blink_path = c["file"].replace("_body.png", "_body_blink.png")
                    talk_path = c["file"].replace("_body.png", "_body_talk.png")
                    half_path = c["file"].replace("_body.png", "_body_half.png")

                if os.path.exists(base_path): self.textures[c["name"]] = CoreImage(base_path).texture
                else: self.textures[c["name"]] = None
                if os.path.exists(blink_path): self.textures[c["name"] + "_blink"] = CoreImage(blink_path).texture
                else: self.textures[c["name"] + "_blink"] = None
                if os.path.exists(talk_path): self.textures[c["name"] + "_talk"] = CoreImage(talk_path).texture
                else: self.textures[c["name"] + "_talk"] = None
                if os.path.exists(half_path): self.textures[c["name"] + "_half"] = CoreImage(half_path).texture
                else: self.textures[c["name"] + "_half"] = None
            except: 
                self.textures[c["name"]] = None
                self.textures[c["name"] + "_blink"] = None
                self.textures[c["name"] + "_talk"] = None
                self.textures[c["name"] + "_half"] = None
        
        # Load Solon Frame Lists
        self.solon_left_frames = []
        self.solon_right_frames = []
        for i in range(1, 6):
            left_path = f"assets/images/solon_left_fin_{i}.png"
            right_path = f"assets/images/solon_right_fin_{i}.png"
            if os.path.exists(left_path): self.solon_left_frames.append(CoreImage(left_path).texture)
            if os.path.exists(right_path): self.solon_right_frames.append(CoreImage(right_path).texture)

        self.fg_texture = CoreImage("assets/images/grass.png").texture if os.path.exists("assets/images/grass.png") else None
        self.mtn_texture = CoreImage("assets/images/mountains.png").texture if os.path.exists("assets/images/mountains.png") else None
        self.pillar_texture = CoreImage("assets/images/pillars.png").texture if os.path.exists("assets/images/pillars.png") else None
        self.dune_texture = CoreImage("assets/images/sand_dunes.png").texture if os.path.exists("assets/images/sand_dunes.png") else None

        self.creatures = []
        for c in CHARACTERS:
            self.creatures.append({
                "name": c["name"], "x_rel": c["x_rel"], "y_rel": c["y_rel"], "scale": c["scale"], 
                "phase": random.uniform(0, 6.28), "cx": c["x_rel"] * Window.width, "cy": c["y_rel"] * Window.height,
                "seek_off_x": random.uniform(-80, 80), "seek_off_y": random.uniform(-50, 50),
                "last_ate_time": 0.0, "blink_timer": random.uniform(1.0, 4.0), "is_blinking": False,
                "prism_burst": 0, "talk_timer": 0.0, "talk_start_time": 0.0, "action": "idle",
                "action_timer": random.uniform(20.0, 45.0), "roll_timer": 0.0, "target_creature": None,
                "blink_cooldowns": {"Solon": 5.0, "Lumen": 8.0, "Vertex": 2.0, "Prism": 4.0, "Ripple": 6.0}
            })

        # --- PARTICLE POOLS ---
        self.max_ambient = 40
        self.ambient_pool = [{"active": False, "x": 0, "y": 0, "vx": 0, "vy": 0, "r": 0, "phase": 0, "color": (0,0,0,1)} for _ in range(self.max_ambient)]
        self.max_dust = 60
        self.dust_pool = [{"active": False, "x": 0, "y": 0, "vx": 0, "vy": 0, "r": 0, "life": 0, "color": (0,0,0,1)} for _ in range(self.max_dust)]
        self.stars = [{"x": random.uniform(0, 1), "y": random.uniform(0.3, 0.95), "r": random.uniform(1, 2.5), "phase": random.uniform(0, 6.28), "speed": random.uniform(0.5, 1.5)} for _ in range(60)]
        
        self.max_sand_bubbles = 20
        self.sand_bubble_pool = [{"active": False, "x": 0, "y": 0, "r": 0, "vy": 0, "life": 0.0} for _ in range(self.max_sand_bubbles)]
        self.sand_vents = [0.15, 0.45, 0.85] 
        
        self.max_bubbles = 15
        self.bubble_pool = [{"active": False, "age": 0.0, "life": 6.0, "x": 0, "y": 0, "sx": 0, "sy": 0, "base_r": 0, "color": (1,1,1,1), "lbl": None, "speaker": None} for _ in range(self.max_bubbles)]
        self.max_food = 20
        self.food_pool = [{"active": False, "x": 0, "y": 0, "vx": 0, "vy": 0, "phase": random.uniform(0,6.28)} for _ in range(self.max_food)]
        self.max_float_text = 10
        self.float_text_pool = [{"active": False, "x": 0, "y": 0, "vx": 0, "life": 0.0, "color": (1,1,1,1), "lbl": None} for _ in range(self.max_float_text)]
        self.max_ripples = 10
        self.ripple_pool = [{"active": False, "x": 0, "y": 0, "age": 0.0, "life": 0.6, "max_radius": 100} for _ in range(self.max_ripples)]

        self.stream_queue = []
        self.stream_timer = 0.0

        # --- UI LABELS ---
        ref_size = min(Window.width, Window.height)
        
        self.lbl_debug = CoreLabel(text="", font_size=int(ref_size * 0.018), color=(1, 1, 1, 1))
        self.lbl_debug.refresh()

        self.biome_labels = {}
        self.biome_labels_selected = {}
        for b in BIOME_PALETTES.keys():
            lbl = CoreLabel(text=b, font_size=int(ref_size * 0.022), color=NEON_GREEN)
            lbl.refresh()
            self.biome_labels[b] = lbl
            lbl_sel = CoreLabel(text=b, font_size=int(ref_size * 0.022), color=NEON_RED)
            lbl_sel.refresh()
            self.biome_labels_selected[b] = lbl_sel

        self.util_slots = ["FEED", "SLEEP", "DIM", "VOL HI", "MENU"]
        self.util_labels = []
        for slot in self.util_slots:
            color = NEON_RED if slot == "VOL HI" else NEON_GREEN
            lbl = CoreLabel(text=slot, font_size=int(ref_size * 0.022), color=color)
            lbl.refresh()
            self.util_labels.append(lbl)

        self.lbl_bond = CoreLabel(text=brain.get_status(), font_size=int(ref_size * 0.04), color=NEON_BLUE)
        self.lbl_bond.refresh()
        
        self.lbl_status = CoreLabel(text="", font_size=int(ref_size * 0.03), color=NEON_ORANGE)
        self.lbl_status.refresh()

        self.lbl_title = CoreLabel(text="WELCOME TO EDENSHORE", font_size=int(ref_size * 0.06), color=NEON_GREEN)
        self.lbl_title.refresh()
        self.lbl_subtitle = CoreLabel(text="A Neuro-Symbolic Vibe Engine", font_size=int(ref_size * 0.03), color=(0.8, 0.8, 0.8, 1.0))
        self.lbl_subtitle.refresh()
        
        self.lbl_milestone = CoreLabel(text="", font_size=int(ref_size * 0.08), color=GOLD)
        self.lbl_milestone.refresh()
        
        self.gradient_textures = {}
        for biome in BIOME_PALETTES.keys():
            self.gradient_textures[biome] = self.generate_gradient_texture(biome)
            
        self.ray_texture = self.generate_ray_texture()

        self.build_static_canvas()
        Clock.schedule_interval(self.tick, 1.0 / 60.0)

    # --- UI POPUPS ---
    def show_name_popup(self):
        if self.name_prompt_shown: return
        self.name_prompt_shown = True
        content = BoxLayout(orientation='vertical', spacing=10, padding=15)
        lbl = Label(text="Welcome to Edenshore.\nWhat shall the Council call you?", font_size='18sp', halign='center')
        content.add_widget(lbl)
        
        self.name_input = TextInput(multiline=False, font_size='18sp', size_hint_y=None, height=60)
        content.add_widget(self.name_input)
        
        btn = Button(text="Submit", size_hint_y=None, height=50, background_color=(0.2, 0.8, 1.0, 1))
        btn.bind(on_release=self.save_name)
        content.add_widget(btn)
        self.name_popup = Popup(title="The Guest", content=content, size_hint=(0.8, 0.4), auto_dismiss=False)
        self.name_popup.open()

    def save_name(self, instance):
        name = self.name_input.text.strip()
        if name: brain.engine.set_user_name(name)
        self.name_popup.dismiss()

    def show_menu_popup(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=15)
        title_lbl = Label(text="THE ECOSYSTEM", font_size='20sp', color=NEON_GREEN, size_hint_y=None, height=40)
        content.add_widget(title_lbl)
        msg = Label(text="IoT Shop, Smart Hub Status,\nand AR Mode are coming soon!", font_size='16sp', halign='center', color=GOLD)
        content.add_widget(msg)
        btn = Button(text="CLOSE", size_hint_y=None, height=50, background_color=(0.8, 0.2, 0.2, 1))
        content.add_widget(btn)
        popup = Popup(title="Ecosystem Menu", content=content, size_hint=(0.8, 0.5), background_color=(0.05, 0.05, 0.08, 0.95))
        btn.bind(on_release=popup.dismiss)
        popup.open()

    # --- TEXTURE GENERATORS ---
    def generate_gradient_texture(self, biome):
        palette = BIOME_PALETTES[biome]
        buf = bytearray()
        for i in range(100):
            t = i / 100
            col_hex = palette[0]
            if t < 0.20: col_hex = lerp(palette[0], palette[1], t/0.20)
            elif t < 0.45: col_hex = lerp(palette[1], palette[2], (t-0.20)/0.25)
            elif t < 0.70: col_hex = lerp(palette[2], palette[3], (t-0.45)/0.25)
            elif t < 0.90: col_hex = lerp(palette[3], palette[4], (t-0.70)/0.20)
            else: col_hex = lerp(palette[4], palette[5], (t-0.90)/0.10)
            rgba = self.hex_to_rgba(col_hex)
            for c in rgba: buf.append(int(c * 255))
        tex = Texture.create(size=(1, 100), colorfmt='rgba')
        tex.blit_buffer(bytes(buf), colorfmt='rgba', bufferfmt='ubyte')
        tex.flip_vertical() 
        return tex

    def generate_ray_texture(self):
        tex = Texture.create(size=(100, 100), colorfmt='rgba')
        buf = bytearray()
        for y in range(100):
            for x in range(100):
                alpha_x = 1.0 - abs((x / 50.0) - 1.0)
                alpha_y = 1.0 - abs((y / 50.0) - 1.0)
                alpha = max(0.0, alpha_x * alpha_y)
                buf.extend([255, 255, 255, int(alpha * 255)])
        tex.blit_buffer(bytes(buf), colorfmt='rgba', bufferfmt='ubyte')
        return tex

    # =====================================================================
    # SECTION 3: STATIC CANVAS (Z-ORDER & DRAWING)
    # =====================================================================
    def build_static_canvas(self):
        with self.canvas:
            self.bg_rect = Rectangle(texture=self.gradient_textures[self.current_biome], pos=(0,0), size=(Window.width, Window.height))
            
            self.god_rays = []
            for i in range(3):
                PushMatrix()
                c = Color(1, 1, 0.8, 0.1) 
                rot = Rotate(angle=15 + (i * 10), origin=(Window.width * 0.5, Window.height))
                rect = Rectangle(texture=self.ray_texture, pos=(-Window.width*0.2 + (i*Window.width*0.4), 0), size=(Window.width*0.3, Window.height*1.5))
                PopMatrix()
                self.god_rays.append((c, rot, rect))
            
            self.star_objs = []
            for s in self.stars:
                c = Color(1, 1, 1, 0.6); e = Ellipse(pos=(0,0), size=(s["r"], s["r"])); self.star_objs.append((c, e))
            self.mtn_objs = []
            if self.mtn_texture:
                for _ in range(3): self.mtn_objs.append((Color(1, 1, 1, 1), Rectangle(texture=self.mtn_texture)))
            self.pillar_objs = []
            if self.pillar_texture:
                for _ in range(3): self.pillar_objs.append((Color(1, 1, 1, 1), Rectangle(texture=self.pillar_texture)))
            self.dune_objs = []
            if self.dune_texture:
                for _ in range(3): self.dune_objs.append((Color(1, 1, 1, 1), Rectangle(texture=self.dune_texture)))
            self.lumen_tentacle_objs = []
            for _ in range(5):
                c_glow = Color(1, 0.5, 0.7, 0.3); l_glow = Line(points=[], width=6, smooth=True)
                c_core = Color(1, 0.8, 0.9, 0.8); l_core = Line(points=[], width=2, smooth=True)
                self.lumen_tentacle_objs.append((c_glow, l_glow, c_core, l_core))
            self.shadow_objs = []
            for _ in self.creatures: self.shadow_objs.append((Color(0, 0, 0, 0.3), Ellipse()))
            
            # --- Z-ORDER FIX: SOLON GROUP (Right Fin -> Body -> Left Fin) ---
            Color(1, 1, 1, 1) 
            self.solon_right_fin_rect = Rectangle(texture=None)
            
            c_solon_color = Color(1, 1, 1, 1)
            c_solon_rect = Rectangle(texture=self.textures["Solon"])
            self.solon_body_rect = (c_solon_color, c_solon_rect)
            
            Color(1, 1, 1, 1)
            self.solon_left_fin_rect = Rectangle(texture=None)
            
            # --- OTHER CREATURES (Drawn on top of Solon) ---
            self.other_creature_objs = []
            for c in self.creatures:
                if c["name"] == "Solon":
                    self.other_creature_objs.append(None) 
                    continue
                color = Color(1, 1, 1, 1)
                rect = Rectangle(texture=self.textures[c["name"]])
                self.other_creature_objs.append((color, rect))
            
            self.food_objs = []
            for _ in range(self.max_food):
                c_glow = Color(1, 0.6, 0.2, 0.3); e_glow = Ellipse()
                c_core = Color(1, 0.9, 0.5, 0.8); e_core = Ellipse()
                self.food_objs.append((c_glow, e_glow, c_core, e_core))

            self.dust_objs = []
            for _ in range(self.max_dust):
                self.dust_objs.append((Color(1, 1, 1, 0), Ellipse(), Color(1, 1, 1, 0), Ellipse()))
            self.ambient_objs = []
            for _ in range(self.max_ambient):
                self.ambient_objs.append((Color(1, 1, 1, 0), Ellipse(), Color(1, 1, 1, 0), Ellipse()))
                
            self.sand_bubble_objs = []
            for _ in range(self.max_sand_bubbles):
                c_rim = Color(1, 1, 1, 0); l_rim = Line(circle=(0,0,0), width=1)
                self.sand_bubble_objs.append((c_rim, l_rim))
                
            self.grass_objs = []
            if self.fg_texture:
                for _ in range(3): self.grass_objs.append((Color(1, 1, 1, 1), Rectangle(texture=self.fg_texture)))
            
            self.weather_tint_color = Color(0, 0, 0, 0.1)
            self.weather_tint_rect = Rectangle(pos=(0,0), size=(Window.width, Window.height))
            self.lights_out_color = Color(0, 0, 0, 0)
            self.lights_out_rect = Rectangle(pos=(0,0), size=(Window.width, Window.height))

            self.bubble_objs = []
            for _ in range(self.max_bubbles):
                c_fill = Color(0, 0, 0, 0); e_fill = Ellipse(pos=(0,0), size=(0,0))
                c_hl = Color(1, 1, 1, 0); l_hl = Line(points=[], width=2)
                c_txt = Color(1, 1, 1, 0); r_txt = Rectangle(pos=(0,0), size=(0,0))
                self.bubble_objs.append((c_fill, e_fill, c_hl, l_hl, c_txt, r_txt))

            self.float_text_objs = []
            for _ in range(self.max_float_text):
                c = Color(1, 1, 1, 0)
                r = Rectangle()
                self.float_text_objs.append((c, r))

            self.ripple_objs = []
            for _ in range(self.max_ripples):
                c = Color(1, 1, 1, 0)
                l = Line(circle=(0,0,0), width=2)
                self.ripple_objs.append((c, l))
                
            self.ui_bar_top_col = Color(0, 0, 0, 1); self.ui_bar_top = Rectangle()
            self.ui_bar_bot_col = Color(0, 0, 0, 1); self.ui_bar_bot = Rectangle()
            self.ui_bar_util_col = Color(0, 0, 0, 0.8); self.ui_bar_util = Rectangle()

            self.debug_bg_color = Color(0, 0, 0, 0.6)
            self.debug_bg_rect = Rectangle(pos=(0,0), size=(Window.width, Window.height))

        with self.canvas.after:
            self.ui_text_objs = []
            self.ui_text_objs.append((Color(1,1,1,1), Rectangle(texture=self.lbl_bond.texture)))
            self.ui_text_objs.append((Color(1,1,1,1), Rectangle(texture=self.lbl_status.texture)))
            
            self.util_text_objs = []
            for lbl in self.util_labels:
                self.util_text_objs.append((Color(1,1,1,1), Rectangle(texture=lbl.texture)))
            
            self.debug_text_color = Color(1,1,1,1)
            self.debug_text_rect = Rectangle(texture=self.lbl_debug.texture)
            
            for b in BIOME_PALETTES.keys():
                self.ui_text_objs.append((Color(1,1,1,1), Rectangle(texture=self.lbl_status.texture)))
            
            self.milestone_color = Color(1, 1, 1, 0)
            self.milestone_rect = Rectangle(texture=self.lbl_milestone.texture)
                
            self.title_bg_color = Color(0, 0, 0, 1)
            self.title_bg_rect = Rectangle(pos=(0,0), size=(Window.width, Window.height))
            self.title_text_color = Color(1, 1, 1, 1)
            self.title_text_rect = Rectangle(texture=self.lbl_title.texture)
            self.subtitle_text_color = Color(1, 1, 1, 1)
            self.subtitle_text_rect = Rectangle(texture=self.lbl_subtitle.texture)

    def update_canvas(self, *args):
        if not hasattr(self, 'bg_rect'): return
        self.bg_rect.size = (self.width, self.height)
        if hasattr(self, 'weather_tint_rect'): self.weather_tint_rect.size = (self.width, self.height)
        if hasattr(self, 'lights_out_rect'): self.lights_out_rect.size = (self.width, self.height)
            
        ref_size = min(self.width, self.height)
        
        if hasattr(self, 'biome_labels'):
            biome_h = self.biome_labels[self.current_biome].texture.height
            bot_bar_h = int(biome_h * 2.5)
        else: bot_bar_h = 60
        
        top_bar_h = int(self.lbl_bond.texture.height * 2.5)
            
        self.ui_bar_top.pos = (0, self.height - top_bar_h); self.ui_bar_top.size = (self.width, top_bar_h)
        self.ui_bar_bot.pos = (0, 0); self.ui_bar_bot.size = (self.width, bot_bar_h)
        
        util_bar_h = int(top_bar_h * 0.7)
        self.ui_bar_util.pos = (0, self.height - top_bar_h - util_bar_h); self.ui_bar_util.size = (self.width, util_bar_h)
        
        if hasattr(self, 'title_bg_rect'): self.title_bg_rect.size = (self.width, self.height)
            
        if hasattr(self, 'lbl_bond'):
            for lbl in self.util_labels:
                lbl.font_size = int(ref_size * 0.022); lbl.refresh()
            self.lbl_bond.font_size = int(ref_size * 0.04); self.lbl_bond.refresh()
            self.lbl_status.font_size = int(ref_size * 0.03); self.lbl_status.refresh()
            self.lbl_debug.font_size = int(ref_size * 0.018); self.lbl_debug.refresh()
            self.lbl_title.font_size = int(ref_size * 0.06); self.lbl_title.refresh()
            self.lbl_subtitle.font_size = int(ref_size * 0.03); self.lbl_subtitle.refresh()
            self.lbl_milestone.font_size = int(ref_size * 0.08); self.lbl_milestone.refresh()
            for b in BIOME_PALETTES.keys():
                self.biome_labels[b].font_size = int(ref_size * 0.022); self.biome_labels[b].refresh()
                self.biome_labels_selected[b].font_size = int(ref_size * 0.022); self.biome_labels_selected[b].refresh()
                
            if hasattr(self, 'ui_text_objs'):
                self.ui_text_objs[0][1].texture = self.lbl_bond.texture

    # =====================================================================
    # SECTION 4: INTERACTION & DIALOGUE MANAGEMENT
    # =====================================================================
    def queue_speech(self, conversation):
        for speaker, text in conversation:
            words = text.split(); chunks = []; current = ""
            for w in words:
                if len(w) > 24:
                    if current: chunks.append(current); current = ""
                    for i in range(0, len(w), 24): chunks.append(w[i:i+24])
                    continue
                if not current: current = w
                elif len(current) + 1 + len(w) <= 24: current += " " + w
                else: chunks.append(current); current = w
            if current: chunks.append(current)
            for chunk in chunks: self.stream_queue.append({"speaker": speaker, "text": chunk, "delay": 1.5})

    def spawn_bubble(self, seat_name, text):
        for i, b in enumerate(self.bubble_pool):
            if not b["active"]:
                c = next((cr for cr in self.creatures if cr["name"] == seat_name), None)
                if not c:
                    c = next((cr for cr in self.creatures if cr["name"] == "Vertex"), None)
                    seat_name = "Vertex"
                    if not c: return 
                
                ref_size = min(self.width, self.height)
                sx = max(self.width * 0.15, min(self.width * 0.85, c["cx"]))
                current_scale = c["scale"] * 1.8 if (seat_name == "Vertex" and self.vertex_greeting_timer > 0) else c["scale"]
                raw_sy = c["cy"] + (self.width * current_scale * 0.5) 
                sy = min(raw_sy, self.height * 0.75)
                
                text_color = TEXT_COLORS.get(seat_name, (0.95, 0.95, 1.0, 1))
                lbl = CoreLabel(text=text, font_size=int(ref_size * 0.035), color=text_color)
                lbl.refresh()
                
                b["active"] = True; b["age"] = 0.0; b["life"] = 6.0; b["sx"] = sx; b["sy"] = sy
                b["color"] = SEAT_COLORS.get(seat_name, (1,1,1,1)); b["lbl"] = lbl; b["speaker"] = seat_name
                
                try:
                    self.sound_bank.duck_volume()
                    self.sound_bank.play_sting(seat_name)
                except: pass
                
                # THE TALKING FIX: Dynamic talk timer based on text length
                talk_duration = max(1.5, min(6.0, len(text) * 0.1))
                c["talk_timer"] = talk_duration
                c["talk_start_time"] = self.time_elapsed
                return

    def spawn_float_text(self, x, y, seat_name, text="+1", color_override=None):
        for i, ft in enumerate(self.float_text_pool):
            if not ft["active"]:
                ref_size = min(self.width, self.height)
                text_color = color_override if color_override else SEAT_COLORS.get(seat_name, (1,1,1,1))
                size = 0.06 if text == "zZz" else 0.04
                lbl = CoreLabel(text=text, font_size=int(ref_size * size), color=text_color); lbl.refresh()
                ft["active"] = True; ft["x"] = max(self.width * 0.1, min(self.width * 0.9, x)); ft["y"] = y
                ft["vx"] = random.uniform(-40, 40); ft["life"] = 3.5; ft["color"] = text_color; ft["lbl"] = lbl
                return

    def spawn_ripple(self, x, y):
        for i, r in enumerate(self.ripple_pool):
            if not r["active"]:
                ref_size = min(self.width, self.height)
                r["active"] = True; r["x"] = x; r["y"] = y; r["age"] = 0.0; r["life"] = 0.6
                r["max_radius"] = ref_size * 0.15
                return
            
    def trigger_milestone(self):
        self.milestone_timer = 3.0
        self.lbl_milestone.text = f"MILESTONE: {brain.engine.bond_score}"; self.lbl_milestone.refresh()
        self.milestone_rect.texture = self.lbl_milestone.texture
        for i in range(20):
            for p in self.ambient_pool:
                if not p["active"]:
                    p.update({"active": True, "x": self.width * 0.5, "y": self.height * 0.5, "vx": random.uniform(-200, 200), "vy": random.uniform(-200, 200), "r": random.uniform(2, 5), "phase": random.uniform(0, 6.28), "color": "#FFD700"})
                    break
        try: self.sound_bank.play_sting("Vertex") 
        except: pass

    def spawn_food(self):
        if brain.engine.sleep_state != "AWAKE": return 
        flakes_spawned = 0
        for f in self.food_pool:
            if not f["active"]:
                f["active"] = True; f["x"] = self.width * 0.5 + random.uniform(-self.width*0.2, self.width*0.2) 
                f["y"] = self.height * 0.9; f["vx"] = random.uniform(-30, 30); f["vy"] = -random.uniform(80, 120) 
                flakes_spawned += 1
                if flakes_spawned >= 8: break 
        if flakes_spawned > 0:
            self.stream_queue.clear() 
            do_vibrate(80); self.feeding_timer = 10.0 
            try: self.sound_bank.play_feed_splash() 
            except: pass
            response = brain.engine.on_feed()
            if response: self.queue_speech(response)

    def on_touch_down(self, touch):
        if self.title_timer > 0: return
            
        if touch.y > self.height - self.ui_bar_top.size[1] - self.ui_bar_util.size[1] and touch.y < self.height - self.ui_bar_top.size[1]:
            btn_width = self.width / 5
            clicked_idx = int(touch.x / btn_width)
            
            if clicked_idx == 0: 
                if brain.engine.sleep_state == "AWAKE": self.spawn_food() 
            elif clicked_idx == 1: 
                brain.engine.trigger_sleep()
                self.stream_queue.clear() 
                for b in self.bubble_pool: b["age"] = b["life"] 
            elif clicked_idx == 2: brain.engine.toggle_lights()
            elif clicked_idx == 3: 
                state = self.sound_bank.cycle_volume()
                ref_size = min(self.width, self.height)
                if state == 0:
                    self.util_labels[3] = CoreLabel(text="VOL HI", font_size=int(ref_size * 0.022), color=NEON_RED)
                elif state == 1:
                    self.util_labels[3] = CoreLabel(text="VOL LO", font_size=int(ref_size * 0.022), color=NEON_GREEN)
                else:
                    self.util_labels[3] = CoreLabel(text="MUTE", font_size=int(ref_size * 0.022), color=NEON_RED)
                self.util_labels[3].refresh()
                self.util_text_objs[3][1].texture = self.util_labels[3].texture
            elif clicked_idx == 4: self.show_menu_popup()
            return
            
        if touch.y < self.ui_bar_bot.size[1]:
            biomes = list(BIOME_PALETTES.keys()); btn_width = self.width / len(biomes)
            clicked_idx = max(0, min(len(biomes) - 1, int(touch.x / btn_width)))
            new_biome = biomes[clicked_idx]
            if new_biome != self.current_biome:
                self.current_biome = new_biome
                self.stream_queue.clear() 
                for b in self.bubble_pool: b["age"] = b["life"]
                self.bg_rect.texture = self.gradient_textures[self.current_biome]
                try: self.sound_bank.play_bed(self.current_biome.lower())
                except: pass
                brain.engine.on_biome_switch(self.current_biome)
                self.update_bond_ui()
            return
            
        if brain.engine.sleep_state in ["SLEEPING", "RESISTING"]:
            brain.engine.wake_up()
            self.stream_queue.clear() 
            for b in self.bubble_pool: b["age"] = b["life"]
            do_vibrate(40); self.spawn_ripple(touch.x, touch.y)
            return

        if brain.engine.game_state == "riddle_wait":
            for c in self.creatures:
                dist = math.hypot(touch.x - c["cx"], touch.y - c["cy"])
                if dist < self.width * c["scale"] * 0.8:
                    do_vibrate(40); self.spawn_ripple(touch.x, touch.y); brain.engine.on_creature_tap(c["name"]); return
            return
        do_vibrate(40); self.spawn_ripple(touch.x, touch.y); brain.engine.on_guest_tap()

    def add_bond(self):
        do_vibrate(15)
        if brain.engine.add_bond(1, "eat"): self.trigger_milestone()
        self.update_bond_ui()

    def update_bond_ui(self):
        new_text = brain.get_status()
        if self.lbl_bond.text != new_text:
            self.lbl_bond.text = new_text
            self.lbl_bond.refresh()
            self.ui_text_objs[0][1].texture = self.lbl_bond.texture

    # =====================================================================
    # SECTION 5: THE MAIN TICK LOOP (Physics, Movement, Animations)
    # =====================================================================
    def tick(self, dt):
        if dt > 0.033: dt = 0.033 
        self.time_elapsed += dt
        self.base_scroll += dt * 100.0
        
        target_alpha = 0.55 if not brain.engine.iot.lights_on or brain.engine.sleep_state in ["SLEEPING", "WAKING"] else 0.0
        current_alpha = self.lights_out_color.a
        if current_alpha < target_alpha: self.lights_out_color.a = min(target_alpha, current_alpha + dt * 2.0)
        elif current_alpha > target_alpha: self.lights_out_color.a = max(target_alpha, current_alpha - dt * 2.0)
        
        ref_size = min(self.width, self.height)
        
        if self.last_lights_on != brain.engine.iot.lights_on:
            self.last_lights_on = brain.engine.iot.lights_on
            lights_color = NEON_RED if self.last_lights_on else NEON_GREEN
            self.util_labels[2] = CoreLabel(text="DIM", font_size=int(ref_size * 0.022), color=lights_color)
            self.util_labels[2].refresh()
            self.util_text_objs[2][1].texture = self.util_labels[2].texture

        if self.last_sleep_state != brain.engine.sleep_state:
            self.last_sleep_state = brain.engine.sleep_state
            if self.last_sleep_state in ["SLEEPING", "RESISTING", "WAKING"]:
                self.stream_queue.clear() 
                for b in self.bubble_pool: b["age"] = b["life"]

        if self.title_timer > 0:
            self.title_timer -= dt
            alpha = max(0.0, min(1.0, self.title_timer))
            self.title_bg_color.rgba = (0, 0, 0, alpha)
            self.title_text_color.rgba = (1, 1, 1, alpha)
            self.subtitle_text_color.rgba = (1, 1, 1, alpha)
            tw, th = self.lbl_title.texture.size
            self.title_text_rect.pos = (self.width * 0.5 - tw/2, self.height * 0.6); self.title_text_rect.size = (tw, th)
            tw2, th2 = self.lbl_subtitle.texture.size
            self.subtitle_text_rect.pos = (self.width * 0.5 - tw2/2, self.height * 0.45); self.subtitle_text_rect.size = (tw2, th2)
            
            if self.title_timer <= 0 and not self.name_prompt_shown:
                if brain.engine.user_name == "Guest" or not brain.engine.user_name:
                    self.show_name_popup()

        if brain.engine.trigger_cinematic:
            self.cinematic.trigger(); brain.engine.trigger_cinematic = False
            
        self.cinematic.update(dt)
        cinematic_targets, cinematic_scale = self.cinematic.get_targets(self.width, self.height)

        self.weather.update(dt, brain.engine.current_mood)
        self.weather_tint_color.rgba = self.weather.current_tint
        
        # --- AUTO-DJ ---
        target_music_mood = "normal"
        if brain.engine.current_mood == "SLEEPY" or brain.engine.sleep_state in ["SLEEPING", "WAKING"]: 
            target_music_mood = "sleepy"
        elif brain.engine.current_mood == "PLAYFUL": 
            target_music_mood = "playful"
        elif brain.engine.current_mood == "CRISIS": 
            target_music_mood = "crisis"
        
        if self.sound_bank.current_mood != target_music_mood:
            self.sound_bank.start_music(target_music_mood)

        for c, rot, rect in self.god_rays: c.rgba = (1, 1, 0.8, self.weather.current_ray_alpha * 0.4)
            
        if self.weather.should_spawn_vent_bubble():
            for vent_x in self.sand_vents:
                if random.random() < 0.5:
                    for b in self.sand_bubble_pool:
                        if not b["active"]:
                            b["active"] = True; b["x"] = self.width * vent_x + random.uniform(-10, 10)
                            b["y"] = self.height * 0.05; b["r"] = random.uniform(1.5, 3.0)
                            b["vy"] = random.uniform(20, 50) * self.weather.current_bubble_speed; b["life"] = 1.0
                            break

        active_bubbles = sum(1 for b in self.bubble_pool if b["active"])
        if active_bubbles == 0 and self.title_timer <= 0:
            try: self.sound_bank.restore_volume()
            except: pass
        
        if self.feeding_timer > 0:
            self.feeding_timer -= dt
            if self.feeding_timer <= 0:
                for f in self.food_pool: f["active"] = False

        if int(self.time_elapsed * 10) % 10 == 0: self.update_bond_ui()

        if brain.engine.sleep_state == "SLEEPING" and random.random() < 0.05:
            for c_state in self.creatures:
                if random.random() < 0.2:
                    self.spawn_float_text(c_state["cx"], c_state["cy"], c_state["name"], text="zZz", color_override=NEON_BLUE)

        status_text = ""
        if brain.engine.listening_for_request: status_text = f"Tap: {brain.engine.tap_count}"
        elif brain.engine.game_state == "riddle_wait": status_text = f"Time: {int(brain.engine.riddle_timer)}s"
        if self.lbl_status.text != status_text:
            self.lbl_status.text = status_text; self.lbl_status.refresh(); self.ui_text_objs[1][1].texture = self.lbl_status.texture

        if active_bubbles < 2:
            next_dialogue = brain.engine.update(dt, self.bond)
            if next_dialogue: self.queue_speech(next_dialogue)
            
        if self.stream_queue and self.title_timer <= 0:
            self.stream_timer += dt
            if self.stream_timer >= self.stream_queue[0]["delay"]:
                self.stream_timer = 0.0
                item = self.stream_queue.pop(0)
                self.spawn_bubble(item["speaker"], item["text"])
                if item["speaker"] == "Vertex" and not self.has_vertex_greeted:
                    self.vertex_greeting_timer = 6.0; self.has_vertex_greeted = True
        
        off_mtn, off_pil, off_dune, off_grass, off_stars = (self.base_scroll * 0.2) % 10000, (self.base_scroll * 0.25) % 10000, (self.base_scroll * 0.4) % 10000, (self.base_scroll * 1.5) % 10000, (self.base_scroll * 0.8) % 10000

        if self.vertex_greeting_timer > 0: self.vertex_greeting_timer -= dt

        active_food = []
        grounded_food = []
        for i, f in enumerate(self.food_pool):
            c_glow, e_glow, c_core, e_core = self.food_objs[i]
            if f["active"]:
                f["x"] += f["vx"] * dt
                if f["y"] > self.height * 0.15: f["y"] += f["vy"] * dt 
                else: f["vy"] = 0; grounded_food.append(f)
                
                pulse = 1.0 + math.sin(self.time_elapsed * 6 + f["phase"]) * 0.2
                r = self.height * 0.005 * pulse 
                c_glow.rgba = (1, 0.6, 0.2, 0.3)
                e_glow.pos = (f["x"] - r*3, f["y"] - r*0.2); e_glow.size = (r*6, r*0.4)
                c_core.rgba = (1, 0.9, 0.5, 0.8)
                e_core.pos = (f["x"] - r*1.5, f["y"] - r*0.1); e_core.size = (r*3, r*0.2)
                active_food.append(f)
            else: e_glow.size = (0,0); e_core.size = (0,0)

        sand_y = self.height * 0.05
        lumen_idx = next((i for i, c in enumerate(self.creatures) if c["name"] == "Lumen"), -1)
        mood = brain.engine.current_mood
        
        if cinematic_targets: 
            formation_coords = cinematic_targets
        else: 
            if brain.engine.sleep_state in ["SLEEPING", "RESISTING"]:
                formation_coords = choreography.get_formation("SLEEPING", self.width, self.height, self.time_elapsed)
            elif brain.engine.sleep_state == "WAKING":
                formation_coords = choreography.get_formation("WAKING", self.width, self.height, self.time_elapsed, waking_leader=brain.engine.waking_leader)
            elif brain.engine.feeding_state_timer > 0:
                formation_coords = choreography.get_formation("FEEDING", self.width, self.height, self.time_elapsed, feeding_timer=brain.engine.feeding_state_timer)
            else:
                formation_coords = choreography.get_formation(mood, self.width, self.height, self.time_elapsed)

        for i, c_state in enumerate(self.creatures):
            current_scale = c_state["scale"]
            if cinematic_targets: current_scale *= cinematic_scale

            if formation_coords:
                target_cx, target_cy = formation_coords[i]
                c_state["action"] = "formation" 
                
                if brain.engine.sleep_state == "RESISTING" and c_state["name"] == "Vertex":
                    target_cx = self.width * c_state["x_rel"]
                    target_cy = self.height * c_state["y_rel"] + abs(math.sin(self.time_elapsed * 5)) * (self.height * 0.1)
            else:
                c_state["action_timer"] -= dt
                if c_state["action_timer"] <= 0:
                    action_choices = ["idle", "idle", "idle", "climb", "rest", "hug"]
                    chosen = random.choice(action_choices)
                    if chosen == "climb" and c_state["name"] in ["Solon", "Lumen"]: chosen = "idle"
                    c_state["action"] = chosen; c_state["action_timer"] = random.uniform(25.0, 45.0) 
                    if c_state["action"] == "hug":
                        others = [x for x in self.creatures if x["name"] != c_state["name"]]
                        c_state["target_creature"] = random.choice(others)
                        
                target_cx = self.width * c_state["x_rel"]; target_cy = self.height * c_state["y_rel"]
                
                if c_state["action"] == "climb": target_cy = self.height * 0.65 
                elif c_state["action"] == "rest": target_cy = self.ui_bar_bot.size[1] + (self.height * 0.05)
                elif c_state["action"] == "hug" and c_state["target_creature"]:
                    target_cx = c_state["target_creature"]["cx"] + random.uniform(-80, 80)
                    target_cy = c_state["target_creature"]["cy"] + random.uniform(-40, 40)
                
                if c_state["name"] == "Vertex": 
                    target_cy = sand_y + (self.width * current_scale * 0.3) + abs(math.sin(self.time_elapsed * 3.5)) * (self.height * 0.04)
                elif c_state["action"] != "rest": 
                    target_cy += math.sin(self.time_elapsed * 2.0 + c_state["phase"]) * (self.height * 0.02)

            breath_scale = 1.0 + (math.sin(self.time_elapsed * 2.5 + c_state["phase"]) * 0.03)
            current_scale = current_scale * breath_scale
            
            if c_state["name"] == "Vertex" and self.vertex_greeting_timer > 0:
                if self.vertex_greeting_timer > 5.0:
                    t = (6.0 - self.vertex_greeting_timer) / 1.0
                    current_scale *= (1.0 + (t * 0.8))
                elif self.vertex_greeting_timer > 1.0: current_scale *= 1.8
                else:
                    t = self.vertex_greeting_timer / 1.0
                    current_scale *= (1.0 + (t * 0.8))
            
            c_state["blink_timer"] -= dt
            if c_state["blink_timer"] <= 0:
                if not c_state["is_blinking"]:
                    if c_state["name"] == "Prism" and c_state["prism_burst"] == 0: c_state["prism_burst"] = 3
                    c_state["is_blinking"] = True; c_state["blink_timer"] = 0.12
                else:
                    c_state["is_blinking"] = False
                    if c_state["name"] == "Prism":
                        c_state["prism_burst"] -= 1
                        if c_state["prism_burst"] > 0: c_state["blink_timer"] = 0.15
                        else: c_state["blink_timer"] = 4.0 + random.uniform(-0.5, 0.5)
                    else: c_state["blink_timer"] = c_state["blink_cooldowns"][c_state["name"]] + random.uniform(-1.0, 1.0)
                        
            if c_state["talk_timer"] > 0: c_state["talk_timer"] -= dt
            
            move_speed = 1.5 if not cinematic_targets else 3.5
            can_eat = (self.time_elapsed - c_state["last_ate_time"]) > 3.0
            
            if self.feeding_timer > 0 and active_food and can_eat and not cinematic_targets:
                nearest_food = min(active_food, key=lambda f: math.hypot(f["x"] - c_state["cx"], f["y"] - c_state["cy"]))
                dist_to_food = math.hypot(nearest_food["x"] - c_state["cx"], nearest_food["y"] - c_state["cy"])
                seek_target_x = nearest_food["x"] + c_state["seek_off_x"]; seek_target_y = nearest_food["y"] + c_state["seek_off_y"]
                seek_target_x = max(self.width * 0.1, min(self.width * 0.9, seek_target_x))
                ate = False
                
                if c_state["name"] == "Prism":
                    target_cx = seek_target_x; target_cy = seek_target_y; move_speed = 2.5 
                    if dist_to_food < 60: ate = True
                elif c_state["name"] == "Lumen":
                    target_cx = seek_target_x; target_cy = seek_target_y; move_speed = 1.2 
                    if dist_to_food < 60: ate = True
                elif c_state["name"] == "Solon":
                    if (10.0 - self.feeding_timer) > 4.0: 
                        target_cx = seek_target_x; target_cy = seek_target_y; move_speed = 0.6 
                        if dist_to_food < 60: ate = True
                elif c_state["name"] == "Vertex" and grounded_food:
                    g_food = min(grounded_food, key=lambda f: math.hypot(f["x"] - c_state["cx"], f["y"] - c_state["cy"]))
                    target_cx = g_food["x"]; target_cy = g_food["y"]; move_speed = 1.8 
                    if math.hypot(g_food["x"] - c_state["cx"], g_food["y"] - c_state["cy"]) < 60:
                        nearest_food = g_food; ate = True
                elif c_state["name"] == "Ripple":
                    if dist_to_food < 120: ate = True

                if ate:
                    c_state["last_ate_time"] = self.time_elapsed 
                    self.spawn_float_text(nearest_food["x"], nearest_food["y"], c_state["name"])
                    nearest_food["active"] = False
                    if nearest_food in active_food: active_food.remove(nearest_food)
                    if nearest_food in grounded_food: grounded_food.remove(nearest_food)
                    self.add_bond(); c_state["action"] = "idle" 

            c_state["cx"] += (target_cx - c_state["cx"]) * dt * move_speed
            c_state["cy"] += (target_cy - c_state["cy"]) * dt * move_speed
            if not cinematic_targets: c_state["cx"] = max(self.width * 0.1, min(self.width * 0.9, c_state["cx"]))
            
            cx = c_state["cx"]; cy = c_state["cy"]
            c_shadow, e_shadow = self.shadow_objs[i]
            if cy > sand_y:
                shadow_dist = cy - sand_y; shadow_alpha = max(0.05, 0.35 - (shadow_dist / self.height)); shadow_scale = max(0.5, 1.0 - (shadow_dist / self.height))
                c_shadow.rgba = (0, 0, 0, shadow_alpha); e_shadow.pos = (cx - (self.width*current_scale*0.4*shadow_scale), sand_y - (self.height*0.01)); e_shadow.size = (self.width*current_scale*0.8*shadow_scale, self.height*0.03*shadow_scale)
            else: e_shadow.size = (0,0)

            if c_state["name"] == "Solon":
                c_sprite, r_sprite = self.solon_body_rect
            else:
                c_sprite, r_sprite = self.other_creature_objs[i]

            tex_name = c_state["name"]
            
            # --- TEXTURE STATE LOGIC (TALK PRIORITY FIX) ---
            if brain.engine.sleep_state == "SLEEPING":
                tex_name += "_blink" 
            elif brain.engine.sleep_state == "RESISTING":
                if c_state["name"] == "Vertex": pass 
                else: tex_name += "_blink"
            elif brain.engine.sleep_state == "WAKING":
                if c_state["name"] == brain.engine.waking_leader:
                    if brain.engine.sleep_timer > 7.0: tex_name += "_blink" 
                    elif brain.engine.sleep_timer > 5.0: tex_name += "_half" 
                    else: pass 
                else:
                    if brain.engine.sleep_timer > 2.0: 
                        if c_state["name"] == "Vertex": tex_name += "_blink" 
                        else: tex_name += "_blink"
                    else:
                        tex_name += "_half"
            elif c_state["talk_timer"] > 0: # TALK PRIORITY ABOVE BLINKING
                if int((self.time_elapsed - c_state["talk_start_time"]) / 0.15) % 2 == 0: tex_name += "_talk"
            elif c_state["is_blinking"]: 
                tex_name += "_blink"
                
            if not self.textures.get(tex_name): tex_name = c_state["name"]
            tex = self.textures[tex_name]; r_sprite.texture = tex

            size_w = self.width * current_scale
            size_h = size_w * (tex.height / tex.width) if tex else size_w
            
            draw_x = cx - size_w/2
            draw_y = cy - size_h/2
            
            if c_state["name"] == "Prism":
                wobble_speed = 10.0 if mood == "PLAYFUL" else 8.0
                if brain.engine.sleep_state != "AWAKE": wobble_speed = 2.0
                
                wobble_x = math.sin(self.time_elapsed * wobble_speed) * (size_w * 0.03)
                wobble_y = math.cos(self.time_elapsed * wobble_speed * 2) * (size_h * 0.02)
                
                draw_x += wobble_x
                draw_y += wobble_y

            r_sprite.pos = (draw_x, draw_y)
            r_sprite.size = (size_w, size_h)

            # --- SOLON FIN ANIMATION (Sprite Swap - Locked Math) ---
            if c_state["name"] == "Solon" and self.solon_left_frames and self.solon_right_frames:
                flap_speed = 8.0 
                if brain.engine.sleep_state in ["SLEEPING", "RESISTING"]: flap_speed = 2.0
                elif mood == "CRISIS": flap_speed = 20.0
                elif mood == "PLAYFUL": flap_speed = 15.0
                
                frame_idx = int(self.time_elapsed * flap_speed) % len(self.solon_left_frames)
                
                scale_factor = size_w / 512.0 
                fin_scale = 0.32 
                fw = 512 * scale_factor * fin_scale
                fh = 512 * scale_factor * fin_scale
                
                left_x = cx - size_w * 0.14
                left_y = cy - size_h * 0.17
                
                right_x = cx + size_w * 0.25
                right_y = cy - size_h * 0.18
                
                self.solon_left_fin_rect.texture = self.solon_left_frames[frame_idx]
                self.solon_left_fin_rect.size = (fw, fh)
                self.solon_left_fin_rect.pos = (left_x - fw/2, left_y - fh/2)
                
                self.solon_right_fin_rect.texture = self.solon_right_frames[frame_idx]
                self.solon_right_fin_rect.size = (fw, fh)
                self.solon_right_fin_rect.pos = (right_x - fw/2, right_y - fh/2)

            if i == lumen_idx and self.textures["Lumen"]:
                base_y = cy - (size_h / 2) 
                for t_idx in range(5):
                    c_glow, l_glow, c_core, l_core = self.lumen_tentacle_objs[t_idx]
                    pts = []; start_x = cx + (t_idx - 2) * (size_w * 0.08)
                    for k in range(15):
                        f = k / 14.0
                        pts_y = max(self.ui_bar_bot.size[1] + 10, base_y - (size_h * 1.1 * f))
                        pts.extend([start_x + (math.sin(self.time_elapsed * 2.0 + (t_idx * 1.3) - (f * 3.0)) * size_w * 0.25 * f), pts_y])
                    l_glow.points = pts; l_core.points = pts

        # --- SAND BUBBLES ---
        for i in range(self.max_sand_bubbles):
            b = self.sand_bubble_pool[i]; c_rim, l_rim = self.sand_bubble_objs[i]
            if b["active"]:
                b["y"] += b["vy"] * dt; b["life"] -= dt * 0.2
                if b["y"] > self.height * 0.9 or b["life"] <= 0: b["active"] = False; l_rim.circle = (0,0,0)
                else:
                    alpha = max(0.0, min(1.0, b["life"]))
                    c_rim.rgba = (1, 1, 1, alpha * 0.6); l_rim.circle = (b["x"], b["y"], b["r"])
            else: l_rim.circle = (0,0,0)

        # --- AMBIENT PARTICLES ---
        for i in range(self.max_ambient):
            p = self.ambient_pool[i]
            if not p["active"]:
                if random.random() < 0.005: 
                    p.update({"active": True, "x": self.width + 10, "y": random.uniform(self.height * 0.15, self.height * 0.85), "vx": -random.uniform(30, 80), "vy": random.uniform(10, 40), "r": random.uniform(1.5, 3.5), "phase": random.uniform(0, 6.28), "color": random.choice(PARTICLE_COLORS[self.current_biome])})
            else:
                p["x"] += p["vx"] * dt; p["y"] += p["vy"] * dt
                if p["x"] < -20: p["active"] = False
        
        # --- CREATURE DUST ---
        for i in range(self.max_dust):
            p = self.dust_pool[i]
            if not p["active"]:
                if random.random() < 0.01:
                    c = random.choice(self.creatures)
                    p.update({"active": True, "x": c["cx"] - (self.width * c["scale"] * 0.3) + random.uniform(-10, 10), "y": c["cy"] + random.uniform(-10, 10), "vx": -random.uniform(10, 30), "vy": random.uniform(-10, 10), "r": random.uniform(1.0, 2.5), "life": 1.0, "color": random.choice(PARTICLE_COLORS[self.current_biome])})
            else:
                p["x"] += p["vx"] * dt; p["y"] += p["vy"] * dt; p["life"] -= dt * 0.08
                if p["life"] <= 0: p["active"] = False
        
        # --- STARS ---
        for i, s in enumerate(self.stars):
            sx = (s["x"] * self.width - off_stars) % self.width
            pulse = 0.5 + 0.5 * math.sin(self.time_elapsed * s["speed"] + s["phase"])
            c, e = self.star_objs[i]; c.rgba = (1, 1, 1, pulse * 0.6); e.pos = (sx, s["y"] * self.height); e.size = (s["r"], s["r"])
        
        # --- PARALLAX BACKGROUNDS ---
        if self.mtn_texture:
            mtn_w, mtn_h = self.width * 1.2, self.width * 1.2 * (self.mtn_texture.height / self.mtn_texture.width); offset = off_mtn % mtn_w
            for i in range(3): c, r = self.mtn_objs[i]; r.pos = (-offset + (i * mtn_w), self.height * 0.03); r.size = (mtn_w, mtn_h)
        if self.pillar_texture:
            pil_w, pil_h = self.width * 1.2, self.width * 1.2 * (self.pillar_texture.height / self.pillar_texture.width); offset = off_pil % pil_w
            for i in range(3): c, r = self.pillar_objs[i]; r.pos = (-offset + (i * pil_w), self.height * 0.02); r.size = (pil_w, pil_h)
        if self.dune_texture:
            tint = SAND_TINTS[self.current_biome]; dune_w, dune_h = self.width * 1.5, self.width * 1.5 * (self.dune_texture.height / self.dune_texture.width); offset = off_dune % dune_w
            for i in range(3): c, r = self.dune_objs[i]; c.rgba = tint; r.pos = (-offset + (i * dune_w), 0); r.size = (dune_w, dune_h)
        
        # --- RENDERING DUST & AMBIENT ---
        for i in range(self.max_dust):
            p = self.dust_pool[i]; c1, e1, c2, e2 = self.dust_objs[i]
            if p["active"] and p["life"] > 0:
                alpha = max(0.0, p["life"]); rgba = self.hex_to_rgba(p["color"])
                c1.rgba = (rgba[0], rgba[1], rgba[2], alpha); e1.pos = (p["x"] - p["r"]*2, p["y"] - p["r"]*2); e1.size = (p["r"]*4, p["r"]*4)
                c2.rgba = (1, 1, 1, alpha); e2.pos = (p["x"] - p["r"]*0.5, p["y"] - p["r"]*0.5); e2.size = (p["r"], p["r"])
            else: e1.size = (0, 0); e2.size = (0, 0)
        for i in range(self.max_ambient):
            p = self.ambient_pool[i]; c1, e1, c2, e2 = self.ambient_objs[i]
            if p["active"]:
                pulse = 0.5 + 0.5 * math.sin(self.time_elapsed * 4 + p["phase"]); rgba = self.hex_to_rgba(p["color"])
                c1.rgba = (rgba[0], rgba[1], rgba[2], 1.0); e1.pos = (p["x"] - p["r"]*2, p["y"] - p["r"]*2); e1.size = (p["r"]*4, p["r"]*4)
                c2.rgba = (1, 1, 1, pulse); e2.pos = (p["x"] - p["r"]*0.5, p["y"] - p["r"]*0.5); e2.size = (p["r"], p["r"])
            else: e1.size = (0, 0); e2.size = (0, 0)
        
        if self.fg_texture:
            fg_w, fg_h = self.width * 1.5, self.width * 1.5 * (self.fg_texture.height / self.fg_texture.width); offset = off_grass % fg_w
            for i in range(3): c, r = self.grass_objs[i]; r.pos = (-offset + (i * fg_w), 0); r.size = (fg_w, fg_h)

        # --- GHOST BUBBLE TRAP ---
        for i in range(self.max_bubbles):
            b = self.bubble_pool[i]; c_fill, e_fill, c_hl, l_hl, c_txt, r_txt = self.bubble_objs[i]
            if b["active"]:
                b["age"] += dt; p = b["age"] / b["life"] 
                if p >= 1.0: 
                    b["active"] = False
                    c_fill.rgba = (0,0,0,0)
                    e_fill.pos = (10000, 10000)
                    e_fill.size = (0,0)
                    e_fill.texture = None
                    l_hl.points = []
                    c_hl.rgba = (0,0,0,0)
                    r_txt.size = (0,0)
                    r_txt.texture = None
                    c_txt.rgba = (0,0,0,0)
                else:
                    max_rise = self.height * 0.48; true_cy = b["sy"] + max_rise * p; true_cx = b["sx"] + math.sin(p * math.pi * 2) * (self.width * 0.08)
                    cy = int(true_cy); cx = int(true_cx)
                    tw, th = b["lbl"].texture.size; r = int((math.sqrt(tw**2 + th**2) / 2) + (min(self.width, self.height) * 0.02))
                    alpha = p/0.1 if p < 0.1 else (1.0-p)/0.2 if p > 0.75 else 1.0
                    
                    c_fill.rgba = (0.15, 0.25, 0.35, alpha * 0.45); e_fill.pos = (cx - r, cy - r); e_fill.size = (r*2, r*2)
                    c_hl.rgba = (1, 1, 1, alpha * 0.8); hr = int(r * 0.75)
                    pts = []
                    for deg in range(100, 141, 5): 
                        rad = math.radians(deg); pts.extend([int(cx + hr * math.cos(rad)), int(cy + hr * math.sin(rad))])
                    l_hl.points = pts
                    
                    c_txt.rgba = (1, 1, 1, alpha); r_txt.texture = b["lbl"].texture
                    r_txt.pos = (cx - tw//2, cy - th//2); r_txt.size = (tw, th)
            else:
                c_fill.rgba = (0,0,0,0)
                e_fill.pos = (10000, 10000)
                e_fill.size = (0,0)
                e_fill.texture = None
                l_hl.points = []
                c_hl.rgba = (0,0,0,0)
                r_txt.size = (0,0)
                r_txt.texture = None
                c_txt.rgba = (0,0,0,0)

        for i in range(self.max_float_text):
            ft = self.float_text_pool[i]; c_ft, r_ft = self.float_text_objs[i]
            if ft["active"]:
                speed = 300.0 if ft["lbl"].text == "zZz" else 180.0
                ft["life"] -= dt; ft["y"] += speed * dt; ft["x"] += ft["vx"] * dt 
                if ft["life"] <= 0: ft["active"] = False; r_ft.size = (0, 0)
                else:
                    alpha = max(0.0, min(1.0, ft["life"])); c_ft.rgba = (1, 1, 1, alpha) 
                    tw, th = ft["lbl"].texture.size; r_ft.texture = ft["lbl"].texture
                    r_ft.pos = (int(ft["x"] - tw//2), int(ft["y"] - th//2)); r_ft.size = (tw, th)
        for i in range(self.max_ripples):
            r = self.ripple_pool[i]; c, l = self.ripple_objs[i]
            if r["active"]:
                r["age"] += dt
                if r["age"] >= r["life"]: r["active"] = False; l.circle = (0, 0, 0); c.rgba = (1, 1, 1, 0)
                else:
                    progress = r["age"] / r["life"]; radius = r["max_radius"] * progress
                    alpha = max(0.0, 1.0 - progress); c.rgba = (1, 1, 1, alpha * 0.5)
                    l.circle = (r["x"], r["y"], radius); l.width = max(1, int(min(self.width, self.height) * 0.005 * (1.0 - progress)))

        # =====================================================================
        # SECTION 6: UI RENDERING AND TEXT UPDATES
        # =====================================================================
        if self.milestone_timer > 0:
            self.milestone_timer -= dt; alpha = max(0.0, min(1.0, self.milestone_timer))
            self.milestone_color.rgba = (1.0, 0.8, 0.0, alpha)
            tw, th = self.lbl_milestone.texture.size
            self.milestone_rect.pos = (self.width * 0.5 - tw/2, self.height * 0.7); self.milestone_rect.size = (tw, th)
        else: self.milestone_color.rgba = (1, 1, 1, 0)

        if hasattr(self, 'biome_labels'):
            biome_h = self.biome_labels[self.current_biome].texture.height
            bot_bar_h = int(biome_h * 2.5)
        else: bot_bar_h = 60
        top_bar_h = int(self.lbl_bond.texture.height * 2.5)

        bond_c, bond_r = self.ui_text_objs[0]
        bond_y = int(self.height - top_bar_h + (top_bar_h - self.lbl_bond.texture.height) / 2)
        bond_r.pos = (int(self.width * 0.5 - self.lbl_bond.texture.width/2), bond_y); bond_r.size = self.lbl_bond.texture.size

        util_bar_h = int(top_bar_h * 0.7)
        btn_width = self.width / 5
        for i, (c_util, r_util) in enumerate(self.util_text_objs):
            lbl = self.util_labels[i]
            r_util.texture = lbl.texture
            lx = int(i * btn_width + (btn_width/2) - (lbl.texture.width/2))
            ly = int(self.height - top_bar_h - util_bar_h + (util_bar_h - lbl.texture.height) / 2)
            r_util.pos = (lx, ly); r_util.size = lbl.texture.size

        status_c, status_r = self.ui_text_objs[1]
        if self.lbl_status.text != "":
            status_r.pos = (int(self.width * 0.5 - self.lbl_status.texture.width/2), int(bond_y - self.lbl_status.texture.height - 5))
            status_r.size = self.lbl_status.texture.size
        else: status_r.size = (0,0)

        if SHOW_DEBUG:
            self.debug_timer += dt
            if self.debug_timer > 0.2:
                self.debug_timer = 0.0
                sensor = brain.engine.sensor_array; mood = brain.engine.current_mood
                act = brain.engine.brain_activity; act_str = ", ".join([f"{a:.1f}" for a in act])
                
                debug_str = (
                    f"Mood: {mood}\n"
                    f"Sleep: {brain.engine.sleep_state}\n"
                    f"Light: {sensor.light_level:.2f} | Temp: {sensor.thermal_baseline:.2f}\n"
                    f"Motion: {sensor.motion_mag:.2f} | Shake: {sensor.shakiness:.2f}\n"
                    f"Rhythm: {sensor.last_tap_interval:.1f}s | Heat: {brain.engine.heat}\n"
                    f"Net: [{act_str}]"
                )
                self.lbl_debug.text = debug_str; self.lbl_debug.refresh(); self.debug_text_rect.texture = self.lbl_debug.texture
                
            tw, th = self.lbl_debug.texture.size
            self.debug_bg_rect.pos = (int(self.width * 0.01), int(self.height - top_bar_h - util_bar_h - th - 15)); self.debug_bg_rect.size = (tw + 20, th + 10)
            self.debug_text_rect.pos = (int(self.width * 0.01) + 10, int(self.height - top_bar_h - util_bar_h - th - 10)); self.debug_text_rect.size = (tw, th)
            self.debug_bg_color.rgba = (0, 0, 0, 0.6); self.debug_text_color.rgba = (0.8, 1.0, 0.8, 1.0) 
        else:
            self.debug_bg_rect.size = (0, 0); self.debug_text_rect.size = (0, 0)

        biomes = list(BIOME_PALETTES.keys()); btn_width = self.width / len(biomes)
        for i, b in enumerate(biomes):
            c_txt, r_txt = self.ui_text_objs[2 + i]
            lbl = self.biome_labels_selected[b] if b == self.current_biome else self.biome_labels[b]
            r_txt.texture = lbl.texture
            lx = int(i * btn_width + (btn_width/2) - (lbl.texture.width/2))
            ly = int((bot_bar_h - lbl.texture.height) / 2)
            r_txt.pos = (lx, ly); r_txt.size = lbl.texture.size

        if active_bubbles < 2:
            self.canvas.ask_update()

    def hex_to_rgba(self, hex_str):
        hex_str = hex_str.lstrip('#')
        if len(hex_str) == 6: return (int(hex_str[0:2], 16)/255.0, int(hex_str[2:4], 16)/255.0, int(hex_str[4:6], 16)/255.0, 1.0)
        return (0, 0, 0, 1.0)

# =====================================================================
# APP RUNNER
# =====================================================================
class TerrariumApp(App):
    def build(self):
        return Terrarium()

if __name__ == '__main__':
    TerrariumApp().run()