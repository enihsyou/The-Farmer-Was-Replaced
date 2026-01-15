from library import *


def harvest_hays(w, h):
    def plant_and_harvest():
        if can_harvest():
            harvest()
        if get_entity_type() != Entities.Grass:
            plant(Entities.Grass)

    traverse_rectangle(plant_and_harvest, w, h)


def poly_hays():
    def plant_bush():
        if get_entity_type() != Entities.Bush:
            harvest()
        if get_entity_type() != Entities.Bush:
            plant(Entities.Bush)

    # 用灌木占满空间
    move_2d_torus(zeroing_position)
    traverse_rectangle(plant_bush, WORLD_SIZE, WORLD_SIZE)
    world_center = (HALF_WORLD_SIZE, HALF_WORLD_SIZE)
    loop = [South, West, North, East]
    core_locations = []
    position = world_center
    for dir in loop:
        position = adjecent_coordination(position, dir)
        core_locations.append(position)

    move_2d_torus(world_center)
    while True:
        for dir in loop:
            if get_entity_type() != Entities.Grass:
                plant(Entities.Grass)
            if can_harvest():
                harvest()
            companion, pos = get_companion()  # type: ignore
            while companion != Entities.Bush or pos in core_locations:
                plant(Entities.Grass)
                companion, pos = get_companion()  # type: ignore
            while get_water() < 0.75 and num_items(Items.Water) > 0:
                use_item(Items.Water)
            move(dir)


if __name__ == "__main__":
    poly_hays()
