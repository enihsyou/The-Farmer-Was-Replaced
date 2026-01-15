from library import *


def is_tree_position(position):
    x, y = position
    return is_even(x + y)


def harvest_woods(w, h):
    def plant_and_harvest():
        if can_harvest():
            harvest()
        if is_tree_position(current_position()):
            plant(Entities.Tree)
        else:
            plant(Entities.Bush)

    traverse_rectangle(plant_and_harvest, w, h)


def poly_woods():
    def plant_tree():
        if is_tree_position(current_position()):
            if get_ground_type() != Grounds.Soil:
                till()
            # if get_entity_type() == Entities.Tree:
            #     # 确保已长成
            #     if not can_harvest():
            #         use_item(Items.Fertilizer) # 十字形布局不影响周边植物
            #         use_item(Items.Fertilizer) # 抵消奇异物质
            while True:
                harvest()
                plant(Entities.Tree)
                companion, pos = get_companion()  # type: ignore
                if not is_tree_position(pos) and companion == Entities.Grass:
                    break
            while get_water() < 0.75 and num_items(Items.Water) > 0:
                use_item(Items.Water)
        # else:
        #     while True:
        #         harvest()
        #         companion, pos = get_companion()
        #         if is_tree_position(pos) and companion == Entities.Tree:
        #             break
    move_2d_torus(zeroing_position)
    traverse_rectangle(plant_tree, 3, 3)


if __name__ == "__main__":
    clear()
    while True:
        poly_woods()
