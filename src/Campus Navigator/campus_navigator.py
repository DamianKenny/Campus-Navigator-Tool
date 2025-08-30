#!/usr/bin/env python3
"""
Campus Navigator - Mobile UI (Simplified Version)
Clean, stable mobile interface for campus navigation without custom graphics
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp, sp
from kivy.clock import Clock

# Import backend functionality
from campus_navigator_backend import CampusNavigator

class StyledButton(Button):
    """Simple styled button without custom graphics"""
    def __init__(self, bg_color=[0.2, 0.6, 0.9, 1], **kwargs):
        super().__init__(**kwargs)
        self.background_color = bg_color
        self.font_size = sp(14)

class StyledTextInput(TextInput):
    """Simple styled text input"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = [0.15, 0.15, 0.22, 1]
        self.foreground_color = [1, 1, 1, 1]
        self.cursor_color = [0.3, 0.7, 1, 1]

class MainScreen(Screen):
    """Main screen with simplified, stable design"""
    def __init__(self, **kwargs):
        super().__init__(name='main', **kwargs)
        self.navigator = CampusNavigator()
        Clock.schedule_once(self.setup_ui, 0.1)
        
    def setup_ui(self, dt):
        """Setup the main user interface"""
        # Main scroll container
        main_scroll = ScrollView(
            do_scroll_x=False,
            bar_width=dp(4)
        )
        
        # Main container
        main_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=[dp(20), dp(30), dp(20), dp(20)],
            size_hint_y=None
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # Header section
        header_section = self.create_header()
        main_layout.add_widget(header_section)
        
        # Quick navigation section
        nav_section = self.create_navigation_section()
        main_layout.add_widget(nav_section)
        
        # Features grid
        features_grid = self.create_features_grid()
        main_layout.add_widget(features_grid)
        
        main_scroll.add_widget(main_layout)
        self.add_widget(main_scroll)
    
    def create_header(self):
        """Create header section"""
        header_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(80),
            spacing=dp(5)
        )
        
        # Main title
        title = Label(
            text='Campus Navigator',
            font_size=sp(24),
            size_hint_y=None,
            height=dp(35),
            color=[1, 1, 1, 1],
            bold=True,
            halign='center'
        )
        
        # Subtitle
        subtitle = Label(
            text='Find your way around NIBM campus',
            font_size=sp(14),
            size_hint_y=None,
            height=dp(20),
            color=[0.8, 0.8, 0.8, 1],
            halign='center'
        )
        
        # Status
        status = Label(
            text='● System Online',
            font_size=sp(12),
            size_hint_y=None,
            height=dp(20),
            color=[0.3, 0.9, 0.4, 1],
            halign='center'
        )
        
        header_layout.add_widget(title)
        header_layout.add_widget(subtitle)
        header_layout.add_widget(status)
        
        return header_layout
    
    def create_navigation_section(self):
        """Create the main navigation section"""
        nav_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(180),
            spacing=dp(15)
        )
        
        # Section title
        nav_title = Label(
            text='🧭 Quick Navigation',
            font_size=sp(18),
            size_hint_y=None,
            height=dp(30),
            color=[1, 1, 1, 1],
            bold=True,
            halign='center'
        )
        
        # Input fields
        inputs_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(100)
        )
        
        self.start_input = StyledTextInput(
            hint_text='Enter start location',
            multiline=False,
            size_hint_y=None,
            height=dp(40)
        )
        
        self.dest_input = StyledTextInput(
            hint_text='Enter destination',
            multiline=False,
            size_hint_y=None,
            height=dp(40)
        )
        
        inputs_layout.add_widget(self.start_input)
        inputs_layout.add_widget(self.dest_input)
        
        # Find path button
        find_btn = StyledButton(
            text='Find Shortest Path',
            size_hint_y=None,
            height=dp(45),
            bg_color=[0.2, 0.7, 0.9, 1]
        )
        find_btn.bind(on_press=self.find_shortest_path)
        
        nav_layout.add_widget(nav_title)
        nav_layout.add_widget(inputs_layout)
        nav_layout.add_widget(find_btn)
        
        return nav_layout
    
    def create_features_grid(self):
        """Create the features grid"""
        features_container = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=None
        )
        features_container.bind(minimum_height=features_container.setter('height'))
        
        # Section title
        section_title = Label(
            text='Navigation Tools',
            font_size=sp(18),
            size_hint_y=None,
            height=dp(30),
            color=[1, 1, 1, 1],
            bold=True,
            halign='center'
        )
        
        # Features grid
        grid = GridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=None,
            row_default_height=dp(60)
        )
        grid.bind(minimum_height=grid.setter('height'))
        
        # Feature buttons
        features = [
            ("📍 Locations", [0.9, 0.5, 0.2, 1], self.list_locations),
            ("🔍 Search", [0.2, 0.7, 0.9, 1], self.search_location),
            ("🌐 BFS Path", [0.5, 0.8, 0.3, 1], self.bfs_traversal),
            ("🌲 DFS Path", [0.8, 0.3, 0.5, 1], self.dfs_traversal),
            ("🌟 Min Tree", [0.9, 0.7, 0.2, 1], self.show_mst),
            ("📝 Sort List", [0.6, 0.3, 0.9, 1], self.show_sorted)
        ]
        
        for title, color, callback in features:
            btn = StyledButton(
                text=title,
                bg_color=color,
                font_size=sp(12)
            )
            btn.bind(on_press=callback)
            grid.add_widget(btn)
        
        features_container.add_widget(section_title)
        features_container.add_widget(grid)
        
        return features_container
    
    def find_shortest_path(self, instance):
        """Find and display shortest path"""
        start = self.start_input.text.strip()
        dest = self.dest_input.text.strip()
        
        if not start or not dest:
            self.show_popup("Input Required", "Please enter both start and destination locations.")
            return
        
        try:
            success, result, distance = self.navigator.find_shortest_path(start, dest)
            
            if success:
                self.show_popup("Route Found", result)
            else:
                self.show_popup("No Route", result)
        except Exception as e:
            self.show_popup("Error", f"An error occurred: {str(e)}")
    
    def list_locations(self, instance):
        """Display all locations"""
        try:
            locations = self.navigator.get_locations()
            content = '\n'.join(f"• {loc}" for loc in locations)
            self.show_popup("Campus Locations", content)
        except Exception as e:
            self.show_popup("Error", f"Could not load locations: {str(e)}")
    
    def search_location(self, instance):
        """Search for location"""
        self.show_input_popup("Search Location", "Enter location name:", self._do_search)
    
    def _do_search(self, location):
        """Perform location search"""
        try:
            found = self.navigator.search_location(location)
            result = f"Location '{location}' {'found' if found else 'not found'}"
            self.show_popup("Search Result", result)
        except Exception as e:
            self.show_popup("Error", f"Search failed: {str(e)}")
    
    def bfs_traversal(self, instance):
        """BFS traversal"""
        self.show_input_popup("BFS Traversal", "Enter start location:", self._do_bfs)
    
    def _do_bfs(self, start):
        """Execute BFS"""
        try:
            success, result = self.navigator.bfs_traversal(start)
            self.show_popup("BFS Traversal", result)
        except Exception as e:
            self.show_popup("Error", f"BFS failed: {str(e)}")
    
    def dfs_traversal(self, instance):
        """DFS traversal"""
        self.show_input_popup("DFS Traversal", "Enter start location:", self._do_dfs)
    
    def _do_dfs(self, start):
        """Execute DFS"""
        try:
            success, result = self.navigator.dfs_traversal(start)
            self.show_popup("DFS Traversal", result)
        except Exception as e:
            self.show_popup("Error", f"DFS failed: {str(e)}")
    
    def show_mst(self, instance):
        """Show minimum spanning tree"""
        try:
            success, result = self.navigator.get_minimum_spanning_tree()
            self.show_popup("Minimum Spanning Tree", result)
        except Exception as e:
            self.show_popup("Error", f"MST calculation failed: {str(e)}")
    
    def show_sorted(self, instance):
        """Show sorted locations"""
        try:
            locations = self.navigator.get_sorted_locations()
            content = '\n'.join(f"• {loc}" for loc in locations)
            self.show_popup("Sorted Locations", content)
        except Exception as e:
            self.show_popup("Error", f"Could not sort locations: {str(e)}")
    
    def show_popup(self, title, content):
        """Show simple popup"""
        popup_content = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(15)
        )
        
        # Content with scroll
        scroll_view = ScrollView()
        
        content_label = Label(
            text=content,
            font_size=sp(13),
            color=[1, 1, 1, 1],
            halign='left',
            valign='top',
            size_hint_y=None,
            text_size=(None, None)
        )
        
        # Update text size based on popup width
        def update_text_size(instance, value):
            content_label.text_size = (value - dp(60), None)
            content_label.height = content_label.texture_size[1] + dp(10)
        
        scroll_view.add_widget(content_label)
        
        # Close button
        close_btn = Button(
            text='Close',
            size_hint_y=None,
            height=dp(40),
            background_color=[0.3, 0.3, 0.3, 1]
        )
        
        popup_content.add_widget(scroll_view)
        popup_content.add_widget(close_btn)
        
        # Create popup
        popup = Popup(
            title=title,
            content=popup_content,
            size_hint=(0.85, 0.7)
        )
        
        # Bind events
        popup.bind(width=update_text_size)
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_input_popup(self, title, message, callback):
        """Show input popup"""
        popup_content = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(15)
        )
        
        # Message
        msg_label = Label(
            text=message,
            font_size=sp(14),
            size_hint_y=None,
            height=dp(30),
            color=[1, 1, 1, 1]
        )
        
        # Text input
        text_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=dp(40),
            font_size=sp(14)
        )
        
        # Buttons
        btn_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        cancel_btn = Button(
            text='Cancel',
            background_color=[0.5, 0.5, 0.5, 1]
        )
        
        ok_btn = Button(
            text='OK',
            background_color=[0.2, 0.7, 0.9, 1]
        )
        
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(ok_btn)
        
        popup_content.add_widget(msg_label)
        popup_content.add_widget(text_input)
        popup_content.add_widget(btn_layout)
        
        # Create popup
        popup = Popup(
            title=title,
            content=popup_content,
            size_hint=(0.8, 0.35)
        )
        
        def on_ok(instance):
            if text_input.text.strip():
                callback(text_input.text.strip())
            popup.dismiss()
        
        ok_btn.bind(on_press=on_ok)
        cancel_btn.bind(on_press=popup.dismiss)
        popup.open()

class CampusNavigatorApp(App):
    """Campus Navigator App - Simplified Version"""
    def build(self):
        # Set window properties
        from kivy.core.window import Window
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        
        # Create screen manager
        sm = ScreenManager()
        sm.add_widget(MainScreen())
        
        return sm

if __name__ == '__main__':
    CampusNavigatorApp().run()