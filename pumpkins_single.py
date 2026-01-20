set_world_size(6)

s = get_world_size()
m = s - 1
n = s - 2


def traverse_rectangle(fn):
    # traverse_rectangle 针对 8 x 8 的性能优化版
    if fn():
        return False
    move(North)
    for i in range(0, s, 2):
        for j in range(m):
            if fn():
                return False
            if j != n:
                move(North)
        move(East)
        for j in range(m):
            if fn():
                return False
            if j != n:
                move(South)
        if i != n:
            move(East)
    move(South)
    for _ in range(m):
        if fn():
            return False
        move(West)

    return True  # loop continues


def move_to(pos):
    cx, cy = get_pos_x(), get_pos_y()
    tx, ty = pos

    a = (tx - cx) % s
    b = (cx - tx) % s
    if a > b:
        for _ in range(b):
            move(West)
    elif b > a:
        for _ in range(a):
            move(East)

    a = (ty - cy) % s
    b = (cy - ty) % s
    if a > b:
        for _ in range(b):
            move(South)
    elif b > a:
        for _ in range(a):
            move(North)


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


def distance_2d(a, b):
    ax, ay = a
    bx, by = b
    return abs(ax - bx) + abs(ay - by)


def indexof_nearest(start, items):
    min_index = 0
    min_value = distance_2d(start, items[0])
    for idx in range(1, len(items)):
        item = items[idx]
        value = distance_2d(start, item)
        if value < min_value:
            min_value = value
            min_index = idx
    return min_index


def replant_dead_pumpkins(positions):
    start = (get_pos_x(), get_pos_y())
    unchecks = positions
    growings = []
    while unchecks:
        while unchecks:
            # mindex = indexof_nearest(start, unchecks)
            mvalue = unchecks.pop(0)
            move_to(mvalue)
            start = mvalue
            if is_ripe_pumpkin():
                continue
            growings.append(mvalue)
            plant(Entities.Pumpkin)
        unchecks, growings = growings, []


def harvest_a_pumpkin():
    unripes = []

    def check_pumpkin():
        if is_ripe_pumpkin():
            return
        if is_dead_pumpkin():
            plant(Entities.Pumpkin)
        unripes.append((get_pos_x(), get_pos_y()))

    traverse_rectangle(plant_pumpkin)
    traverse_rectangle(check_pumpkin)
    replant_dead_pumpkins(unripes)

    harvest()


harvest_a_pumpkin()
while num_items(Items.Pumpkin) < 10000000:
    harvest_a_pumpkin()
