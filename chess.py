BLACK = {
    "king": "♔",
    "queen": "♕",
    "rook": "♖",
    "bishop": "♗",
    "knight": "♘",
    "pawn": "♙",
}
WHITE_SETUP = ["e1", "d1", "a1", "h1", "b1", "g1", "c1", "f1"] + [
    c + "2" for c in "abcdefgh"
]
WHITE = {
    "king": "♚",
    "queen": "♛",
    "rook": "♜",
    "bishop": "♝",
    "knight": "♞",
    "pawn": "♟",
}
BLACK_SETUP = ["e8", "d8", "a8", "h8", "b8", "g8", "c8", "f8"] + [
    c + "7" for c in "abcdefgh"
]
COLOR = {"white": WHITE, "black": BLACK}
OPPOSITE_COLOR = {"white": BLACK, "black": WHITE}
ALGEBRAIC_X = "abcdefgh"


def translate_algebraic(coord, dx, dy):
    """Apply movements to algebraic coordinates and return a new algebraic coordinate,
    or None if out side of a chessboard"""
    x, y = ALGEBRAIC_X.index(coord[0]), int(coord[1])
    if 0 <= x + dx < 8 and 1 <= y + dy < 9:  # y is 1 indexed
        return ALGEBRAIC_X[x + dx] + str(y + dy)


class Board:
    def __init__(self):
        self.pieces = {}  # store board state by piece
        self.board = {}  # store board state by square
        self.removed = []
        for y in range(8):
            for x in range(8):
                square = ALGEBRAIC_X[x] + str(y + 1)
                self.board[square] = None

    def add_piece(self, piece, coord):
        assert isinstance(piece, Piece)
        assert coord in self.board
        if (square := self.board[coord]) is not None:
            self.remove_piece(self.board[square])
        self.pieces[piece] = coord
        self.board[coord] = piece

    def remove_piece(self, piece):
        assert piece in self.pieces
        square = self.pieces[piece]
        self.board[square] = None
        del self.pieces[piece]
        self.removed.append(piece)

    def move_piece(self, piece, coord):
        assert piece in self.pieces
        assert coord in self.board
        if (piece_on_square := self.board[coord]) is not None:
            self.remove_piece(piece_on_square)
        self.board[self.pieces[piece]] = None  # remove link to piece from old square
        self.pieces[piece] = coord
        self.board[coord] = piece

    def __str__(self):
        black_on_white = "\u001b[47m\u001b[30m"  # ]]
        reset = "\u001b[0m"  # ]
        string = ""
        for y in range(8):
            string += str(y + 1) + " --"
            for x in range(8):
                string += black_on_white if (x + y) % 2 == 0 else ""
                square = "abcdefgh"[x] + str(y + 1)
                if self.board[square]:
                    string += self.board[square].board_display((x + y) % 2 == 0) + " "
                else:
                    string += "  "
                string += reset if (x + y) % 2 == 0 else ""
            string += "\n" if y < 7 else "\n  *  " + " ".join("|" * 8)
        string += "\n" + " " * 5 + " ".join(list("abcdefgh"))
        return string

    def __repr__(self):
        return "Board()"


class Piece:
    """Base class for chess pieces. Not to be instantiated directly."""

    def __init__(self, board, color):
        self.board = board
        self.color = color

    def board_display(self, white_background=False):
        """Returns a string depiction of the piece, using the alternate style
        of icon for white tiles."""
        if white_background:
            return OPPOSITE_COLOR[self.color][self.piece]
        return COLOR[self.color][self.piece]


class King(Piece):
    piece = "king"

    def __init__(self, board, color):
        self.moved = False
        Piece.__init__(self, board, color)

    @property
    def legal_moves(self):
        pos = self.board.pieces[self]
        board = self.board.board
        assert pos, "can't check moves on a piece not on the board"
        moves = []
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                if not (x == 0 and y == 0):
                    step = translate_algebraic(pos, x, y)
                    if step is not None:
                        if not self.test_check(step):
                            if board[step] is None or board[step].color != self.color:
                                moves.append(step)
        return moves

    @property
    def in_check(self):
        return self.test_check(self.pos)

    def test_check(self, coord):
        # TODO
        pass


class Queen(Piece):
    piece = "queen"

    @property
    def legal_moves(self):
        pos = self.board.pieces[self]
        board = self.board.board
        assert pos, "can't check moves on a piece not on the board"
        moves = []
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                if not (x == 0 and y == 0):
                    i = 1
                    while True:
                        line = translate_algebraic(pos, x * i, y * i)
                        if line is not None and board[line] is None:
                            moves.append(line)
                            i += 1
                        else:
                            if line is not None and board[line].color != self.color:
                                moves.append(line)
                            break
        return moves


class Rook(Piece):
    piece = "rook"

    def __init__(self, board, color):
        self.moved = False
        Piece.__init__(self, board, color)

    @property
    def legal_moves(self):
        pos = self.board.pieces[self]
        board = self.board.board
        assert pos, "can't check moves on a piece not on the board"
        moves = []
        for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            i = 1
            while True:
                line = translate_algebraic(pos, x * i, y * i)
                if line is not None and board[line] is None:
                    moves.append(line)
                    i += 1
                else:
                    if line is not None and board[line].color != self.color:
                        moves.append(line)
                    break
        # TODO: castling
        # needs a way to find own King -- via Board or Player?
        return moves


class Knight(Piece):
    piece = "knight"

    @property
    def legal_moves(self):
        pos = self.board.pieces[self]
        board = self.board.board
        assert pos, "can't check moves on a piece not on the board"
        moves = []
        knight_moves = []
        for x in [-2, -1, 1, 2]:
            for y in [-2, -1, 1, 2]:
                if abs(x) != abs(y) and (new_pos := translate_algebraic(pos, x, y)):
                    if not board[new_pos]:
                        knight_moves.append(new_pos)
                    elif board[new_pos].color != self.color:
                        knight_moves.append(new_pos)
        return knight_moves


class Bishop(Piece):
    piece = "bishop"

    @property
    def legal_moves(self):
        pos = self.board.pieces[self]
        board = self.board.board
        assert pos, "can't check moves on a piece not on the board"
        moves = []
        for x, y in [(1, 1), (1, -1), (-1, -1), (-1, 1)]:
            i = 1
            while True:
                diag = translate_algebraic(pos, x * i, y * i)
                if diag is not None and board[diag] is None:
                    moves.append(diag)
                    i += 1
                else:
                    if diag is not None and board[diag].color != self.color:
                        moves.append(diag)
                    break
        return moves


class Pawn(Piece):
    piece = "pawn"

    def __init__(self, board, color):
        self.moved = False
        Piece.__init__(self, board, color)

    @property
    def legal_moves(self):
        pos = self.board.pieces[self]
        dir = 1 if self.color == "white" else -1
        board = self.board.board
        assert pos, "can't check moves on a piece not on the board"
        moves = []
        one_step = translate_algebraic(pos, 0, dir)
        two_step = translate_algebraic(pos, 0, 2 * dir)
        diagonals = [translate_algebraic(pos, i, dir) for i in (-1, 1)]
        # move
        if one_step is not None and board[one_step] is None:
            moves.append(one_step)
            if two_step is not None and not self.moved and board[two_step] is None:
                moves.append(two_step)
        # take
        for diag in diagonals:
            if (
                diag is not None
                and board[diag] is not None
                and board[diag].color != self.color
            ):
                moves.append(diag)
            elif diag is not None and board[diag] is None:
                side = translate_algebraic(diag, 0, -dir)
                if board[side] is not None and board[side].color != self.color:
                    moves.append(diag)
        return moves


class Player:
    def __init__(self, color):
        assert color == "white" or color == "black"
        self.color = color
        self._gen_pieces()

    def _gen_pieces(self):
        self.pieces = []
        for piece in ["king", "queen"]:
            self.pieces.append(Piece(self.color, piece))
        for piece in ["rook", "bishop", "knight"]:
            self.pieces.append(Piece(self.color, piece))
            self.pieces.append(Piece(self.color, piece))
        for _ in range(8):
            self.pieces.append(Piece(self.color, "pawn"))

    def __repr__(self):
        return "Player('" + self.color + "')"


class Game:
    def __init__(self):
        self.white, self.black = Player("white"), Player("black")
        self._set_up_board()

    def _set_up_board(self):
        self.board = Board()
        for i, piece in enumerate(self.white.pieces):
            self.board.add_piece(piece, WHITE_SETUP[i])
        for i, piece in enumerate(self.black.pieces):
            self.board.add_piece(piece, BLACK_SETUP[i])
