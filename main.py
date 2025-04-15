import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock  # To handle automatic resource generation

kivy.require('1.11.1')  # Ensure the correct Kivy version

class TapToEarnScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.resources = 0
        self.income = 1  # Base resource generation (from tapping)
        self.resources_per_second = 0  # Resources per second (from upgrades)

        layout = FloatLayout()

        # Label showing resources
        self.resource_label = Label(text=f'Resources: {self.resources}',
                                    size_hint=(None, None),
                                    size=(200, 50),
                                    pos_hint={'center_x': 0.5, 'top': 0.9},
                                    color=(1, 1, 1, 1))
        layout.add_widget(self.resource_label)

        # Label showing resources per second
        self.rps_label = Label(text=f'RPS: {self.resources_per_second}',
                               size_hint=(None, None),
                               size=(200, 50),
                               pos_hint={'center_x': 0.5, 'top': 0.85},
                               color=(1, 1, 1, 1))
        layout.add_widget(self.rps_label)

        # Button to earn resources (Tap to earn)
        self.icon_button = Button(size_hint=(None, None), size=(150, 150),
                                  background_normal='path_to_your_icon.png', 
                                  background_down='path_to_your_icon_pressed.png',
                                  pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.icon_button.bind(on_press=self.on_click)
        layout.add_widget(self.icon_button)

        self.add_widget(layout)

        # Start a clock that updates the resources per second
        Clock.schedule_interval(self.auto_generate_resources, 1)

    def on_click(self, instance):
        # When the player taps, they earn resources
        self.resources += self.income
        self.resource_label.text = f'Resources: {self.resources}'

    def auto_generate_resources(self, dt):
        # This function is called every second to auto-generate resources
        self.resources += self.resources_per_second
        self.resource_label.text = f'Resources: {self.resources}'
        self.rps_label.text = f'RPS: {self.resources_per_second}'


class UpgradeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.upgrades = [
            {'name': 'Upgrade 1', 'cost': 10, 'rps': 1},
            {'name': 'Upgrade 2', 'cost': 50, 'rps': 5},
            {'name': 'Upgrade 3', 'cost': 200, 'rps': 20}
        ]

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.upgrade_labels = []  # List to store label widgets

        for upgrade in self.upgrades:
            label = Label(text=f"{upgrade['name']} - Cost: {upgrade['cost']} Resources\n+{upgrade['rps']} RPS",
                          color=(1, 1, 1, 1))  # White text
            self.layout.add_widget(label)
            self.upgrade_labels.append(label)  # Add label to list
            buy_button = Button(text=f"Buy {upgrade['name']}", size_hint=(None, None), size=(200, 50))
            buy_button.bind(on_press=lambda btn, u=upgrade: self.buy_upgrade(u))
            self.layout.add_widget(buy_button)

        self.add_widget(self.layout)

    def buy_upgrade(self, upgrade):
        tap_screen = self.manager.get_screen('tap_screen')  # Get the TapToEarnScreen
        if tap_screen.resources >= upgrade['cost']:
            tap_screen.resources -= upgrade['cost']  # Deduct resources
            tap_screen.resources_per_second += upgrade['rps']  # Increase RPS
            self.update_upgrade_labels()

    def update_upgrade_labels(self):
        # Update the labels to reflect the current state of the upgrades
        for i, upgrade in enumerate(self.upgrades):
            # Now this list should contain all upgrade labels
            self.upgrade_labels[i].text = f"{upgrade['name']} - Cost: {upgrade['cost']} Resources\n+{upgrade['rps']} RPS"


class BuyUpgradesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Label or any content for this screen
        self.buy_label = Label(text="Buy Upgrades Screen", color=(1, 1, 1, 1))  # White text color
        layout.add_widget(self.buy_label)

        self.add_widget(layout)


class IdleClickerApp(App):
    def build(self):
        # Create the ScreenManager to manage switching between pages
        screen_manager = ScreenManager()

        # Add the three screens to the screen manager
        screen_manager.add_widget(TapToEarnScreen(name='tap_screen'))
        screen_manager.add_widget(UpgradeScreen(name='upgrade_screen'))
        screen_manager.add_widget(BuyUpgradesScreen(name='buy_upgrade_screen'))

        # Create the Tabbed Panel for navigation at the bottom
        tabs = TabbedPanel(do_default_tab=False, size_hint=(1, None), height=50)

        # Create a tab for each screen, and remove redundant labels
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
        layout.add_widget(tabs)            # Tabs at the top level
        layout.add_widget(screen_manager)  # ScreenManager remains at the bottom

        return layout

    def switch_screen(self, screen_manager, screen_name):
        # Switch to the appropriate screen in the ScreenManager
        screen_manager.current = screen_name


if __name__ == '__main__':
    IdleClickerApp().run()
