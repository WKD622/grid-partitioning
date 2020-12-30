from src.definitions import NORMAL_AREA_COLOR_CODE, INDIVISIBLE_AREA_COLOR_CODE, OFF_AREA_COLOR_CODE


def is_normal(pixel):
    return tuple(pixel) == NORMAL_AREA_COLOR_CODE


def is_indivisible(pixel):
    return tuple(pixel) == INDIVISIBLE_AREA_COLOR_CODE


def is_off(pixel):
    return tuple(pixel) == OFF_AREA_COLOR_CODE
