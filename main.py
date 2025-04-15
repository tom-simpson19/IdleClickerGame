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
            {'name': 'Overtime', "Description": "More work more results right?", 'cost': 200, 'rps': 20, 'owned': 0},
            {'name': 'Accommodation', "Description": "No better place to sleep than work", 'cost': 200, 'rps': 20, 'owned': 0},
            {'name': 'Fuel inflation', "Description": "If you can't afford to go home, may as well work right?", 'cost': 200, 'rps': 20, 'owned': 0},
            {'name': 'Energy drinks', "Description": "CAFFFIIINEEEE", 'cost': 200, 'rps': 20, 'owned': 0}
        ]

        self.layout = BoxLayout(orientation='vertical')
        self.grid_layout = GridLayout(cols=5, padding=10, spacing=10, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))

        # Header
        self.grid_layout.add_widget(Label(text="Upgrade Name", color=(1, 1, 1, 1)))
        self.grid_layout.add_widget(Label(text="Description", color=(1, 1, 1, 1)))
        self.grid_layout.add_widget(Label(text="Cost", color=(1, 1, 1, 1)))
        self.grid_layout.add_widget(Label(text="RPS", color=(1, 1, 1, 1)))
        self.grid_layout.add_widget(Label(text="Buy", color=(1, 1, 1, 1)))

        self.buy_buttons = []

        for upgrade in self.upgrades:
            self.grid_layout.add_widget(Label(text=upgrade['name'], color=(1, 1, 1, 1)))
            self.grid_layout.add_widget(Label(text=upgrade['Description'], color=(1, 1, 1, 1)))
            self.grid_layout.add_widget(Label(text=str(upgrade['cost']), color=(1, 1, 1, 1)))
            self.grid_layout.add_widget(Label(text=f"+{upgrade['rps']}", color=(1, 1, 1, 1)))

            btn = Button(
                text=f"Buy {upgrade['name']} (Owned: {upgrade['owned']})",
                size_hint=(None, None), size=(200, 50)
            )
            btn.bind(on_press=lambda b, u=upgrade: self.buy_upgrade(u))
            self.buy_buttons.append(btn)
            self.grid_layout.add_widget(btn)

        self.layout.add_widget(self.grid_layout)
        self.add_widget(self.layout)

    def buy_upgrade(self, upgrade):
        tap_screen = self.manager.get_screen('tap_screen')
        if tap_screen.resources >= upgrade['cost']:
            tap_screen.resources -= upgrade['cost']
            tap_screen.resources_per_second += upgrade['rps']
            upgrade['owned'] += 1
            self.update_buttons()

    def update_buttons(self):
        for i, upgrade in enumerate(self.upgrades):
            self.buy_buttons[i].text = f"Buy {upgrade['name']} (Owned: {upgrade['owned']})"


class BuyUpgradesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.buy_label = Label(text="Buy Upgrades Screen", color=(1, 1, 1, 1))
        layout.add_widget(self.buy_label)
        self.add_widget(layout)


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
