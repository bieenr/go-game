from sente import stone


def score(game):
    """
        Score of black and white at the current state
        args: None
        return:
            black_score, white_score
    """
    num_pass = 0
    try:
        game.pss()
        num_pass += 1
        game.pss()
        num_pass += 1
    except:
        pass
    for _ in range(num_pass):
        game.step_up()
    return game.score()[stone.BLACK] - game.score()[stone.WHITE]