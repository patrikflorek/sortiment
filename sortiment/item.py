from typing import Dict, Any

from kivy.properties import DictProperty, BooleanProperty

from kivymd.uix.list import (
    MDListItem,
    MDListItemTrailingIcon,
    MDListItemHeadlineText,
    MDListItemSupportingText,
    MDListItemTertiaryText,
)


UNSELECTED_OPACITY = 0.5
SELECTED_OPACITY = 1.0
DRAG_ICON = "drag"


class DragHandle(MDListItemTrailingIcon):
    """A handle widget that allows for dragging the parent drag-n-drop list item."""

    def __init__(self, parent_item: "DragNDropListItem", **kwargs) -> None:
        """
        Initializes the drag handle.

        Args:
            parent_item: The parent drag-n-drop list item that contains this handle.
            **kwargs: Additional keyword arguments to pass to the superclass constructor.
        """
        super().__init__(**kwargs)
        self.parent_item = parent_item
        self.icon = DRAG_ICON

    def on_touch_down(self, touch) -> bool:
        """
        Handles touch down events to start dragging the parent drag-n-drop list item.

        Args:
            touch: The touch event.

        Returns:
            bool: True if the touch was handled, False otherwise.
        """
        if self.collide_point(*touch.pos):
            touch.ud["dragged_item"] = self.parent_item
            return super().on_touch_down(touch)

        return False


class DragNDropListItem(MDListItem):
    """A list item that can be dragged and dropped within a list."""

    item_data = DictProperty({})
    selected = BooleanProperty(False)

    def __init__(self, item_data: Dict[str, Any], **kwargs) -> None:
        """
        Initializes the draggable list item.

        Args:
            item_data: Dictionary containing item data to be displayed.
            **kwargs: Additional keyword arguments to pass to the superclass constructor.
        """
        super().__init__(**kwargs)
        self.item_data = item_data
        self._setup_item_components()

        self.ripple_effect = False  # Disable ripple effect
        self.opacity = UNSELECTED_OPACITY

    def _setup_item_components(self) -> None:
        """Sets up the child widgets of the list item based on the provided item data."""
        if headline_text := self.item_data.get("headline_text"):
            self.add_widget(MDListItemHeadlineText(text=headline_text))

        if supporting_text := self.item_data.get("supporting_text"):
            self.add_widget(MDListItemSupportingText(text=supporting_text))

        if tertiary_text := self.item_data.get("tertiary_text"):
            self.add_widget(MDListItemTertiaryText(text=tertiary_text))

        self.add_widget(DragHandle(parent_item=self))

    def on_selected(self, instance: "DragNDropListItem", value: bool) -> None:
        """
        Updates the opacity of the list item based on its selection state.

        Args:
            instance: The instance of the list item.
            value: The new selection state.
        """
        self.opacity = SELECTED_OPACITY if value else UNSELECTED_OPACITY

    def on_touch_move(self, touch) -> bool:
        """
        Handles touch move events to update the position of the list item during dragging.

        Args:
            touch: The touch event.

        Returns:
            bool: True if the touch was handled, False otherwise.
        """
        if touch.ud.get("dragged_item") == self:
            self.y = touch.y - self.height // 2
            return True
        return False

    def on_press(self) -> None:
        """Handles press events by selecting the list item."""
        self.selected = True
