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

    def __str__(self):
        if self.player.board.checkered_square(self.pos):
            return ICONS[OPPOSITE_COLOR[self.player.color]][self.type]
        return ICONS[self.player.color][self.type]

    @property
    def legal_moves(self):
        # TEST
        l = []
        for x in range(8):
            for y in range(8):
                l.append((x, y))
        return l


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
