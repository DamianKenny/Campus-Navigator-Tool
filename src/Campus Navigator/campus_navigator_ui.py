#!/usr/bin/env python3
"""
Campus Navigator - Frontend Mobile UI
Dark theme Kivy mobile application for campus navigation
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
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.widget import Widget


from backend.campus_navigator_backend import CampusNavigator


class RoundedButton(Button):
   
    def __init__(self, bg_color=[0.2, 0.2, 0.2, 1], **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = bg_color
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        
    def update_graphics(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.background_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])

class GradientButton(Button):
    
    def __init__(self, gradient_colors=[[0.5, 0.3, 0.8, 1], [0.3, 0.6, 0.9, 1]], **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.gradient_colors = gradient_colors
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        
    def update_graphics(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.gradient_colors[0])
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])

class MainScreen(Screen):
   
    def __init__(self, **kwargs):
        super().__init__(name='main', **kwargs)
        
        
        self.navigator = CampusNavigator()
        
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
       
        header = Label(
            text='Campus Navigator',
            font_size=dp(24),
            size_hint_y=None,
            height=dp(60),
            color=[1, 1, 1, 1]
        )
        layout.add_widget(header)
        
        
        nav_card = self.create_quick_nav_card()
        layout.add_widget(nav_card)
        
        
        menu_grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None)
        menu_grid.bind(minimum_height=menu_grid.setter('height'))
        
        
        buttons_config = [
            ("📍 List Locations", self.list_locations, [0.9, 0.5, 0.2, 1]),
            ("🔍 Search Location", self.search_location, [0.2, 0.7, 0.9, 1]),
            ("🌐 BFS Traversal", self.bfs_traversal, [0.5, 0.8, 0.3, 1]),
            ("🌲 DFS Traversal", self.dfs_traversal, [0.8, 0.3, 0.5, 1]),
            ("🌟 Min Spanning Tree", self.show_mst, [0.9, 0.7, 0.2, 1]),
            ("📝 Sorted Locations", self.show_sorted, [0.3, 0.5, 0.8, 1])
        ]
        
        
        for text, callback, color in buttons_config:
            btn = GradientButton(
                text=text,
                size_hint_y=None,
                height=dp(70),
                font_size=dp(16),
                gradient_colors=[color, [c * 0.8 for c in color]]
            )
            btn.bind(on_press=callback)
            menu_grid.add_widget(btn)
        
        layout.add_widget(menu_grid)
        
        
        layout.add_widget(Widget(size_hint_y=None, height=dp(20)))
        
        self.add_widget(layout)
    
    def create_quick_nav_card(self):
      
        card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(200),
            padding=dp(15),
            spacing=dp(10)
        )
        
        
        with card.canvas.before:
            Color(0.2, 0.2, 0.3, 1)
            card.rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(15)])
        card.bind(pos=self.update_card_bg, size=self.update_card_bg)
        
        
        title = Label(
            text='Quick Navigation',
            font_size=dp(18),
            size_hint_y=None,
            height=dp(30),
            color=[1, 1, 1, 1]
        )
        card.add_widget(title)
        
       
        input_layout = BoxLayout(orientation='horizontal', spacing=dp(10))
        
        self.start_input = TextInput(
            hint_text='Start Location',
            multiline=False,
            size_hint_x=1,
            height=dp(40),
            background_color=[0.1, 0.1, 0.2, 1],
            foreground_color=[1, 1, 1, 1]
        )
        
        self.dest_input = TextInput(
            hint_text='Destination',
            multiline=False,
            size_hint_x=1,
            height=dp(40),
            background_color=[0.1, 0.1, 0.2, 1],
            foreground_color=[1, 1, 1, 1]
        )
        
        input_layout.add_widget(self.start_input)
        input_layout.add_widget(self.dest_input)
        card.add_widget(input_layout)
        
        
        find_btn = GradientButton(
            text='🚀 Find Shortest Path',
            size_hint_y=None,
            height=dp(50),
            font_size=dp(16),
            gradient_colors=[[0.6, 0.3, 0.9, 1], [0.3, 0.6, 0.9, 1]]
        )
        find_btn.bind(on_press=self.find_shortest_path)
        card.add_widget(find_btn)
        
        return card
    
    def update_card_bg(self, instance, value):
        
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
    
    def find_shortest_path(self, instance):
      
        start = self.start_input.text.strip()
        dest = self.dest_input.text.strip()
        
        if not start or not dest:
            self.show_popup("Error", "Please enter both start and destination locations.")
            return
        
        success, result, distance = self.navigator.find_shortest_path(start, dest)
        
        if success:
            self.show_popup("Shortest Path Found", result, large=True)
        else:
            self.show_popup("No Path", result)
    
    def list_locations(self, instance):
        
        locations = self.navigator.get_locations()
        content = '\n'.join(f"• {loc}" for loc in locations)
        self.show_popup("All Locations", content, large=True)
    
    def search_location(self, instance):
       
        self.show_input_popup("Search Location", "Enter location name:", self._do_search)
    
    def _do_search(self, location):
       
        found = self.navigator.search_location(location)
        result = "✅ Found!" if found else "❌ Not found."
        self.show_popup("Search Result", f"Location: {location}\n{result}")
    
    def bfs_traversal(self, instance):
       
        self.show_input_popup("BFS Traversal", "Enter start location:", self._do_bfs)
    
    def _do_bfs(self, start):
        
        success, result = self.navigator.bfs_traversal(start)
        if success:
            self.show_popup("BFS Traversal Result", result, large=True)
        else:
            self.show_popup("Error", result)
    
    def dfs_traversal(self, instance):
        
        self.show_input_popup("DFS Traversal", "Enter start location:", self._do_dfs)
    
    def _do_dfs(self, start):
        
        success, result = self.navigator.dfs_traversal(start)
        if success:
            self.show_popup("DFS Traversal Result", result, large=True)
        else:
            self.show_popup("Error", result)
    
    def show_mst(self, instance):
       
        success, result = self.navigator.get_minimum_spanning_tree()
        if success:
            self.show_popup("Minimum Spanning Tree", result, large=True)
        else:
            self.show_popup("Error", result)
    
    def show_sorted(self, instance):
        
        sorted_locations = self.navigator.get_sorted_locations()
        content = '\n'.join(f"• {loc}" for loc in sorted_locations)
        self.show_popup("Sorted Locations (BST)", content, large=True)
    
    def show_popup(self, title, content, large=False):
        
        popup_content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        
        scroll = ScrollView()
        label = Label(
            text=content,
            text_size=(None, None),
            halign='left',
            valign='top',
            color=[1, 1, 1, 1],
            font_size=dp(14),
            size_hint_y=None
        )
        
        def update_text_size(instance, value):
            instance.text_size = (value - dp(20), None)
            instance.height = instance.texture_size[1]
        
        label.bind(width=update_text_size)
        label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        scroll.add_widget(label)
        popup_content.add_widget(scroll)
        
        
        close_btn = RoundedButton(
            text='Close',
            size_hint_y=None,
            height=dp(50),
            bg_color=[0.5, 0.3, 0.8, 1]
        )
        popup_content.add_widget(close_btn)
        
        
        popup = Popup(
            title=title,
            content=popup_content,
            size_hint=(0.9, 0.8 if large else 0.6),
            background_color=[0.1, 0.1, 0.2, 1]
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_input_popup(self, title, message, callback):
      
        popup_content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        
        label = Label(
            text=message,
            size_hint_y=None,
            height=dp(40),
            color=[1, 1, 1, 1]
        )
        popup_content.add_widget(label)
        
        text_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=dp(40),
            background_color=[0.1, 0.1, 0.2, 1],
            foreground_color=[1, 1, 1, 1]
        )
        popup_content.add_widget(text_input)
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
        
        ok_btn = RoundedButton(text='OK', bg_color=[0.3, 0.7, 0.3, 1])
        cancel_btn = RoundedButton(text='Cancel', bg_color=[0.7, 0.3, 0.3, 1])
        
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(ok_btn)
        popup_content.add_widget(btn_layout)
        
        popup = Popup(
            title=title,
            content=popup_content,
            size_hint=(0.8, 0.4),
            background_color=[0.1, 0.1, 0.2, 1]
        )
        
        def on_ok(instance):
            if text_input.text.strip():
                callback(text_input.text.strip())
            popup.dismiss()
        
        ok_btn.bind(on_press=on_ok)
        cancel_btn.bind(on_press=popup.dismiss)
        popup.open()

class CampusNavigatorApp(App):
    
    def build(self):
        from kivy.core.window import Window
        Window.clearcolor = (0.05, 0.05, 0.1, 1)
        
        # main screen
        sm = ScreenManager()
        sm.add_widget(MainScreen())
        
        return sm

if __name__ == '__main__':
    CampusNavigatorApp().run()