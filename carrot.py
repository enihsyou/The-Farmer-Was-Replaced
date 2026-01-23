from __builtins__ import can_harvest, spawn_drone
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
            companion, pos = get_companion()  # ty: ignore
            if companion == Entities.Grass:
                break
        while get_water() < 0.75 and num_items(Items.Water) > 0:
            use_item(Items.Water)

    traverse_rectangle(plant_carrot, 2, 4)


def ploy_multidrone_carrots():
    w, h = 4, 8
    def plant_carrot():
        if get_ground_type() != Grounds.Soil:
            till()
        while True:
            while True:
                harvest()
                plant(Entities.Carrot)
                companion, (x, y) = get_companion()  # ty: ignore
                if companion == Entities.Grass:
                    if not (0 <= x < w and 0 <= y < h):
                        break
            while get_water() < 0.75 and num_items(Items.Water) > 0:
                use_item(Items.Water)
            while not can_harvest():
                pass

    def spawn_task():
        spawn_drone(plant_carrot)

    traverse_rectangle(spawn_task, w, h)
    plant_carrot()


if __name__ == "__main__":
    clear()
    ploy_multidrone_carrots()
