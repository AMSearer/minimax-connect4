import copy
import time
import abc
import random


class Game(object):
    """A connect four game."""

    def __init__(self, grid):
        """Instances differ by their board."""
        self.grid = copy.deepcopy(grid)  # No aliasing!

    def display(self):
        """Print the game board."""
        for row in self.grid:
            for mark in row:
                print(mark, end='')
            print()
        print()

    def possible_moves(self):
        """Return a list of possible moves given the current board."""
        # YOU FILL THIS IN
        colsEmpty = []
        col = 0
        while col <= 7:
            if self.colEmpty(col)[0]:
                colsEmpty.append(col)
            col += 1
        return colsEmpty

    def neighbor(self, col, color):
        """Return a Game instance like this one but with a move made into the specified column."""
        # YOU FILL THIS IN
        tempGrid = copy.deepcopy(self.grid)
        colTest = self.colEmpty(col)
        if colTest[0]:
            tempGrid[colTest[1]][col] = color
        newGame = Game(tempGrid)
        return newGame

    def utility(self, color):
        """Return the minimax utility value of this game"""
        # YOU FILL THIS IN
        w4s= 10
        w3s = 5
        w2s = 2
        if color == 'B':
            oColor = 'R'
        else:
            oColor = 'B'

        val = self.winning_state()
        if val != None:
            return val
        my4s = self.streakCheck(color, 4)
        my3s = self.streakCheck(color, 3)
        my2s = self.streakCheck(color, 2)
        o4s = self.streakCheck(oColor, 4)
        o3s = self.streakCheck(oColor, 3)
        o2s = self.streakCheck(oColor, 2)

        return (my4s * w4s + my3s * w3s + my2s * w2s) - (o4s * w4s + o3s * w3s + o2s * w2s)

    def streakCheck(self, color, streak):
        numStreaks = 0
        for row in range(0,8):
            for col in range(0,8):
                if self.grid[row][col] == color:
                    numStreaks += self.vertStreak(row, col, streak)
                    numStreaks += self.horzStreak(row, col, streak)
                    numStreaks += self.diagStreak(row, col, streak)
        return numStreaks

    def horzStreak(self, row, col, streak):
        runningCount = 0
        color = self.grid[row][col]
        for colJ in range(col, 8):
            if self.grid[row][colJ] == color:
                runningCount += 1
            else:
                break
        if runningCount >= streak:
            return 1
        else:
            return 0

    def vertStreak(self, row, col, streak):
        runningCount = 0
        color = self.grid[row][col]
        for rowI in range(row, 8):
            if self.grid[rowI][col] == color:
                runningCount += 1
            else:
                break
        if runningCount >= streak:
            return 1
        else:
            return 0

    def diagStreak(self, row, col, streak):
        runningCount = 0
        totalCount = 0
        color = self.grid[row][col]
        colJ = col

        #check the \ diag
        for rowI in range(row, 8):
            if colJ > 7:
                break
            elif self.grid[rowI][colJ] == color:
                runningCount += 1
            else:
                break
            colJ += 1

        if runningCount >= streak:
            totalCount += 1

        #reset counters
        runningCount = 0
        colJ = col

        #check the / diag
        for rowI in range (row, -1, -1):
            if colJ > 7:
                break
            elif self.grid[rowI][colJ] == color:
                runningCount += 1
            else:
                break
            colJ += 1

        if runningCount >= streak:
            totalCount += 1

        return totalCount

    def colEmpty(self, col):
        row = 7
        while row >= 0:
            if self.grid[row][col] == '-':
                return (True, row)
            else:
                row -= 1
        return (False, 8)

    def winning_state(self):
        """Returns float("inf") if Red wins; float("-inf") if Black wins;
           0 if board full; None if not full and no winner"""
        # YOU FILL THIS IN
        col = 0
        full = True
        while col <= 7:
            if self.colEmpty(col)[0]: # Returns True if not full
                full = False
            col += 1

        if self.winHorz('R') or self.winVert('R') or self.winDiag('R'):
            return float('inf')
        elif self.winHorz('B') or self.winVert('B') or self.winDiag('B'):
            return float('-inf')
        elif full:
            return 0
        else:
            return None

    def winHorz(self, color):
        for row in range(0,8):
            for col in range(0,5):
                if self.grid[row][col] == color:
                    win = True
                    for newCol in range(col+1, col+4):
                        if self.grid[row][newCol] != color:
                            win = False
                    if win:
                        return True
        return False

    def winVert(self, color):
        for col in range(0,8):
            for row in range(0,5):
                if self.grid[row][col] == color:
                    win = True
                    for newRow in range(row+1, row+4):
                        if self.grid[newRow][col] != color:
                            win = False
                    if win:
                        return True
        return False

    def winDiag(self, color):
        #check for \ diags
        for row in range(0,5):
            for col in range(0,5):
                if self.grid[row][col] == color:
                    win = True
                    for offSet in range(1,4):
                        if self.grid[row + offSet][col + offSet] != color:
                            win = False
                    if win:
                        return True
        #check for / diags
        for row in range(0,5):
            for col in range(3,8):
                if self.grid[row][col] == color:
                    win = True
                    for offSet in range(1,4):
                        if self.grid[row + offSet][col - offSet] != color:
                            win = False
                    if win:
                        return True
        return False

class Agent(object):
    """Abstract class, extended by classes RandomAgent, FirstMoveAgent, MinimaxAgent.
    Do not make an instance of this class."""

    def __init__(self, color):
        """Agents use either RED or BLACK chips."""
        self.color = color

    @abc.abstractmethod
    def move(self, game):
        """Abstract. Must be implemented by a class that extends Agent."""
        pass


class RandomAgent(Agent):
    """Naive agent -- always performs a random move"""

    def move(self, game):
        """Returns a random move"""
        # YOU FILL THIS IN
        moves = game.possible_moves()
        return random.choice(moves)


class FirstMoveAgent(Agent):
    """Naive agent -- always performs the first move"""

    def move(self, game):
        """Returns the first possible move"""
        # YOU FILL THIS IN
        return game.possible_moves()[0]


class MinimaxAgent(Agent):
    """Smart agent -- uses minimax to determine the best move"""

    def move(self, game):
        """Returns the best move using minimax"""
        # YOU FILL THIS IN
        fullTurnDepth = 2
        halfTurnDepth = 2 * fullTurnDepth - 1

        moves = game.possible_moves()
        choices = []
        for m in moves:
            choices.append((self.mini(game.neighbor(m, self.color), halfTurnDepth), m))
        mx = max(choices)
        return mx[1]


    def maxi(self, game, depth):
        end = game.winning_state()
        parentGame = Game(copy.deepcopy(game.grid))
        kidGames = []
        value = float("-inf")
        if end is not None:
            return end
        elif depth == 0:
            return game.utility(self.color)
        else:
            for m in parentGame.possible_moves():
                kid = parentGame.neighbor(m, self.color)
                kidGames.append(kid)
            for kid in kidGames:
                value = max(value, self.mini(kid, depth-1))
            return value

    def mini(self, game, depth):
        end = game.winning_state()
        parentGame = Game(copy.deepcopy(game.grid))
        kidGames = []
        value = float("inf")
        if end is not None:
            return end
        elif depth == 0:
            return game.utility(self.color)
        else:
            for m in parentGame.possible_moves():
                kid = parentGame.neighbor(m, self.color)
                kidGames.append(kid)
            for kid in kidGames:
                value = min(value, self.maxi(kid, depth-1))
            return value


def tournament(simulations=50):
    """Simulate connect four games, of a minimax agent playing
    against a random agent"""

    redwin, blackwin, tie = 0,0,0
    for i in range(simulations):

        game = single_game(io=False)
        winState = game.winning_state()

        print(i, end=" ")
        if winState == float("inf"):
            redwin += 1
        elif winState == float("-inf"):
            blackwin += 1
        elif winState == 0:
            tie += 1

    print("Red %d (%.0f%%) Black %d (%.0f%%) Tie %d" % (redwin,redwin/simulations*100,blackwin,blackwin/simulations*100,tie))

    return redwin/simulations


def single_game(io=True):
    """Create a game and have two agents play it."""

    game = Game([['-' for i in range(8)] for j in range(8)])   # 8x8 empty board
    if io:
        game.display()

    maxplayer = MinimaxAgent('R')
    minplayer = RandomAgent('B')

    while True:

        m = maxplayer.move(game)
        game = game.neighbor(m, maxplayer.color)
        winState = game.winning_state()
        if io:
            time.sleep(1)
            game.display()

        if winState is not None:
            break

        m = minplayer.move(game)
        game = game.neighbor(m, minplayer.color)
        if io:
            time.sleep(1)
            game.display()

        if winState is not None:
            break

    if winState == float("inf"):
        print("RED WINS!")
    elif winState == float("-inf"):
        print("BLACK WINS!")
    elif winState == 0:
        print("TIE!")

    return game


if __name__ == '__main__':
    #single_game(io=True)
    tournament(simulations=50)