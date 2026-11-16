# atmosphere.py

class WeatherEngine:
    def __init__(self):
        # Current values (start at normal)
        self.current_tint = [0.0, 0.0, 0.0, 0.1] # RGBA
        self.current_ray_alpha = 0.4
        self.current_bubble_speed = 1.0
        
        # Target values
        self.target_tint = [0.0, 0.0, 0.0, 0.1]
        self.target_ray_alpha = 0.4
        self.target_bubble_speed = 1.0
        
        # Sand vent timer
        self.vent_timer = 0.0
        self.vent_threshold = 2.0

    def update(self, dt, mood):
        # Set targets based on Mood
        if mood == "SLEEPY":
            self.target_tint = [0.05, 0.0, 0.2, 0.4] # Deep blue
            self.target_ray_alpha = 0.1
            self.target_bubble_speed = 0.3
            self.vent_threshold = 5.0
            
        elif mood == "CRISIS":
            self.target_tint = [0.2, 0.2, 0.2, 0.6] # Storm grey
            self.target_ray_alpha = 0.0
            self.target_bubble_speed = 0.0
            self.vent_threshold = 10.0
            
        elif mood == "PLAYFUL":
            self.target_tint = [0.0, 0.0, 0.0, 0.0] # Clear
            self.target_ray_alpha = 0.8
            self.target_bubble_speed = 2.0
            self.vent_threshold = 1.0
            
        else: # NORMAL
            self.target_tint = [0.0, 0.0, 0.0, 0.1] # Slight haze
            self.target_ray_alpha = 0.4
            self.target_bubble_speed = 1.0
            self.vent_threshold = 2.5

        # Smoothly interpolate current values towards targets
        lerp_speed = dt * 0.5 # Adjust for transition speed
        
        for i in range(4):
            self.current_tint[i] += (self.target_tint[i] - self.current_tint[i]) * lerp_speed
            
        self.current_ray_alpha += (self.target_ray_alpha - self.current_ray_alpha) * lerp_speed
        self.current_bubble_speed += (self.target_bubble_speed - self.current_bubble_speed) * lerp_speed

        # Update vent timer
        self.vent_timer += dt

    def should_spawn_vent_bubble(self):
        if self.vent_timer >= self.vent_threshold and self.current_bubble_speed > 0.1:
            self.vent_timer = 0.0
            return True
        return False