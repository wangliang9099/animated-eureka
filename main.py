from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from strategy_engine import StrategyEngine
from probability_model import ProbabilityModel
from game_tracker import GameTracker

class HomeScreen(Screen):
    def on_enter(self):
        self.update_labels()

    def update_labels(self):
        stats = self.manager.tracker.get_stats()
        prob = self.manager.model.predict_win_rate(stats["history"])
        self.manager.engine.auto_select_strategy(
            predict_prob=prob["banker"],
            loss_streak=stats["loss_streak"],
            win_streak=stats["win_streak"],
            profit_curve=stats["profit_curve"]
        )
        bet = self.manager.engine.next_bet(
            last_win=(stats["profit_curve"][-1] > stats["profit_curve"][-2]),
            predict_prob=prob["banker"],
            bankroll=stats["bankroll"],
            profit_curve=stats["profit_curve"]
        )
        self.ids.prob_label.text = f"胜率预测 - 庄: {prob['banker']:.2%} 闲: {prob['player']:.2%} 和: {prob['tie']:.2%}"
        self.ids.strategy_label.text = f"当前策略：{self.manager.engine.strategy} | 建议下注：{bet}"

class BaccaratApp(App):
    def build(self):
        sm = ScreenManager()
        sm.engine = StrategyEngine()
        sm.model = ProbabilityModel()
        sm.tracker = GameTracker()
        sm.add_widget(HomeScreen(name='home'))
        return sm

if __name__ == '__main__':
    BaccaratApp().run()