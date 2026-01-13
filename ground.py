from library import *


def cell_till():
    if get_ground_type() != Grounds.Soil:
        till()


def soil_ground(w, h):
    if get_ground_type() != Grounds.Soil:
        traverse_rectangle(cell_till, w, h)
