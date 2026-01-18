for i in range(8):
    till()
    plant(Entities.Carrot)
    move(East)

while num_items(Items.Carrot) < 100000000:
    if can_harvest():
        while True:
            harvest()
            plant(Entities.Carrot)
            c, p = get_companion()  # type: ignore
            if c == Entities.Grass and p[1] != 0:
                break

    if get_water() < 0.95:
        use_item(Items.Water)

    move(East)
