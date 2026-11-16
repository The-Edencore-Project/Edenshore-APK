# cinematics.py

class CinematicEngine:
    def __init__(self):
        self.state = "IDLE"
        self.timer = 0.0
        self.zoom_progress = 0.0

    def trigger(self):
        if self.state == "IDLE":
            self.state = "ZOOMING_IN"
            self.timer = 0.0
            self.zoom_progress = 0.0

    def update(self, dt):
        if self.state == "IDLE":
            return

        self.timer += dt

        if self.state == "ZOOMING_IN":
            self.zoom_progress += dt * 1.5
            if self.zoom_progress >= 1.0:
                self.zoom_progress = 1.0
                self.state = "STARING"
                self.timer = 0.0

        elif self.state == "STARING":
            if self.timer >= 5.0:
                self.state = "ZOOMING_OUT"
                self.timer = 0.0

        elif self.state == "ZOOMING_OUT":
            self.zoom_progress -= dt * 1.5
            if self.zoom_progress <= 0.0:
                self.zoom_progress = 0.0
                self.state = "IDLE"

    def get_targets(self, width, height):
        if self.state == "IDLE":
            return None, 1.0

        cx, cy = width * 0.5, height * 0.5
        
        # Target positions for a wide, dramatic arc
        base_positions = [
            (cx - width*0.25, cy - height*0.05), # Left (Solon)
            (cx + width*0.25, cy - height*0.05), # Right (Prism)
            (cx - width*0.10, cy + height*0.15), # Top Left (Lumen)
            (cx + width*0.10, cy + height*0.15), # Top Right (Ripple)
            (cx, cy - height*0.20)               # Bottom Center (Vertex)
        ]

        # Scale multiplier: grows up to 2.0x size (was 3.5x)
        scale_mult = 1.0 + (1.0 * self.zoom_progress)
        
        if self.state in ["ZOOMING_IN", "STARING"]:
            return base_positions, scale_mult
        else:
            return base_positions, scale_mult