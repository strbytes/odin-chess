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
        if piece in self.removed:
            self.removed.remove(piece)
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

    @property
    def threatened_squares(self):
        # threatened squares are named for the side being threatened
        threatened = {"black": set(), "white": set()}
        for piece in self.pieces:
            for move in piece.can_take:
                threatened["black" if piece.color == "white" else "white"].add(move)
        return threatened

    def __str__(self):
        black_on_white = "\u001b[47m\u001b[30m"  # ]]
        reset = "\u001b[0m"  # ]
        string = ""
        for y in reversed(range(8)):
            string += str(y + 1) + " --"
            for x in range(8):
                string += black_on_white if (x + y) % 2 == 0 else ""
                square = "abcdefgh"[x] + str(y + 1)
                if self.board[square]:
                    string += self.board[square].board_display((x + y) % 2 == 0) + " "
                else:
                    string += "  "
                string += reset if (x + y) % 2 == 0 else ""
            string += "\n" if y > 0 else "\n  *  " + " ".join("|" * 8)
        string += "\n" + " " * 5 + " ".join(list("abcdefgh"))
        return string

    def __repr__(self):
        return "Board()"


class Piece:
    """Base class for chess pieces. Not to be instantiated directly."""

    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.moved = False

    @property
    def pos(self):
        if self not in self.board.pieces:
            return None
        return self.board.pieces[self]

    @property
    def can_take(self):
        """Needed to for Pawn to override and not show double-steps in Board.threatened_squares"""
        return self.legal_moves

    def board_display(self, white_background=False):
        """Returns a string depiction of the piece, using the alternate style
        of icon for white tiles."""
        if white_background:
            return OPPOSITE_COLOR[self.color][self.piece]
        return COLOR[self.color][self.piece]

    def move(self, coord):
        assert coord in self.legal_moves
        if self.board.board[coord]:
            assert self.board.board[coord].color != self.color, "cannot take own piece"
        self.board.move_piece(self, coord)

    def __repr__(self):
        return self.color + " " + self.piece + " at " + self.pos


class King(Piece):
    piece = "king"

    @property
    def legal_moves(self):
        assert self.pos, "can't check moves on a piece not on the board"
        moves = []
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                if not (x == 0 and y == 0):
                    step = translate_algebraic(self.pos, x, y)
                    if step is not None:
                        moves.append(step)
        return moves

    @property
    def can_castle(self):
        if self.moved or self.in_check:
            return {}
        castleable_rooks = {}
        column = str(self.pos[1])
        for piece in self.board.pieces:
            if piece.color == self.color:
                if piece.piece == "rook" and not piece.moved:
                    # check rook location to determine side
                    # a column is queenside
                    if self.board.pieces[piece][0] == "a":
                        knight_square = "b" + column
                        bishop_square = "c" + column
                        queen_square = "d" + column
                        if (
                            self.board.board[knight_square] == None
                            and self.board.board[bishop_square] == None
                            and self.board.board[queen_square] == None
                            and not any(
                                [
                                    self.test_check(square)
                                    for square in [queen_square, bishop_square]
                                ]
                            )
                        ):
                            castleable_rooks["queenside"] = piece
                    else:  # if not queenside must be kingside
                        knight_square = "g" + column
                        bishop_square = "f" + column
                        if (
                            self.board.board[knight_square] == None
                            and self.board.board[bishop_square] == None
                            and not any(
                                [
                                    self.test_check(square)
                                    for square in [knight_square, bishop_square]
                                ]
                            )
                        ):
                            castleable_rooks["kingside"] = piece
        return castleable_rooks

    def move(self, coord):
        assert not self.test_check(coord), "King cannot move into check"
        Piece.move(self, coord)

    def castle(self, side):
        assert self.pos, "King must be on board to castle"
        assert side == "queenside" or side == "kingside"
        if side not in self.can_castle:
            raise ValueError(f"cannot castle " + side)
        else:
            rook = self.can_castle[side]
            row = self.pos[1]
            king_col = "c" if side == "queenside" else "g"
            rook_col = "d" if side == "queenside" else "f"
            self.board.move_piece(self, king_col + row)
            self.board.move_piece(rook, rook_col + row)

    @property
    def in_check(self):
        return self.test_check(self.pos)

    def test_check(self, coord):
        return coord in self.board.threatened_squares[self.color]


class Queen(Piece):
    piece = "queen"

    @property
    def legal_moves(self):
        board = self.board.board
        assert self.pos, "can't check moves on a piece not on the board"
        moves = []
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                if not (x == 0 and y == 0):
                    i = 1
                    # keep looking further out in each direction until end of
                    # board or a piece is hit
                    while True:
                        line = translate_algebraic(self.pos, x * i, y * i)
                        if line is not None and board[line] is None:
                            moves.append(line)
                            i += 1
                        else:
                            if line is not None:
                                moves.append(line)
                            break
        return moves


class Rook(Piece):
    piece = "rook"

    @property
    def legal_moves(self):
        board = self.board.board
        assert self.pos, "can't check moves on a piece not on the board"
        moves = []
        for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            i = 1
            # keep looking further out in each direction until end of
            # board or a piece is hit
            while True:
                line = translate_algebraic(self.pos, x * i, y * i)
                if line is not None and board[line] is None:
                    moves.append(line)
                    i += 1
                else:
                    if line is not None:
                        moves.append(line)
                    break
        return moves


class Knight(Piece):
    piece = "knight"

    @property
    def legal_moves(self):
        assert self.pos, "can't check moves on a piece not on the board"
        knight_moves = []
        for x in [-2, -1, 1, 2]:
            for y in [-2, -1, 1, 2]:
                if abs(x) != abs(y) and (
                    new_pos := translate_algebraic(self.pos, x, y)
                ):
                    knight_moves.append(new_pos)
        return knight_moves


class Bishop(Piece):
    piece = "bishop"

    @property
    def legal_moves(self):
        board = self.board.board
        assert self.pos, "can't check moves on a piece not on the board"
        moves = []
        for x, y in [(1, 1), (1, -1), (-1, -1), (-1, 1)]:
            i = 1
            while True:
                diag = translate_algebraic(self.pos, x * i, y * i)
                if diag is not None and board[diag] is None:
                    moves.append(diag)
                    i += 1
                else:
                    if diag is not None:
                        moves.append(diag)
                    break
        return moves


class Pawn(Piece):
    piece = "pawn"

    def __init__(self, board, color):
        # self.double_step_turn = None
        self.just_double_stepped = False
        Piece.__init__(self, board, color)

    # def just_double_stepped(self, turn):
    #     # Refactor Piece to accept a Game attribute so pawns can check the turn themselves?
    #     if self.double_step_turn:
    #         return turn == self.double_step_turn + 1
    #     return False

    def move(self, coord):
        assert coord in self.legal_moves
        dir = 1 if self.color == "white" else -1
        board = self.board.board
        diags = [translate_algebraic(self.pos, i, dir) for i in (-1, 1)]
        # check for en passant
        if coord in diags and board[coord] is None:
            side = translate_algebraic(coord, 0, -dir)
            if (
                board[side] is not None
                and board[side].color != self.color
                and board[side].piece == "pawn"
                and board[side].just_double_stepped == True
            ):
                self.board.move_piece(self, coord)
                self.board.remove_piece(board[side])
        else:
            if coord == translate_algebraic(self.pos, 0, 2 * dir):
                self.just_double_stepped = True
            Piece.move(self, coord)

    @property
    def legal_moves(self):
        dir = 1 if self.color == "white" else -1
        board = self.board.board
        assert self.pos, "can't check moves on a piece not on the board"
        moves = []
        one_step = translate_algebraic(self.pos, 0, dir)
        # move
        if one_step is not None and board[one_step] is None:
            moves.append(one_step)
            if not self.moved:
                two_step = translate_algebraic(self.pos, 0, 2 * dir)
                if two_step is not None:
                    moves.append(two_step)
        # take
        diagonals = [translate_algebraic(self.pos, i, dir) for i in (-1, 1)]
        for diag in diagonals:
            if diag is not None and board[diag] is not None:
                moves.append(diag)
            # check for en passant
            elif diag is not None and board[diag] is None:
                side = translate_algebraic(diag, 0, -dir)
                if (
                    board[side] is not None
                    and board[side].color != self.color
                    and board[side].piece == "pawn"
                    and board[side].just_double_stepped == True
                ):
                    moves.append(diag)
        return moves

    @property
    def can_take(self):
        """Return only squares actually threatened by pawn"""
        dir = 1 if self.color == "white" else -1
        moves = []
        diagonals = [translate_algebraic(self.pos, i, dir) for i in (-1, 1)]
        for diag in diagonals:
            if diag is not None:
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
