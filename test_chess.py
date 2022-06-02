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


@pytest.fixture
def empty_board(new_game):
    game, board, white, black = new_game
    for p in white.pieces + black.pieces:
        board.remove_piece(p)
    return game, board, white, black


def test_empty_board(empty_board):
    game, board, white, black = empty_board
    for x in range(8):
        for y in range(8):
            assert board[x][y] == None


@pytest.fixture
def en_passant_setup(empty_board):
    game, board, white, black = empty_board
    board.add_piece(white["king"], (0, 0))
    board.add_piece(black["king"], (7, 3))
    board.add_piece(white["qrook"], (0, 3))
    board.add_piece(black["qbishop"], (7, 7))
    board.add_piece(white["pawn_1"], (4, 3))
    white["pawn_1"].moved = True
    white["pawn_1"].double_step = 0
    black["pawn_1"].moved = True
    black["pawn_1"].double_step = 0
    board.add_piece(black["pawn_1"], (3, 3))
    game.turn = 1
    return game, board, white, black


def test_en_passant_special_case(en_passant_setup):
    game, board, white, black = en_passant_setup
    breakpoint()
