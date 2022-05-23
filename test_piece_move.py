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
    } | {
        f"p{ALGEBRAIC_X[i]}": board_white_pawns.board[ALGEBRAIC_X[i] + "2"]
        for i in range(8)
    }


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

    def test_castle_qside(self, board_white_all):
        board = board_white_all["board"]
        qrook = board_white_all["qrook"]
        qknight = board_white_all["qknight"]
        qbishop = board_white_all["qbishop"]
        queen = board_white_all["queen"]
        king = board_white_all["king"]
        with pytest.raises(ValueError) as e:
            king.castle("queenside")
        assert "cannot castle" in str(e.value)
        board.remove_piece(queen)
        board.remove_piece(qbishop)
        with pytest.raises(ValueError) as e:
            king.castle("queenside")
        assert "cannot castle" in str(e.value)
        board.remove_piece(qknight)
        board.add_piece(black_pawn := Pawn(board, "black"), "c2")
        with pytest.raises(ValueError) as e:
            king.castle("queenside")
        assert "cannot castle" in str(e.value)
        board.remove_piece(black_pawn)
        king.castle("queenside")
        assert king.pos == "c1"
        assert qrook.pos == "d1"

    def test_castle_kside(self, board_white_all):
        board = board_white_all["board"]
        krook = board_white_all["krook"]
        kknight = board_white_all["kknight"]
        kbishop = board_white_all["kbishop"]
        king = board_white_all["king"]
        with pytest.raises(ValueError) as e:
            king.castle("kingside")
        assert "cannot castle" in str(e.value)
        board.remove_piece(kbishop)
        with pytest.raises(ValueError) as e:
            king.castle("kingside")
        assert "cannot castle" in str(e.value)
        board.remove_piece(kknight)
        board.add_piece(black_pawn := Pawn(board, "black"), "g2")
        with pytest.raises(ValueError) as e:
            king.castle("kingside")
        assert "cannot castle" in str(e.value)
        board.remove_piece(black_pawn)
        king.castle("kingside")
        assert king.pos == "g1"
        assert krook.pos == "f1"

    def test_discovered_check(self, board_white_all):
        board = board_white_all["board"]
        pawn_d = board_white_all["pd"]
        pawn_e = board_white_all["pe"]
        pawn_f = board_white_all["pf"]
        board.add_piece(black_qbishop := Bishop(board, "black"), "c3")
        board.add_piece(black_rook := Rook(board, "black"), "g3")
        board.add_piece(black_kbishop := Bishop(board, "black"), "g3")
        with pytest.raises(AssertionError) as e:
            pawn_d.move("d3")
        assert "king in check" in str(e.value)
        pawn_d.move("c3")
        assert pawn_d.pos == "c3"
        assert black_qbishop in board.removed
        pawn_e.move("e4")
        assert pawn_e.pos == "e4"
        with pytest.raises(AssertionError) as e:
            pawn_f.move("f3")
        assert "king in check" in str(e.value)
        pawn_f.move("g3")
        assert pawn_f.pos == "g3"
        assert black_kbishop in board.removed
