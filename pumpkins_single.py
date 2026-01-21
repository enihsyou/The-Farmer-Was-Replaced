set_world_size(6)

s = get_world_size()
m = s - 1


def traverse_topdown(fn):
    # 宽度为 2 的逆时针圈不断向东
    for i in range(0, s, 2):
        for j in range(s):
            if fn():
                return True
            if j != m:
                move(North)
        move(East)
        for j in range(s):
            if fn():
                return True
            if j != m:
                move(South)
        move(East)
    return False


def move_to(pos):
    cx, cy = get_pos_x(), get_pos_y()
    tx, ty = pos

    dx_east = (tx - cx) % s
    dx_west = (cx - tx) % s
    if dx_east < dx_west:
        for _ in range(dx_east):
            move(East)
    else:
        for _ in range(dx_west):
            move(West)

    dy_north = (ty - cy) % s
    dy_south = (cy - ty) % s
    if dy_north < dy_south:
        for _ in range(dy_north):
            move(North)
    else:
        for _ in range(dy_south):
            move(South)


def plant_pumpkin_first():
    till()
    plant_pumpkin()


def plant_pumpkin():
    plant(Entities.Pumpkin)
    if get_water() < 0.65:
        use_item(Items.Water)


def is_fully_grown_compare_with(d):
    v = measure()
    if v != None and measure(d) == v:
        return True


def is_fully_grown():
    # 四个角落拥有同一个 id 说明南瓜已完全合并
    x, y = get_pos_x(), get_pos_y()
    return (
        (y == 0 and is_fully_grown_compare_with(South))
        or (y == m and is_fully_grown_compare_with(North))
        or (x == 0 and is_fully_grown_compare_with(West))
        or (x == m and is_fully_grown_compare_with(East))
    )


def replant_dead_pumpkins():
    while unripes:
        mvalue = unripes.pop(0)
        move_to(mvalue)
        if plant(Entities.Pumpkin):  # dead pumpkin
            unripes.append(mvalue)
            continue
        if can_harvest():
            if unripes and is_fully_grown():  # fully grown up and merged
                return True # 只在还有其他为检查的植物时做这个提前判断
            continue
        if use_item(Items.Fertilizer):
            if can_harvest():
                if unripes and is_fully_grown():
                    return True
                continue
        unripes.append(mvalue)  # still growing
        continue


def check_pumpkin():
    if plant(Entities.Pumpkin):  # dead pumpkin
        unripes.append((get_pos_x(), get_pos_y()))
        return
    if not can_harvest():  # still growing
        unripes.append((get_pos_x(), get_pos_y()))
        return


def harvest_a_pumpkin():
    traverse_topdown(plant_pumpkin)
    if not traverse_topdown(check_pumpkin):
        replant_dead_pumpkins()
    harvest()


def harvest_a_pumpkin_first():
    traverse_topdown(plant_pumpkin_first)
    if not traverse_topdown(check_pumpkin):
        replant_dead_pumpkins()
    harvest()


unripes = []
harvest_a_pumpkin_first()
while num_items(Items.Pumpkin) < 10000000:
    unripes = []
    harvest_a_pumpkin()
