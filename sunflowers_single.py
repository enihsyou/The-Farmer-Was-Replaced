from __builtins__ import get_water

set_world_size(8)
s = get_world_size()
m = s - 1


def traverse_topdown(fn):
    # 宽度为 2 的逆时针圈不断向东
    for i in range(0, s, 2):
        for j in range(m):
            if fn():
                return True
            move(North)
        if fn():
            return True
        move(East)
        for j in range(m):
            if fn():
                return True
            move(South)
        if fn():
            return True
        move(East)
    return False


def traverse_topdown_no_if(fn):
    for i in range(0, s, 2):
        for j in range(m):
            fn()
            move(North)
        fn()
        move(East)
        for j in range(m):
            fn()
            move(South)
        fn()
        move(East)


def move_to(pos):
    cx, cy = get_pos_x(), get_pos_y()
    tx, ty = pos

    dx_east = (tx - cx) % s
    dx_west = s - dx_east
    if dx_east < dx_west:
        for _ in range(dx_east):
            move(East)
    else:
        for _ in range(dx_west):
            move(West)

    dy_north = (ty - cy) % s
    dy_south = s - dy_north
    if dy_north < dy_south:
        for _ in range(dy_north):
            move(North)
    else:
        for _ in range(dy_south):
            move(South)


def plant_a_sunflower_first():
    till()
    plant_a_sunflower()


def plant_a_sunflower():
    plant(Entities.Sunflower)
    sunflower_dict[measure()].append((get_pos_x(), get_pos_y()))
    while get_water() < 0.75:
        use_item(Items.Water)


def harvest_riped_sunflower(positions):
    unripes = []
    for pos in positions:
        move_to(pos)
        if can_harvest():
            harvest()
        else:
            unripes.append(pos)
    return unripes


def harvest_sunflowers(plant_a_sunflower):
    for petals in range(7, 16):
        sunflower_dict[petals] = []

    traverse_topdown_no_if(plant_a_sunflower)
    for petal in range(15, 6, -1):
        positions = sunflower_dict[petal]
        while positions:
            positions = harvest_riped_sunflower(positions)


sunflower_dict = {}  # 记录不同花瓣数的向日葵位置
harvest_sunflowers(plant_a_sunflower_first)
while num_items(Items.Power) < 10000:
    sunflower_dict = {}
    harvest_sunflowers(plant_a_sunflower)
