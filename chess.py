from piece import *


class Game:
    def __init__(self):
        self.board = Board(self)
        self.turn = 0

    @property
    def whose_turn(self):
        return self.board.players["white" if self.turn % 2 == 0 else "black"]

    def play_turn(self, coord=None):
        player = self.whose_turn
        if coord:
            # automatic turn play via function call for testing purposes
            player.make_move(*translate_algebraic(coord))
            self.turn += 1
            return
        print(self.board)
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

    def remove_piece(self, piece):
        if isinstance(piece, tuple):
            piece = self[piece]
            assert piece, f"attempted to remove piece from empty square {piece}"
        coord = piece.pos
        self[coord] = None
        piece.pos = None
        piece.player.removed.append(piece)

    def test_move(self, piece, coord):
        """Preview a move and return whether it results in self-check"""
        player = piece.player
        start_pos = piece.pos
        if (
            isinstance(piece, Pawn)
            and abs(piece.pos[0] - coord[0]) != 0
            and self[coord] == None
        ):
            other_coord = (coord[0], piece.pos[1])
            other = self[other_coord]
            self.remove_piece(other)
        else:
            other = self[coord]
            other_coord = coord
        self.move_piece(piece, coord)
        valid = not player.king.in_check
        self.move_piece(piece, start_pos)
        if other:
            self.add_piece(other, other_coord)
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
        elif isinstance(i, tuple):
            x, y = i
            self.board[x][y] = item
        else:
            raise IndexError(f"invalid format to access board: {i}")

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
        "qrook": (Rook, (0, 0)),
        "qknight": (Knight, (1, 0)),
        "qbishop": (Bishop, (2, 0)),
        "queen": (Queen, (3, 0)),
        "king": (King, (4, 0)),
        "kbishop": (Bishop, (5, 0)),
        "kknight": (Knight, (6, 0)),
        "krook": (Rook, (7, 0)),
    }
    | {f"pawn_{i}": (Pawn, (i, 1)) for i in range(8)},
    "black": {
        "qrook": (Rook, (0, 7)),
        "qknight": (Knight, (1, 7)),
        "qbishop": (Bishop, (2, 7)),
        "queen": (Queen, (3, 7)),
        "king": (King, (4, 7)),
        "kbishop": (Bishop, (5, 7)),
        "kknight": (Knight, (6, 7)),
        "krook": (Rook, (7, 7)),
    }
    | {f"pawn_{i}": (Pawn, (i, 6)) for i in range(8)},
}


class Player:
    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.pieces = []
        self.pieces_dict = {}
        self.removed = []
        setup = SETUP[self.color]
        for entry in setup:
            p, coord = setup[entry]
            piece = p(self)
            self.board.add_piece(piece, coord)
            self.pieces.append(piece)
            self.pieces_dict[entry] = piece
            if isinstance(piece, King):
                self.king = piece

    def make_move(self, type, coord, file=None, rank=None):
        can_move = []
        for p in self.pieces:
            if isinstance(p, type) and coord in p.legal_moves:
                can_move.append(p)
        if len(can_move) == 1:
            piece = can_move[0]
            if piece.type == "pawn":
                if piece.moved == False and abs(piece.pos[1] - coord[1]) == 2:
                    piece.double_step = self.board.game.turn
                # if x axis changes, means diagonal step
                elif abs(piece.pos[0] - coord[0]) != 0:
                    # if square being moved to is empty, must be en passant
                    if self.board[coord] is None:
                        # remove pawn being taken en passant
                        self.board.remove_piece((coord[0], piece.pos[1]))
            self.board.move_piece(piece, coord)
            piece.moved = True
        elif len(can_move) > 1:
            raise ValueError(f"multiple pieces can make that move: {can_move}")
        else:
            raise ValueError(f"No pieces of type {type} can move to {coord}")

    def __getitem__(self, item):
        return self.pieces_dict[item]

    def __repr__(self):
        return f"{self.color} player"
