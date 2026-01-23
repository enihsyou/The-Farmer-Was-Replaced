# set_world_size(8)
from __builtins__ import can_harvest, change_hat
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


last_few = s * 2 - 3 # 最后三个浇水快速成长
for i in range(s * 2):
    for j in range(i + 1):
        # 走一个 x + y = i 形状的对角线，左下角是排好序的
        if j > m or i - j > m:
            continue
        move_to((j, i - j))
        till()
        plant(Entities.Cactus)
        perform_insertion_sort()
        if i >= last_few:
            use_item(Items.Water)

while not can_harvest():
    change_hat(Hats.Brown_Hat)  # 消耗时间等待长成
harvest()
