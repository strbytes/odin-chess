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
        assert coord in self.board
        if (piece_on_square := self.board[coord]) is not None:
            self.remove_piece(piece_on_square)
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
