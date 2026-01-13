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


if __name__ == "__main__":
    move_2d_torus(zeroing_position)
    while True:
        harvest_carrots(WORLD_SIZE, WORLD_SIZE)
