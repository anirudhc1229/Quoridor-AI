import logging
import time

from tqdm import tqdm

log = logging.getLogger(__name__)


class Arena():
    """
    An Arena class where any 2 agents can be pit against each other.
    """

    def __init__(self, players, game):
        """
        Input:
            players: List of players, either two or four
            game: Game object
        """
        self.players = players
        self.game = game

    def playGame(self, verbose=False):
        """
        Executes one episode of a game.

        Returns
            res: player who won the game (1 if player1, -1 if player2) or
                draw result returned from the game that is neither 1, -1, nor 0.
            average_turn_lengths:
                average time for each player to decide their moves
        """
        curPlayer = 0
        board = self.game.getInitBoard()
        it = 0

        while True:
            it += 1
            if verbose:
                print("Turn ", str(it), "Player ", str(curPlayer + 1))
                self.game.display(board)

            #start_time = time.time()
            valid_moves = self.game.getValidMoves(board, curPlayer)
            action = self.players[curPlayer](self.game.getCanonicalForm(board, curPlayer), valid_moves)
            #decision_time = time.time() - start_time

            #valids = self.game.getValidMoves(self.game.getCanonicalForm(board, curPlayer), curPlayer)

            if not action in valid_moves:
                log.error(f'Action {action} is not valid!')
                log.debug(f'valids = {valid_moves}')
            board, curPlayer = self.game.getNextState(board, curPlayer, action)
            self.game._base_board = board
            game_value = self.game.getGameEnded(board)
            if game_value != -1:
                break
        #res = curPlayer * self.game.getGameEnded(board, curPlayer)
        #average_turn_lengths = [total_turn_lengths[0] / ((it + 1) // 2), total_turn_lengths[1] / (it // 2)]
        if verbose:
            print("Game over: Turn ", str(it), "Result: Player ", str(game_value + 1), " wins!")
            self.game.display(board)
        return game_value

    def playGames(self, num, verbose=False):
        """
        Plays num games in which player1 starts num/2 games and player2 starts
        num/2 games.

        Returns:
            oneWon: games won by player1
            twoWon: games won by player2
            draws:  games won by nobody
        """

        num = int(num / 2)
        oneWon = 0
        twoWon = 0
        draws = 0
        average_times = [0, 0]
        for _ in tqdm(range(num), desc="Arena.playGames (1)"):
            gameResult, game_average_times = self.playGame(verbose=verbose)
            if gameResult == 1:
                oneWon += 1
            elif gameResult == -1:
                twoWon += 1
            else:
                draws += 1
            average_times[0] += game_average_times[0]
            average_times[1] += game_average_times[1]

        self.player1, self.player2 = self.player2, self.player1
        print("Swapping sides!")

        for _ in tqdm(range(num), desc="Arena.playGames (2)"):
            gameResult, game_average_times = self.playGame(verbose=verbose)
            if gameResult == -1:
                oneWon += 1
            elif gameResult == 1:
                twoWon += 1
            else:
                draws += 1
            average_times[0] += game_average_times[1]
            average_times[1] += game_average_times[0]
        average_times[0] /= num * 2
        average_times[1] /= num * 2
        return oneWon, twoWon, draws, average_times
