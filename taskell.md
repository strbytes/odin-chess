## To Do

- Add test_check to King
    > Test if any square is threatened. can be called on a specific square to check if a move is possible, or check own square (in_check method?) if no argument
- Add a method to Board that checks all legal moves and builds a dict every turn?

## Doing

- Add tests for Piece.move
    * [ ] Piece.move (most pieces)
    * [ ] Pawn.move (en passant)
    * [ ] King.castle
    * [ ] King.test_check
- Add subclasses for Piece types
    * [x] Redefine basic class structure
    * [x] King
    * [ ] - test check
    * [x] - Castling
    * [x] Queen
    * [x] Rook
    * [x] Knight
    * [x] Bishop
    * [x] Pawn

## Done

- Finish basic layout sketch
    * [x] Update which characters are shown for pieces on white squares so they look more consistent
    * [x] Add basic movement function to Board (just ability to move an existing piece to another location, with no constraints, overwriting any piece that is already there)
- Add basic movement logic
    * [x] Piece types have movement logic
- Add can_castle to King
    > Dictionary by name in Player class?
    * [x] can_castle in King
    * [x] if king not moved:
    * [x] finds rooks through Board
    * [x] if not moved, identify queen side or king side based on position
    * [x] then check if same side squares are free
    * [x] if pass all these, return True, else False
