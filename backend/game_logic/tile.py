class Tile():
    """Tile class: there are 144 tiles in the game mahjong. Each follows this outline. 

    attributes
    ------------
    - suit (str): ball bam or crack
    - rank (int): 0-9


    methods
    --------------
    - displayTile: shows a pretty version
    - __eq__: two tiles are the same if suit and rank match (even though there are up to 4 copies)

    """
    def __init__(self, suit:str, rank:int) -> None:

        if suit in ["Ball", "Bam", "Crack"]:
            self.suit = suit
        else: 
            raise ValueError("creating tile improper suit")  #could add flowers in future
        
        if rank in range(1,10):
            self.rank = rank
        else: 
            raise ValueError("creating tile improper rank")  #could add flowers in future
    
    def displayTile(self)->str:   #test this out
        horiz = "--------- "
        vert =  "|       | "
        return "\n".join([horiz, vert, vert, str(self), vert, vert, horiz])

    def __str__(self):
        return f"|{self.suit:<5} {self.rank:>1}| "
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Tile):
            return (self.rank == other.rank) & (self.suit == other.suit)
        else: 
            return False

