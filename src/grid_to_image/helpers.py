from src.definitions import (NORMAL_AREA, INDIVISIBLE_AREA, OFF_AREA_COLOR_CODE, NORMAL_AREA_COLOR_CODE,
                             INDIVISIBLE_AREA_COLOR_CODE)


def get_color(node_type):
    if node_type == NORMAL_AREA:
        return NORMAL_AREA_COLOR_CODE
    elif node_type == INDIVISIBLE_AREA:
        return INDIVISIBLE_AREA_COLOR_CODE
    return OFF_AREA_COLOR_CODE
