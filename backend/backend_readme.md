I need to be more deliberate about the input/outputs for how Tkinter will interact with the game_logic. 

Let's assume open hand play at first for testing purposes.

1) Need to render tiles for each player at different parts of the screen
    - should probably delete the old tiles and replace in case you're in the middle of dragging?
        - or maybe it waits
2) Needs to render the graveyard?
    - 
3) Need to be able to pong/chou/kong
    - provide a button for each move? 
    - Maybe you click the graveyard tile to pick up, 
        - then it highlights/raises the relevant cards in your hand
        - then you "confirm move" or "cancel" or change the highlighted tiles to indicate the other chou type
4) Need to be able to draw a tile from the deck
5) Need to be able to choose a discard 
6) Edge case but need to be able to indicate which chou is desired when picking from the graveyard
7) Could implement a "pass to next player" to avoid revealing tiles 
8) should be able to reorder tiles in your hand 

Modes
- open hand vs closed hand
    - open hand: 
        - no pass & play
        - just switch immediately to next player or do single player 
    - closed: 
- pass & play view v.s. single player view(vs bots or vs online)
    - pass & play needs the pause between turns
    - single player view needs 

To simplify
- we could just do clicks... avoid drag and drop? 
    - but then tile reordering might be tricky. 


Other Notes
- I could make PNGs for each tile / the table
- Tags seem like a useful thing for canvas objects
- 

Tests
- Lol make sure you can't move/click other's tiles
- 