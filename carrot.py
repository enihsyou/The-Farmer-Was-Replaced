from __builtins__ import can_harvest
from library import *


def harvest_carrots(w, h):
    def plant_and_harvest():
        if can_harvest():
            harvest()
        if get_ground_type() != Grounds.Soil:
            till()
        if get_entity_type() != Entities.Carrot:
            plant(Entities.Carrot)

    traverse_rectangle(plant_and_harvest, w, h)


def poly_carrots():
    def plant_carrot():
        if get_ground_type() != Grounds.Soil:
            till()
        while True:
            harvest()
            plant(Entities.Carrot)
            companion, pos = get_companion()  # type: ignore
            if companion == Entities.Grass:
                break
        while get_water() < 0.75 and num_items(Items.Water) > 0:
            use_item(Items.Water)

    traverse_rectangle(plant_carrot, 2, 4)

if __name__ == "__main__":
    clear()
    while True:
        poly_carrots()
