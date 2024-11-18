from typing import Dict, Any

from kivy.properties import DictProperty, BooleanProperty

from kivymd.uix.list import (
    MDListItem,
    MDListItemTrailingIcon,
    MDListItemHeadlineText,
    MDListItemSupportingText,
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
        self._setup_item_components()
        self.item_data = item_data

        self.ripple_effect = False  # Disable ripple effect
        self.opacity = UNSELECTED_OPACITY

    def _setup_item_components(self) -> None:
        """Sets up the child widgets of the list item based on the provided item data."""
        self.headline_text_widget = MDListItemHeadlineText(text="Headline text")
        self.add_widget(self.headline_text_widget)

        self.supporting_text_widget = MDListItemSupportingText(text="Supporting text")
        self.add_widget(self.supporting_text_widget)

        self.add_widget(DragHandle(parent_item=self))

    def on_item_data(self, instance: Any, value: Dict[str, Any]) -> None:
        """
        Handles changes to the item data by updating the child widgets.

        Args:
            instance: The instance of the list item.
            value: The new item data.
        """
        self.headline_text_widget.text = value.get("headline_text", "")
        self.supporting_text_widget.text = value.get("supporting_text", "")

    def on_selected(self, instance: Any, value: bool) -> None:
        """
        Updates the opacity of the list item based on its selection state.

        Args:
            instance: The instance of the list item or the list managing widget.
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
