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


last_one = m * 2  # 等待最后一个成熟
last_few = last_one - 1  # 最后几株先种再排序
for i in range(last_few):
    for j in range(min(i + 1, s)):
        # 走一个 x + y = i 形状的对角线，左下角是排好序的
        if i - j > m:
            continue
        move_to(j, i - j)
        till()
        plant(Entities.Cactus)
        perform_insertion_sort()


move_to(m, m - 1)
use_item(Items.Fertilizer)
harvest()  # harvest weird substance

till()
plant(Entities.Cactus)
use_item(Items.Fertilizer)
move(West)
move(North)  # at (m - 1, m)
till()
plant(Entities.Cactus)
use_item(Items.Fertilizer)
move(East)  # at (m, m)
till()
plant(Entities.Cactus)
use_item(Items.Fertilizer)
use_item(Items.Weird_Substance)
move(South)  # at (m, m - 1)
perform_insertion_sort()
move_to(m - 1, m)
perform_insertion_sort()
move_to(m, m)
perform_insertion_sort()
# 最后几株生长时间大于排序时间就有几率失败
harvest()
