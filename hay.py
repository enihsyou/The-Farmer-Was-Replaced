from library import *


def harvest_hays(w, h):
    def plant_and_harvest():
        if can_harvest():
            harvest()
        if get_entity_type() != Entities.Grass:
            plant(Entities.Grass)
            use_item(Items.Fertilizer)

    traverse_rectangle(plant_and_harvest, w, h)


if __name__ == "__main__":
    move_2d_torus(zeroing_position)
    while True:
        harvest_hays(3, 3)
