from _pytest.assertion import pytest_addoption
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
        black_bishop.move("e2")
        assert (
            board.board["e2"] == black_bishop
        ), "black bishop should be at e2 after move"
        white_bishop.move("e2")
        assert (
            board.board["e2"] == white_bishop
        ), "white bishop should be at e2 after move"
        assert (
            black_bishop in board.removed
        ), "black bishop should be removed after being taken"


@pytest.fixture
def board_knight_and_pawns(board_white_pawns):
    board_white_pawns.add_piece(wk := Knight(board_white_pawns, "white"), "b1")
    board_white_pawns.add_piece(bk := Knight(board_white_pawns, "black"), "d5")
    return {"board": board_white_pawns, "white_knight": wk, "black_knight": bk}


class TestKnight:
    def test_knight(self, board_knight_and_pawns):
        board = board_knight_and_pawns["board"]
        white_knight = board_knight_and_pawns["white_knight"]
        black_knight = board_knight_and_pawns["black_knight"]
        white_knight.move("c3")
        black_knight.move("c3")
        assert board.board["c3"] == black_knight
        assert white_knight in board.removed


@pytest.fixture
def board_rooks_and_pawns(board_white_pawns):
    board_white_pawns.add_piece(wr := Rook(board_white_pawns, "white"), "h1")
    board_white_pawns.add_piece(br := Rook(board_white_pawns, "black"), "h4")
    return {"board": board_white_pawns, "white_rook": wr, "black_rook": br}


class TestRook:
    def test_rook(self, board_rooks_and_pawns):
        board = board_rooks_and_pawns["board"]
        white_rook = board_rooks_and_pawns["white_rook"]
        black_rook = board_rooks_and_pawns["black_rook"]
        black_rook.move("h2")
        assert board.board["h2"] == black_rook, "black rook should be at h2 after move"
        white_rook.move("h2")
        assert board.board["h2"] == white_rook, "white rook should be at h2 after move"
        assert (
            black_rook in board.removed
        ), "black rook should be removed after being taken"


@pytest.fixture
def board_queens_and_pawns(board_white_pawns):
    board_white_pawns.add_piece(wq := Queen(board_white_pawns, "white"), "d1")
    board_white_pawns.add_piece(bq := Queen(board_white_pawns, "black"), "d4")
    return {"board": board_white_pawns, "white_queen": wq, "black_queen": bq}


class TestQueen:
    def test_queen(self, board_queens_and_pawns):
        board = board_queens_and_pawns["board"]
        white_queen = board_queens_and_pawns["white_queen"]
        black_queen = board_queens_and_pawns["black_queen"]
        black_queen.move("d2")
        assert (
            board.board["d2"] == black_queen
        ), "black queen should be at d2 after move"
        white_queen.move("d2")
        assert (
            board.board["d2"] == white_queen
        ), "white queen should be at d2 after move"
        assert (
            black_queen in board.removed
        ), "black queen should be removed after being taken"


def test_threatened_squares(board_white_pawns):
    assert not board_white_pawns.threatened_squares[
        "white"
    ], "expect no threatened squares for white on a board with no black pieces"
    for square in [col + "3" for col in ALGEBRAIC_X]:
        assert (
            square in board_white_pawns.threatened_squares["black"]
        ), f"expected {square} in threatened squares for black"


@pytest.fixture
def board_kings_and_pawns(board_white_pawns):
    board_white_pawns.add_piece(wk := King(board_white_pawns, "white"), "e1")
    board_white_pawns.add_piece(bk := King(board_white_pawns, "black"), "e4")
    return {"board": board_white_pawns, "white_king": wk, "black_king": bk}


@pytest.fixture
def board_white_all(board_white_pawns):
    board_white_pawns.add_piece(qr := Rook(board_white_pawns, "white"), "a1")
    board_white_pawns.add_piece(qk := Knight(board_white_pawns, "white"), "b1")
    board_white_pawns.add_piece(qb := Bishop(board_white_pawns, "white"), "c1")
    board_white_pawns.add_piece(q := Queen(board_white_pawns, "white"), "d1")
    board_white_pawns.add_piece(k := King(board_white_pawns, "white"), "e1")
    board_white_pawns.add_piece(kb := Bishop(board_white_pawns, "white"), "f1")
    board_white_pawns.add_piece(kk := Knight(board_white_pawns, "white"), "g1")
    board_white_pawns.add_piece(kr := Rook(board_white_pawns, "white"), "h1")
    return {
        "board": board_white_pawns,
        "qrook": qr,
        "qknight": qk,
        "qbishop": qb,
        "queen": q,
        "king": k,
        "kbishop": kb,
        "kknight": kk,
        "krook": kr,
    } | {f"p{i}": board_white_pawns.board[ALGEBRAIC_X[i] + "2"] for i in range(8)}


class TestKing:
    def test_move(self, board_kings_and_pawns):
        board = board_kings_and_pawns["board"]
        white_king = board_kings_and_pawns["white_king"]
        black_king = board_kings_and_pawns["black_king"]
        white_king.move("d1")
        assert board.pieces[white_king] == "d1"
        black_king.move("d4")
        assert board.pieces[black_king] == "d4"
        with pytest.raises(AssertionError) as e:
            black_king.move("d3")
        assert "cannot move into check" in str(e.value)
