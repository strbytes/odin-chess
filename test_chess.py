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


def test_pawn(new_game):
    game, board, white, black = new_game
    # test white pawn double step
    game.play_turn("d4")
    assert isinstance(board["d4"], Pawn)
    assert (
        board["d4"].double_step == 0
    ), f"{board['d4']} should have double_step set on turn 0"
    # test white pawn double step
    game.play_turn("c5")
    assert isinstance(board["c5"], Pawn)
    assert (
        board["c5"].double_step == 1
    ), f"{board['c5']} should have double_step set on turn 1"
    # set up for en passant
    game.play_turn("d5")
    game.play_turn("e5")
    # should be able to take e5 en passant, but not c5
    assert board["d5"].legal_moves == [
        (3, 5),
        (4, 5),
    ], f"{board['d5']} should have option to take en-passant"
    assert board["e5"].legal_moves == [
        (4, 3)
    ], f"{board['e5']} should only have forward step available"
    assert board["c5"].legal_moves == [
        (2, 3)
    ], f"{board['c5j']} should only have forward step available"
    game.play_turn("e6")
    assert black["pawn_4"] in black.removed, f"{black['pawn_4']} should be removed"
    game.play_turn("c4")
    game.play_turn("e7")
    game.play_turn("c3")
    assert board["c3"].legal_moves == [(1, 1)]
