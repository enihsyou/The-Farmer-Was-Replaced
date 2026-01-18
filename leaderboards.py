def run_leaderboard_dianosaus():
    leaderboard_run(Leaderboards.Dinosaur, "dianosaus", 40960)


def run_leaderboard_hay_single():
    leaderboard_run(Leaderboards.Hay_Single, "hay_single", 40960)


def run_leaderboard_carrots_single():
    leaderboard_run(Leaderboards.Carrots_Single, "carrots_single", 40960)


if __name__ == "__main__":
    run_leaderboard_carrots_single()
