# choreography.py
import math

def get_formation(mood, width, height, time_elapsed, feeding_timer=0, waking_leader=None):
    if mood == "CRISIS":
        phase = int(time_elapsed / 4.0) % 4
        cx, cy = width * 0.5, height * 0.5
        
        if phase == 0:
            return [(cx - 80, cy + 40), (cx + 80, cy + 40), (cx - 60, cy - 60), (cx + 60, cy - 60), (cx, cy)]
        elif phase == 1:
            radius = min(width, height) * 0.20
            return [(cx + radius * math.cos(i * (2 * math.pi / 5)), cy + radius * math.sin(i * (2 * math.pi / 5))) for i in range(5)]
        elif phase == 2:
            return [((width * 0.15) + (i * (width * 0.15)), (height * 0.35) + math.sin((i / 4.0) * math.pi * 2 + time_elapsed * 3) * (height * 0.15)) for i in range(5)]
        else:
            return [(width * 0.10, height * 0.10), (width * 0.90, height * 0.10), (width * 0.25, height * 0.05), (width * 0.75, height * 0.05), (cx, height * 0.05)]
            
    elif mood == "FEEDING" and feeding_timer > 0:
        # Theatre of Feeding
        cx, cy = width * 0.5, height * 0.6
        time_left = 10.0 - feeding_timer # 0 to 10 seconds
        
        solon = (cx - width * 0.30, height * 0.15) # waits at bottom
        prism = (cx + width * 0.20 + math.sin(time_elapsed * 8) * 50, cy + math.cos(time_elapsed * 8) * 50) # darts
        lumen = (cx - width * 0.10, cy - height * 0.05) # drifts slowly
        ripple = (cx + width * 0.05, cy + math.sin(time_elapsed * 2) * 30) # floats
        vertex = (cx + math.sin(time_elapsed * 10) * 80, height * 0.15 + abs(math.sin(time_elapsed * 5)) * 50) # bounces at bottom
        
        return [solon, prism, lumen, ripple, vertex]
        
    elif mood == "SLEEPING":
        bot_y = height * 0.15
        cx = width * 0.5
        return [
            (cx - width * 0.30, bot_y), (cx + width * 0.25, bot_y),
            (cx - width * 0.05, bot_y + height * 0.08), (cx + width * 0.35, bot_y),
            (cx - width * 0.25, bot_y)
        ]
        
    elif mood == "WAKING":
        bot_y = height * 0.15
        cx = width * 0.5
        
        # Default sleeping positions
        coords = [
            (cx - width * 0.30, bot_y), (cx + width * 0.25, bot_y),
            (cx - width * 0.05, bot_y + height * 0.08), (cx + width * 0.35, bot_y),
            (cx - width * 0.25, bot_y)
        ]
        
        # The Leader floats up and nudges
        if waking_leader:
            name_to_idx = {"Solon": 0, "Prism": 1, "Lumen": 2, "Ripple": 3, "Vertex": 4}
            if waking_leader in name_to_idx:
                idx = name_to_idx[waking_leader]
                # Move the leader up and towards the center to "nudge"
                coords[idx] = (cx, height * 0.35)
                
        return coords
        
    elif mood == "SLEEPY":
        cy = height * 0.20
        spacing = width / 6
        return [(spacing * i, cy) for i in range(1, 6)]
        
    elif mood == "PLAYFUL":
        cx, cy = width * 0.5, height * 0.5
        radius = min(width, height) * 0.25
        return [(cx + radius * math.cos((i * (2 * math.pi / 5)) + (time_elapsed * 0.5)), cy + radius * math.sin((i * (2 * math.pi / 5)) + (time_elapsed * 0.5))) for i in range(5)]
        
    elif mood == "TOTEM":
        cx = width * 0.5
        cy_start = height * 0.20
        spacing = height * 0.10
        return [(cx, cy_start + spacing * i) for i in range(5)]
        
    return None