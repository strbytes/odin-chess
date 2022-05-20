import pytest
from chess import *


def test_translate_algebraic():
    assert translate_algebraic("a1", 7, 7) == "h8"
    assert translate_algebraic("h8", -7, -7) == "a1"
    assert translate_algebraic("a1", -1, -1) == None
    assert translate_algebraic("h8", 1, 1) == None


@pytest.fixture
def board():
    return Board()


@pytest.fixture
def board_one_pawn(board):
    board.add_piece(Pawn(board, "white"), "d2")
    return board


@pytest.fixture
def board_two_pawns(board_one_pawn):
    board_one_pawn.add_piece(Pawn(board_one_pawn, "black"), "e3")
    black_pawn = board_one_pawn.board["e3"]
    black_pawn.board.board["e3"].moved = True
    return board_one_pawn


@pytest.fixture
def board_three_pawns(board_two_pawns):
    board_two_pawns.add_piece(Pawn(board_two_pawns, "white"), "e2")
    return board_two_pawns


class TestPawn:
    def test_one_pawn(self, board_one_pawn):
        pawn = board_one_pawn.board["d2"]
        # checking starting moves available
        assert pawn.legal_moves == ["d3", "d4"], "expected legal moves d3 and d4"
        pawn.moved = True
        # checking moved flag prevents double step
        assert pawn.legal_moves == [
            "d3"
        ], "expected d3 to be only legal move after setting moved"
        board_one_pawn.move_piece(pawn, "d8")
        # checking no movement at end of board
        # (promotion to be handled by Game)
        assert pawn.legal_moves == [], "expected no legal moves at end of board"

    def test_two_pawns(self, board_two_pawns):
        white_pawn = board_two_pawns.board["d2"]
        black_pawn = board_two_pawns.board["e3"]
        # allows moves to take as well as basic moves
        assert white_pawn.legal_moves == [
            "d3",
            "d4",
            "e3",
        ], "expected starting moves + take option"
        # same but doesn't allow moving two spaces since moved is set
        assert black_pawn.legal_moves == [
            "e2",
            "d2",
        ], "expected basic move + take option"
        board_two_pawns.move_piece(black_pawn, "e2")
        # shows option for en-passant move
        assert white_pawn.legal_moves == [
            "d3",
            "d4",
            "e3",
        ], "expected starting moves + en passant option"
        assert black_pawn.legal_moves == [
            "e1",
            "d1",
        ], "expected basic move + en passant option"
        # checking no movement at end of board for black
        board_two_pawns.move_piece(black_pawn, "e1")
        assert black_pawn.legal_moves == []

    def test_three_pawns(self, board_three_pawns):
        white_pawn_d = board_three_pawns.board["d2"]
        white_pawn_e = board_three_pawns.board["e2"]
        black_pawn = board_three_pawns.board["e3"]
        assert white_pawn_d.legal_moves == [
            "d3",
            "d4",
            "e3",
        ], "expected starting moves + take option"
        assert white_pawn_e.legal_moves == [], "expected blocked pawn to have no moves"
        assert black_pawn.legal_moves == [
            "d2"
        ], "expected blocked pawn to have only one move"
        board_three_pawns.move_piece(white_pawn_d, "e3")
        assert white_pawn_e.legal_moves == [], "expected blocked pawn to have no moves"
        assert (
            black_pawn in board_three_pawns.removed
        ), "expected black pawn removed from board"


@pytest.fixture
def board_two_bishops(board):
    board.add_piece(Bishop(board, "white"), "c5")
    board.add_piece(Bishop(board, "black"), "f5")
    for i in range(8):
        board.add_piece(Pawn(board, "black"), ALGEBRAIC_X[i] + "7")
    return board


class TestBishop:
    def test_bishop(self, board_two_bishops):
        white_bishop = board_two_bishops.board["c5"]
        black_bishop = board_two_bishops.board["f5"]
        assert white_bishop.legal_moves == [
            "d6",
            "e7",
            "d4",
            "e3",
            "f2",
            "g1",
            "b4",
            "a3",
            "b6",
            "a7",
        ]
        assert black_bishop.legal_moves == [
            "g6",
            "g4",
            "h3",
            "e4",
            "d3",
            "c2",
            "b1",
            "e6",
        ]


@pytest.fixture
def board_two_rooks(board):
    board.add_piece(Rook(board, "white"), "c5")
    board.add_piece(Rook(board, "black"), "f5")
    for i in range(8):
        board.add_piece(Pawn(board, "black"), ALGEBRAIC_X[i] + "7")
    return board


class TestRook:
    def test_rook(self, board_two_rooks):
        white_rook = board_two_rooks.board["c5"]
        black_rook = board_two_rooks.board["f5"]
        assert white_rook.legal_moves == [
            "d5",
            "e5",
            "f5",
            "c6",
            "c7",
            "b5",
            "a5",
            "c4",
            "c3",
            "c2",
            "c1",
        ]
        assert black_rook.legal_moves == [
            "g5",
            "h5",
            "f6",
            "e5",
            "d5",
            "c5",
            "f4",
            "f3",
            "f2",
            "f1",
        ]

        # TODO test castling
