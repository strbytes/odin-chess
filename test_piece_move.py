from chess import *
import pytest


@pytest.fixture
def board_pawns():
    b = Board()
    b.add_piece(wp1 := Pawn(b, "white"), "b2")
    b.add_piece(bp1 := Pawn(b, "black"), "c3")
    b.add_piece(wp2 := Pawn(b, "white"), "f5")
    b.add_piece(bp2 := Pawn(b, "black"), "e7")
    b.add_piece(bp3 := Pawn(b, "black"), "g5")
    return {
        "board": b,
        "white_pawn_1": wp1,
        "black_pawn_1": bp1,
        "white_pawn_2": wp2,
        "black_pawn_2": bp2,
    }


class TestPawn:
    def test_pawn(self, board_pawns):
        board_pawns["white_pawn_1"].move("c3")
        assert board_pawns["board"].board["c3"] == board_pawns["white_pawn_1"]
        assert board_pawns["black_pawn_1"] in board_pawns["board"].removed
        assert board_pawns["black_pawn_1"] not in board_pawns["board"].pieces
        board_pawns["black_pawn_2"].move("e5")
        assert (
            "e6" in board_pawns["white_pawn_2"].legal_moves
        ), "black pawn just moved to e5 should trigger en passant move in white pawn at f5"
        assert (
            "d6" not in board_pawns["white_pawn_2"].legal_moves
        ), "black pawn at d5 (not just moved) should not trigger en passant move in white pawn at f5"
        board_pawns["white_pawn_2"].move("e6")
        assert board_pawns["board"].board["e6"] == board_pawns["white_pawn_2"]
        assert board_pawns["black_pawn_2"] in board_pawns["board"].removed
        assert board_pawns["black_pawn_2"] not in board_pawns["board"].pieces


@pytest.fixture
def board_white_pawns():
    b = Board()
    row = "2"
    for c in ALGEBRAIC_X:
        b.add_piece(Pawn(b, "white"), c + row)
    return b


@pytest.fixture
def board_bishops_and_pawns(board_white_pawns):
    board_white_pawns.add_piece(wb := Bishop(board_white_pawns, "white"), "f1")
    board_white_pawns.add_piece(bb := Bishop(board_white_pawns, "black"), "c4")
    return {"board": board_white_pawns, "white_bishop": wb, "black_bishop": bb}


class TestBishop:
    def test_bishop(self, board_bishops_and_pawns):
        board = board_bishops_and_pawns["board"]
        white_bishop = board_bishops_and_pawns["white_bishop"]
        black_bishop = board_bishops_and_pawns["black_bishop"]
        assert (
            len(white_bishop.legal_moves) == 0
        ), "white bishop behind pawns should have no legal moves"
        black_bishop.move("e2")
        assert (
            board.board["e2"] == black_bishop
        ), "black bishop should be at e2 after move"
        assert white_bishop.legal_moves == [
            "e2"
        ], "only legal move for white bishop should be e2"
        white_bishop.move("e2")
        assert (
            board.board["e2"] == white_bishop
        ), "white bishop should be at e2 after move"
        assert (
            "a6" in white_bishop.legal_moves
        ), "white bishop should be able to move across board after taking black bishop"
        assert (
            black_bishop in board.removed
        ), "black bishop should be removed after being taken"
