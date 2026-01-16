from __builtins__ import North, get_pos_x, num_items, quick_print


def harvest_dianosaus():
    # https://www.reddit.com/r/TheFarmerWasReplaced/comments/1o90hxs/my_sna_i_mean_dinosaur_algorithm/
    change_hat(Hats.Dinosaur_Hat)
    cycle_loop()
    change_hat(Hats.Brown_Hat)


def cycle_loop():
    s = get_world_size()
    m = s - 1
    l = s * s // 2

    dir = East
    snake = 0
    while True:
        x, y = get_pos_x(), get_pos_y()
        if get_entity_type() == Entities.Apple:
            snake += 1
            wx, wy = measure()  # type: ignore

        # 不留缝隙地占满空间，强迫果子生成在前方，提速 10%
        if snake > l:
            if can_move(North) and y == 0 and x % 2 == 1:
                for _ in range(m - 1):  # 避开最北的一行
                    move(North)
                continue

        # 访问中心区域的果子
        if x != 0 and x != m:  # 不在左右两侧
            if (x == wx or x + 1 == wx) and x % 2 == 1:
                if can_move(North) and wy > y and wy != m:  # 向北可以到达苹果
                    for _ in range(wy - y):
                        move(North)
                    continue
            if (x == wx or x - 1 == wx) and x % 2 == 0:
                if can_move(South) and y > wy and wy != 0:  # 向南可以前往苹果
                    for _ in range(y - wy):
                        move(South)
                    continue

        # 围着操场逆时针转圈
        if dir == East:
            if y != 0 and can_move(South):
                move(South)  # 回归边线
                continue
            if x == m:
                dir = North  # 在边界转向
            if not move(dir):  # 碰到边界或尾巴，向有空间的方向前进
                if not move(North):
                    break
            continue
        if dir == West:
            if y != m and can_move(North):
                move(North)  # 回归边线
                continue
            if x == 0:
                dir = South  # 在边界转向
            if not move(dir):  # 碰到边界或尾巴，向有空间的方向前进
                if not move(South):
                    break
            continue
        if dir == South:
            if x != 0 and can_move(West):
                move(West)  # 回归边线
                continue
            if x == 0 and y != 0:
                while move(dir) and get_entity_type() != Entities.Apple:
                    pass  # 边界上走直线，避免循环顶层大 while
                continue
            dir = East  # 在边界转向
            continue
        if dir == North:
            if x != m and can_move(East):
                move(East)  # 回归边线
                continue
            if x == m and y != m:
                while move(dir) and get_entity_type() != Entities.Apple:
                    pass  # 边界上走直线，避免循环顶层大 while
                continue
            dir = West  # 在边界转向
            continue


if __name__ == "__main__":
    set_world_size(8)
    b = num_items(Items.Bone)
    harvest_dianosaus()
    a = num_items(Items.Bone)
    h = a - b
    quick_print("Harvest Bones", h, "is Done?", h >= 33488928)
