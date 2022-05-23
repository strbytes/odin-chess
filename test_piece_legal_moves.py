import pytest
from board import *
from pieces import *


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


@pytest.fixture
def board_two_pawns_en_passant(board_one_pawn):
    board_one_pawn.add_piece(Pawn(board_one_pawn, "black"), "e4")
    black_pawn = board_one_pawn.board["e4"]
    black_pawn.board.board["e4"].moved = True
    return board_one_pawn


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

    def test_en_passant(self, board_two_pawns_en_passant):
        white_pawn = board_two_pawns_en_passant.board["d2"]
        black_pawn = board_two_pawns_en_passant.board["e4"]
        board_two_pawns_en_passant.move_piece(white_pawn, "d4")
        white_pawn.just_double_stepped = True
        assert black_pawn.legal_moves == ["e3", "d3"]


@pytest.fixture
def board_two_knights(board):
    board.add_piece(Knight(board, "white"), "c5")
    board.add_piece(Knight(board, "black"), "f5")
    for i in range(8):
        board.add_piece(Pawn(board, "black"), ALGEBRAIC_X[i] + "7")
    return board


class TestKnight:
    def test_knight(self, board_two_knights):
        white_knight = board_two_knights.board["c5"]
        black_knight = board_two_knights.board["f5"]
        assert white_knight.legal_moves == [
            "a4",
            "a6",
            "b3",
            "b7",
            "d3",
            "d7",
            "e4",
            "e6",
        ]
        assert black_knight.legal_moves == [
            "d4",
            "d6",
            "e3",
            "e7",
            "g3",
            "g7",
            "h4",
            "h6",
        ]


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
            "h7",
            "g4",
            "h3",
            "e4",
            "d3",
            "c2",
            "b1",
            "e6",
            "d7",
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
            "f7",
            "e5",
            "d5",
            "c5",
            "f4",
            "f3",
            "f2",
            "f1",
        ]

        # TODO test castling


@pytest.fixture
def board_two_queens(board):
    board.add_piece(Queen(board, "white"), "c5")
    board.add_piece(Queen(board, "black"), "f5")
    for i in range(8):
        board.add_piece(Pawn(board, "black"), ALGEBRAIC_X[i] + "7")
    return board


class TestQueen:
    def test_queen(self, board_two_queens):
        white_queen = board_two_queens.board["c5"]
        black_queen = board_two_queens.board["f5"]
        assert white_queen.legal_moves == [
            "b4",
            "a3",
            "b5",
            "a5",
            "b6",
            "a7",
            "c4",
            "c3",
            "c2",
            "c1",
            "c6",
            "c7",
            "d4",
            "e3",
            "f2",
            "g1",
            "d5",
            "e5",
            "f5",
            "d6",
            "e7",
        ]
        assert black_queen.legal_moves == [
            "e4",
            "d3",
            "c2",
            "b1",
            "e5",
            "d5",
            "c5",
            "e6",
            "d7",
            "f4",
            "f3",
            "f2",
            "f1",
            "f6",
            "f7",
            "g4",
            "h3",
            "g5",
            "h5",
            "g6",
            "h7",
        ]


@pytest.fixture
def board_two_kings(board):
    board.add_piece(King(board, "white"), "c4")
    board.add_piece(King(board, "black"), "f6")
    for i in range(8):
        board.add_piece(Pawn(board, "black"), ALGEBRAIC_X[i] + "7")
    return board


@pytest.fixture
def board_white_backline(board):
    board.add_piece(Rook(board, "white"), "a1")
    board.add_piece(Knight(board, "white"), "b1")
    board.add_piece(Bishop(board, "white"), "c1")
    board.add_piece(Queen(board, "white"), "d1")
    board.add_piece(King(board, "white"), "e1")
    board.add_piece(Bishop(board, "white"), "f1")
    board.add_piece(Knight(board, "white"), "g1")
    board.add_piece(Rook(board, "white"), "h1")
    return board


class TestKing:
    def test_two_kings(self, board_two_kings):

        white_king = board_two_kings.board["c4"]
        black_king = board_two_kings.board["f6"]
        assert white_king.legal_moves == [
            "b3",
            "b4",
            "b5",
            "c3",
            "c5",
            "d3",
            "d4",
            "d5",
        ]
        assert black_king.legal_moves == [
            "e5",
            "e6",
            "e7",
            "f5",
            "f7",
            "g5",
            "g6",
            "g7",
        ]

    def test_castle_no_check(self, board_white_backline):
        qside = {
            "rook": board_white_backline.board["a1"],
            "knight": board_white_backline.board["b1"],
            "bishop": board_white_backline.board["c1"],
            "queen": board_white_backline.board["d1"],
        }
        kside = {
            "king": board_white_backline.board["e1"],
            "bishop": board_white_backline.board["f1"],
            "knight": board_white_backline.board["g1"],
            "rook": board_white_backline.board["h1"],
        }
        assert kside["king"].can_castle == {}
        board_white_backline.remove_piece(qside["knight"])
        board_white_backline.remove_piece(qside["bishop"])
        assert kside["king"].can_castle == {}
        board_white_backline.remove_piece(qside["queen"])
        assert list(kside["king"].can_castle.keys()) == ["queenside"]
        board_white_backline.remove_piece(kside["knight"])
        board_white_backline.remove_piece(kside["bishop"])
        assert list(kside["king"].can_castle.keys()) == ["queenside", "kingside"]
        qside["rook"].moved = True
        assert list(kside["king"].can_castle.keys()) == ["kingside"]
        kside["rook"].moved = True
        assert kside["king"].can_castle == {}
        qside["rook"].moved = False
        kside["rook"].moved = False
        kside["king"].moved = True
        assert kside["king"].can_castle == {}
