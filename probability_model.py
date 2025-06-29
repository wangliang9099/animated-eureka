import random

class ProbabilityModel:
    def __init__(self):
        pass

    def predict_win_rate(self, history):
        if not history:
            return {"banker": 0.505, "player": 0.475, "tie": 0.02}
        return {"banker": random.uniform(0.48, 0.52), "player": random.uniform(0.46, 0.5), "tie": 1 - random.uniform(0.95, 0.98)}