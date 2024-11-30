"""
examples/select_one_item.py

This module provides an example application using KivyMD to showcase drag-and-drop 
list functionality. Users can select an item from the list to view its associated 
content.
"""

from typing import Dict, List

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
        "item_id": "item_1",
        "headline_text": "Item 1",
        "supporting_text": "Lorem ipsum dolor...",
    },
    {
        "item_id": "item_2",
        "headline_text": "Item 2",
        "supporting_text": "Sed do eiusmod...",
    },
    {
        "item_id": "item_3",
        "headline_text": "Item 3",
        "supporting_text": "Ut enim ad minim veniam...",
    },
    {
        "item_id": "item_4",
        "headline_text": "Item 4",
        "supporting_text": "Duis aute irure dolor in reprehenderit...",
    },
    {
        "item_id": "item_5",
        "headline_text": "Item 5",
        "supporting_text": "Excepteur sint occaecat cupidatat non proident...",
    },
    {
        "item_id": "item_6",
        "headline_text": "Item 6",
        "supporting_text": "Amet minim mollit...",
    },
    {
        "item_id": "item_7",
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
        MDBoxLayout:
            orientation: "vertical"
            spacing: "12dp"

            ScrollableDragNDropListContainer:
                id: items_list_container

            MDBoxLayout:
                orientation: "horizontal"
                spacing: "12dp"
                size_hint_y: None
                height: "48dp"

                MDButton:
                    pos_hint: {"center_x": 0.5}
                    on_release: root.add_item()
                    MDButtonIcon: 
                        icon: "plus"
                    MDButtonText:
                        text: "Add Item"

                MDButton:
                    pos_hint: {"center_x": 0.5}
                    on_release: root.clear_items()
                    MDButtonIcon:
                        icon: "delete"
                    MDButtonText:
                        text: "Clear Items"


        MDCard:
            style: "outlined"
            padding: "12dp"

            MDLabel:
                id: content_label
                text: "Related Content"
                halign: "center"
"""

Builder.load_string(KV)

from kivy.clock import Clock

class AppRoot(MDScreen):
    items_list_container = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Bind events to get notified when the items list is updated or an item is selected
        self.items_list_container.bind(items_data=self.on_items_list_updated)
        self.items_list_container.bind(selected_item_data=self.on_item_selected)

        self.items_list_container.items_data = ITEMS_DATA
        self.items_list_container.selected_item_data = ITEMS_DATA[0]

        Clock.schedule_once(self._set_item_test_content, 5.0)

    def _set_item_test_content(self, *args):
        self.items_list_container.update_selected_item_data({
            "headline_text": "SELECTED ITEM CHANGED",
            "supporting_text": "This item was selected and itscontent has been changed.",
        })

    def on_items_list_updated(self, instance, items_data):
        """Handles changes to the items list."""

    def on_item_selected(self, instance, selected_item_data):
        if selected_item_data is None:
            self.ids.content_label.text = ""
            return

        item_id = selected_item_data.get("item_id", "")
        self.ids.content_label.text = ITEM_CONTENTS.get(item_id, "")

    def add_item(self):
        new_item_data = {
            "item_id": f"item_{len(self.items_list_container.items_data) + 1}",
            "headline_text": f"Item {len(self.items_list_container.items_data) + 1}",
            "supporting_text": "New item description...",
        }
        self.items_list_container.items_data.append(new_item_data)
        self.items_list_container.selected_item_data = new_item_data

    def clear_items(self):
        self.items_list_container.items_data = []
        self.items_list_container.selected_item_data = None


class SelectOneApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

    def build(self):
        return AppRoot()


if __name__ == "__main__":
    SelectOneApp().run()
