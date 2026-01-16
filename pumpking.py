from __builtins__ import get_world_size, wait_for, East
from library import *


def plant_pumpkin():
    if get_entity_type() != Entities.Pumpkin:
        harvest()  # 有就收获，清空土地
    if get_ground_type() != Grounds.Soil:
        till()
    if get_entity_type() != Entities.Pumpkin:
        plant(Entities.Pumpkin)
    if get_water() < 0.75 and num_items(Items.Water) > 100:
        use_item(Items.Water)


def is_ripe_pumpkin():
    return get_entity_type() == Entities.Pumpkin and can_harvest()


def is_dead_pumpkin():
    return get_entity_type() == Entities.Dead_Pumpkin


def replant_dead_pumpkins(positions):
    unripes = []
    for cell in routing_nearest(positions):
        move_2d_torus(cell)
        if is_ripe_pumpkin():
            continue
        unripes.append(cell)
        plant_pumpkin()
    return unripes


def harvest_pumpkins(size):
    # 从 position (x, y) 坐标开始种植一个 size 为边长的正方形南瓜田
    unripes = []

    def check_pumpkin():
        if is_ripe_pumpkin():
            return
        if is_dead_pumpkin():
            plant(Entities.Pumpkin)
        unripes.append(current_position())

    starting_position = current_position()
    traverse_rectangle(plant_pumpkin, size, size)
    traverse_rectangle(check_pumpkin, size, size)
    while unripes:
        unripes = replant_dead_pumpkins(unripes)
    harvest()
    move_2d_torus(starting_position)


def multidrone_pumpkins():
    move_2d_torus(zeroing_position)

    def drone_behavior(starting_position, size):
        def task():
            move_2d_torus(starting_position)
            while True:
                harvest_pumpkins(size)

        return task

    def safe_spawn_drone(task):
        if spawn_drone(task):
            return
        task()

    for i in range(0, WORLD_SIZE, 7):
        for j in range(0, WORLD_SIZE, 7):
            if i + 6 < WORLD_SIZE and j + 6 < WORLD_SIZE:
                safe_spawn_drone(drone_behavior((i, j), 6))


def world_size_pumpkins():
    move_2d_torus(zeroing_position)

    def plant_column():
        for i in range(get_world_size()):
            plant_pumpkin()
            if i != get_world_size() - 1:
                move(North)
        unripes = []

        def check_pumpkin():
            if is_ripe_pumpkin():
                return
            if is_dead_pumpkin():
                plant(Entities.Pumpkin)
            unripes.append(current_position())

        for i in range(get_world_size()):
            check_pumpkin()
            if i != get_world_size() - 1:
                move(North)

        while unripes:
            unripes = replant_dead_pumpkins(unripes)

    def spawn_plant_bush():
        drones = []
        for i in range(get_world_size()):
            drone = spawn_drone(plant_column)
            if drone != None:
                drones.append(drone)
            else:
                plant_column()
            if i != get_world_size() - 1:
                move(East)
        for drone in drones:
            wait_for(drone)

    spawn_plant_bush()
    harvest()

if __name__ == "__main__":
    world_size_pumpkins()
