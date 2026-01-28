def run_leaderboard_dianosaus():
    leaderboard_run(Leaderboards.Dinosaur, "dianosaus", 40960)


def run_leaderboard_hay():
    leaderboard_run(Leaderboards.Hay, "hay", 4096)


def run_leaderboard_hay_single():
    leaderboard_run(Leaderboards.Hay_Single, "hay_single", 40960)


def run_leaderboard_wood_single():
    leaderboard_run(Leaderboards.Wood_Single, "wood_single", 40960)


def run_leaderboard_carrots_single():
    leaderboard_run(Leaderboards.Carrots_Single, "carrots_single", 40960)


def run_leaderboard_cactus_single():
    leaderboard_run(Leaderboards.Cactus_Single, "cactus_single", 40960)


def run_leaderboard_pumpkins_single():
    leaderboard_run(Leaderboards.Pumpkins_Single, "pumpkins_single", 40960)


def run_leaderboard_sunflowers_single():
    leaderboard_run(Leaderboards.Sunflowers_Single, "sunflowers_single", 40960)


def simulate_leaderboard(filename, sim_items, sim_globals):
    runtimes = []
    runtimes_sum = 0
    for _ in range(5):
        runtime = simulate(filename, Unlocks, sim_items, sim_globals, 0, 40960)
        runtimes.append(runtime)
        runtimes_sum += runtime
        quick_print(runtime, sim_globals)
    quick_print(
        sim_globals,
        "max",
        max(runtimes),
        "min",
        min(runtimes),
        "avg",
        runtimes_sum / len(runtimes),
    )


def simulate_leaderboard_sunflowers_single():
    sim_items = {Items.Carrot: 1000000000}
    for water_level in range(0.6, 0.8, 0.01):
        sim_globals = {"W": water_level}
        simulate_leaderboard("sunflowers_single", sim_items, sim_globals)


if __name__ == "__main__":
    run_leaderboard_hay()
