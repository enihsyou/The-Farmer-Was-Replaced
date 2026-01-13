from library import *


def plant_pumpkin():
    if get_entity_type() == Entities.Pumpkin:
        return  # 已经种了南瓜就不动
    harvest()  # 有就收获，清空土地
    plant(Entities.Pumpkin)


def is_ripe_pumpkin():
    return get_entity_type() == Entities.Pumpkin and can_harvest()


def is_dead_pumpkin():
    return get_entity_type() == Entities.Dead_Pumpkin


def replant_dead_pumpkins(positions):
    unripes = []
    for cell in routing_nearest(positions):
        move_2d_torus(cell)
        if is_ripe_pumpkin():
            harvest()
        else:
            unripes.append(cell)
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

    traverse_rectangle(plant_pumpkin, size, size)
    traverse_rectangle(check_pumpkin, size, size)
    while unripes:
        unripes = replant_dead_pumpkins(unripes)
    harvest()
