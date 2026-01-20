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


def traverse_rectangle2(fn):
    cells = set()
    if fn():
        cells.add((get_pos_x(), get_pos_y()))
    move(North)
    for i in range(0, s, 2):
        for j in range(m):
            if fn():
                cells.add((get_pos_x(), get_pos_y()))
            if j != n:
                move(North)
        move(East)
        for j in range(m):
            if fn():
                cells.add((get_pos_x(), get_pos_y()))
            if j != n:
                move(South)
        if i != n:
            move(East)
    move(South)
    for _ in range(m):
        if fn():
            cells.add((get_pos_x(), get_pos_y()))
        move(West)

    return cells  # loop continues


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


def plant_pumpkin_first():
    till()
    plant_pumpkin()


def plant_pumpkin():
    plant(Entities.Pumpkin)
    if get_water() < 0.75:
        use_item(Items.Water)


def replant_dead_pumpkins(positions):
    while len(positions) > num_items(Items.Fertilizer) / 2:
        for mvalue in list(positions):
            move_to(mvalue)
            if can_harvest():
                positions.remove(mvalue)
                continue
            plant(Entities.Pumpkin)

    for mvalue in positions:
        move_to(mvalue)
        while not can_harvest():
            plant(Entities.Pumpkin)
            use_item(Items.Fertilizer)


def check_pumpkin():
    if can_harvest():
        return False
    plant(Entities.Pumpkin)
    return True


def harvest_a_pumpkin():
    traverse_rectangle(plant_pumpkin)
    unripes = traverse_rectangle2(check_pumpkin)
    replant_dead_pumpkins(unripes)
    harvest()


def harvest_a_pumpkin_first():
    traverse_rectangle(plant_pumpkin_first)
    unripes = traverse_rectangle2(check_pumpkin)
    replant_dead_pumpkins(unripes)
    harvest()


harvest_a_pumpkin_first()
while num_items(Items.Pumpkin) < 10000000:
    harvest_a_pumpkin()
