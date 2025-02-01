# from unittest import TestCase
# from mahjong.tile import Tile
# import mahjong.check_win
# from mahjong.deck import Deck

# class checkWinTests(TestCase):
#     def setUp(self):
#         self.myHand = []
#         d = Deck()
#         d.shuffle(test = True) #test fixes seed
#         '''|Bam3| 
#         |Ball3| |Bam8| |Bam3| |Crack5| |Ball6| |Crack5| |Bam7| |Crack7|
#         |Bam3| |Crack8| |Ball7| |Ball7| |Ball5| |Bam7| |Ball7| |Crack7| |Ball6|
#         '''
#         d.moveNRandom(17, self.myHand, test = True)

#     def test_getChouIndices(self):  
#         convenienceMeld = mahjong.checkWin.getChouIndices(4,self.myHand)
#         for thrupplePosInd in [i for i in convenienceMeld if i != None]: 
#             handString = "\n".join([str(x) + str(self.myHand[x]) for x in range(len(self.myHand))])
#             meldString = "\n".join([str(x) + str(self.myHand[x]) for x in thrupplePosInd])
#             msg = "\nTarget: " + str(self.myHand[4])+"\nHand:\n"+ handString + "\nMeld:\n" + meldString
#             self.assertEqual(thrupplePosInd, [4,12,14], msg = msg)

#     def test_checkWinMelds_simpleCase(self):
#         """
#         original
#         ----------
#        0 |Ball3| |Bam8| |Bam3| |Crack5| 
#        4 |Ball6| |Crack5| |Bam7| |Crack7|
#        8 |Bam3| |Crack8| |Ball7| |Ball7| 
#       12 |Ball5| |Bam7| |Ball7| |Crack7| |Ball6|
        
#          modified
#          ----------
#        0 |Ball3|X  |Ball3|X  |Bam6|X  |Crack7| X                  Ball3 pair, ball 678, ball 567
#        4 |Ball6|X  |Crack5|X |Bam7|X  |Crack7|X                   Crack 7 * 3, crack 567
#        8 |Ball8|X  |Crack7|X |Bam8|X  |Ball7|X                    Bam 678 
#       12 |Ball5|X  |Crack6|X |Ball7|X |Crack7|X |Ball6|X           


#         0: pair         15
#         1: pair         
#         2: chou         10
#         3: chou (567)
#         4: chou (678)
#         5: 


#         STEPS BY HAND
#         -------------------
#         0: pair   -> drop (0,1) [recursion couter 1 \/]

#                              |Bam6|X  |Crack7| X                  Ball3 pair, ball 678, ball 567
#        4 |Ball6|X  |Crack5|X |Bam7|X  |Crack7|X                   Crack 7 * 3, crack 567
#        8 |Ball8|X  |Crack7|X |Bam8|X  |Ball7|X                    Bam 678 
#       12 |Ball5|X  |Crack6|X |Ball7|X |Crack7|X |Ball6|X 

        
#         0: chou XOO   -> drop (0,4,8) [recursion counter 2 \/]

#                                       |Crack7| X                  Ball3 pair, ball 678, ball 567
#        4 |Ball6|X  |Crack5|X          |Crack7|X                   Crack 7 * 3, crack 567
#        8 |Ball8|X  |Crack7|X          |Ball7|X                    Bam 678 
#       12 |Ball5|X  |Crack6|X |Ball7|X |Crack7|X |Ball6|X 

#       0: chou OOX -> [[0,3,5,10], [2],[8]] drop (10,2,8) [recursion counter 3 \/]
        
#                                       |Crack7| X                  Ball3 pair, ball 678, ball 567
#        4 |Ball6|X                     |Crack7|X                   Crack 7 * 3, crack 567
#        8 |Ball8|X  |Crack7|X          |Ball7|X                    Bam 678 
#       12 |Ball5|X            |Ball7|X           |Ball6|X 

#       0: pong  -> drop (0,2,4) [recursion counter 4 \/]
        
#                                                                   Ball3 pair, ball 678, ball 567
#        4 |Ball6|X                                                 Crack 7 * 3, crack 567
#        8 |Ball8|X                     |Ball7|X                    Bam 678 
#       12 |Ball5|X            |Ball7|X           |Ball6|X 

#       0: chou XOO  -> drop (0,1,2) [recursion counter 5 \/]  ~ note could cause confusion if this were 7 ball rn
#                                                                   Ball3 pair, ball 678, ball 567
#        4                                                          Crack 7 * 3, crack 567
#        8                                                          Bam 678 
#       12 |Ball5|X            |Ball7|X           |Ball6|X 

#       0: chou XOO  -> drop (0,1,2) [recursion counter 6 \/]  ~ note could cause confusion if this were 7 ball rn
#                                                                   Ball3 pair, ball 678, ball 567
#        4                                                          Crack 7 * 3, crack 567
#        8                                                          Bam 678 
#       12           


#       STEPS IN DEBUG 
#         -------------------
#         No chou
#         0: pair   -> drop (0,1) [recursion couter 1 \/]
#         Indeed first is 6 bam
#                              |Bam6|X  |Crack7| X                  Ball3 pair, ball 678, ball 567
#        4 |Ball6|X  |Crack5|X |Bam7|X  |Crack7|X                   Crack 7 * 3, crack 567
#        8 |Ball8|X  |Crack7|X |Bam8|X  |Ball7|X                    Bam 678 
#       12 |Ball5|X  |Crack6|X |Ball7|X |Crack7|X |Ball6|X 

#         It found the 048 chou
#         0: chou XOO   -> drop (0,4,8) [recursion counter 2 \/]
#         Dropped to this config correctly (12 tiles)
#                                       |Crack7| X                  Ball3 pair, ball 678, ball 567
#        4 |Ball6|X  |Crack5|X          |Crack7|X                   Crack 7 * 3, crack 567
#        8 |Ball8|X  |Crack7|X          |Ball7|X                    Bam 678 
#       12 |Ball5|X  |Crack6|X |Ball7|X |Crack7|X |Ball6|X 

      
#       0: chou OOX -> [[0,3,5,10], [2],[8]] drop (10,2,8) [recursion counter 3 \/]
#       0: chou OOX -> [[0,3,5,10], [2],[8]] drop (0,8,2) [recursion counter 3 \/] ACTUAL; EXPLANATION INDEX ALWAYS INCLUDED AS FIRST IN LIST OF GETCHOU
#         Dropped to this fig (9 tiles) DIFFERENT!
#                                       |Crack7| X                  Ball3 pair, ball 678, ball 567
#        4 |Ball6|X                     |Crack7|X                   Crack 7 * 3, crack 567
#        8 |Ball8|X  |Crack7|X          |Ball7|X                    Bam 678 
#       12 |Ball5|X            |Ball7|X           |Ball6|X 

#       ACTUAL
#                                                                   Ball3 pair, ball 678, ball 567
#        4 |Ball6|X                     |Crack7|X                   Crack 7 * 3, crack 567
#        8 |Ball8|X  |Crack7|X          |Ball7|X                    Bam 678 
#       12 |Ball5|X            |Ball7|X |Crack7|X |Ball6|X 

#     0: chou XOO & chou OXO (which wins? XOO but doesn't matter in this case) 
#     -> [[0,8], [4,6],[2]] drop (0,6,2) [recursion counter 4 \/] 

#     Dropped correctly
#                                                                   Ball3 pair, ball 678, ball 567
#        4                              |Crack7|X                   Crack 7 * 3, crack 567
#        8           |Crack7|X          |Ball7|X                    Bam 678 
#       12 |Ball5|X                     |Crack7|X |Ball6|X 

      
#        0: triple  -> drop (0,1,4) [recursion counter 5 \/] 
#     Dropped Correctly                                             Ball3 pair, ball 678, ball 567
#        4                                                          Crack 7 * 3, crack 567
#        8                              |Ball7|X                    Bam 678 
#       12 |Ball5|X                               |Ball6|X 

      
#       0: chou OOX  -> drop (0,1,2) [recursion counter 6 \/] 
#                                                                   Ball3 pair, ball 678, ball 567
#        4                                                          Crack 7 * 3, crack 567
#        8                                                          Bam 678 
#       12  

#       Returns true and starts climbing back up recursion ladder
#       Counts 1 for counter 6 but got stored in the rest
#       += meldcount for level 5 but didn't add theRest to meldcount
#       FIXED 
#         """
#         self.myHand[1] = Tile("Ball", 3)
#         self.myHand[2] = Tile("Bam", 6)
#         self.myHand[10] = Tile("Bam", 8)
#         self.myHand[3] = Tile("Crack", 7)
#         self.myHand[9] = Tile("Crack", 7)
#         self.myHand[13] = Tile("Crack", 6)
#         self.myHand[8] = Tile("Ball", 8)

#         res = mahjong.checkWin.checkMahjongMelds(self.myHand) #maybe need a required parameter. 
#         self.assertEqual(res, (True, 5, 1))

#     def test_checkWinMelds_wrongTurn(self):
#         """
#        wrong turn cases should invert 4->2 w 2 -> 4 O a Kind priority or invert chou before O kind)
#          ---------- 
#        0 |Ball1|X  |Ball2|X |Ball3|X  |Ball4| X                  Ball3 pair, ball 678, ball 567
#        4 |Ball1|X  |Crack5|X |Bam8|X  |Crack2|X                   Crack 7 * 3, crack 567
#        8 |Ball8|X  |Crack7|X |Bam8|X  |Ball7|X                    Bam 678 
#       12 |Ball9|X  |Crack2|X |Bam8|X |Crack6|X |Crack2|X      
       
#        STUCK!
#        0                              |Ball4| X                  Ball3 pair, ball 678, ball 567
#        4 |Ball1|X  |Crack5|X |Bam8|X  |Crack2|X                   Crack 7 * 3, crack 567
#        8 |Ball8|X  |Crack7|X |Bam8|X  |Ball7|X                    Bam 678 
#       12 |Ball9|X  |Crack2|X |Bam8|X |Crack6|X |Crack2|X    
#     """
#         suits = ["Ball"]*5 + ["Crack", "Bam", "Crack", "Ball", "Crack", "Bam", "Ball", "Ball", "Crack", "Bam", "Crack", "Crack"]
#         ranks = [1,2,3,4,1,5,8,2,8,7,8,7,9,2,8,6,2]
#         assert(len(suits) == len(ranks) & len(ranks)==17)
#         self.myHand = list(map(lambda x,y: Tile(x,y), suits, ranks))  #verified, good creation
#         res = mahjong.checkWin.checkMahjongMelds(self.myHand) #maybe need a required parameter. 
#         self.assertEqual(res, (True, 5, 1))
#     # def test_checkWinMelds_fourPairs(self):  #TODO: TEST restriction on number of pairs (or kongs?), already restricted. 
    
#     def test_checkWinMelds_wrongTurnDeep(self):
#         """
#        wrong turn cases should invert 4->2 w 2 -> 4 O a Kind priority or invert chou before O kind)
#          ---------- 
#        0 |Ball1|X  |Ball2|X |Ball3|X  |Crack2| X                  Ball3 pair, ball 678, ball 567
#        4 |Crack6|X  |Crack5|X |Bam8|X  |Ball4|X                   Crack 7 * 3, crack 567
#        8 |Ball8|X  |Crack7|X |Bam8|X  |Ball7|X                    Bam 678 
#       12 |Ball9|X  |Crack2|X |Bam8|X |Ball1|X |Crack2|X      
#        """
#         suits = ["Ball"]*3 + ["Crack", "Crack", "Crack", "Bam", "Ball", "Ball", "Crack", "Bam", "Ball", "Ball", "Crack", "Bam", "Ball", "Crack"]
#         ranks = [1,2,3,2,6,5,8,4,8,7,8,7,9,2,8,1,2]
#         assert(len(suits) == len(ranks) & len(ranks)==17)
#         self.myHand = list(map(lambda x,y: Tile(x,y), suits, ranks))  #verified, good creation
#         res = mahjong.checkWin.checkMahjongMelds(self.myHand) #maybe need a required parameter. 
#         self.assertEqual(res, (True, 5, 1))
#     def test_getChou2(self): #TODO: see if this returns anything valid? Also it didn't lock the tile. 
#         suits = ["Bam","Crack","Bam","Crack","Crack","Ball","Ball","Ball","Crack","Ball","Bam","Ball","Ball","Ball"]
#         ranks = [7,1,8,2,3,6,3,3,3,4,7,4,4,9]
#         self.testHand = list(map(lambda x,y: Tile(x,y), suits, ranks))
#         res = mahjong.checkWin.getChouIndices(-1, self.testHand)
#         self.assertEqual(res, [None, None, None])

#         """PlayerW got |Ball  9|  from graveyard.
# Hand
#  1 |Bam   7|
#  2 |Crack 1|
#  3 |Bam   8|
#  4 |Crack 2|
#  5 |Crack 3|
#  6 |Ball  6|
#  7 |Ball  3|
#  8 |Ball  3|
#  9 |Crack 3|
# 10 |Ball  4|
# 11 |Bam   7|
# 12 |Ball  4|
# 13 |Ball  4|
# 14 |Ball  9|"""
#         pass