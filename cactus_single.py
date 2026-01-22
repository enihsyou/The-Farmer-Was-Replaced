# set_world_size(8)
s = get_world_size()
m = s - 1


def traverse_topdown(fn):
    # 宽度为 2 的逆时针圈不断向东
    for i in range(0, s, 2):
        for j in range(s - 1):
            fn()
            move(North)
        fn()
        move(East)
        for j in range(s - 1):
            fn()
            move(South)
        fn()
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


def plant_a_cactus_north():
    till()
    plant(Entities.Cactus)

def perform_insertion_sort():
    while True:
        v = measure()
        x, y = get_pos_x(), get_pos_y()
        vw = measure(West)
        vs = measure(South)
        if x != 0 and v < vw:  # type: ignore
            if y != 0 and vw < vs:  # type: ignore
                dir = South  # 和更大的一个交换，维持已有顺序
            else:
                dir = West
            swap(dir)
            move(dir)
            continue
        if y != 0 and v < vs:  # type: ignore
            if x != 0 and vs < vw:  # type: ignore
                dir = West
            else:
                dir = South
            swap(dir)
            move(dir)
            continue
        break


traverse_topdown(plant_a_cactus_north)

for i in range(s * 2):
    for j in range(i + 1):
        if j > m or i - j > m:
            continue
        move_to((j, i - j))
        perform_insertion_sort()

harvest()
