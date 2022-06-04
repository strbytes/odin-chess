(WIP) Chess project for The Odin Project. https://www.theodinproject.com/lessons/ruby-ruby-final-project

Implemented in Python because I don't feel like learning Ruby. Using a more relaxed approach after focusing on TDD for the last two projects. Basic logic for piece movement is implemented, now need to develop the main Game object and loop to play an actual game with the pieces.

-- chess.py --
Game - Manages the game state at the highest level. Logic for playing a single turn at a time, keeping track of turn number, checking game-over states, playing a full game on a loop. TODO: Saving and loading gamesj

Board - Stores the Players and implements basic logic for adding, moving, and removing pieces from the board.

Player - Stores Pieces and methods for making moves.

-- pieces.py --
Piece - Generic class and specific subclasses for each type of chess piece. Pieces contain the logic for evaluating legal moves, including Pawn and King special rules.

-- test_chess.py --
Tests for all implemented features, including running several famous games from https://www.chessgames.com/perl/chesscollection?cid=1019178 all the way through.

-- taskell.md --
Kanban board for project managed with taskell.
