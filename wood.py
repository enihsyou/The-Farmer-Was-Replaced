from library import *


def harvest_woods(w, h):
    def plant_and_harvest():
        if can_harvest():
            harvest()
        x, y = current_position()
        if is_odd(x + y):
            plant(Entities.Tree)
        else:
            plant(Entities.Bush)

    traverse_rectangle(plant_and_harvest, w, h)


if __name__ == "__main__":
    move_2d_torus(zeroing_position)
    while True:
        harvest_woods(WORLD_SIZE, WORLD_SIZE)
