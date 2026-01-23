from __builtins__ import Entities, can_harvest, get_world_size, use_item, set_execution_speed
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
                companion, pos = get_companion()  # ty: ignore
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


def ploy_multidrone_woods():
    def plant_tree():
        if get_ground_type() != Grounds.Soil:
            till()
        while True:
            while True:
                harvest()
                plant(Entities.Tree)
                companion, pos = get_companion()  # ty: ignore
                x, y = pos
                if companion == Entities.Grass:
                    if y > 0 or not is_tree_position(pos):
                        break
            while get_water() < 0.75 and num_items(Items.Water) > 0:
                use_item(Items.Water)
            use_time = 0
            while not can_harvest():
                use_item(Items.Fertilizer)
                use_time = 1
            if use_time % 2 == 1:
                use_item(Items.Weird_Substance)

    def spawn_task():
        if is_tree_position(current_position()):
            spawn_drone(plant_tree)

    move_2d_torus(zeroing_position)
    traverse_rectangle(spawn_task, get_world_size(), 1)


if __name__ == "__main__":
    clear()
    ploy_multidrone_woods()
