from __builtins__ import (
    East,
    North,
    can_harvest,
    get_world_size,
    max_drones,
    num_drones,
    spawn_drone,
)
from library import *


def harvest_hays(w, h):
    def plant_and_harvest():
        if can_harvest():
            harvest()
        if get_entity_type() != Entities.Grass:
            plant(Entities.Grass)

    traverse_rectangle(plant_and_harvest, w, h)


def poly_hays():
    def plant_bush():
        if get_entity_type() != Entities.Bush:
            harvest()
        if get_entity_type() != Entities.Bush:
            plant(Entities.Bush)

    # 用灌木占满空间
    move_2d_torus(zeroing_position)
    traverse_rectangle(plant_bush, WORLD_SIZE, WORLD_SIZE)
    world_center = (HALF_WORLD_SIZE, HALF_WORLD_SIZE)
    loop = [South, West, North, East]
    core_locations = []
    position = world_center
    for dir in loop:
        position = adjecent_coordination(position, dir)
        core_locations.append(position)

    move_2d_torus(world_center)
    while True:
        for dir in loop:
            if get_entity_type() != Entities.Grass:
                plant(Entities.Grass)
            if can_harvest():
                harvest()
            companion, pos = get_companion()  # ty: ignore
            while companion != Entities.Bush or pos in core_locations:
                plant(Entities.Grass)
                companion, pos = get_companion()  # ty: ignore
            while get_water() < 0.75 and num_items(Items.Water) > 0:
                use_item(Items.Water)
            move(dir)


def multidrone_hays():
    def harvest_hay_column():
        for i in range(get_world_size()):
            harvest()
            if i != get_world_size() - 1:
                move(North)

    def spawn_task():
        while True:
            if spawn_drone(harvest_hay_column):
                move(East)

    spawn_task()


def poly_multidrone_hays():
    def plant_bush_column():
        for i in range(get_world_size()):
            if get_entity_type() != Entities.Bush:
                harvest()
            if get_entity_type() != Entities.Bush:
                plant(Entities.Bush)
            if i != get_world_size() - 1:
                move(North)

    def spawn_plant_bush():
        for i in range(get_world_size()):
            while not spawn_drone(plant_bush_column):
                pass
            move(East)

    def harvest_hay_column():
        while True:
            while True:
                harvest()
                plant(Entities.Grass)
                companion, (x, y) = get_companion()  # ty: ignore
                if companion == Entities.Bush and y > 0:
                    break
            while get_water() < 0.75 and num_items(Items.Water) > 0:
                use_item(Items.Water)
            while not can_harvest():
                pass

    def spawn_harvest_hay():
        for _ in range(max_drones() - 1):
            while not spawn_drone(harvest_hay_column):
                pass
            move(East)
        harvest_hay_column()

    spawn_plant_bush()
    spawn_harvest_hay()


if __name__ == "__main__":
    clear()
    poly_multidrone_hays()
