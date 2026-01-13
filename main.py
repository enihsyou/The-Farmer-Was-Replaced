import ground
from library import *


def harvest_hay():
    import hay

    move_2d_torus(zeroing_position)
    hay.harvest_hays(WORLD_SIZE, WORLD_SIZE)


def harvest_wood():
    import wood

    move_2d_torus(zeroing_position)
    wood.harvest_woods(WORLD_SIZE, WORLD_SIZE)


def harvest_carrot():
    import carrot

    move_2d_torus(zeroing_position)
    ground.soil_ground(WORLD_SIZE, WORLD_SIZE)
    carrot.harvest_carrots(WORLD_SIZE, WORLD_SIZE)


def harvest_pumpkin():
    import pumpking

    move_2d_torus(zeroing_position)
    ground.soil_ground(WORLD_SIZE, WORLD_SIZE)
    pumpking.harvest_pumpkins(6)


def harvest_sunflower():
    import sunflower

    move_2d_torus(zeroing_position)
    sunflower.harvest_sunflowers(WORLD_SIZE, WORLD_SIZE)


def harvest_cactus():
    import cactus

    move_2d_torus(zeroing_position)
    ground.soil_ground(WORLD_SIZE, WORLD_SIZE)
    cactus.harvest_cactus(WORLD_SIZE, WORLD_SIZE)


def main_loop():
    while True:
        targets = [
            (Items.Hay, Entities.Grass, 20000, harvest_hay),
            (Items.Wood, Entities.Tree, 20000, harvest_wood),
            (Items.Carrot, Entities.Carrot, 20000, harvest_carrot),
            (Items.Pumpkin, Entities.Pumpkin, 30000, harvest_pumpkin),
            (Items.Power, Entities.Sunflower, 100, harvest_sunflower),
            (Items.Cactus, Entities.Cactus, 20000, harvest_cactus),
        ]

        for target in targets:
            item, corp, threshold, action = target
            need_items = get_cost(corp) or {}
            have_items = set()
            while num_items(item) < threshold:
                for need_item in need_items:
                    if num_items(need_item) > need_items[need_item]:
                        have_items.add(need_item)
                if len(need_items) != len(have_items):
                    print("Not enough resources for", corp)
                    break
                action()


def test_run():
    pass


test_run()
