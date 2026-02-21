s = get_world_size()
m = s - 1
W = 0.75


def traverse_rectangle(fn, w, h, mirror):
    if mirror:
        base, back = (West, East)
    else:
        base, back = (East, West)
    fn()
    for i in range(1, h):
        move(North)
        fn()
    move(base)
    for i in range(h, 0, -2):
        for j in range(w, 1, -1):
            fn()
            if j != 2:
                move(base)
        move(South)
        for j in range(w, 1, -1):
            fn()
            if j != 2:
                move(back)
        if i != 2:
            move(South)
    move(back)


def work_drone_task():
    start = (get_pos_x(), get_pos_y())
    unripes = []

    def plant_pumpkin():
        if get_ground_type() != Grounds.Soil:
            till()
        plant(Entities.Pumpkin)

    def check_pumpkin():
        if (
            plant(Entities.Pumpkin)  # dead pumpkin
            or not can_harvest()  # still growing
        ):
            if get_water() < W:
                use_item(Items.Water)
            if can_harvest():
                # 浇水过程中可能成熟了
                return
            if not unripes and measure():
                # 只剩这一个仍在生长
                use_item(Items.Fertilizer)
            # 长成了但是坏南瓜
            plant(Entities.Pumpkin)
            # 长成了且是好南瓜
            if can_harvest():
                return
            unripes.append((get_pos_x(), get_pos_y()))

    def cycle_pumpkin():
        while unripes:
            last_d = move_to_without_last_move(unripes.pop(0))
            if last_d:
                # 移动之前就能判断是否成熟
                if measure() == measure(last_d):
                    continue
                move(last_d)
            check_pumpkin()

    def right_side():
        traverse_rectangle(plant_pumpkin, 3, 6, False)
        traverse_rectangle(check_pumpkin, 3, 6, False)
        cycle_pumpkin()

    def left_side(right_drone):
        traverse_rectangle(plant_pumpkin, 3, 6, True)
        traverse_rectangle(check_pumpkin, 3, 6, True)
        cycle_pumpkin()
        move_to(start)
        wait_for(right_drone)
        harvest()

    def while_round():
        left_side(spawn_drone(straight_move_do(1, East, right_side)))
        unripes = []
        return num_items(Items.Pumpkin) < 200000000

    while while_round():
        continue


def move_to(pos):
    cx, cy = get_pos_x(), get_pos_y()
    tx, ty = pos

    dx = abs(tx - cx)
    if cx < tx:
        dir_x = East
    else:
        dir_x = West
    for _ in range(dx):
        move(dir_x)

    dy = abs(ty - cy)
    if cy < ty:
        dir_y = North
    else:
        dir_y = South
    for _ in range(dy):
        move(dir_y)


def move_to_without_last_move(pos):
    cx, cy = get_pos_x(), get_pos_y()
    tx, ty = pos

    dx = abs(tx - cx)
    dy = abs(ty - cy)
    if dx == 0 and dy == 0:
        return None
    if cx < tx:
        dir_x = East
    else:
        dir_x = West
    if cy < ty:
        dir_y = North
    else:
        dir_y = South

    if dy > 0:
        dy -= 1
        return_d = dir_y
    elif dx > 0:
        dx -= 1
        return_d = dir_x
    for _ in range(dx):
        move(dir_x)
    for _ in range(dy):
        move(dir_y)
    return return_d


def straight_move_do(side_length, d, do):
    def fn():
        for _ in range(side_length):
            move(d)
        do()

    return fn


def spawn_drone_task1(w, h):
    def fn():
        if w > 1:
            spawn_drone(straight_move_do(8, East, spawn_drone_task1(w - 1, h)))
        spawn_drone_task2(h)()

    return fn


def spawn_drone_task2(h):
    def fn():
        if h > 1:
            spawn_drone(straight_move_do(8, North, spawn_drone_task2(h - 1)))
        work_drone_task()

    return fn


move(East)
move(East)
spawn_drone_task1(4, 4)()
