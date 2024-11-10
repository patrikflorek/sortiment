"""
examples/select_one_item.py

This module provides an example application using KivyMD to showcase drag-and-drop 
list functionality. Users can select an item from the list to view its associated 
content.
"""

from typing import Dict, List

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


# Constants for window size
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 360

# Data for items
ITEMS_DATA: List[Dict[str, str]] = [
    {
        "id": "item_1",
        "headline_text": "Item 1",
        "supporting_text": "Lorem ipsum dolor...",
    },
    {
        "id": "item_2",
        "headline_text": "Item 2",
        "supporting_text": "Sed do eiusmod...",
    },
    {
        "id": "item_3",
        "headline_text": "Item 3",
        "supporting_text": "Ut enim ad minim veniam...",
    },
    {
        "id": "item_4",
        "headline_text": "Item 4",
        "supporting_text": "Duis aute irure dolor in reprehenderit...",
    },
    {
        "id": "item_5",
        "headline_text": "Item 5",
        "supporting_text": "Excepteur sint occaecat cupidatat non proident...",
    },
    {
        "id": "item_6",
        "headline_text": "Item 6",
        "supporting_text": "Amet minim mollit...",
    },
    {
        "id": "item_7",
        "headline_text": "Item 7",
        "supporting_text": "Nostrud exercitation ullamco laboris...",
    },
]


ITEM_CONTENTS: Dict[str, str] = {
    "item_1": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    "item_2": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    "item_3": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    "item_4": "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
    "item_5": "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    "item_6": "Amet minim mollit non deserunt ullamco est sit aliqua dolor do amet sint.",
    "item_7": "Nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
}

Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)

KV = """
#:import ScrollableDragNDropListContainer sortiment.ScrollableDragNDropListContainer

<AppRoot>:
    items_list_container: items_list_container

    MDGridLayout:
        cols: 2
        padding: "12dp"
        spacing: "12dp"

        ScrollableDragNDropListContainer:
            id: items_list_container

        MDCard:
            style: "outlined"
            padding: "12dp"

            MDLabel:
                id: content_label
                text: "Related Content"
                halign: "center"
"""

Builder.load_string(KV)


class AppRoot(MDScreen):
    items_list_container = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items_list_container.items_data = ITEMS_DATA

        Clock.schedule_once(self._late_init)  # Wait for the list to be initialized

    def _late_init(self, dt):
        self.items_list_container.selected_item_idx = 0

    def display_item_content(self, item_idx):
        item_data = ITEMS_DATA[item_idx]
        self.ids.content_label.text = ITEM_CONTENTS[item_data["id"]]


class SelectOneApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

    def build(self):
        return AppRoot()

    def on_item_selected(self, selected_item_idx):
        """Handles item selection events."""
        self.root.display_item_content(selected_item_idx)


if __name__ == "__main__":
    SelectOneApp().run()
