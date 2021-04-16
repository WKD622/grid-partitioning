NORMAL_AREA_COLOR_CODE = (255, 255, 255)
INDIVISIBLE_AREA_COLOR_CODE = (0, 255, 255)
OFF_AREA_COLOR_CODE = (0, 0, 255)


def is_normal(pixel):
    return tuple(pixel) == NORMAL_AREA_COLOR_CODE


def is_indivisible(pixel):
    return tuple(pixel) == INDIVISIBLE_AREA_COLOR_CODE


def is_off(pixel):
    return tuple(pixel) == OFF_AREA_COLOR_CODE
