from chess import *
import pytest


@pytest.fixture
def new_game():
    g = Game()
    players = [
        g.board.players["white"],
        g.board.players["black"],
    ]
    return g, g.board, *players


def test_fixture(new_game):
    game, board, white, black = new_game
    assert isinstance(game, Game)
    assert isinstance(board, Board)
    assert isinstance(white, Player)
    assert isinstance(black, Player)
