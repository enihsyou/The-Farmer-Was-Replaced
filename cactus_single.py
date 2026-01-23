# set_world_size(8)
s = get_world_size()
m = s - 1


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


# 记录每个位置的测量值
board = {}


def perform_insertion_sort():
    while True:
        v = measure()
        x, y = get_pos_x(), get_pos_y()
        board[(x, y)] = v
        vw = measure(West)
        vs = measure(South)

        cont = False
        if x != 0 and v < vw:  # type: ignore
            if y != 0 and vw < vs:  # type: ignore
                dir = South  # 和更大的一个交换，维持已有顺序
                board[(x, y - 1)] = v
                board[(x, y)] = vs
                if x - 1 >= 0 and y - 1 >= 0:
                    cont = cont or board[(x - 1, y - 1)] > v
                if y - 2 >= 0:
                    cont = cont or board[(x, y - 2)] > v
            else:
                dir = West
                board[(x - 1, y)] = v
                board[(x, y)] = vw
                if x - 1 >= 0 and y - 1 >= 0:
                    cont = cont or board[(x - 1, y - 1)] > v
                if x - 2 >= 0:
                    cont = cont or board[(x - 2, y)] > v
            swap(dir)
            if cont:  # 如果交换过去后仍不满足排序才移动过去
                move(dir)
            continue
        if y != 0 and v < vs:  # type: ignore
            if x != 0 and vs < vw:  # type: ignore
                dir = West
                board[(x - 1, y)] = v
                board[(x, y)] = vw
                if x - 1 >= 0 and y - 1 >= 0:
                    cont = cont or board[(x - 1, y - 1)] > v
                if x - 2 >= 0:
                    cont = cont or board[(x - 2, y)] > v
            else:
                dir = South
                board[(x, y - 1)] = v
                board[(x, y)] = vs
                if x - 1 >= 0 and y - 1 >= 0:
                    cont = cont or board[(x - 1, y - 1)] > v
                if y - 2 >= 0:
                    cont = cont or board[(x, y - 2)] > v
            swap(dir)
            if cont:
                move(dir)
            continue
        break


def perform_insertion_sort_last_few():
    while True:
        v = measure()
        x, y = get_pos_x(), get_pos_y()
        vw = measure(West)
        vs = measure(South)

        cont = False
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
        use_item(Items.Water)
        use_item(Items.Water)
        break


def perform_insertion_sort_last_one():
    while True:
        v = measure()
        x, y = get_pos_x(), get_pos_y()
        vw = measure(West)
        vs = measure(South)

        cont = False
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
        while not can_harvest():
            # 水量充足后不再花 200 tick 浇水，转而只用 2 tick 做判断
            if get_water() < 0.75:
                use_item(Items.Water)
        break


last_few = m * 2 - 1  # 最后几个浇水快速成长
last_one = m * 2  # 等待最后一个成熟
for i in range(s * 2):
    for j in range(i + 1):
        # 走一个 x + y = i 形状的对角线，左下角是排好序的
        if j > m or i - j > m:
            continue
        move_to((j, i - j))
        till()
        plant(Entities.Cactus)
        if i == last_one:
            perform_insertion_sort_last_one()
        elif i >= last_few:
            perform_insertion_sort_last_few()
        else:
            perform_insertion_sort()

harvest()
