# set_world_size(8)
s = get_world_size()
m = s - 1
n = s - 2


def traverse_rectangle(fn):
    # traverse_rectangle 针对 8 x 8 的性能优化版
    if fn():
        return False
    move(North)
    for i in range(0, s, 2):
        for j in range(m):
            if fn():
                return False
            if j != n:
                move(North)
        move(East)
        for j in range(m):
            if fn():
                return False
            if j != n:
                move(South)
        if i != n:
            move(East)
    move(South)
    for _ in range(m):
        if fn():
            return False
        move(West)

    return True  # loop continues

def traverse_rectangle_no_if(fn):
    fn()
    move(North)
    for i in range(0, s, 2):
        for j in range(m):
            fn()
            if j != n:
                move(North)
        move(East)
        for j in range(m):
            fn()
            if j != n:
                move(South)
        if i != n:
            move(East)
    move(South)
    for _ in range(m):
        fn()
        move(West)



wants = {}  # 记录种植需求


def is_tree_pos(p):
    x, y = p
    return (x + y) % 2 == 0


def on_eachcell():
    t = (get_pos_x(), get_pos_y())

    if get_water() < 0.15:
        # 访问间隔挺长的，不需要太多水
        use_item(Items.Water)

    if t in wants:
        # 满足当前位置的种植需求
        c = wants.pop(t)
        if get_entity_type() != c:
            harvest()
            if plant(c):
                return
            plant(Entities.Bush) # may failed at Carrot with no enough resource

        return

    if is_tree_pos(t):
        while True:
            harvest()
            plant(Entities.Tree)
            c, p = get_companion()
            if is_tree_pos(p):
                continue  #  和树的位置冲突
            if p in wants and wants[p] != c:
                continue  # 和其他植物的请求种植的冲突
            wants[p] = c  # 标记格子接下来要种植的作物
            break
    else:
        while True:
            harvest()
            plant(Entities.Bush)
            c, p = get_companion()
            if is_tree_pos(p):
                if c == Entities.Tree:
                    break
                continue  #  和树的位置冲突
            if p in wants and wants[p] != c:
                continue  # 和其他植物的请求种植的冲突
            wants[p] = c  # 标记格子接下来要种植的作物
            break


def first_round():
    till()
    on_eachcell()


def while_round():
    on_eachcell()
    return num_items(Items.Wood) >= 500000000


traverse_rectangle_no_if(first_round)
for _ in range(34): # 需要约 37 轮能够收集到足够的木头
    traverse_rectangle_no_if(on_eachcell)
while traverse_rectangle(while_round):
    continue
