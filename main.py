from QuoridorGame import QuoridorGame
from HumanPlayer import HumanPlayer
from RandomPlayer import RandomPlayer
from AnirudhConor import AnirudhConor

from Arena import Arena

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

g = QuoridorGame(n_players = 2, visualize = True, thorough_check = True)

# all players
rp = RandomPlayer(g).play
hp = HumanPlayer(g).play
yp = AnirudhConor(g).play

players = [yp,hp]

arena = Arena(players, g)


result = arena.playGame(verbose=True)
print ("Player %i won!" % (result + 1))

"""
p1wins, p2wins, draws, average_times = arena.playGames(num=10, verbose=True)

print('P1 won', p1wins, 'times')
print('P2 won', p2wins, 'times')
print('Draw', draws, 'times')
"""
