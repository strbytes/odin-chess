## To Do

- Main game loop
    * [x] accept algebraic notation as moves
    * [ ] display helpful messages for unallowed moves
- check/mate/draw
    > Game method to test for check and draw
    * [ ] need to be able to access each player's king every turn and test for check (to alert the player, the Piece movement logic already won't allow moves that break the check rule)
    * [ ] if king is in check, test if the king has any moves available or if another piece can take or block the checker
- Game object
    * [x] manage turns
    * [ ] manage checkmate
    * [x] work with Pawn to allow en passant only turn immediately after double step
    * [x] pawn promotion
- Display removed pieces in board string
- Test en-passant King-in-check special case

## Doing

- Rework legal_moves
    > Need to be able to see only truly legal moves available to every piece every turn in order to evaluate checkmate and draw
    * [ ] needs to filter for moves that would check self (this logic is currently in the move method)
    * [ ] needs to show moves that would block or take a checking piece (this logic is currently in the move method)
    * [ ] need to prevent test_check loops when looking at opposing Pieces' legal moves
    * [ ] rewrite tests that expect legal_moves to return a full list of untested potential moves

## Done

- Finish basic layout sketch
    * [x] Update which characters are shown for pieces on white squares so they look more consistent
    * [x] Add basic movement function to Board (just ability to move an existing piece to another location, with no constraints, overwriting any piece that is already there)
- Add basic movement logic
    * [x] Piece types have movement logic
- Add a method to Board that checks all legal moves and builds a dict every turn?
- Add subclasses for Piece types
    * [x] Redefine basic class structure
    * [x] King
    * [x] - test check
    * [x] - Castling
    * [x] Queen
    * [x] Rook
    * [x] Knight
    * [x] Bishop
    * [x] Pawn
- Add test_check to King
    > Test if any square is threatened. can be called on a specific square to check if a move is possible, or check own square (in_check method?) if no argument
- Add can_castle to King
    > Dictionary by name in Player class?
    * [x] King cannot castle if in check or pass through squares in check (not just final square)
    * [x] can_castle in King
    * [x] if king not moved:
    * [x] finds rooks through Board
    * [x] if not moved, identify queen side or king side based on position
    * [x] then check if same side squares are free
    * [x] if pass all these, return True, else False
- Piece.can_take needs to account for threats to squares with own pieces on them
    > Can't just use legal_moves bc that won't stop a King from putting itself in check by taking a piece
    * [x] or maybe have legal_moves include own pieces but disallow moving into them?
    * [x] similar to how king legal_moves shows moves into check, only move actually checks for check
- Minor issues
    * [x] Display board columns bottom to top (1 should be at bottom)
    * [x] update Piece.__repr__ to have a better message for piece with no pos
- Add tests for Piece.move
    * [x] Piece.move (most pieces)
    * [x] Pawn.move (en passant)
    * [x] King.castle
    * [x] King.test_check
- prevent moving another piece and putting king in check
    * [x] fix this to preview the whole move not just remove the piece
    * [x] e.g. a pawn can step forward if it continues to block a rook
    * [x] also taking a piece can remove a potential threat
- Move Pieces to module
- Refactor
    > Rebuild whole game structure to be more logical
    * [x] Game creates Board
    * [x] Board creates Players
    * [x] Players create Pieces and add to board
- Pawn promotion
