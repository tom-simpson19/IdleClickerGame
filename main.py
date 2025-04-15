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
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
kivy.require('1.11.1')

THEME_BG = (0.1, 0.1, 0.1, 1)
TEXT_COLOR = (1, 1, 1, 1)
ACCENT_COLOR = (0.3, 0.7, 0.9, 1)
GRAY_BORDER = (0.2, 0.2, 0.2, 1)

class TapToEarnScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.resources = 0
        self.income = 1
        self.resources_per_second = 0
        self.play_time = 0  # Initialize play_time
        self.upgrades_bought = 0  # Initialize upgrades_bought
        self.resources_spent_on_upgrades = 0  # Initialize resources_spent_on_upgrades
        self.upgrades_maxed_out = False  # Initialize upgrades_maxed_out
        self.unlocked_achievements = []  # Initialize the unlocked achievements list
        self.automation_time = 0  # Initialize automation_time (important fix)

        self.resource_label = Label(text=f'Resources: {self.resources}', font_size=28, color=TEXT_COLOR)
        layout.add_widget(self.resource_label)

        self.rps_label = Label(text=f'RPS: {self.resources_per_second}', font_size=24, color=TEXT_COLOR)
        layout.add_widget(self.rps_label)

        self.icon_button = Button(size_hint=(None, None), size=(200, 200),
                                  background_normal='Factory.png', background_down='Factory.png',
                                  pos_hint={'center_x': 0.5}, color=ACCENT_COLOR)
        self.icon_button.bind(on_press=self.on_click)
        layout.add_widget(self.icon_button)

        self.add_widget(layout)
        Clock.schedule_interval(self.auto_generate_resources, 1)

        # Add a clock to increment play_time and automation_time every second
        Clock.schedule_interval(self.update_play_time, 1)
        Clock.schedule_interval(self.update_automation_time, 1)  # This will update automation_time every second

        # Achievements Data (200 Achievements)
        self.achievements = [
            # Resource Milestones
            {'name': 'First Tap', 'description': 'Tap the button for the first time', 'completed': False, 'criteria': lambda: self.resources > 0},
            {'name': 'Rookie', 'description': 'Reach 100 resources', 'completed': False, 'criteria': lambda: self.resources >= 100},
            {'name': 'Millionaire', 'description': 'Reach 1,000 resources', 'completed': False, 'criteria': lambda: self.resources >= 1000},
            {'name': 'Income Boost', 'description': 'Reach 5 RPS', 'completed': False, 'criteria': lambda: self.resources_per_second >= 5},
            {'name': 'Automation Master', 'description': 'Reach 100 RPS', 'completed': False, 'criteria': lambda: self.resources_per_second >= 100},
            {'name': 'Super Clicker', 'description': 'Tap the button 50 times', 'completed': False, 'criteria': lambda: self.resources >= 50},
            {'name': 'Wealthy Tycoon', 'description': 'Reach 10,000 resources', 'completed': False, 'criteria': lambda: self.resources >= 10000},
            {'name': 'Giga Tycoon', 'description': 'Reach 100,000 resources', 'completed': False, 'criteria': lambda: self.resources >= 100000},
            {'name': 'Billionaire', 'description': 'Reach 1,000,000 resources', 'completed': False, 'criteria': lambda: self.resources >= 1000000},
            {'name': 'Trillionaire', 'description': 'Reach 1,000,000,000 resources', 'completed': False, 'criteria': lambda: self.resources >= 1000000000},
            # Time Milestones
            {'name': 'First Minute', 'description': 'Play the game for 1 minute', 'completed': False, 'criteria': lambda: self.play_time >= 60},
            {'name': 'First Hour', 'description': 'Play the game for 1 hour', 'completed': False, 'criteria': lambda: self.play_time >= 3600},
            {'name': 'Overnight Tycoon', 'description': 'Play the game for 12 hours', 'completed': False, 'criteria': lambda: self.play_time >= 43200},
            {'name': 'Long-Term Player', 'description': 'Play the game for 24 hours', 'completed': False, 'criteria': lambda: self.play_time >= 86400},
            {'name': 'Hardcore Gamer', 'description': 'Play for 100 hours', 'completed': False, 'criteria': lambda: self.play_time >= 360000},
            {'name': 'Endurance', 'description': 'Play the game for 500 hours', 'completed': False, 'criteria': lambda: self.play_time >= 1800000},
            {'name': 'Binge Player', 'description': 'Play the game for 1,000 hours', 'completed': False, 'criteria': lambda: self.play_time >= 3600000},
            # Clicks Milestones
            {'name': 'Tap Addict', 'description': 'Tap the button 10 times', 'completed': False, 'criteria': lambda: self.resources >= 10},
            {'name': 'Tap Mania', 'description': 'Tap the button 50 times', 'completed': False, 'criteria': lambda: self.resources >= 50},
            {'name': 'Tap King', 'description': 'Tap the button 100 times', 'completed': False, 'criteria': lambda: self.resources >= 100},
            {'name': 'Clicker Extraordinaire', 'description': 'Tap the button 200 times', 'completed': False, 'criteria': lambda: self.resources >= 200},
            {'name': 'Tap Champion', 'description': 'Tap the button 500 times', 'completed': False, 'criteria': lambda: self.resources >= 500},
            {'name': 'Tap Master', 'description': 'Tap the button 1,000 times', 'completed': False, 'criteria': lambda: self.resources >= 1000},
            {'name': 'Clicking Machine', 'description': 'Tap the button 5,000 times', 'completed': False, 'criteria': lambda: self.resources >= 5000},
            {'name': 'Tapper of the Year', 'description': 'Tap the button 10,000 times', 'completed': False, 'criteria': lambda: self.resources >= 10000},
            # RPS Milestones
            {'name': 'Steady Income', 'description': 'Reach 1 RPS', 'completed': False, 'criteria': lambda: self.resources_per_second >= 1},
            {'name': 'RPS Boost', 'description': 'Reach 10 RPS', 'completed': False, 'criteria': lambda: self.resources_per_second >= 10},
            {'name': 'RPS Pro', 'description': 'Reach 50 RPS', 'completed': False, 'criteria': lambda: self.resources_per_second >= 50},
            {'name': 'Automation Boss', 'description': 'Reach 100 RPS', 'completed': False, 'criteria': lambda: self.resources_per_second >= 100},
            {'name': 'RPS Overload', 'description': 'Reach 500 RPS', 'completed': False, 'criteria': lambda: self.resources_per_second >= 500},
            {'name': 'Giga RPS', 'description': 'Reach 1,000 RPS', 'completed': False, 'criteria': lambda: self.resources_per_second >= 1000},
            {'name': 'Supercharge', 'description': 'Reach 5,000 RPS', 'completed': False, 'criteria': lambda: self.resources_per_second >= 5000},
            {'name': 'Automation Overlord', 'description': 'Reach 10,000 RPS', 'completed': False, 'criteria': lambda: self.resources_per_second >= 10000},
            # Upgrade Milestones
            {'name': 'Upgrade Junkie', 'description': 'Buy 5 upgrades', 'completed': False, 'criteria': lambda: self.upgrades_bought >= 5},
            {'name': 'Upgrade Enthusiast', 'description': 'Buy 10 upgrades', 'completed': False, 'criteria': lambda: self.upgrades_bought >= 10},
            {'name': 'Upgrade Investor', 'description': 'Buy 50 upgrades', 'completed': False, 'criteria': lambda: self.upgrades_bought >= 50},
            {'name': 'Upgrade Master', 'description': 'Buy 100 upgrades', 'completed': False, 'criteria': lambda: self.upgrades_bought >= 100},
            {'name': 'Upgrade King', 'description': 'Buy 500 upgrades', 'completed': False, 'criteria': lambda: self.upgrades_bought >= 500},
            {'name': 'First Mega Upgrade', 'description': 'Buy your first mega upgrade', 'completed': False, 'criteria': lambda: self.upgrades_bought >= 1},
            {'name': 'Super Upgrader', 'description': 'Spend 1,000 resources on upgrades', 'completed': False, 'criteria': lambda: self.resources_spent_on_upgrades >= 1000},
            {'name': 'Upgrade God', 'description': 'Spend 10,000 resources on upgrades', 'completed': False, 'criteria': lambda: self.resources_spent_on_upgrades >= 10000},
            {'name': 'Resource Overhaul', 'description': 'Max out an upgrade', 'completed': False, 'criteria': lambda: self.upgrades_maxed_out >= 1},
            # Achievement Unlocked
            {'name': 'Achievement Hunter', 'description': 'Unlock 10 achievements', 'completed': False, 'criteria': lambda: len(self.unlocked_achievements) >= 10},
            {'name': 'Master of Achievements', 'description': 'Unlock 50 achievements', 'completed': False, 'criteria': lambda: len(self.unlocked_achievements) >= 50},
            {'name': 'Achievement Expert', 'description': 'Unlock 100 achievements', 'completed': False, 'criteria': lambda: len(self.unlocked_achievements) >= 100},
            {'name': 'Achievement Conqueror', 'description': 'Unlock 200 achievements', 'completed': False, 'criteria': lambda: len(self.unlocked_achievements) >= 200},
            {'name': 'Ultimate Achievement', 'description': 'Unlock every single achievement', 'completed': False, 'criteria': lambda: len(self.unlocked_achievements) == 200},
            # Time-based Achievements
            {'name': 'First Automation', 'description': 'Automate resource generation for 1 minute', 'completed': False, 'criteria': lambda: self.automation_time >= 60},
            {'name': '10-Minute Automation', 'description': 'Automate resource generation for 10 minutes', 'completed': False, 'criteria': lambda: self.automation_time >= 600},
            {'name': '30-Minute Automation', 'description': 'Automate resource generation for 30 minutes', 'completed': False, 'criteria': lambda: self.automation_time >= 1800},
            {'name': '1-Hour Automation', 'description': 'Automate resource generation for 1 hour', 'completed': False, 'criteria': lambda: self.automation_time >= 3600},
            {'name': '2-Hour Automation', 'description': 'Automate resource generation for 2 hours', 'completed': False, 'criteria': lambda: self.automation_time >= 7200},
            {'name': '4-Hour Automation', 'description': 'Automate resource generation for 4 hours', 'completed': False, 'criteria': lambda: self.automation_time >= 14400},
            {'name': '8-Hour Automation', 'description': 'Automate resource generation for 8 hours', 'completed': False, 'criteria': lambda: self.automation_time >= 28800},
            {'name': '12-Hour Automation', 'description': 'Automate resource generation for 12 hours', 'completed': False, 'criteria': lambda: self.automation_time >= 43200},
            {'name': '24-Hour Automation', 'description': 'Automate resource generation for 24 hours', 'completed': False, 'criteria': lambda: self.automation_time >= 86400}
        ]

    def update_play_time(self, dt):
        self.play_time += 1  # Increment play_time by 1 every second

    def update_automation_time(self, dt):
        self.automation_time += 1  # Increment automation_time by 1 every second

    def on_click(self, instance):
        self.resources += self.income
        self.update_labels()

        # Apply animation only once when the button is clicked.
        if not hasattr(instance, 'is_animating') or not instance.is_animating:
            instance.is_animating = True  # Mark that the button is animating
            
            # Ensure the button does not affect the layout or cause movement
            with instance.canvas.before:
                # Fix the position and make sure the button doesn't shift the layout
                instance.original_pos = instance.pos
                instance.original_size = instance.size

            anim = Animation(size=(instance.width * 1.2, instance.height * 1.2), duration=0.2) + \
                Animation(size=(instance.original_size[0], instance.original_size[1]), duration=0.2)
            anim.start(instance)

            # Once animation is done, reset the animation flag
            anim.bind(on_complete=lambda *args: setattr(instance, 'is_animating', False))

    def auto_generate_resources(self, dt):
        self.resources += self.resources_per_second
        self.update_labels()

    def update_labels(self):
        self.resource_label.text = f'Resources: {self.resources}'
        self.rps_label.text = f'RPS: {self.resources_per_second}'
        self.check_achievements()

    def check_achievements(self):
        for achievement in self.achievements:
            if not achievement['completed'] and achievement['criteria']():
                achievement['completed'] = True
                if achievement['name'] not in self.unlocked_achievements:
                    self.unlocked_achievements.append(achievement['name'])  # Track unlocked achievements
                    self.show_achievement_popup(achievement)

    def show_achievement_popup(self, achievement):
        popup = Popup(title='Achievement Unlocked',
                      content=Label(text=f"Congratulations! You unlocked: {achievement['name']}\n\n{achievement['description']}"),
                      size_hint=(0.8, 0.4))
        popup.open()
class UpgradeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.upgrades = [
    {'name': 'Oil', "Description": "Well oiled machines just work better", 'cost': 10, 'rps': 1},
    {'name': 'Workers', "Description": "Hire more workers", 'cost': 50, 'rps': 5},
    {'name': 'Machinery', "Description": "Buy more machinery", 'cost': 200, 'rps': 20},
    {'name': 'Overtime', "Description": "More work more results right?", 'cost': 400, 'rps': 35},
    {'name': 'Accommodation', "Description": "No better place to sleep than work", 'cost': 800, 'rps': 50},
    {'name': 'Fuel Inflation', "Description": "If you can't afford to go home, may as well work", 'cost': 1600, 'rps': 70},
    {'name': 'Energy Drinks', "Description": "CAFFFIIINEEEE", 'cost': 2500, 'rps': 100},
    {'name': 'Motivational Posters', "Description": "‘Hang in there!’ does wonders", 'cost': 3200, 'rps': 120},
    {'name': 'AI Surveillance', "Description": "Smile! You're being productive", 'cost': 4200, 'rps': 140},
    {'name': 'Forced Team Building', "Description": "Bond or be fired", 'cost': 5400, 'rps': 160},
    {'name': 'Productivity Charts', "Description": "Guilt graphs", 'cost': 6800, 'rps': 180},
    {'name': 'Broken Vending Machines', "Description": "Frustration fuels output", 'cost': 8400, 'rps': 210},
    {'name': 'Invisible Bonuses', "Description": "They're totally coming next quarter", 'cost': 10000, 'rps': 240},
    {'name': 'Intern Army', "Description": "Cheap, eager, and expendable", 'cost': 12000, 'rps': 280},
    {'name': 'Management Retreats', "Description": "They get rest. You get deadlines", 'cost': 14500, 'rps': 320},
    {'name': 'Mandatory Smiles', "Description": "Frown and you're gone", 'cost': 17500, 'rps': 360},
    {'name': 'Ergonomic Hazards', "Description": "Pain builds character", 'cost': 21000, 'rps': 400},
    {'name': 'Offshore Automation', "Description": "Work never sleeps", 'cost': 25000, 'rps': 450},
    {'name': 'Broken Clocks', "Description": "No end in sight", 'cost': 30000, 'rps': 500},
    {'name': 'Micromanagers', "Description": "Hovering increases efficiency", 'cost': 36000, 'rps': 560},
    {'name': 'Heat Lamps', "Description": "Keep the pressure high (literally)", 'cost': 43000, 'rps': 620},
    {'name': 'Hope Reduction Plan', "Description": "Less hope, more grind", 'cost': 50000, 'rps': 680},
    {'name': 'Unpaid Breaks', "Description": "Rest is for the weak", 'cost': 58000, 'rps': 750},
    {'name': 'Industrial Coffee', "Description": "Jet fuel for humans", 'cost': 67000, 'rps': 820},
    {'name': 'Paperwork Avalanche', "Description": "Buried in bureaucracy", 'cost': 77000, 'rps': 900},
    {'name': 'Middle Management', "Description": "A layer of confusion", 'cost': 88000, 'rps': 980},
    {'name': 'Wall Clocks Removed', "Description": "Time is an illusion", 'cost': 100000, 'rps': 1060},
    {'name': 'Cubicle Compression', "Description": "More bodies per square meter", 'cost': 113000, 'rps': 1150},
    {'name': 'Broken Air Conditioning', "Description": "Sweat faster, produce faster", 'cost': 127000, 'rps': 1240},
    {'name': 'Overtime Denial', "Description": "More hours, same pay", 'cost': 143000, 'rps': 1340},
    {'name': 'Closed Windows', "Description": "Trapped like profits", 'cost': 160000, 'rps': 1440},
    {'name': 'Motivational Whistles', "Description": "One tweet = one task", 'cost': 180000, 'rps': 1550},
    {'name': 'Digital Distractions Blocker', "Description": "No memes, no mercy", 'cost': 200000, 'rps': 1660},
    {'name': 'Overseer Drone', "Description": "Always watching", 'cost': 225000, 'rps': 1780},
    {'name': 'Silent Alarm System', "Description": "For unproductive thoughts", 'cost': 250000, 'rps': 1900},
    {'name': 'Mandatory Chanting', "Description": "Unity breeds output", 'cost': 280000, 'rps': 2030},
    {'name': 'Noise-Canceling Walls', "Description": "No complaints escape", 'cost': 310000, 'rps': 2160},
    {'name': 'Vitamin IV Drips', "Description": "Sleep is obsolete", 'cost': 345000, 'rps': 2300},
    {'name': '24-Hour Shifts', "Description": "Time is money, sleep is theft", 'cost': 380000, 'rps': 2440},
    {'name': 'Biometric Check-ins', "Description": "Track every second", 'cost': 420000, 'rps': 2590},
    {'name': 'Fire-the-bottom-10%', "Description": "Motivation by fear", 'cost': 460000, 'rps': 2740},
    {'name': 'Optimized Pathways', "Description": "No time wasted walking", 'cost': 505000, 'rps': 2900},
    {'name': 'Task Implants', "Description": "Work... hardwired", 'cost': 550000, 'rps': 3060},
    {'name': 'Loyalty Scoring', "Description": "Work more, rank higher", 'cost': 600000, 'rps': 3230},
    {'name': 'Workplace Anthem', "Description": "Sing before you clock in", 'cost': 655000, 'rps': 3400},
    {'name': 'Drone Delivery Lines', "Description": "Zero downtime", 'cost': 710000, 'rps': 3580},
    {'name': 'Factory Religion', "Description": "Worship the grind", 'cost': 775000, 'rps': 3760},
    {'name': 'Nano Efficiency Protocol', "Description": "Micromanagement perfected", 'cost': 840000, 'rps': 3950}
]

        # Outer layout
        root_layout = BoxLayout(orientation='vertical')

        # Scrollable area
        scroll = ScrollView(size_hint=(1, 1))
        self.layout = GridLayout(cols=5, padding=20, spacing=10, row_default_height=50, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))  # Dynamic height based on content

        # Headers
        self.layout.add_widget(Label(text="Upgrade Name", color=TEXT_COLOR))
        self.layout.add_widget(Label(text="Description", color=TEXT_COLOR))
        self.layout.add_widget(Label(text="Cost", color=TEXT_COLOR))
        self.layout.add_widget(Label(text="RPS", color=TEXT_COLOR))
        self.layout.add_widget(Label(text="Buy", color=TEXT_COLOR))

        # Upgrade rows
        for upgrade in self.upgrades:
            self.layout.add_widget(Label(text=f"[b]{upgrade['name']}[/b]", markup=True, font_size=18, color=TEXT_COLOR))
            self.layout.add_widget(Label(text=upgrade['Description'], font_size=14, color=TEXT_COLOR))
            self.layout.add_widget(Label(text=str(upgrade['cost']), font_size=14, color=TEXT_COLOR))
            self.layout.add_widget(Label(text=f"+{upgrade['rps']}", font_size=14, color=TEXT_COLOR))

            buy_button = Button(text=f"Buy {upgrade['name']}", size_hint=(None, None), size=(150, 50), background_color=ACCENT_COLOR)
            buy_button.bind(on_press=lambda btn, u=upgrade: self.buy_upgrade(u, buy_button))
            upgrade['buy_button'] = buy_button
            self.layout.add_widget(buy_button)

        scroll.add_widget(self.layout)
        root_layout.add_widget(scroll)
        self.add_widget(root_layout)


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


from kivy.uix.scrollview import ScrollView

class AchievementsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="Achievements", font_size=28, color=TEXT_COLOR))

        # Create a ScrollView to hold the achievements
        self.scrollview = ScrollView(size_hint=(1, None), height=Window.height - 100)
        
        # Create a GridLayout to hold the achievements in a table-like structure
        self.achievements_grid = GridLayout(cols=3, size_hint_y=None, padding=10, spacing=15)  # Increased spacing here
        self.achievements_grid.bind(minimum_height=self.achievements_grid.setter('height'))

        # Add the achievements grid inside the scrollview
        self.scrollview.add_widget(self.achievements_grid)

        layout.add_widget(self.scrollview)
        self.add_widget(layout)

    def on_enter(self):
        # Ensure we clear any old widgets when switching to this screen
        self.achievements_grid.clear_widgets()

        # Get the 'tap_screen' to retrieve the achievements data
        tap_screen = self.manager.get_screen('tap_screen')

        # Add headers for the table (with some padding and spacing)
        self.achievements_grid.add_widget(Label(text="Achievement", font_size=18, color=TEXT_COLOR, bold=True, size_hint_y=None, height=50))
        self.achievements_grid.add_widget(Label(text="Status", font_size=18, color=TEXT_COLOR, bold=True, size_hint_y=None, height=50))
        self.achievements_grid.add_widget(Label(text="Description", font_size=18, color=TEXT_COLOR, bold=True, size_hint_y=None, height=50))

        # Add achievements to the grid with proper spacing and alignment
        for achievement in tap_screen.achievements:
            achievement_status = "Completed" if achievement['completed'] else "In Progress"
            
            self.achievements_grid.add_widget(Label(
                text=achievement['name'], font_size=16, color=TEXT_COLOR, size_hint_y=None, height=60))  # Increased row height
            self.achievements_grid.add_widget(Label(
                text=achievement_status, font_size=16, color=TEXT_COLOR, size_hint_y=None, height=60))  # Increased row height
            self.achievements_grid.add_widget(Label(
                text=achievement['description'], font_size=16, color=TEXT_COLOR, size_hint_y=None, height=60))  # Increased row height

class IdleClickerApp(App):
    def build(self):
        self.title = "Idle Factory Clicker"
        screen_manager = ScreenManager()

        screen_manager.add_widget(TapToEarnScreen(name='tap_screen'))
        screen_manager.add_widget(UpgradeScreen(name='upgrade_screen'))
        screen_manager.add_widget(BuyUpgradesScreen(name='buy_upgrade_screen'))
        screen_manager.add_widget(AchievementsScreen(name='achievements_screen'))

        tabs = BoxLayout(size_hint=(1, None), height=50)
        for label, screen in [
            ('Tap to Earn', 'tap_screen'),
            ('Upgrades', 'upgrade_screen'),
            ('Buy Upgrade', 'buy_upgrade_screen'),
            ('Achievements', 'achievements_screen')
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
