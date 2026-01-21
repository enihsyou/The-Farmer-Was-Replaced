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


unripes = []
zero_measures = {}


def plant_pumpkin_first():
    till()
    plant_pumpkin()


def plant_pumpkin():
    plant(Entities.Pumpkin)
    if get_water() < 0.75:
        use_item(Items.Water)


def replant_dead_pumpkins():
    # if unripes and len(unripes) > num_items(Items.Fertilizer) / 2:
    #     for mvalue in list(unripes):
    #         move_to(mvalue)
    #         x, y = get_pos_x(), get_pos_y()
    #         if y == m:
    #             if x in zero_measures and zero_measures[x] == measure():
    #                 return True
    #         if can_harvest():
    #             unripes.remove(mvalue)
    #             continue
    #             plant_pumpkin()
    while unripes:
        mvalue = unripes.pop(0)
        move_to(mvalue)
        if plant(Entities.Pumpkin):  # dead pumpkin
            unripes.append(mvalue)
            continue
        if not can_harvest():  # still growing
            if num_items(Items.Fertilizer):
                use_item(Items.Fertilizer)
                if can_harvest():
                    continue
            unripes.append(mvalue)
            continue
        # if num_items(Items.Fertilizer) > 0:
        #     use_item(Items.Fertilizer)
    # for mvalue in unripes:
    #     move_to(mvalue)
    #     x, y = get_pos_x(), get_pos_y()
    #     if y == m:
    #         if x in zero_measures and zero_measures[x] == measure():
    #             return True
    #     while not can_harvest():
    #         plant_pumpkin()
    #         use_item(Items.Fertilizer)


def is_fully_grown_compare_with(c, d):
    if c:
        v = measure()
        if v != None and measure(d) == v:
            return True


def is_fully_grown():
    x, y = get_pos_x(), get_pos_y()
    return (
        is_fully_grown_compare_with(y == 0, South)
        or is_fully_grown_compare_with(y == m, North)
        or is_fully_grown_compare_with(x == 0, West)
        or is_fully_grown_compare_with(x == m, East)
    )


def check_pumpkin():
    # if is_fully_grown():
    #     return True
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


harvest_a_pumpkin_first()
while num_items(Items.Pumpkin) < 10000000:
    unripes = []
    zero_measures = {}
    harvest_a_pumpkin()
