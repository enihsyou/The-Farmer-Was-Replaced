set_world_size(8)
s = get_world_size()
wants = {}  # 记录种植需求


def pos_index(x, y):
    return x * s + y


def eachcell(fn):
    for i in range(s):
        for j in range(s):
            if get_ground_type() != Grounds.Soil:
                till()
            fn()
            move(North)
        move(East)
    while True:
        for i in range(s):
            for j in range(s):
                fn()
                if num_items(Items.Carrot) > 100000000:
                    return
                move(North)
            move(East)


def on_eachcell():
    t = (get_pos_x(), get_pos_y())

    while get_water() < 0.8:
        use_item(Items.Water)

    if t in wants:
        # 满足当前位置的种植需求
        c = wants.pop(t)
        if get_entity_type() != c:
            harvest()
            plant(c)
        return

    while True:
        harvest()
        plant(Entities.Carrot)
        c, p = get_companion()
        if p in wants and wants[p] != c:
            continue  # 和其他植物的请求种植的冲突
        wants[p] = c  # 标记格子接下来要种植的作物
        break


eachcell(on_eachcell)
