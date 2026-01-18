from __builtins__ import Entities, can_harvest, harvest

dirs = [North, East, South, West]

for dir in dirs:
    till()
    plant(Entities.Carrot)
    move(dir)

i = 0
while num_items(Items.Carrot) < 100000000:
    if can_harvest():
        while True:
            harvest()
            plant(Entities.Carrot)
            c, _ = get_companion()  # type: ignore
            if c == Entities.Grass:
                break

    if can_harvest():
        continue
    if get_water() < 0.95:
        use_item(Items.Water)

    move(dirs[i % 4])
    i += 1
