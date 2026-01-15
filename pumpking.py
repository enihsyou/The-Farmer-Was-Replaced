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


if __name__ == "__main__":
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

    clear()
    safe_spawn_drone(drone_behavior((0, 0), 6))
    safe_spawn_drone(drone_behavior((0, 7), 6))
    safe_spawn_drone(drone_behavior((7, 0), 6))
    safe_spawn_drone(drone_behavior((7, 7), 6))
