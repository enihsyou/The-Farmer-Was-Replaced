from __builtins__ import East, North, get_world_size, set_world_size, spawn_drone
from library import *


def cocktail_forward(start, end, direction):
    swapped = False
    for i in range(start, end):
        if measure() > measure(direction):  # ty: ignore
            swap(direction)
            swapped = True
        if i != end - 1:
            move(direction)
    return swapped


def cocktail_backward(start, end, direction):
    swapped = False
    for i in range(end - 1, start - 1, -1):
        if measure() < measure(direction):  # ty: ignore
            swap(direction)
            swapped = True
        if i != start:
            move(direction)
    return swapped


def harvest_cactus(w, h):
    w = min(w, WORLD_SIZE)
    h = min(h, WORLD_SIZE)

    def plant_a_cactus():
        if get_entity_type() != Entities.Cactus:
            harvest()
        if get_ground_type() != Grounds.Soil:
            till()
        if get_entity_type() != Entities.Cactus:
            plant(Entities.Cactus)

    traverse_rectangle(plant_a_cactus, w, h)

    starting_position = current_position()
    starting_x, starting_y = starting_position

    for i in range(w):
        move_2d_torus((starting_x + i, starting_y))
        l, r = 0, h - 1
        while True:
            swapped = cocktail_forward(l, r, North)
            if not swapped:
                break
            r -= 1
            swapped = cocktail_backward(l, r, South)
            if not swapped:
                break
            l += 1

    for i in range(h):
        move_2d_torus((starting_x, starting_y + i))
        l, r = 0, w - 1
        while True:
            swapped = cocktail_forward(l, r, East)
            if not swapped:
                break
            r -= 1
            swapped = cocktail_backward(l, r, West)
            if not swapped:
                break
            l += 1

    harvest()


def multidrone_cactus():
    def plant_a_cactus(i):
        def f():
            for i in range(get_world_size()):
                if get_entity_type() != Entities.Cactus:
                    harvest()
                if get_ground_type() != Grounds.Soil:
                    till()
                if get_entity_type() != Entities.Cactus:
                    plant(Entities.Cactus)
                if i != get_world_size() - 1:
                    move(North)

        return f

    def sort_col(i):
        def f():
            move_2d_torus((i, 0))
            l, r = 0, get_world_size() - 1
            while True:
                swapped = cocktail_forward(l, r, North)
                if not swapped:
                    break
                r -= 1
                swapped = cocktail_backward(l, r, South)
                if not swapped:
                    break
                l += 1

        return f

    def sort_row(i):
        def f():
            move_2d_torus((0, i))
            l, r = 0, get_world_size() - 1
            while True:
                swapped = cocktail_forward(l, r, East)
                if not swapped:
                    break
                r -= 1
                swapped = cocktail_backward(l, r, West)
                if not swapped:
                    break
                l += 1

        return f

    spawn_drone_foreach_col(plant_a_cactus)
    spawn_drone_foreach_col(sort_col)
    spawn_drone_foreach_row(sort_row)
    harvest()


if __name__ == "__main__":
    change_hat(Hats.Cactus_Hat)
    while True:
        move_2d_torus(zeroing_position)
        multidrone_cactus()
