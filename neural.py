# neural.py
import math
import random

class NeuralNet:
    def __init__(self):
        self.input_size = 32
        self.hidden_size = 8
        self.output_size = 4
        
        self.w1 = [[0.0 for _ in range(self.hidden_size)] for _ in range(self.input_size)]
        self.b1 = [0.0 for _ in range(self.hidden_size)]
        self.w2 = [[0.0 for _ in range(self.output_size)] for _ in range(self.hidden_size)]
        self.b2 = [0.0 for _ in range(self.output_size)]
        
        self.activity = [0.0] * self.hidden_size
        self.learning_rate = 0.005
        self.last_output_idx = 0
        
        self._apply_heuristics()

    def _apply_heuristics(self):
        LIGHT, MOTION, ORIENT, AUDIO, BATTERY, CHARGING, THERMAL, SHAKE = 0, 1, 2, 3, 4, 5, 6, 7
        HOUR, DAY, WEEKEND, ABSENCE, SESSION, T_FEED, T_RIDDLE, MONTH = 8, 9, 10, 11, 12, 13, 14, 15
        TAP_FREQ, SWIPE_FREQ, IDLE, BOND, HEAT, RHYTHM, WALKING, RIDDLE_WIN = 16, 17, 18, 19, 20, 21, 22, 23
        MOOD, CINE_COOL, BIOME, WEATHER, BAG_EX, FOCUS, CHOREO, QUEUE = 24, 25, 26, 27, 28, 29, 30, 31
        
        NORMAL, SLEEPY, PLAYFUL, CRISIS = 0, 1, 2, 3
        
        # SLEEPY
        self.w1[HOUR][0] = 3.0       
        self.w1[LIGHT][0] = -2.0     
        self.w1[MOTION][0] = -1.0    
        self.w1[IDLE][0] = 1.5       
        self.b1[0] = -1.0            
        self.w2[0][SLEEPY] = 4.0     
        
        # PLAYFUL
        self.w1[TAP_FREQ][1] = 2.0
        self.w1[BOND][1] = 2.0
        self.w1[LIGHT][1] = 1.0      
        self.w1[HEAT][1] = -2.0      
        self.b1[1] = -1.0
        self.w2[1][PLAYFUL] = 4.0
        
        # CRISIS
        self.w1[HEAT][2] = 3.0
        self.w1[SHAKE][2] = 4.0      
        self.w1[RHYTHM][2] = 3.0     
        self.w1[AUDIO][2] = 2.0
        self.b1[2] = -4.0            
        self.w2[2][CRISIS] = 6.0     
        
        # NORMAL
        self.w1[IDLE][3] = 1.0
        self.w1[LIGHT][3] = 1.0
        self.w1[HEAT][3] = -2.0
        self.b1[3] = 1.0             
        self.w2[3][NORMAL] = 3.0
        
    def _sigmoid(self, x):
        if x < -500: return 0.0
        if x > 500: return 1.0
        return 1.0 / (1.0 + math.exp(-x))

    def process(self, inputs):
        if len(inputs) != self.input_size:
            return "NORMAL"
            
        # Forward pass: Hidden layer
        self.activity = []
        for h in range(self.hidden_size):
            val = self.b1[h]
            for i in range(self.input_size):
                val += inputs[i] * self.w1[i][h]
            self.activity.append(self._sigmoid(val))
            
        # Forward pass: Output layer
        outputs = []
        for o in range(self.output_size):
            val = self.b2[o]
            for h in range(self.hidden_size):
                val += self.activity[h] * self.w2[h][o]
            outputs.append(self._sigmoid(val))
            
        max_idx = outputs.index(max(outputs))
        self.last_output_idx = max_idx
        
        # --- REAL-TIME HEBBIAN LEARNING ---
        # If the system is in CRISIS, strengthen the connections that caused it.
        if max_idx == 3: # CRISIS
            for i in [1, 7, 16, 20, 21]: # Motion, Shake, TapFreq, Heat, Rhythm
                if inputs[i] > 0.5:
                    self.w1[i][2] = min(6.0, self.w1[i][2] + self.learning_rate)
                    
        # If the system is PLAYFUL, strengthen the positive connections.
        elif max_idx == 2: # PLAYFUL
            for i in [16, 19]: # TapFreq, Bond
                if inputs[i] > 0.5:
                    self.w1[i][1] = min(6.0, self.w1[i][1] + self.learning_rate)
            
        moods = ["NORMAL", "SLEEPY", "PLAYFUL", "CRISIS"]
        return moods[max_idx]

class Arbiter:
    def __init__(self):
        self.net = NeuralNet()

    def get_mood(self, sensor_data):
        return self.net.process(sensor_data)
        
    def get_activity(self):
        return self.net.activity