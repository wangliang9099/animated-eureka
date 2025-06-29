import math

class StrategyEngine:
    def __init__(self, base_bet=10):
        self.base_bet = base_bet
        self.current_bet = base_bet
        self.strategy = "martingale"
        self.fib_seq = [1, 1]
        self.fib_index = 1
        self.lucas_seq = [2, 1]
        self.lucas_index = 1
        self.mc_seq = [1, 3, 5, 7]
        self.mc_index = 0

    def reset(self):
        self.current_bet = self.base_bet
        self.fib_index = 1
        self.lucas_index = 1
        self.mc_index = 0

    def set_strategy(self, name):
        self.strategy = name
        self.reset()

    def auto_select_strategy(self, predict_prob, loss_streak, win_streak, profit_curve):
        if predict_prob > 0.52 and win_streak >= 2:
            self.set_strategy("anti_martingale")
        elif loss_streak >= 3:
            self.set_strategy("fibonacci")
        elif predict_prob < 0.48 and profit_curve[-1] < 0:
            self.set_strategy("kelly")
        elif abs(predict_prob - 0.5) < 0.02:
            self.set_strategy("monte_carlo")
        else:
            self.set_strategy("martingale")

    def next_bet(self, last_win, predict_prob=0.5, bankroll=1000, profit_curve=[0]):
        if self.strategy == "martingale":
            return self.martingale(last_win)
        elif self.strategy == "anti_martingale":
            return self.anti_martingale(last_win)
        elif self.strategy == "fibonacci":
            return self.fibonacci(last_win)
        elif self.strategy == "lucas":
            return self.lucas(last_win)
        elif self.strategy == "kelly":
            return self.kelly(predict_prob, 1, bankroll)
        elif self.strategy == "monte_carlo":
            return self.monte_carlo(last_win)
        else:
            return self.base_bet

    def martingale(self, last_win):
        if last_win is None or last_win:
            self.current_bet = self.base_bet
        else:
            self.current_bet *= 2
        return self.current_bet

    def anti_martingale(self, last_win):
        if last_win is None or not last_win:
            self.current_bet = self.base_bet
        else:
            self.current_bet *= 2
        return self.current_bet

    def fibonacci(self, last_win):
        if last_win:
            self.fib_index = max(1, self.fib_index - 2)
        else:
            self.fib_index += 1
        while len(self.fib_seq) <= self.fib_index:
            self.fib_seq.append(self.fib_seq[-1] + self.fib_seq[-2])
        self.current_bet = self.fib_seq[self.fib_index] * self.base_bet
        return self.current_bet

    def lucas(self, last_win):
        if last_win:
            self.lucas_index = max(1, self.lucas_index - 2)
        else:
            self.lucas_index += 1
        while len(self.lucas_seq) <= self.lucas_index:
            self.lucas_seq.append(self.lucas_seq[-1] + self.lucas_seq[-2])
        self.current_bet = self.lucas_seq[self.lucas_index] * self.base_bet
        return self.current_bet

    def kelly(self, p, b, bankroll):
        f_star = (b * p - (1 - p)) / b
        f_star = max(0, min(f_star, 1))
        self.current_bet = int(f_star * bankroll)
        return max(self.base_bet, self.current_bet)

    def monte_carlo(self, last_win):
        if last_win:
            self.mc_index = max(0, self.mc_index - 2)
        else:
            self.mc_index += 1
        if self.mc_index >= len(self.mc_seq):
            self.mc_index = len(self.mc_seq) - 1
        return self.mc_seq[self.mc_index] * self.base_bet