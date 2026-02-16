from __builtins__ import Entities, harvest

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


def is_fully_grown():
    # 在右半 start 位置检测和左边拥有相同的 id
    v = measure()
    return v != None and v == measure(West)


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
                return
            use_item(Items.Fertilizer)
            plant(Entities.Pumpkin)
            if can_harvest():
                return
            unripes.append((get_pos_x(), get_pos_y()))

    def cycle_pumpkin():
        while unripes:
            move_to(unripes.pop(0))
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
    s = 32

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
