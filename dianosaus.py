from __builtins__ import Entities, South, get_entity_type, get_pos_x, get_pos_y


def harvest_dianosaus():
    change_hat(Hats.Dinosaur_Hat)
    snake = 0
    snake = quick_loop()
    cycle_loop(snake)
    change_hat(Hats.Brown_Hat)


def quick_loop():
    # 直接走向目标，可能形成圈卡死
    s = get_world_size()
    l = s * 3 // 2  # 大于这个长度就换算法

    snake = 0
    while True:
        if get_entity_type() == Entities.Apple:
            snake += 1
            if snake > l:
                break  # make sure stop at the apple location
            wx, wy = measure()  # type: ignore
        while get_pos_x() < wx and move(East):
            continue  # 来替代 200 tick 的 pass 语句
        while get_pos_x() > wx and move(West):
            continue
        while get_pos_y() < wy and move(North):
            continue
        while get_pos_y() > wy and move(South):
            continue

        if get_entity_type() != Entities.Apple:
            x, y = get_pos_x(), get_pos_y()
            # 移动不到下一个苹果去，可能是新苹果生成在身后, 朝能走的方向前进，试试运气
            if x == wx and y != wy:
                if move(East):
                    continue
                if move(West):
                    continue
            if x != wx and y == wy:
                if move(North):
                    continue
                if move(South):
                    continue

            # stuck, bad luck, let's restart
            change_hat(Hats.Dinosaur_Hat)
            snake = 0
    return snake


def cycle_loop(snake):
    # 参照这个地址来实现
    # https://www.reddit.com/r/TheFarmerWasReplaced/comments/1o90hxs/my_sna_i_mean_dinosaur_algorithm/
    # 最后一个苹果生成在四边时有几率头尾卡在最后一步
    s = get_world_size()
    m = s - 1
    l = s * s // 2  # 大于这个长度就强制走汉密顿路径

    dir = East
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
                while move(South) and get_entity_type() != Entities.Apple:
                    continue  # 回归边线
                continue
            if x == m:
                dir = North  # 在边界转向
            if not move(dir):  # 碰到边界或尾巴，向有空间的方向前进
                if not move(North):
                    break
            continue
        if dir == West:
            if y != m and can_move(North):
                while move(North) and get_entity_type() != Entities.Apple:
                    continue  # 回归边线
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
                    continue  # 边界上走直线，避免循环顶层大 while
                if not (can_move(dir) or can_move(East)):
                    break  # 碰到尾巴
                continue
            dir = East  # 在边界转向
            continue
        if dir == North:
            if x != m and can_move(East):
                move(East)  # 回归边线
                continue
            if x == m and y != m:
                while move(dir) and get_entity_type() != Entities.Apple:
                    continue  # 边界上走直线，避免循环顶层大 while
                if not can_move(dir) and not can_move(West):
                    break  # 碰到尾巴
                continue
            dir = West  # 在边界转向
            continue


if __name__ == "__main__":
    # set_world_size(8)
    b = num_items(Items.Bone)
    harvest_dianosaus()
    a = num_items(Items.Bone)
    h = a - b
    quick_print("Harvest Bones", h, "is Done?", h >= 33488928)
