s = get_world_size()
m = s - 1
W = 0.70
B = 3


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


def traverse_spiral(fn, w, h, cww):
    if cww:
        pair_even = (East, South)
        pair_odd = (West, North)
    else:
        pair_even = (West, North)
        pair_odd = (East, South)
    fn()
    i = 0
    while True:
        if not (w and h):
            break
        if i % 2:
            dir_x, dir_y = pair_even
        else:
            dir_x, dir_y = pair_odd
        for _ in range(w):
            move(dir_x)
            fn()
        for _ in range(h):
            move(dir_y)
            fn()
        w -= 1
        h -= 1
        i += 1


def seven_loop_part_cw(fn):
    for _ in range(2):
        move(North)
        fn()
    move(North)
    traverse_spiral(fn, 3, 6, False)
    for _ in range(2):
        move(West)
        move(North)


def seven_loop_part_cww(fn):
    for _ in range(2):
        move(South)
        fn()
    move(South)
    traverse_spiral(fn, 3, 6, True)
    for _ in range(2):
        move(East)
        move(South)


def work_drone_task(size):
    start = (get_pos_x(), get_pos_y())
    unripes = []
    plant_times = {}

    def plant_pumpkin():
        if get_ground_type() != Grounds.Soil:
            till()
        plant(Entities.Pumpkin)
        plant_times[(get_pos_x(), get_pos_y())] = 1

    def check_pumpkin():
        if can_harvest():
            return
        pos = (get_pos_x(), get_pos_y())
        if plant(Entities.Pumpkin):
            plant_times[pos] += 1
        if get_water() < W:
            use_item(Items.Water)
        if plant_times[pos] > B:
            if use_item(Items.Fertilizer) and can_harvest():
                return
        if can_harvest():
            return
        unripes.append(pos)

    def cycle_pumpkin():
        while unripes:
            last_d = move_to_without_last_move(unripes.pop(0))
            if last_d:
                # 移动之前就能判断是否成熟
                if measure() == measure(last_d):
                    continue
                move(last_d)
            check_pumpkin()

    def one_side_n(size, mirror):
        size_2 = size * 2

        def fn():
            traverse_rectangle(plant_pumpkin, size, size_2, mirror)
            traverse_rectangle(check_pumpkin, size, size_2, mirror)
            cycle_pumpkin()

        return fn

    def wait_merge(right_drone):
        move_to(start)
        wait_for(right_drone)
        harvest()

    def while_round_6():
        left_side = one_side_n(3, True)
        right_side = one_side_n(3, False)
        right_drone = spawn_drone(straight_move_do(1, East, right_side))
        left_side()
        wait_merge(right_drone)

    def while_round_8():
        left_side = one_side_n(4, True)
        right_side = one_side_n(4, False)
        right_drone = spawn_drone(straight_move_do(1, East, right_side))
        left_side()
        wait_merge(right_drone)

    def cw_side():
        plant_pumpkin()
        check_pumpkin()
        seven_loop_part_cw(plant_pumpkin)
        seven_loop_part_cw(check_pumpkin)
        cycle_pumpkin()

    def cww_side(cw_drone):
        seven_loop_part_cww(plant_pumpkin)
        seven_loop_part_cww(check_pumpkin)
        cycle_pumpkin()
        wait_for(cw_drone)
        harvest()

    def while_round_7():
        cww_side(spawn_drone(cw_side))
        move_to(start)

    if size == 6:
        while_round = while_round_6
    if size == 7:
        while_round = while_round_7
    if size == 8:
        while_round = while_round_8
    while num_items(Items.Pumpkin) < 200000000:
        while_round()
        unripes = []
        plant_times = {}


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


drones = {
    (3, 3): 7,
    (11, 0): 8,
    (20, 0): 8,
    (28, 0): 6,
    (3, 8): 8,
    (12, 12): 7,
    (19, 20): 7,
    (20, 12): 7,
    (11, 17): 6,
    (27, 15): 8,
    (28, 10): 7,
    (3, 17): 8,
    (2, 26): 6,
    (11, 24): 8,
    (20, 28): 7,
    (28, 28): 7,
}

clear()
for pos in drones:
    size = drones[pos]

    def spawn_drone_task(pos, size):
        def fn():
            move_to(pos)
            work_drone_task(size)

        return fn

    fn = spawn_drone_task(pos, size)
    if not spawn_drone(fn):
        fn()
