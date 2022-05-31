OPPOSITE_COLOR = {"white": "black", "black": "white"}

ICONS = {
    "white": {
        "king": "♚",
        "queen": "♛",
        "rook": "♜",
        "bishop": "♝",
        "knight": "♞",
        "pawn": "♟",
    },
    "black": {
        "king": "♔",
        "queen": "♕",
        "rook": "♖",
        "bishop": "♗",
        "knight": "♘",
        "pawn": "♙",
    },
}


class Piece:
    def __init__(self, player):
        self.player = player
        self.pos = None
        self.moved = False

    def __str__(self):
        if self.player.board.checkered_square(self.pos):
            return ICONS[OPPOSITE_COLOR[self.player.color]][self.type]
        return ICONS[self.player.color][self.type]

    @property
    def legal_moves(self):
        potential = []
        for m in self.potential_moves:
            board = self.player.board
            x, y = m
            if (current := board.board[x][y]) is None:
                potential.append(m)
            else:
                if current.player.color != self.player.color:
                    potential.append(m)
        legal = []
        for p in potential:
            if board.test_move(self, p):
                legal.append(p)
        return legal


class King(Piece):
    type = "king"


class Queen(Piece):
    type = "queen"


class Rook(Piece):
    type = "rook"


class Bishop(Piece):
    type = "bishop"


class Knight(Piece):
    type = "knight"


class Pawn(Piece):
    type = "pawn"

    def __init__(self, player):
        self.double_step = None
        Piece.__init__(self, player)

    @property
    def potential_moves(self):
        direction = 1 if self.player.color == "white" else -1
        board = self.player.board.board
        assert self.pos, "potential_moves called on a piece with no position"
        moves = []
        x, y = self.pos
        if 0 <= y + direction <= 7:  # piece not at end of board
            if board[x][y + direction] is None:
                moves.append((x, y + direction))
                if not self.moved and board[x][y + 2 * direction] is None:
                    moves.append((x, y + 2 * direction))
            for lateral in [-1, 1]:
                if 0 <= x + lateral <= 7:  # piece not at side of board
                    if board[x + lateral][y + direction] is not None:
                        moves.append((x + lateral, y + direction))
                    else:
                        side = board[x + lateral][y]
                        if (
                            side is not None
                            and side.player.color != self.player.color
                            and side.type == "pawn"
                            and side.double_step == self.player.board.game.turn - 1
                        ):
                            moves.append((x + lateral, y + direction))
        return moves

    @property
    def threatens(self):
        direction = 1 if self.player.color == "white" else -1
        board = self.player.board.board
        x, y = self.pos
        threatens = []
        for lateral in [-1, 1]:
            if (
                0 <= x + lateral <= 7 and 0 <= y + direction <= 7
            ):  # piece not on edges of board
                threatens.append((x + lateral, y + direction))
        return threatens
