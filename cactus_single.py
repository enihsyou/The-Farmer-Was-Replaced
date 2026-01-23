# set_world_size(8)
s = get_world_size()
m = s - 1


def move_to(tx, ty):
    cx, cy = get_pos_x(), get_pos_y()

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


# 记录每个位置的测量值
board = {}


def perform_insertion_sort():
    while True:
        v = measure()
        x, y = get_pos_x(), get_pos_y()

        if x > 0:
            vw = measure(West)
            if v < vw:  # ty: ignore
                vs = measure(South)
                if y > 0 and vw < vs:  # ty: ignore
                    board[(x, y - 1)] = v
                    board[(x, y)] = vs
                    swap(South)
                    # 判断移动到下一个位置后，是否还需要继续交换
                    if (
                        board[(x - 1, y - 1)] > v  # 还能和左边交换
                    ) or (
                        y > 1 and board[(x, y - 2)] > v  # 还能和下面交换
                    ):
                        move(South)
                    else:
                        break
                else:
                    board[(x - 1, y)] = v
                    board[(x, y)] = vw
                    swap(West)
                    if (
                        y > 0 and board[(x - 1, y - 1)] > v  # 还能和下面交换
                    ) or (
                        x > 1 and board[(x - 2, y)] > v  # 还能和左边交换
                    ):
                        move(West)
                    else:
                        break
                continue

        if y > 0:
            vs = measure(South)
            if v < vs:  # ty: ignore
                if x > 0 and vs < vw:  # ty: ignore
                    board[(x - 1, y)] = v
                    board[(x, y)] = vw
                    swap(West)
                    if (
                        board[(x - 1, y - 1)] > v  # 还能和下面交换
                    ) or (
                        x > 1 and board[(x - 2, y)] > v  # 还能和左边交换
                    ):
                        move(West)
                    else:
                        break
                else:
                    board[(x, y - 1)] = v
                    board[(x, y)] = vs
                    swap(South)
                    if (
                        x > 0 and board[(x - 1, y - 1)] > v  # 还能和左边交换
                    ) or (
                        y > 1 and board[(x, y - 2)] > v  # 还能和下面交换
                    ):
                        move(South)
                    else:
                        break
                continue

        board[(x, y)] = v
        break


def perform_insertion_sort_last_few():
    while True:
        v = measure()
        x, y = get_pos_x(), get_pos_y()

        if x > 0:
            vw = measure(West)
            if v < vw:  # ty: ignore
                vs = measure(South)
                if y > 0 and vw < vs:  # ty: ignore
                    dir = South  # 和更大的一个交换，维持已有顺序
                else:
                    dir = West
                swap(dir)
                move(dir)
                continue

        if y > 0:
            vs = measure(South)
            if v < vs:  # ty: ignore
                if x > 0 and vs < vw:  # ty: ignore
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

        if x > 0:
            vw = measure(West)
            if v < vw:  # ty: ignore
                vs = measure(South)
                if y > 0 and vw < vs:  # ty: ignore
                    dir = South  # 和更大的一个交换，维持已有顺序
                else:
                    dir = West
                swap(dir)
                move(dir)
                continue

        if y > 0:
            vs = measure(South)
            if v < vs:  # ty: ignore
                if x > 0 and vs < vw:  # ty: ignore
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


last_one = m * 2  # 等待最后一个成熟
last_few = last_one - 1  # 最后几个浇水快速成长
for i in range(s * 2):
    for j in range(i + 1):
        # 走一个 x + y = i 形状的对角线，左下角是排好序的
        if j > m or i - j > m:
            continue
        move_to(j, i - j)
        till()
        plant(Entities.Cactus)
        if i == last_one:
            perform_insertion_sort_last_one()
        elif i >= last_few:
            perform_insertion_sort_last_few()
        else:
            perform_insertion_sort()

harvest()
