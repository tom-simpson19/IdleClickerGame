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
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
kivy.require('1.11.1')

THEME_BG = (0.1, 0.1, 0.1, 1)
TEXT_COLOR = (1, 1, 1, 1)
ACCENT_COLOR = (1, 0.5, 0, 1)


class TapToEarnScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        self.resources = 0
        self.income = 1
        self.resources_per_second = 0

        self.resource_label = Label(text=f'Resources: {self.resources}', font_size=24, color=TEXT_COLOR,
                                     size_hint=(None, None), size=(300, 50), pos_hint={'center_x': 0.5, 'top': 0.9})
        layout.add_widget(self.resource_label)

        self.rps_label = Label(text=f'RPS: {self.resources_per_second}', font_size=20, color=TEXT_COLOR,
                               size_hint=(None, None), size=(300, 50), pos_hint={'center_x': 0.5, 'top': 0.85})
        layout.add_widget(self.rps_label)

        # Factory image as a button (use your own image file)
        self.icon_button = Button(
            size_hint=(None, None), size=(200, 200),
            background_normal='Factory.png',
            background_down='Factory.png',
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
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

        # Main layout (BoxLayout) that centers everything vertically and horizontally
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20, size_hint=(None, None), size=(800, 600))
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Center layout

        # Title of the screen
        layout.add_widget(Label(text="Upgrades", font_size=32, color=ACCENT_COLOR, size_hint_y=None, height=50))

        # Creating a BoxLayout for the table-like structure
        grid_layout = GridLayout(cols=5, padding=10, spacing=10, row_default_height=50, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))  # Make gridLayout height flexible

        # Create the header row
        grid_layout.add_widget(Label(text="Upgrade Name", color=(1, 1, 1, 1), size_hint_y=None, height=40))
        grid_layout.add_widget(Label(text="Description", color=(1, 1, 1, 1), size_hint_y=None, height=40))
        grid_layout.add_widget(Label(text="Cost", color=(1, 1, 1, 1), size_hint_y=None, height=40))
        grid_layout.add_widget(Label(text="RPS", color=(1, 1, 1, 1), size_hint_y=None, height=40))
        grid_layout.add_widget(Label(text="Buy", color=(1, 1, 1, 1), size_hint_y=None, height=40))

        # Add upgrade rows
        for upgrade in self.upgrades:
            # Upgrade Name
            name_label = Label(
                text=f"[b]{upgrade['name']}[/b]",
                markup=True,
                font_size=18,
                color=(1, 1, 1, 1),
                halign='left',
                valign='middle'  # Center vertically
            )
            name_label.bind(size=name_label.setter('text_size'))  # Ensure text wrapping works
            grid_layout.add_widget(name_label)

            # Description
            desc_label = Label(
                text=upgrade['Description'],
                font_size=14,
                color=(0.9, 0.9, 0.9, 1),
                halign='left',
                valign='middle'  # Center vertically
            )
            desc_label.bind(size=desc_label.setter('text_size'))  # Ensure text wrapping works
            grid_layout.add_widget(desc_label)

            # Cost
            cost_label = Label(
                text=str(upgrade['cost']),
                font_size=14,
                color=(1, 1, 1, 1),
                halign='center',
                valign='middle'
            )
            grid_layout.add_widget(cost_label)

            # RPS
            rps_label = Label(
                text=f"+{upgrade['rps']}",
                font_size=14,
                color=(1, 1, 1, 1),
                halign='center',
                valign='middle'
            )
            grid_layout.add_widget(rps_label)

            # Buy Button
            buy_button = Button(
                text=f"Buy {upgrade['name']}",
                size_hint=(None, None),
                size=(150, 50),
                pos_hint={'center_x': 0.5}  # Center button horizontally
            )
            buy_button.bind(on_press=lambda btn, u=upgrade: self.buy_upgrade(u))
            grid_layout.add_widget(buy_button)

        # Add the grid layout to the main layout
        layout.add_widget(grid_layout)
        self.add_widget(layout)

    def buy_upgrade(self, upgrade):
        tap_screen = self.manager.get_screen('tap_screen')  # Get the TapToEarnScreen
        if tap_screen.resources >= upgrade['cost']:
            tap_screen.resources -= upgrade['cost']  # Deduct resources
            tap_screen.resources_per_second += upgrade['rps']  # Increase RPS
            self.update_upgrade_labels()

    def update_upgrade_labels(self):
        # No update needed here for this example; upgrades are updated immediately
        pass  # For this example, no update is required after purchase


class BuyUpgradesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Title centered at the top
        layout.add_widget(Label(text="💰 Microtransactions", font_size=28, color=ACCENT_COLOR,
                               size_hint=(None, None), size=(300, 50), pos_hint={'center_x': 0.5, 'top': 0.9}))

        microtransactions = [
            {"name": "Golden Wrench", "desc": "Double RPS for 5 minutes", "effect": self.double_rps},
            {"name": "Speed Boost", "desc": "Auto tap for 30s", "effect": self.auto_tap},
            {"name": "Instant Resources", "desc": "Gain 1000 resources instantly", "effect": self.give_resources},
            {"name": "Support Dev", "desc": "Show some love (no real effect)", "effect": self.fake_thanks}
        ]

        # Loop through the microtransactions and create each row
        for idx, item in enumerate(microtransactions):
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10,
                            size_hint=(None, None), size=(500, 50), pos_hint={'center_x': 0.5, 'top': 0.75 - (idx * 0.1)})

            row.add_widget(Label(text=f"{item['name']}: {item['desc']}", font_size=14, color=TEXT_COLOR,
                                 size_hint=(0.7, 1)))
            btn = Button(text="Buy", size_hint=(None, None), size=(100, 50), background_color=ACCENT_COLOR)
            btn.bind(on_press=lambda _, eff=item["effect"]: eff())
            row.add_widget(btn)

            layout.add_widget(row)

        self.add_widget(layout)

    def double_rps(self):
        tap_screen = self.manager.get_screen('tap_screen')
        tap_screen.resources_per_second *= 2
        print("🔥 RPS Doubled!")

    def auto_tap(self):
        print("Auto tap active for 30s")
        Clock.schedule_interval(self.tap_once, 1)
        Clock.schedule_once(self.stop_auto_tap, 30)

    def tap_once(self, dt):
        tap_screen = self.manager.get_screen('tap_screen')
        tap_screen.resources += tap_screen.income
        tap_screen.update_labels()

    def stop_auto_tap(self, dt):
        Clock.unschedule(self.tap_once)
        print("Auto tap ended")

    def give_resources(self):
        tap_screen = self.manager.get_screen('tap_screen')
        tap_screen.resources += 1000
        tap_screen.update_labels()
        print("+1000 Resources")

    def fake_thanks(self):
        print("❤️ Thanks for supporting the dev!")


class IdleClickerApp(App):
    def build(self):
        self.title = "Idle Factory Clicker"
        screen_manager = ScreenManager()

        screen_manager.add_widget(TapToEarnScreen(name='tap_screen'))
        screen_manager.add_widget(UpgradeScreen(name='upgrade_screen'))
        screen_manager.add_widget(BuyUpgradesScreen(name='buy_upgrade_screen'))

        tabs = TabbedPanel(do_default_tab=False, size_hint=(1, None), height=50)

        for label, screen in [
            ('Tap to Earn', 'tap_screen'),
            ('Upgrades', 'upgrade_screen'),
            ('Buy Upgrade', 'buy_upgrade_screen')
        ]:
            tab = TabbedPanelItem(text=label, size_hint=(None, 1), width=150)
            tab.bind(on_release=lambda x, s=screen: self.switch_screen(screen_manager, s))
            tabs.add_widget(tab)

        root = BoxLayout(orientation='vertical')
        root.add_widget(tabs)
        root.add_widget(screen_manager)
        return root

    def switch_screen(self, manager, name):
        manager.current = name


if __name__ == '__main__':
    IdleClickerApp().run()
