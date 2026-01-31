def traverse_rectangle(fn, w, h):
    fn()
    move(North)
    for i in range(w, 0, -2):
        for j in range(h, 1, -1):
            fn()
            if j != 2:
                move(North)
        move(East)
        for j in range(h, 1, -1):
            fn()
            if j != 2:
                move(South)
        if i != 2:
            move(East)
    move(South)
    for _ in range(1, w):
        fn()
        move(West)


def is_tree_pos(p):
    x, y = p
    return (x + y) % 2 == 0


# 4 x 8 区域中第 0, 2 列种树
def work_drone_task():
    wants = {}

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
                plant(Entities.Bush)  # may failed at Carrot with no enough resource
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

    traverse_rectangle(first_round, 4, 8)
    while True:
        traverse_rectangle(while_round, 4, 8)


clear()
set_world_size(8)
work_drone_task()
