import pygame
from pygame.locals import *
from Layout import *
from random import choice
class SOSGame:
    def __init__(self, n):
        self.board = self.newBoard(n)
        self.scores = [0, 0]
        self.player = 1
        self.n = n
        self.last_placed_cell = [-1, -1]
        self.game_record = ""  # Initialize an empty string to record game events

    def record_event(self, event):
        self.game_record += event + "\n"  # Append the event and a newline to the record
    def newBoard(self, n):
        return [[0] * n for _ in range(n)]

    def possibleSquare(self, i, j):
        return self.board[i][j] == 0

    def check_direction(self, i, j, di, dj):
        return (0 <= i + 2 * di < self.n and 0 <= j + 2 * dj < self.n and
                self.board[i][j] == 1 and self.board[i + di][j + dj] == 2 and self.board[i + 2 * di][j + 2 * dj] == 1)

    def check_sos_at(self, i, j, dx, dy):
        # Check if the positions i+dx and i+2*dx, j+dy and j+2*dy are within the board
        if 0 <= i + 2 * dx < self.n and 0 <= j + 2 * dy < self.n:
            # Check for the sequence "SOS"
            if self.board[i][j] == 1 and self.board[i + dx][j + dy] == 2 and self.board[i + 2 * dx][j + 2 * dy] == 1:
                return True
        return False

    def updateScoreS(self, i, j):
        lines = []

        # Define directions: Horizontal, Vertical, Diagonal (top-left to bottom-right), Diagonal (top-right to bottom-left)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for di, dj in directions:
            if 0 <= i + di < self.n and 0 <= j + dj < self.n and self.board[i + di][j + dj] == 2:  # Check for 'O'
                if 0 <= i + 2 * di < self.n and 0 <= j + 2 * dj < self.n and self.board[i + 2 * di][
                    j + 2 * dj] == 1:  # Check for another 'S'
                    lines.append([i, j, i + 2 * di, j + 2 * dj])  # SOS pattern found

        return lines

    def updateScoreO(self, i, j):
        lines = []

        # Define directions: Horizontal, Vertical, Diagonal (top-left to bottom-right), Diagonal (top-right to bottom-left)
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for di, dj in directions:
            if 0 <= i - di < self.n and 0 <= j - dj < self.n and self.board[i - di][
                j - dj] == 1:  # Check for 'S' in one direction
                if 0 <= i + di < self.n and 0 <= j + dj < self.n and self.board[i + di][
                    j + dj] == 1:  # Check for 'S' in the opposite direction
                    lines.append([i - di, j - dj, i + di, j + dj])  # SOS pattern found

        return lines

    def checkSOS(self, i, j):
        # Define all possible directions: right, down, diagonal down-right, diagonal up-right
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        sos_lines = []

        for dx, dy in directions:
            # If an SOS sequence is found in any direction, add to sos_lines
            if self.check_sos_at(i, j, dx, dy):
                sos_lines.append([i, j, i + 2 * dx, j + 2 * dy])
        print(f"Checking sequences at ({i}, {j}): {directions}")
        return sos_lines

    def checkAllSOS(self, i, j):
        all_sos_lines = []

        # Checking for all possible directions for the "S" cell
        if self.board[i][j] == 1:
            all_sos_lines.extend(self.updateScoreS(i, j))

        # Checking for all possible directions for the "O" cell
        elif self.board[i][j] == 2:
            all_sos_lines.extend(self.updateScoreO(i, j))

        return all_sos_lines

    def computer_move(self):
        valid_moves = [(i, j) for i in range(self.n) for j in range(self.n) if self.possibleSquare(i, j)]
        if valid_moves:
            move = choice(valid_moves)
            letter = choice(['S', 'O'])  # Randomly choose between 'S' and 'O'
            self.board[move[0]][move[1]] = 1 if letter == 'S' else 2
            self.record_event(f"Computer placed {letter} at ({move[0]}, {move[1]})")
            return move
        return None

    def gameloop(self, n, size, player1_type, player2_type):
        pygame.init()
        mySurface = pygame.display.set_mode((width, heigth))
        pygame.display.set_caption('SOS')
        inProgress = True

        self.board = self.newBoard(n)
        self.scores = [0, 0]
        self.player = 1

        mySurface.fill(GREY)
        drawBoard(mySurface, n)
        displayTeam(mySurface)

        while inProgress:
            displayScore(mySurface, n, self.scores)
            displayPlayer(mySurface, n, self.player)

            # Handle Computer moves
            if ((player1_type == 'Computer' and self.player == 1) or
                    (player2_type == 'Computer' and self.player == 2)):
                pygame.time.wait(500)  # Delay for computer move simulation
                i, j = self.computer_move()
                if i is not None and j is not None:
                    drawCell(mySurface, self.board, i, j, self.player)
                    sos_lines = self.checkAllSOS(i, j)
                    if sos_lines:
                        self.scores[self.player - 1] += len(sos_lines)
                        for line in sos_lines:
                            drawLines(mySurface, [line], self.player)
                        displayScore(mySurface, n, self.scores)
                    self.player = 2 if self.player == 1 else 1

                    if self.end_condition_met():
                        inProgress = False
                        continue

            # Handle Human player moves
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if self.player == 1 and player1_type == 'Human':
                        position = self.selectSquare(mySurface, n, size, self.player)
                    elif self.player == 2 and player2_type == 'Human':
                        position = self.selectSquare(mySurface, n, size, self.player)

                    if position != [-1, -1]:
                        letter = 'S' if self.board[position[1]][position[0]] == 1 else 'O'
                        self.record_event(f"Player {self.player} placed {letter} at ({position[1]}, {position[0]})")
                        drawCell(mySurface, self.board, position[1], position[0], self.player)
                        sos_lines = self.checkAllSOS(position[1], position[0])
                        if sos_lines:
                            self.scores[self.player - 1] += len(sos_lines)
                            for line in sos_lines:
                                drawLines(mySurface, [line], self.player)
                            displayScore(mySurface, n, self.scores)
                        self.player = 1 if self.player == 2 else 2

                        if self.end_condition_met():
                            inProgress = False
                            continue

                if event.type == QUIT:
                    inProgress = False

            pygame.display.update()

        # Announce Winner and end the game
        if not inProgress:
            # Debug: Print scores for verification
            print("Debug - Player 1 Score:", self.scores[0], "Player 2 Score:", self.scores[1])

            # Determine the winner
            if self.scores[0] > self.scores[1]:
                winner = "Player 1 wins!"
            elif self.scores[0] < self.scores[1]:
                winner = "Player 2 wins!"
            else:
                winner = "It's a tie!"

            print(winner)
            self.record_event(winner)

            # Write game record to a file
            with open("game_record.txt", "w") as file:
                file.write(self.game_record)

        pygame.display.update()

        pygame.display.update()

    def selectSquare(self, mySurface, n, size, player):
        mouse = pygame.mouse.get_pos()
        letter = ''

        i = (mouse[0] - 70) // squareSize
        j = (mouse[1] - 70) // squareSize

        # Check if mouse click is inside the board's bounds and if it's a valid move
        if 70 <= mouse[0] <= (70 + n * size) and 70 <= mouse[1] <= (70 + n * size) and self.possibleSquare(j, i):
            # Determine which letter to place based on mouse position
            if mouse[0] % squareSize < squareSize / 2:
                letter = 'S'
            else:
                letter = 'O'
            self.board[j][i] = 1 if letter == 'S' else 2
            return [i, j]

        return [-1, -1]

    def game_over(self):
        # Define game over condition (e.g., all cells filled or any other condition)
        return all(cell != 0 for row in self.board for cell in row)



class SimpleGame(SOSGame):
    def __init__(self, n):
        super().__init__(n)

    def end_condition_met(self):
        # Check the entire board for an SOS sequence
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                sos_lines = self.checkSOS(i, j)
                if sos_lines:
                    current_player = 1 if self.player == 2 else 2
                    self.scores[current_player - 1] += len(sos_lines)
                    print(f"End condition checked. SOS found by Player {current_player}? True")
                    return True
        print("End condition checked. SOS found? False")
        return False

class ComplexGame(SOSGame):
    def end_condition_met(self):
        return all(cell != 0 for row in self.board for cell in row)

def end_condition_met(self):
    return False