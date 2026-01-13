from library import *

def harvest_weird(w, h):
    clear()
    move_2d_torus((1, 1))
    use_item(Items.Weird_Substance)


if __name__ == "__main__":
    harvest_weird(WORLD_SIZE, WORLD_SIZE)
