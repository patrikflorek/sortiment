from typing import List, Optional, Dict, Any

from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.relativelayout import MDRelativeLayout

from sortiment.item import DragNDropListItem

KV = """
<ScrollableDragNDropListContainer>:
    
    ScrollView:
        id: scroll_view

        MDList:
            id: drag_n_drop_list
"""

Builder.load_string(KV)


class ScrollableDragNDropListContainer(MDRelativeLayout):
    """A scrollable container that supports drag and drop functionality for list items."""

    @property
    def items_data(self) -> List[Dict[str, Any]]:
        """Returns the data of all items in the list in their current order."""
        return [item.item_data for item in self.ids.drag_n_drop_list.children[::-1]]

    @items_data.setter
    def items_data(self, data: List[Dict[str, Any]]) -> None:
        """
        Sets the list items from the provided data.

        Args:
            data: List of dictionaries containing item data
        """
        self.ids.drag_n_drop_list.clear_widgets()
        for item_data in data:
            self._add_list_item(item_data)

    def _add_list_item(self, item_data: Dict[str, Any]) -> None:
        """Helper method to create and add a new list item."""
        item_widget = DragNDropListItem(item_data=item_data)
        item_widget.bind(selected=self.on_item_selected_callback)
        self.ids.drag_n_drop_list.add_widget(item_widget)

    @property
    def selected_item_idx(self) -> Optional[DragNDropListItem]:
        """Returns the index of the currently selected item."""
        for idx, item in enumerate(self.ids.drag_n_drop_list.children[::-1]):
            if item.selected:
                return idx

    @selected_item_idx.setter
    def selected_item_idx(self, item_idx: int) -> None:
        """
        Selects the item at the given index.

        Args:
            item_idx: Index of the item to select
        """
        list_child_idx = len(self.ids.drag_n_drop_list.children) - item_idx - 1
        self.ids.drag_n_drop_list.children[list_child_idx].selected = True

    def on_item_selected_callback(
        self, item: DragNDropListItem, selected: bool
    ) -> None:
        """Handles item selection events."""
        if not selected:
            return

        # Deselect other items
        for list_item in self.ids.drag_n_drop_list.children:
            if item != list_item:
                list_item.selected = False

        # Notify the app about the selected item
        app = MDApp.get_running_app()
        if hasattr(app, "on_item_selected"):
            app.on_item_selected(self.selected_item_idx)

    def on_touch_move(self, touch) -> bool:
        """Handles touch move events for drag and drop functionality."""
        dragged_item = touch.ud.get("dragged_item")
        if dragged_item is None:
            return super().on_touch_move(touch)

        if dragged_item in self.ids.drag_n_drop_list.children:
            self._start_drag(touch, dragged_item)

        return super().on_touch_move(touch)

    def _start_drag(self, touch, dragged_item):
        """Initializes drag operation for the given item."""
        dragged_item_start_pos = dragged_item.to_window(*dragged_item.pos)
        touch.ud["dragged_item_idx"] = self.ids.drag_n_drop_list.children.index(
            dragged_item
        )
        self.ids.drag_n_drop_list.remove_widget(dragged_item)
        self.add_widget(dragged_item)
        dragged_item.pos = self.to_widget(*dragged_item_start_pos)

    def on_touch_up(self, touch):
        """Handles touch up events to finalize the drag and drop operations."""
        dragged_item = touch.ud.get("dragged_item")
        if not dragged_item:
            return super().on_touch_up(touch)

        self._finish_drag(touch, dragged_item)
        return super().on_touch_up(touch)

    def _finish_drag(self, touch, dragged_item):
        """Finalizes the drag operation by placing the dragged item in its new position."""
        dragged_item_idx = touch.ud.get("dragged_item_idx")
        if dragged_item_idx is None:
            # The drag did no start yet
            return

        self.remove_widget(dragged_item)
        new_idx = self._get_dragged_item_new_idx(touch, fallback_idx=dragged_item_idx)

        self.ids.drag_n_drop_list.add_widget(dragged_item, new_idx)

    def _get_dragged_item_new_idx(self, touch, fallback_idx=0):
        """Determines the new index for the dragged item based on touch position."""
        if not self.collide_point(*touch.pos):
            return fallback_idx

        for idx, item in enumerate(self.ids.drag_n_drop_list.children):
            touch_pos_in_item = item.to_widget(*touch.pos)
            if item.collide_point(*touch_pos_in_item):
                return (
                    idx if touch_pos_in_item[1] < item.y + item.height / 2 else idx + 1
                )

        return fallback_idx
