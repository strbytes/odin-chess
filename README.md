(WIP) Chess project for The Odin Project. https://www.theodinproject.com/lessons/ruby-ruby-final-project

Implemented in Python because I don't feel like learning Ruby. Using a more relaxed approach after focusing on TDD for the last two projects. Basic logic for piece movement is implemented, now need to develop the main Game object and loop to play an actual game with the pieces.

chess.py - Game and Player classes -- TODO

board.py - Board class and helper constants. A Board stores all of the pieces and their locations, as well as handling fundamental movements.

pieces.py - Piece generic class, specific subclasses for each type of chess piece, and a helper function translate_algebraic. Pieces contain the logic for their own movement, including Pawn special movement rules and castling and testing for check in Kings.

test_legal_moves.py - Tests for lower level functions in Pieces, particularly for evaluating what moves are available to a piece at a particular time.

test_move.py - Tests for moving Pieces using their internal movement functions. Includes tests on castling and preventing Kings moving into check or other pieces moving and putting their King into check.

taskell.md - Kanban board for project managed with taskell
