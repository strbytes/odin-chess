(WIP) Chess project for The Odin Project. https://www.theodinproject.com/lessons/ruby-ruby-final-project

Implemented in Python because I don't feel like learning Ruby. Using a more relaxed approach after focusing on TDD for the last two projects. Basic logic for piece movement is implemented, now need to develop the main Game object and loop to play an actual game with the pieces.

-- chess.py --
Game - Manages the game state at the highest level.
Implemented: Playing a single turn at a time, keeping track of turn number. TODO: Check for game-over states (e.g. checkmate, stalemate), saving and loading games, playing a full game on a loop.

Board - Stores the Players and implements basic logic for adding, moving, and removing pieces from the board.

Player - Stores Pieces and methods for making moves.

-- pieces.py --
Piece generic class and specific subclasses for each type of chess piece. Pieces contain the logic for evaluating legal moves, including Pawn special movement rules and castling and testing for check in Kings.

-- test_chess.py --
Tests for currently implemented features.

-- taskell.md --
Kanban board for project managed with taskell.
