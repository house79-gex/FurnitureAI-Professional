def _create_side_panels(height, plinth_height, thickness, width):
    return {
        'left_panel': {
            'position': (0, 0, plinth_height),
            'size': (thickness, width, height - plinth_height)
        },
        'right_panel': {
            'position': (width - thickness, 0, plinth_height),
            'size': (thickness, width, height - plinth_height)
        }
    }


def _create_top_bottom_panels(height, plinth_height, thickness, width):
    return {
        'bottom_panel': {
            'position': (0, 0, plinth_height),
            'size': (width, thickness, height - plinth_height)
        },
        'top_panel': {
            'position': (0, 0, height - thickness),
            'size': (width, thickness, thickness)
        }
    }


def _create_shelves(shelf_count, height, plinth_height, thickness, width, depth, shelf_front_setback):
    shelf_height = (height - plinth_height) / (shelf_count + 1)
    shelves = []
    for i in range(shelf_count):
        shelf_position = plinth_height + (i + 1) * shelf_height
        shelves.append({
            'shelf': {
                'position': (thickness, 0, shelf_position),
                'size': (width - thickness * 2, thickness, depth - shelf_front_setback)
            }
        })
    return shelves
