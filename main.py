import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
kivy.require('1.11.1')

THEME_BG = (0.1, 0.1, 0.1, 1)
TEXT_COLOR = (1, 1, 1, 1)
ACCENT_COLOR = (1, 0.5, 0, 1)
GRAY_BORDER = (0.3, 0.3, 0.3, 1)  # Gray color for the border

class BorderScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            # Fill entire background with gray
            Color(*GRAY_BORDER)
            self.bg = RoundedRectangle(radius=[0])

            # Draw black "screen" area with rounded corners inset from the edges
            Color(0, 0, 0, 1)
            self.inner = RoundedRectangle(radius=[50])

        self.bind(size=self.update_border, pos=self.update_border)

    def update_border(self, *args):
        # Full screen gray background
        self.bg.pos = self.pos
        self.bg.size = self.size

        # Inset black screen to simulate a rounded "container"
        padding = 20
        self.inner.pos = (self.x + padding, self.y + padding)
        self.inner.size = (self.width - 2 * padding, self.height - 2 * padding)





class TapToEarnScreen(BorderScreen):
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

        # Factory image as a button (use your own image file)
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


class UpgradeScreen(BorderScreen):
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

        # Creating a GridLayout for table-like structure
        self.layout = GridLayout(cols=5, padding=10, spacing=10, row_default_height=50)

        # Create the header row
        self.layout.add_widget(Label(text="Upgrade Name", color=(1, 1, 1, 1), size_hint_y=None, height=40))
        self.layout.add_widget(Label(text="Description", color=(1, 1, 1, 1), size_hint_y=None, height=40))
        self.layout.add_widget(Label(text="Cost", color=(1, 1, 1, 1), size_hint_y=None, height=40))
        self.layout.add_widget(Label(text="RPS", color=(1, 1, 1, 1), size_hint_y=None, height=40))
        self.layout.add_widget(Label(text="Buy", color=(1, 1, 1, 1), size_hint_y=None, height=40))

        for upgrade in self.upgrades:
            # Add each upgrade's details in the grid
            name_label = Label(
                text=f"[b]{upgrade['name']}[/b]",
                markup=True,
                font_size=18,
                color=(1, 1, 1, 1),
                halign='left',
                valign='top'  # Top alignment to prevent space above text
            )
            name_label.bind(size=name_label.setter('text_size'))  # Bind text_size to size
            self.layout.add_widget(name_label)

            desc_label = Label(
                text=upgrade['Description'],
                font_size=14,
                color=(0.9, 0.9, 0.9, 1),
                halign='left',
                valign='top'  # Top alignment to prevent space above text
            )
            desc_label.bind(size=desc_label.setter('text_size'))  # Bind text_size to size
            self.layout.add_widget(desc_label)

            cost_label = Label(
                text=str(upgrade['cost']),
                font_size=14,
                color=(1, 1, 1, 1),
                halign='center',
                valign='middle'
            )
            self.layout.add_widget(cost_label)

            rps_label = Label(
                text=f"+{upgrade['rps']}",
                font_size=14,
                color=(1, 1, 1, 1),
                halign='center',
                valign='middle'
            )
            self.layout.add_widget(rps_label)

            # Create the buy button with fixed height
            buy_button = Button(text=f"Buy {upgrade['name']}", size_hint=(None, None), size=(150, 50))
            buy_button.bind(on_press=lambda btn, u=upgrade: self.buy_upgrade(u))

            # Centering button vertically
            buy_button.valign = 'middle'  # Ensures that the button is vertically centered
            self.layout.add_widget(buy_button)  # Add the buy button for each upgrade

        self.add_widget(self.layout)

    def buy_upgrade(self, upgrade):
        tap_screen = self.manager.get_screen('tap_screen')  # Get the TapToEarnScreen
        if tap_screen.resources >= upgrade['cost']:
            tap_screen.resources -= upgrade['cost']  # Deduct resources
            tap_screen.resources_per_second += upgrade['rps']  # Increase RPS
            self.update_upgrade_labels()

    def update_upgrade_labels(self):
        # No need for this method in this case because the upgrades are updated immediately
        pass  # For this example, no update is required after purchase


class BuyUpgradesScreen(BorderScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        layout.add_widget(Label(text="💰 Microtransactions", font_size=28, color=ACCENT_COLOR))

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

        # Remove the TabbedPanel and direct buttons to change screens
        tabs = BoxLayout(size_hint=(1, None), height=50)

        for label, screen in [
            ('Tap to Earn', 'tap_screen'),
            ('Upgrades', 'upgrade_screen'),
            ('Buy Upgrade', 'buy_upgrade_screen')
        ]:
            button = Button(text=label, size_hint=(None, 1), width=150, background_color=ACCENT_COLOR)
            button.bind(on_release=lambda btn, s=screen: self.switch_screen(screen_manager, s))
            tabs.add_widget(button)

        root = BoxLayout(orientation='vertical')
        root.add_widget(tabs)
        root.add_widget(screen_manager)
        return root

    def switch_screen(self, manager, name):
        manager.current = name


if __name__ == '__main__':
    IdleClickerApp().run()

