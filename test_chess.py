from io import StringIO
from chess import *
import pytest


def translate_coord(coord):
    """Translate a tuple coord into an algebraic coord and vice-versa"""
    xs = "abcdefgh"
    ys = "12345678"
    if isinstance(coord, str):
        return xs.index(coord[0]), ys.index(coord[1])
    else:
        return xs[coord[0]], ys[coord[1]]


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
    assert len(white.removed) == 16
    assert len(black.removed) == 16


def format_pgn(file):
    with open(file) as f:
        entries = f.read().strip().split(" ")
    f.close()
    if entries[-1] == "0-1" or entries[-1] == "1-0":
        entries[-1] = "F"
    processing = []
    for e in [e for e in entries if "." not in e]:  # filter turn numbers out
        e = e.replace("x", "")
        e = e.replace("+", "")
        processing.append(e)
    finished = "\n".join(processing)
    return finished


class TestGame:
    def test_game_over(self, empty_board):
        game, board, white, black = empty_board
        board.add_piece(white["king"], (3, 3))
        board.add_piece(black["qrook"], (2, 2))
        board.add_piece(black["krook"], (4, 4))
        board.add_piece(black["pawn_0"], (1, 3))
        board.add_piece(black["pawn_1"], (5, 5))
        assert game.game_over == "stalemate"
        board.add_piece(black["pawn_2"], (2, 4))
        assert game.game_over == "checkmate"

    def test_pillsbury_lasker(self, new_game, monkeypatch, capsys):
        game, board, white, black = new_game
        gameIO = StringIO(format_pgn("pillsbury_lasker_1896.pgn"))
        monkeypatch.setattr("sys.stdin", gameIO)
        game.play_game()
        assert game.forfeit
        assert white.king.in_check
        assert white.king.pos == (1, 4)
        assert not black.king.in_check
        assert black.king.pos == (7, 6)

    def test_steinitz_bardeleben(self, new_game, monkeypatch, capsys):
        game, board, white, black = new_game
        gameIO = StringIO(format_pgn("steinitz_bardeleben_1895.pgn"))
        monkeypatch.setattr("sys.stdin", gameIO)
        game.play_game()
        assert game.forfeit
        assert not white.king.in_check
        assert white.king.pos == (6, 0)
        assert black.king.in_check
        assert black.king.pos == (7, 7)

    def test_reti_alekhine(self, new_game, monkeypatch, capsys):
        game, board, white, black = new_game
        gameIO = StringIO(format_pgn("reti_alekhine_1925.pgn"))
        monkeypatch.setattr("sys.stdin", gameIO)
        game.play_game()
        assert game.forfeit
        assert not white.king.in_check
        assert white.king.pos == (7, 1)
        assert not black.king.in_check
        assert black.king.pos == (6, 7)

    def test_botvinnik_capablanca(self, new_game, monkeypatch, capsys):
        game, board, white, black = new_game
        gameIO = StringIO(format_pgn("botvinnik_capablanca_1938.pgn"))
        monkeypatch.setattr("sys.stdin", gameIO)
        game.play_game()
        assert game.forfeit
        assert not white.king.in_check
        assert white.king.pos == (7, 4)
        assert not black.king.in_check
        assert black.king.pos == (6, 7)

    def test_kasparov_topalov(self, new_game, monkeypatch, capsys):
        game, board, white, black = new_game
        gameIO = StringIO(format_pgn("kasparov_topalov_1999.pgn"))
        monkeypatch.setattr("sys.stdin", gameIO)
        game.play_game()
        assert game.forfeit
        assert not white.king.in_check
        assert white.king.pos == (2, 0)
        assert not black.king.in_check
        assert black.king.pos == (4, 0)


class TestKing:
    def test_empty(self, empty_board):
        game, board, white, black = empty_board
        board.add_piece(white["king"], (3, 3))
        assert white["king"].legal_moves == [
            (2, 2),
            (2, 3),
            (2, 4),
            (3, 2),
            (3, 4),
            (4, 2),
            (4, 3),
            (4, 4),
        ]

    def test_check(self, empty_board):
        game, board, white, black = empty_board
        board.add_piece(white["king"], (3, 3))
        board.add_piece(black["qrook"], (2, 2))
        assert white.king.legal_moves == [(2, 2), (3, 4), (4, 3), (4, 4)]
        assert not white.king.in_check
        board.add_piece(black["krook"], (4, 4))
        assert white.king.legal_moves == [(2, 2), (4, 4)]
        assert not white.king.in_check
        board.add_piece(black["queen"], (2, 2))
        board.remove_piece(black["krook"])
        assert white.king.legal_moves == [(2, 2), (3, 4), (4, 3)]
        assert white.king.in_check
        board.add_piece(black["pawn_1"], (4, 4))
        black.promote(black["pawn_1"], (4, 4), Queen)

    def test_can_castle(self, new_game):
        game, board, white, black = new_game
        assert white.king.can_castle == []
        board.remove_piece(white["queen"])
        board.remove_piece(white["qbishop"])
        board.remove_piece(white["qknight"])
        assert white.king.can_castle == ["queenside"]
        board.move_piece(black["pawn_1"], (2, 1))
        assert white.king.can_castle == []
        board.remove_piece(white["kknight"])
        board.remove_piece(white["kbishop"])
        assert white.king.can_castle == ["kingside"]
        white["krook"].moved = True
        assert white.king.can_castle == []

    def test_castle(self, new_game):
        game, board, white, black = new_game
        with pytest.raises(ValueError) as e:
            game.play_turn("O-O-O")
        assert "Cannot castle" in str(e.value)
        board.remove_piece(white["queen"])
        board.remove_piece(white["qbishop"])
        board.remove_piece(white["qknight"])
        game.play_turn("O-O-O")
        assert white.king.pos == (2, 0)
        assert white["qrook"].pos == (3, 0)
        board.remove_piece(black["kbishop"])
        board.remove_piece(black["kknight"])
        game.play_turn("O-O")
        assert black.king.pos == (6, 7)
        assert black["krook"].pos == (5, 7)


class TestQueen:
    def test_empty(self, empty_board):
        game, board, white, black = empty_board
        board.add_piece(white["queen"], (3, 3))
        assert white["queen"].legal_moves == [
            (2, 2),
            (1, 1),
            (0, 0),
            (2, 3),
            (1, 3),
            (0, 3),
            (2, 4),
            (1, 5),
            (0, 6),
            (3, 2),
            (3, 1),
            (3, 0),
            (3, 4),
            (3, 5),
            (3, 6),
            (3, 7),
            (4, 2),
            (5, 1),
            (6, 0),
            (4, 3),
            (5, 3),
            (6, 3),
            (7, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
        ]

    def test_game(self, new_game):
        game, board, white, black = new_game
        game.play_turn("e4")
        game.play_turn("c5")
        game.play_turn("Qh5")
        game.play_turn("Qa5")
        assert (2, 4) in white["queen"].threatens
        assert (2, 4) in white["queen"].legal_moves
        assert (2, 4) in black["queen"].threatens
        assert (2, 4) not in black["queen"].legal_moves


class TestRook:
    def test_empty(self, empty_board):
        game, board, white, black = empty_board
        board.add_piece(white["qrook"], (3, 3))
        assert white["qrook"].legal_moves == [
            (4, 3),
            (5, 3),
            (6, 3),
            (7, 3),
            (3, 2),
            (3, 1),
            (3, 0),
            (2, 3),
            (1, 3),
            (0, 3),
            (3, 4),
            (3, 5),
            (3, 6),
            (3, 7),
        ]

    def test_game(self, new_game):
        game, board, white, black = new_game
        game.play_turn("h4")
        assert (7, 2) in white["krook"].legal_moves
        game.play_turn("a5")
        game.play_turn("Rh3")
        assert (0, 2) in white["krook"].legal_moves
        game.play_turn("Ra6")
        game.play_turn("Re3")
        assert translate_coord("e7") in white["krook"].legal_moves
        assert translate_coord("e2") not in white["krook"].legal_moves
        assert translate_coord("e7") in white["krook"].threatens
        assert translate_coord("e2") in white["krook"].threatens


class TestBishop:
    def test_empty(self, empty_board):
        game, board, white, black = empty_board
        board.add_piece(white["qbishop"], (3, 3))
        assert white["qbishop"].legal_moves == [
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (4, 2),
            (5, 1),
            (6, 0),
            (2, 2),
            (1, 1),
            (0, 0),
            (2, 4),
            (1, 5),
            (0, 6),
        ]

    def test_game(self, new_game):
        game, board, white, black = new_game
        game.play_turn("e4")
        assert (0, 5) in white["kbishop"].legal_moves
        game.play_turn("b5")
        assert (0, 5) in black["qbishop"].legal_moves
        game.play_turn("Bb5")
        assert (3, 6) in white["kbishop"].legal_moves
        assert (4, 7) not in white["kbishop"].legal_moves


class TestPawn:
    game = Game()
    board = game.board
    white, black = game.board.players["white"], game.board.players["black"]

    def test_double_step(self):
        # test white pawn double step
        self.game.play_turn("d4")
        assert isinstance(self.board["d4"], Pawn)
        assert (
            self.board["d4"].double_step == 0
        ), f"{self.board['d4']} should have double_step set on turn 0"
        # test black pawn double step
        self.game.play_turn("c5")
        assert isinstance(self.board["c5"], Pawn)
        assert (
            self.board["c5"].double_step == 1
        ), f"{self.board['c5']} should have double_step set on turn 1"

    def test_en_passant(self):
        # set up for en passant
        self.game.play_turn("d5")
        self.game.play_turn("e5")
        # should be able to take e5 en passant, but not c5
        assert self.board["d5"].legal_moves == [
            (3, 5),
            (4, 5),
        ], f"{self.board['d5']} should have option to take en-passant"
        assert self.board["e5"].legal_moves == [
            (4, 3)
        ], f"{self.board['e5']} should only have forward step available"
        assert self.board["c5"].legal_moves == [
            (2, 3)
        ], f"{self.board['c5j']} should only have forward step available"
        self.game.play_turn("e6")
        assert (
            self.black["pawn_4"] in self.black.removed
        ), f"{self.black['pawn_4']} should be removed"

    def test_forward_block(self):
        self.game.play_turn("c4")
        self.game.play_turn("e7")
        self.game.play_turn("c3")
        assert self.board["c3"].legal_moves == [(1, 1)]

    def test_promotion(self):
        with pytest.raises(ValueError) as e:
            self.game.play_turn("f8")
        assert "specify promotion" in str(e.value)
        self.game.play_turn("f8Q")
        assert isinstance(self.board["f8"], Queen)
        assert self.board["f8"].player.color == "white"
        self.game.play_turn("Kf8")
        self.game.play_turn("f4")
        with pytest.raises(ValueError) as e:
            self.game.play_turn("b2Q")
        assert "inappropriate" in str(e.value)

    @pytest.fixture
    def en_passant_setup(self, empty_board):
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

    def test_en_passant_special_case(self, en_passant_setup):
        """Test special setup to make sure en-passant doesn't allow moves that put King into check"""
        game, board, white, black = en_passant_setup
        assert translate_coord("d5") not in white["pawn_1"].legal_moves
        assert translate_coord("e3") not in black["pawn_1"].legal_moves
        board.remove_piece(black["qbishop"])
        assert translate_coord("d5") in white["pawn_1"].legal_moves
        board.remove_piece(white["qrook"])
        assert translate_coord("e3") in black["pawn_1"].legal_moves
