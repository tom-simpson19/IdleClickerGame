import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle

kivy.require('1.11.1')

THEME_BG = (0.1, 0.1, 0.1, 1)
TEXT_COLOR = (1, 1, 1, 1)
ACCENT_COLOR = (1, 0.5, 0, 1)
GRAY_BORDER = (0.3, 0.3, 0.3, 1)

class TapToEarnScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.resources = 0
        self.income = 1
        self.resources_per_second = 0

        self.resource_label = Label(text=f'Resources: {self.resources}', font_size=24, color=TEXT_COLOR)
        layout.add_widget(self.resource_label)

        self.rps_label = Label(text=f'RPS: {self.resources_per_second}', font_size=20, color=TEXT_COLOR)
        layout.add_widget(self.rps_label)

        self.icon_button = Button(
            size_hint=(None, None), size=(200, 200),
            background_normal='Factory.png',
            background_down='Factory.png',
            pos_hint={'center_x': 0.5}
        )
        self.icon_button.bind(on_press=self.on_click)
        layout.add_widget(self.icon_button)

        self.add_widget(layout)
        Clock.schedule_interval(self.auto_generate_resources, 1)

    def on_click(self, instance):
        self.resources += self.income
        self.update_labels()

    def auto_generate_resources(self, dt):
        self.resources += self.resources_per_second
        self.update_labels()

    def update_labels(self):
        self.resource_label.text = f'Resources: {self.resources}'
        self.rps_label.text = f'RPS: {self.resources_per_second}'


class UpgradeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.upgrades = [
            {'name': 'Oil', "Description" : "Well oiled machines just work better", 'cost': 10, 'rps': 1},
            {'name': 'Workers', "Description" : "Hire more workers",'cost': 50, 'rps': 5},
            {'name': 'Machinery', "Description" : "Buy more machinery",'cost': 200, 'rps': 20},
            {'name': 'Overtime', "Description" : "More work more results right?",'cost': 200, 'rps': 20},
            {'name': 'Accomodation', "Description" : "No better place to sleep than work",'cost': 200, 'rps': 20},
            {'name': 'Fuel inflation', "Description" : "If you can't afford to go home may as well work right?",'cost': 200, 'rps': 20},
            {'name': 'Energy drinks', "Description" : "CAFFFIIINEEEE",'cost': 200, 'rps': 20}
        ]

        self.layout = GridLayout(cols=5, padding=20, spacing=10, row_default_height=50)

        self.layout.add_widget(Label(text="Upgrade Name", color=TEXT_COLOR))
        self.layout.add_widget(Label(text="Description", color=TEXT_COLOR))
        self.layout.add_widget(Label(text="Cost", color=TEXT_COLOR))
        self.layout.add_widget(Label(text="RPS", color=TEXT_COLOR))
        self.layout.add_widget(Label(text="Buy", color=TEXT_COLOR))

        for upgrade in self.upgrades:
            self.layout.add_widget(Label(text=f"[b]{upgrade['name']}[/b]", markup=True, font_size=18, color=TEXT_COLOR))
            self.layout.add_widget(Label(text=upgrade['Description'], font_size=14, color=TEXT_COLOR))
            self.layout.add_widget(Label(text=str(upgrade['cost']), font_size=14, color=TEXT_COLOR))
            self.layout.add_widget(Label(text=f"+{upgrade['rps']}", font_size=14, color=TEXT_COLOR))

            buy_button = Button(text=f"Buy {upgrade['name']}", size_hint=(None, None), size=(150, 50))
            buy_button.bind(on_press=lambda btn, u=upgrade: self.buy_upgrade(u))
            self.layout.add_widget(buy_button)

        self.add_widget(self.layout)

    def buy_upgrade(self, upgrade):
        tap_screen = self.manager.get_screen('tap_screen')
        if tap_screen.resources >= upgrade['cost']:
            tap_screen.resources -= upgrade['cost']
            tap_screen.resources_per_second += upgrade['rps']
            tap_screen.update_labels()


class BuyUpgradesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        layout.add_widget(Label(text="\U0001F4B0 Microtransactions", font_size=28, color=ACCENT_COLOR))

        microtransactions = [
            {"name": "Golden Wrench", "desc": "Double RPS for 5 minutes", "effect": self.double_rps},
            {"name": "Speed Boost", "desc": "Auto tap for 30s", "effect": self.auto_tap},
            {"name": "Instant Resources", "desc": "Gain 1000 resources instantly", "effect": self.give_resources},
            {"name": "Support Dev", "desc": "Show some love (no real effect)", "effect": self.fake_thanks}
        ]

        for item in microtransactions:
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
            row.add_widget(Label(text=f"{item['name']}: {item['desc']}", font_size=14, color=TEXT_COLOR))
            btn = Button(text="Buy", size_hint=(None, 1), width=100, background_color=ACCENT_COLOR)
            btn.bind(on_press=lambda _, eff=item["effect"]: eff())
            row.add_widget(btn)
            layout.add_widget(row)

        self.add_widget(layout)

    def double_rps(self):
        tap_screen = self.manager.get_screen('tap_screen')
        tap_screen.resources_per_second *= 2

    def auto_tap(self):
        Clock.schedule_interval(self.tap_once, 1)
        Clock.schedule_once(self.stop_auto_tap, 30)

    def tap_once(self, dt):
        tap_screen = self.manager.get_screen('tap_screen')
        tap_screen.resources += tap_screen.income
        tap_screen.update_labels()

    def stop_auto_tap(self, dt):
        Clock.unschedule(self.tap_once)

    def give_resources(self):
        tap_screen = self.manager.get_screen('tap_screen')
        tap_screen.resources += 1000
        tap_screen.update_labels()

    def fake_thanks(self):
        print("Thanks for supporting the dev!")


class IdleClickerApp(App):
    def build(self):
        self.title = "Idle Factory Clicker"
        screen_manager = ScreenManager()

        screen_manager.add_widget(TapToEarnScreen(name='tap_screen'))
        screen_manager.add_widget(UpgradeScreen(name='upgrade_screen'))
        screen_manager.add_widget(BuyUpgradesScreen(name='buy_upgrade_screen'))

        tabs = BoxLayout(size_hint=(1, None), height=50)
        for label, screen in [
            ('Tap to Earn', 'tap_screen'),
            ('Upgrades', 'upgrade_screen'),
            ('Buy Upgrade', 'buy_upgrade_screen')
        ]:
            button = Button(text=label, size_hint=(None, 1), width=150, background_color=ACCENT_COLOR)
            button.bind(on_release=lambda btn, s=screen: self.switch_screen(screen_manager, s))
            tabs.add_widget(button)

        bordered_container = FloatLayout()

        with bordered_container.canvas.before:
            Color(*GRAY_BORDER)
            self.outer_border = RoundedRectangle(radius=[40])
            Color(*THEME_BG)
            self.inner_background = RoundedRectangle(radius=[40])

        def update_rects(instance, value):
            padding = 20
            size = (instance.width - padding * 2, instance.height - padding * 2)
            pos = (instance.x + padding, instance.y + padding)
            self.outer_border.size = (instance.width, instance.height)
            self.outer_border.pos = instance.pos
            self.inner_background.size = size
            self.inner_background.pos = pos

        bordered_container.bind(size=update_rects, pos=update_rects)
        bordered_container.add_widget(screen_manager)

        root = BoxLayout(orientation='vertical')
        root.add_widget(tabs)
        root.add_widget(bordered_container)
        return root

    def switch_screen(self, manager, name):
        manager.current = name


if __name__ == '__main__':
    IdleClickerApp().run()