
Planning

What are the objects?


What are the rules? 


How do we manage players? 
I want to switch to pytest from unittest. 


How do we determine/check who wins? 



How do we get user input/select actions? 


What is the deck like anyway? 




Overview of Gamemaster:
    generating deck? from file? programatically?
    Selects first player
    Deals 16 to each (gets rid of flowers and redeals?)

    First Person's turn:
        draw tile (first time has to be from wall)
        option to declare mahjong/check for mahjong? 
        discard a tile to the center 
    
    Wait time 5 seconds to give opportunity for pong, kong  (if playing computer, otherwise wait for )
        Or we could just offer each player option to take. 

    (centralized turn status. Clockwise.)






Checking for Mahjong:
    two win conditions: 7 pairs or all sets of 3 (or 4 of a kind) and 1 pair.
    one option: rely on the human to submit the pattern and have computer verify it's a valid pattern...
    COULD check 7! ways for each hand... expensive
    break it up by suits? 
    look for matches? How does it check/look for matches? 
        start at left... search right if it's the same; 
        reaches end next card. pop the cards as they come up. 
    Alternative way for matches: each tile has a numeric value for comparison's sake... each hand is a trie and you search the trie for it
    

    Go through player hand: 
        checking for 7 pair victory:
            go through 4 tiles and find exclusive pairs (if doesn't exist, reject)
            can delete pairs from effective hand as found, no problem.
        for each tile form possible contributions to mahjong:
            kong: hmm secret vs open kong 
                is there ever a situation where     
            pong
            chou
            pair
        essentially there's a tree of possibilities. For first tile 
                     T1
                    |  |  \
                    |  |     \
                  /     \      \
               /           \      \
             /              \      \
          /    /            \        \
       /      |               \         \
    doesnt   kong              pong     chou 
    belong    |                     \ 
             remove as if kong     remove thrupple as if pont
             |
             remaiing tiles search
game state

some kind 
