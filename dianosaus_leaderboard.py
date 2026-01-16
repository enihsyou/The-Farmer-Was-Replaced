from __builtins__ import Leaderboard, leaderboard_run


def run_simulate():
    filename = "dianosaus"
    sim_unlocks = Unlocks
    sim_items = {Items.Cactus : 1000000000, Items.Power: 1000000000}
    sim_globals = {}
    seed = 0
    speedup = 64
    run_time = simulate(filename, sim_unlocks, sim_items, sim_globals, seed, speedup)
    print(run_time)


def run_leaderboard():
    leaderboard_run(Leaderboards.Dinosaur, "dianosaus", 1024)


if __name__ == "__main__":
    # run_simulate()
    run_leaderboard()
