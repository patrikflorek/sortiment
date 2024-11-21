from typing import Optional, Dict, Any

from kivy.lang import Builder
from kivy.properties import DictProperty, ListProperty

from kivymd.app import MDApp
from kivymd.uix.relativelayout import MDRelativeLayout

from sortiment.item import DragNDropListItem


KV = """
<ScrollableDragNDropListContainer>:
    scroll_view: scroll_view
    items_list: items_list
    
    ScrollView:
        id: scroll_view

        MDList:
            id: items_list
"""

Builder.load_string(KV)


class ScrollableDragNDropListContainer(MDRelativeLayout):
    """A scrollable container that supports drag-and-drop functionality for list items."""

    items_data = ListProperty([])
    selected_item_data = DictProperty(None)

    def on_items_data(self, instance, items_data):
        """Handles changes to the items data."""
        self.items_list.clear_widgets()
        for item_data in items_data:
            self._add_list_item(item_data)
        self.on_selected_item_data(self, self.selected_item_data)

    def _add_list_item(self, item_data: Dict[str, Any]) -> None:
        """Creates and adds a new list item."""
        item_widget = DragNDropListItem(item_data=item_data)
        item_widget.bind(selected=self.on_item_selected_callback)
        self.items_list.add_widget(item_widget)

    def on_selected_item_data(self, instance, selected_item_data):
        """Handles changes to the selected item data."""
        for item in self.items_list.children:
            item.selected = item.item_data == selected_item_data
            if item.selected and item.y < 0:
                self.scroll_view.scroll_to(item)

    # -------------------------------------------------------------------------
    # Deprecated - Do not use! This will be removed in the next major release.
    @property
    def selected_item_idx(self) -> Optional[DragNDropListItem]:
        """Returns the index of the currently selected item."""
        for idx, item in enumerate(self.items_list.children[::-1]):
            if item.selected:
                return idx

    @selected_item_idx.setter
    def selected_item_idx(self, item_idx: int) -> None:
        """
        Selects the item at the given index.

        Args:
            item_idx: Index of the item to select.
        """
        list_child_idx = len(self.items_list.children) - item_idx - 1
        self.items_list.children[list_child_idx].selected = True

    # -------------------------------------------------------------------------

    def on_item_selected_callback(
        self, item: DragNDropListItem, selected: bool
    ) -> None:
        """Handles item selection events."""
        if not selected:
            return

        self.selected_item_data = item.item_data

        # -------------------------------------------------------------------------
        # Deprecated - Do not use! This will be removed in the next major release.
        # Notify the app about the selected item.
        app = MDApp.get_running_app()
        if hasattr(app, "on_item_selected"):
            app.on_item_selected(self.selected_item_idx)
        # -------------------------------------------------------------------------

    def on_touch_move(self, touch) -> bool:
        """Handles touch move events for drag-and-drop functionality."""
        dragged_item = touch.ud.get("dragged_item")
        if dragged_item is None:
            return super().on_touch_move(touch)

        if dragged_item in self.items_list.children:
            self._start_drag(touch, dragged_item)

        return super().on_touch_move(touch)

    def _start_drag(self, touch, dragged_item):
        """Initializes the drag operation for the given item."""
        dragged_item_start_pos = dragged_item.to_window(*dragged_item.pos)
        touch.ud["dragged_item_idx"] = self.items_list.children.index(dragged_item)
        self.items_list.remove_widget(dragged_item)
        self.add_widget(dragged_item)
        dragged_item.pos = self.to_widget(*dragged_item_start_pos)

    def on_touch_up(self, touch):
        """Handles touch up events to finalize the drag-and-drop operations."""
        dragged_item = touch.ud.get("dragged_item")
        if not dragged_item:
            return super().on_touch_up(touch)

        self._finish_drag(touch, dragged_item)
        return super().on_touch_up(touch)

    def _finish_drag(self, touch, dragged_item):
        """Finalizes the drag operation by placing the dragged item in its new position."""
        dragged_item_idx = touch.ud.get("dragged_item_idx")
        if dragged_item_idx is None:
            # The drag did not start yet.
            return

        self.remove_widget(dragged_item)
        new_idx = self._get_dragged_item_new_idx(touch, fallback_idx=dragged_item_idx)
        self.items_list.add_widget(dragged_item, new_idx)
        self.items_data = [item.item_data for item in self.items_list.children[::-1]]

    def _get_dragged_item_new_idx(self, touch, fallback_idx=0):
        """Determines the new index for the dragged item based on touch position."""
        if not self.collide_point(*touch.pos):
            return fallback_idx

        for idx, item in enumerate(self.items_list.children):
            touch_pos_in_item = item.to_widget(*touch.pos)
            if item.collide_point(*touch_pos_in_item):
                return (
                    idx if touch_pos_in_item[1] < item.y + item.height / 2 else idx + 1
                )

        return fallback_idx

    def insert_item(self, item_data: Dict[str, Any], index=None) -> None:
        """Adds a new item to the list."""
        if index is None:
            self.items_data.append(item_data)
        else:
            self.items_data.insert(index, item_data)

        self.selected_item_data = item_data

    def remove_item(self, item_data: Dict[str, Any]) -> None:
        """Removes an item from the list."""
        self.items_data.remove(item_data)
