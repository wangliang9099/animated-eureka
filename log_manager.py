class LogManager:
    def __init__(self):
        self.logs = []

    def add_log(self, round_num, bet, result, profit):
        self.logs.append({
            "round": round_num,
            "bet": bet,
            "result": result,
            "profit": profit
        })

    def get_logs(self, last_n=10):
        return self.logs[-last_n:]