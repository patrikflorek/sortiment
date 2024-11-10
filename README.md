# Sortiment
Sortiment is a project that provides simple KivyMD-based widgets for drag-and-drop arrangement of a scrollable list of items. Despite the project's name, only one widget is currently implemented.

**Disclaimer:** This implementation focuses on code and functionality minimalism, so the user experience may not be perfect.

## Features

- Drag-and-drop arrangement of items
- Scrollable list of items
- Customizable item widget

## Installation

```bash
pip install git+https://github.com/patrikflorek/sortiment
```

## Usage

```python
from sortiment import ScrollableDragNDropListContainer

drag_n_drop_list = ScrollableDragNDropListContainer()

# Set list data
drag_n_drop_list.items_data = [
    {
        "headline_text": "Item 1",
        "supporting_text": "Lorem ipsum dolor...",
        "tertiary_text": "Consectetur adipiscing elit!",
    },
    ...
]

# Get list data
items_data = drag_n_drop_list.items_data

# Set selected item by its index
drag_n_drop_list.selected_item_idx = 0

# Get selected item index
selected_item_idx = drag_n_drop_list.selected_item_idx
```

To notify the encompassing application that an item has been selected, the `ScrollableDragNDropListContainer` component attempts to call the application's `on_item_selected` method with the selected item index as an argument.

## Example

The `example/select_one.py` script demonstrates the usage.

<video src="examples/select_one_example.mp4" width=640>
