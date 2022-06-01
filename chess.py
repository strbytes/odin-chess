from piece import *


class Game:
    def __init__(self):
        self.board = Board(self)
        self.turn = 0

    @property
    def whose_turn(self):
        return self.board.players["white" if self.turn % 2 == 0 else "black"]

    def play_turn(self):
        print(self.board)
        player = self.whose_turn
        print(player, ", it's your turn!")
        while True:
            try:
                play = input("Enter a move using algebraic notation > ")
                player.make_move(*translate_algebraic(play))
                self.turn += 1
                break
            except (AssertionError, ValueError) as e:
                print(e)


def translate_algebraic(alg_coord):
    pieces = {"K": King, "Q": Queen, "R": Rook, "B": Bishop, "N": Knight}
    xs = "abcdefgh"
    ys = "12345678"
    file, rank = None, None
    if len(alg_coord) == 2:
        piece = Pawn
        coord = alg_coord
    elif len(alg_coord) == 3:
        if alg_coord[0] in pieces:
            piece = pieces[alg_coord[0]]
        elif alg_coord[0] in xs:
            piece = Pawn
            file = xs.index(alg_coord[0])
        elif alg_coord[0] in ys:
            piece = Pawn
            rank = ys.index(alg_coord[0])
        else:
            raise ValueError(
                f"invalid character {alg_coord[0]} in coordinate {alg_coord}"
            )
        coord = alg_coord[1:]
    elif len(alg_coord) == 4:
        piece = pieces[alg_coord[0]]
        if alg_coord[1] in xs:
            file = xs.index(alg_coord[1])
        elif alg_coord[1] in ys:
            rank = ys.index(alg_coord[1])
        else:
            raise ValueError(
                f"invalid character {alg_coord[1]} in coordinate {alg_coord}"
            )
        coord = alg_coord[2:]
    elif len(alg_coord) == 5:
        piece = pieces[alg_coord[0]]
        if alg_coord[1] in xs and alg_coord[2] in ys:
            file, rank = xs.index(alg_coord[1]), ys.index(alg_coord[2])
        else:
            raise ValueError(
                f"invalid characters {alg_coord[1:3]} in coordinate {alg_coord}"
            )
        coord = alg_coord[3:]
    else:
        raise ValueError(f"invalid coordinate {alg_coord}")
    return piece, (xs.index(coord[0]), ys.index(coord[1])), file, rank


class Board:
    def __init__(self, game):
        self.game = game
        self.board = []
        for x in range(8):
            self.board.append([])
            for y in range(8):
                self.board[x].append(None)
        self.players = {color: Player(self, color) for color in ["white", "black"]}

    def add_piece(self, piece, coord):
        assert piece.pos is None, "attempted to add a piece already on the board"
        if current := self[coord]:
            current.player.removed.append(current)
            current.pos = None
        self[coord] = piece
        if piece in piece.player.removed:
            piece.player.removed.remove(piece)
        piece.pos = coord

    def move_piece(self, piece, coord):
        assert piece.pos, "attempted to move a piece not on the board"
        if current := self[coord]:
            current.player.removed.append(current)
            current.pos = None
        self[coord] = piece
        old_pos = piece.pos
        self[old_pos] = None
        piece.pos = coord

    def test_move(self, piece, coord):
        """Preview a move and return whether it results in self-check"""
        player = piece.player
        start_pos = piece.pos
        other = self[coord]
        self.move_piece(piece, coord)
        valid = not player.king.in_check
        self.move_piece(piece, start_pos)
        if other:
            self.add_piece(other, coord)
        return valid

    def checkered_square(self, coord):
        x, y = coord
        return (x + y) % 2 == 0

    def __getitem__(self, i):
        if isinstance(i, int):
            return self.board[i]
        if isinstance(i, tuple):
            x, y = i
            return self.board[x][y]
        if isinstance(i, str):
            return self.board["abcdefgh".index(i[0])]["12345678".index(i[1])]

    def __setitem__(self, i, item):
        if isinstance(i, int):
            return self.board[i]
        if isinstance(i, tuple):
            x, y = i
            self.board[x][y] = item

    def __str__(self):
        black_on_white = "\u001b[47m\u001b[30m"  # ]]
        reset = "\u001b[0m"  # ]
        string = ""
        for y in reversed(range(8)):
            string += str(y + 1) + " --"
            for x in range(8):
                string += black_on_white if (x + y) % 2 == 0 else ""
                if self.board[x][y]:
                    string += str(self.board[x][y]) + " "
                else:
                    string += "  "
                string += reset if (x + y) % 2 == 0 else ""
            string += "\n" if y > 0 else "\n  *  " + " ".join("|" * 8)
        string += "\n" + " " * 5 + " ".join(list("abcdefgh"))
        return string


SETUP = {
    "white": {
        (Rook, (0, 0)),
        (Knight, (1, 0)),
        (Bishop, (2, 0)),
        (Queen, (3, 0)),
        (King, (4, 0)),
        (Bishop, (5, 0)),
        (Knight, (6, 0)),
        (Rook, (7, 0)),
    }
    | {(Pawn, (i, 1)) for i in range(8)},
    "black": {
        (Rook, (0, 7)),
        (Knight, (1, 7)),
        (Bishop, (2, 7)),
        (Queen, (3, 7)),
        (King, (4, 7)),
        (Bishop, (5, 7)),
        (Knight, (6, 7)),
        (Rook, (7, 7)),
    }
    | {(Pawn, (i, 6)) for i in range(8)},
}


class Player:
    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.pieces = []
        self.removed = []
        setup = SETUP[self.color]
        for p, coord in setup:
            piece = p(self)
            self.board.add_piece(piece, coord)
            self.pieces.append(piece)
            if isinstance(piece, King):
                self.king = piece

    def make_move(self, type, coord, file=None, rank=None):
        can_move = []
        for p in self.pieces:
            if isinstance(p, type) and coord in p.legal_moves:
                can_move.append(p)
        if len(can_move) == 1:
            piece = can_move[0]
            self.board.move_piece(piece, coord)
            if piece.type == "pawn" and piece.moved == False:
                if abs(piece.pos[1] - coord[1]) == 2:
                    type.double_step = self.board.game.turn
            piece.moved = True
        elif len(can_move) > 1:
            raise ValueError(f"multiple pieces can make that move: {can_move}")
        else:
            raise ValueError(f"No pieces of type {type} can move to {coord}")

    def __repr__(self):
        return f"{self.color} player"
