import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout

kivy.require('1.11.1')


class TapToEarnScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.resources = 0
        self.income = 1
        self.resources_per_second = 0

        layout = FloatLayout()

        self.resource_label = Label(text=f'Resources: {self.resources}',
                                    size_hint=(None, None),
                                    size=(200, 50),
                                    pos_hint={'center_x': 0.5, 'top': 0.9},
                                    color=(1, 1, 1, 1))
        layout.add_widget(self.resource_label)

        self.rps_label = Label(text=f'RPS: {self.resources_per_second}',
                               size_hint=(None, None),
                               size=(200, 50),
                               pos_hint={'center_x': 0.5, 'top': 0.85},
                               color=(1, 1, 1, 1))
        layout.add_widget(self.rps_label)

        self.icon_button = Button(size_hint=(None, None), size=(150, 150),
                                  background_normal='Factory.png',
                                  background_down='Factory.png',
                                  pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.icon_button.bind(on_press=self.on_click)
        layout.add_widget(self.icon_button)

        self.add_widget(layout)
        Clock.schedule_interval(self.auto_generate_resources, 1)

    def on_click(self, instance):
        self.resources += self.income
        self.resource_label.text = f'Resources: {self.resources}'

    def auto_generate_resources(self, dt):
        self.resources += self.resources_per_second
        self.resource_label.text = f'Resources: {self.resources}'
        self.rps_label.text = f'RPS: {self.resources_per_second}'


class UpgradeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.upgrades = [
            {'name': 'Oil', "Description": "Well oiled machines just work better", 'cost': 10, 'rps': 1, 'owned': 0},
            {'name': 'Workers', "Description": "Hire more workers", 'cost': 50, 'rps': 5, 'owned': 0},
            {'name': 'Machinery', "Description": "Buy more machinery", 'cost': 200, 'rps': 20, 'owned': 0},
            {'name': 'Overtime', "Description": "More work more results right?", 'cost': 300, 'rps': 25, 'owned': 0},
            {'name': 'Accommodation', "Description": "No better place to sleep than work", 'cost': 500, 'rps': 30, 'owned': 0},
            {'name': 'Fuel inflation', "Description": "If you can't afford to go home may as well work right?", 'cost': 800, 'rps': 40, 'owned': 0},
            {'name': 'Energy drinks', "Description": "CAFFFIIINEEEE", 'cost': 1000, 'rps': 50, 'owned': 0}
        ]

        self.layout = GridLayout(cols=5, padding=10, spacing=10, row_default_height=60, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        headers = ["Upgrade Name", "Description", "Cost", "RPS", "Buy"]
        for header in headers:
            self.layout.add_widget(Label(text=header, color=(1, 1, 1, 1)))

        self.buttons = []

        for upgrade in self.upgrades:
            self.layout.add_widget(Label(text=upgrade['name'], color=(1, 1, 1, 1)))
            self.layout.add_widget(Label(text=upgrade['Description'], color=(1, 1, 1, 1)))
            self.layout.add_widget(Label(text=str(upgrade['cost']), color=(1, 1, 1, 1)))
            self.layout.add_widget(Label(text=f"+{upgrade['rps']}", color=(1, 1, 1, 1)))

            buy_button = Button(text=f"Buy {upgrade['name']} (Owned: {upgrade['owned']})", size_hint=(None, None), size=(200, 50))
            buy_button.bind(on_press=lambda btn, u=upgrade, b=buy_button: self.buy_upgrade(u, b))
            self.buttons.append(buy_button)
            self.layout.add_widget(buy_button)

        root = BoxLayout(orientation='vertical')
        root.add_widget(self.layout)
        self.add_widget(root)

    def buy_upgrade(self, upgrade, button):
        tap_screen = self.manager.get_screen('tap_screen')
        if tap_screen.resources >= upgrade['cost']:
            tap_screen.resources -= upgrade['cost']
            tap_screen.resources_per_second += upgrade['rps']
            upgrade['owned'] += 1
            button.text = f"Buy {upgrade['name']} (Owned: {upgrade['owned']})"
            tap_screen.resource_label.text = f"Resources: {tap_screen.resources}"
            tap_screen.rps_label.text = f"RPS: {tap_screen.resources_per_second}"


class BuyUpgradesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="Microtransactions", font_size=24, color=(1, 1, 0.5, 1)))

        microtransactions = [
            {"name": "Golden Wrench", "desc": "Double RPS for 5 minutes", "effect": self.double_rps},
            {"name": "Speed Boost", "desc": "Auto tap once per second for 30s", "effect": self.auto_tap},
            {"name": "Instant Resources", "desc": "Gain 1000 resources instantly", "effect": self.give_resources},
            {"name": "Remove Ads", "desc": "There are no ads. But thanks anyway!", "effect": self.fake_thanks},
            {"name": "Support Dev", "desc": "Support the dev (does nothing)", "effect": self.fake_thanks}
        ]

        for item in microtransactions:
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
            row.add_widget(Label(text=f"{item['name']}: {item['desc']}", color=(1, 1, 1, 1)))
            buy_button = Button(text="Buy", size_hint=(None, 1), width=100)
            buy_button.bind(on_press=lambda b, effect=item["effect"]: effect())
            row.add_widget(buy_button)
            layout.add_widget(row)

        self.add_widget(layout)

    def double_rps(self):
        tap_screen = self.manager.get_screen('tap_screen')
        tap_screen.resources_per_second *= 2
        print("RPS Doubled!")

    def auto_tap(self):
        print("Auto tap for 30s started!")
        Clock.schedule_interval(self.tap_once, 1)
        Clock.schedule_once(self.stop_auto_tap, 30)

    def tap_once(self, dt):
        tap_screen = self.manager.get_screen('tap_screen')
        tap_screen.resources += tap_screen.income
        tap_screen.resource_label.text = f"Resources: {tap_screen.resources}"

    def stop_auto_tap(self, dt):
        Clock.unschedule(self.tap_once)
        print("Auto tap ended.")

    def give_resources(self):
        tap_screen = self.manager.get_screen('tap_screen')
        tap_screen.resources += 1000
        tap_screen.resource_label.text = f"Resources: {tap_screen.resources}"
        print("Given 1000 resources.")

    def fake_thanks(self):
        print("Thanks for your support! ❤️")


class IdleClickerApp(App):
    def build(self):
        screen_manager = ScreenManager()

        screen_manager.add_widget(TapToEarnScreen(name='tap_screen'))
        screen_manager.add_widget(UpgradeScreen(name='upgrade_screen'))
        screen_manager.add_widget(BuyUpgradesScreen(name='buy_upgrade_screen'))

        tabs = TabbedPanel(do_default_tab=False, size_hint=(1, None), height=50)

        tab1 = TabbedPanelItem(text='Tap to Earn', size_hint=(None, 1), width=150)
        tab1.bind(on_release=lambda x: self.switch_screen(screen_manager, 'tap_screen'))
        tabs.add_widget(tab1)

        tab2 = TabbedPanelItem(text='Upgrades', size_hint=(None, 1), width=150)
        tab2.bind(on_release=lambda x: self.switch_screen(screen_manager, 'upgrade_screen'))
        tabs.add_widget(tab2)

        tab3 = TabbedPanelItem(text='Buy Upgrade', size_hint=(None, 1), width=150)
        tab3.bind(on_release=lambda x: self.switch_screen(screen_manager, 'buy_upgrade_screen'))
        tabs.add_widget(tab3)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(tabs)
        layout.add_widget(screen_manager)

        return layout

    def switch_screen(self, screen_manager, screen_name):
        screen_manager.current = screen_name


if __name__ == '__main__':
    IdleClickerApp().run()
