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

    def __repr__(self):
        return f"{self.player.color} {self.type} at {self.pos}"

    @property
    def legal_moves(self):
        if not self.pos:
            return []
        potential = []
        for m in self.potential_moves:
            board = self.player.board
            if (current := board[m]) is None:
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

    @property
    def in_check(self):
        # test if king is in the other player's list of threatened squares
        return self.pos in self.player.other_player.threatens_all

    @property
    def can_castle(self):
        if self.moved:
            return []
        rooks = (self.player["qrook"], self.player["krook"])
        castleable = []
        for rook in rooks:
            if rook.moved:
                continue
            # if queenside rook, check those squares are empty and unthreatened
            if rook.pos[0] == 0:
                castle_squares = [(i, rook.pos[1]) for i in range(1, 4)]
                side = "queenside"
            # else check kingside squares
            elif rook.pos[0] == 7:
                castle_squares = [(i, rook.pos[1]) for i in range(5, 7)]
                side = "kingside"
            else:
                raise RuntimeError(f"Castling evaluation run on invalid piece, {rook}")
            if all(
                [
                    self.player.board[c] is None
                    and c not in self.player.other_player.threatens_all
                    for c in castle_squares
                ]
            ):
                castleable.append(side)
        return castleable

    @property
    def potential_moves(self):
        assert self.pos, "potential_moves called on a piece with no position"
        x, y = self.pos
        moves = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if not dx == 0 == y:
                    if 0 <= x + dx <= 7 and 0 <= y + dy <= 7:
                        coord = (x + dx, y + dy)
                        moves.append(coord)
        return moves

    @property
    def threatens(self):
        if not self.pos:
            return []
        return self.potential_moves


class Queen(Piece):
    type = "queen"

    @property
    def potential_moves(self):
        assert self.pos, "potential_moves called on a piece with no position"
        x, y = self.pos
        moves = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if not dx == 0 == y:
                    i = 1
                    while 0 <= x + dx * i <= 7 and 0 <= y + dy * i <= 7:
                        coord = (x + dx * i, y + dy * i)
                        moves.append(coord)
                        i += 1
                        if self.player.board[coord] is not None:
                            break
        return moves

    @property
    def threatens(self):
        if not self.pos:
            return []
        return self.potential_moves


class Rook(Piece):
    type = "rook"

    @property
    def potential_moves(self):
        assert self.pos, "potential_moves called on a piece with no position"
        x, y = self.pos
        moves = []
        for dx, dy in [(1, 0), (0, -1), (-1, -0), (-0, 1)]:
            i = 1
            while 0 <= x + dx * i <= 7 and 0 <= y + dy * i <= 7:
                coord = (x + dx * i, y + dy * i)
                moves.append(coord)
                i += 1
                if self.player.board[coord] is not None:
                    break
        return moves

    @property
    def threatens(self):
        if not self.pos:
            return []
        return self.potential_moves


class Bishop(Piece):
    type = "bishop"

    @property
    def potential_moves(self):
        assert self.pos, "potential_moves called on a piece with no position"
        x, y = self.pos
        moves = []
        for dx, dy in [(1, 1), (1, -1), (-1, -1), (-1, 1)]:
            i = 1
            while 0 <= x + dx * i <= 7 and 0 <= y + dy * i <= 7:
                coord = (x + dx * i, y + dy * i)
                moves.append(coord)
                i += 1
                if self.player.board[coord] is not None:
                    break
        return moves

    @property
    def threatens(self):
        if not self.pos:
            return []
        return self.potential_moves


class Knight(Piece):
    type = "knight"

    @property
    def potential_moves(self):
        assert self.pos, "potential_moves called on a piece with no position"
        x, y = self.pos
        moves = []
        for dx in [-2, -1, 1, 2]:
            for dy in [-2, -1, 1, 2]:
                if abs(dx) != abs(dy) and 0 <= x + dx <= 7 and 0 <= y + dy <= 7:
                    moves.append((x + dx, y + dy))
        return moves

    @property
    def threatens(self):
        if not self.pos:
            return []
        return self.potential_moves


class Pawn(Piece):
    type = "pawn"

    def __init__(self, player):
        self.double_step = None
        Piece.__init__(self, player)

    @property
    def potential_moves(self):
        direction = 1 if self.player.color == "white" else -1
        board = self.player.board
        assert self.pos, "potential_moves called on a piece with no position"
        moves = []
        x, y = self.pos
        if 0 <= y + direction <= 7:  # piece not at end of board
            one_step = (x, y + direction)
            if board[one_step] is None:
                moves.append(one_step)
                two_step = (x, y + 2 * direction)
                if not self.moved and board[two_step] is None:
                    moves.append(two_step)
            for lateral in [-1, 1]:
                if 0 <= x + lateral <= 7:  # piece not at side of board
                    diagonal = (x + lateral, y + direction)
                    if board[diagonal] is not None:
                        moves.append(diagonal)
                    else:
                        side = (x + lateral, y)
                        side_piece = board[side]
                        if (
                            side_piece is not None
                            and side_piece.player.color != self.player.color
                            and side_piece.type == "pawn"
                            and side_piece.double_step
                            == self.player.board.game.turn - 1
                        ):
                            moves.append(diagonal)
        return moves

    @property
    def threatens(self):
        direction = 1 if self.player.color == "white" else -1
        if not self.pos:
            return []
        x, y = self.pos
        threatens = []
        for lateral in [-1, 1]:
            diagonal = (x + lateral, y + direction)
            if (
                0 <= x + lateral <= 7 and 0 <= y + direction <= 7
            ):  # piece not on edges of board
                threatens.append(diagonal)
        return threatens
