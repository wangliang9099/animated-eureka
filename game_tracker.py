class GameTracker:
    def __init__(self):
        self.history = []
        self.profit_curve = [0]
        self.bankroll = 1000
        self.loss_streak = 0
        self.win_streak = 0

    def add_result(self, result, bet, win):
        self.history.append(result)
        delta = win - bet if result != "tie" else 0
        self.bankroll += delta
        self.profit_curve.append(self.bankroll)
        if win > 0:
            self.win_streak += 1
            self.loss_streak = 0
        else:
            self.loss_streak += 1
            self.win_streak = 0

    def get_stats(self):
        return {
            "history": self.history[-10:],
            "loss_streak": self.loss_streak,
            "win_streak": self.win_streak,
            "profit_curve": self.profit_curve[-10:],
            "bankroll": self.bankroll
        }