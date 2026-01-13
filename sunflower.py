from library import *

def harvest_sunflowers(w, h):
    if w * h <= 10:
        return harvest_sunflower_simple(w, h)
    return harvest_sunflower_octuple(w, h)


def plant_and_harvest():
    if can_harvest():
        harvest()
    plant(Entities.Sunflower)


def harvest_sunflower_simple(w, h):
    # 简单版向日葵收割，仅适用于小于 10 的田块

    traverse_rectangle(plant_and_harvest, w, h)


def harvest_sunflower_octuple(w, h):
    # 努力取得八倍增益 (忽略区块之外的其他向日葵)
    # 从花瓣数最多的向日葵开始采集

    sunflower_dict = {}  # 记录不同花瓣数的向日葵位置
    for petals in range(7, 16):
        sunflower_dict[petals] = []

    def plant_a_sunflower():
        if get_entity_type() != Entities.Sunflower:
            harvest()
        if get_ground_type() != Grounds.Soil:
            till()
        if get_entity_type() != Entities.Sunflower:
            plant(Entities.Sunflower)
        sunflower_dict[measure()].append(current_position())

    def harvest_riped_sunflower(positions):
        unripes = []
        for cell in routing_nearest(positions):
            move_2d_torus(cell)
            if can_harvest():
                harvest()
            else:
                unripes.append(cell)
        return unripes

    traverse_rectangle(plant_a_sunflower, w, h)
    for petal in range(15, 6, -1):
        positions = sunflower_dict[petal]
        while positions:
            positions = harvest_riped_sunflower(positions)


if __name__ == "__main__":
    move_2d_torus(zeroing_position)
    while True:
        harvest_sunflower_octuple(WORLD_SIZE, WORLD_SIZE)
