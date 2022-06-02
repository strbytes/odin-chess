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


class TestGame:
    game = Game()
    board = game.board
    white, black = game.board.players["white"], game.board.players["black"]


class TestPawn(TestGame):
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
        game, board, white, black = en_passant_setup
        # TODO
