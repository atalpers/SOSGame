#!/usr/bin/python3

width = 900
heigth = 600
squareSize = 70

import pygame
from pygame.locals import *
from GameLogic import *
import pygame
from pygame.locals import *

# Common Setting

GREY = (50, 50, 50)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 50, 100)
MAGENTA = (255, 0, 255)
GREEN = (0, 100, 0)
YELLOW = (255, 100, 0)

# Initialize
pygame.init()

# Common Fonts and Texts
logoFont = pygame.font.Font('sewer.ttf', 50)
sbuttonFont = pygame.font.Font('sewer.ttf', 30)
mbuttonFont = pygame.font.Font('sewer.ttf', 28)
boardFont = pygame.font.Font('FFF_Tusj.ttf', 25)
scoreFont = pygame.font.Font('sewer.ttf', 32)
score1Font = pygame.font.Font('sewer.TTF', 32)
playerFont = pygame.font.Font('sewer.ttf', 32)
cellFont = pygame.font.Font('FFF_Tusj.ttf', 55)

# Text
logoText = logoFont.render('S O S', True, BLUE)
sbuttonText = sbuttonFont.render('SIMPLE', True, BLACK)
sbuttonhoverText = sbuttonFont.render('SIMPLE', True, MAGENTA)
mbuttonText = mbuttonFont.render('COMPLEX', True, BLACK)
mbuttonhoverText = mbuttonFont.render('COMPLEX', True, MAGENTA)
boardText = boardFont.render('SO', True, MAGENTA)
bscoreText = scoreFont.render('BLK:', True, BLACK)
rscoreText = scoreFont.render('WHT:', True, WHITE)
player1onText = playerFont.render('<--', True, GREEN)
player2onText = playerFont.render('<--', True, GREEN)
playeroffText = playerFont.render('<--', True, GREEN)

from GameLogic import *

# Import algorithms after common elements, I think pygame requires this ordering.

def drawBoard(mySurface, n):
    x = 70
    y = 70
    size = 70
    i = 0
    j = 0
    while (i != n):
        while (j != n):
            drawBoardCell(mySurface, MAGENTA, x, y, size)
            x = x + size
            j = j + 1
        j = 0
        i = i + 1
        x = 70
        y = y + size

def drawBoardCell(mySurface, COLOR, x, y, size):
    pos1 = (x, y)
    pos2 = (x + size, y)
    pos3 = (x + size, y + size)
    pos4 = (x, y + size)
    pygame.draw.line(mySurface, COLOR, pos1, pos2)
    pygame.draw.line(mySurface, COLOR, pos2, pos3)
    pygame.draw.line(mySurface, COLOR, pos3, pos4)
    pygame.draw.line(mySurface, COLOR, pos4, pos1)
    drawBoardLetter(mySurface, x, y, size)

def drawBoardLetter(mySurface, x, y, size):
    textRect = boardText.get_rect()
    textRect.topleft = (x, (y + 15))
    mySurface.blit(boardText, textRect)

def displayTeam(mySurface):
    textRect = bscoreText.get_rect()
    textRect.topleft = (600, 200)
    mySurface.blit(bscoreText, textRect)
    textRect.topleft = (600, 300)
    mySurface.blit(rscoreText, textRect)

def displayScore(mySurface, n, scores):
    clearScore(mySurface)
    player1str = str(scores[0])
    player2str = str(scores[1])
    player1 = score1Font.render(player1str, True, BLACK)
    player2 = score1Font.render(player2str, True, WHITE)
    textRect = player1.get_rect()
    textRect.topleft = (715, 190)
    mySurface.blit(player1, textRect)
    textRect.topleft = (715, 290)
    mySurface.blit(player2, textRect)

def clearScore(mySurface):
    rect = (715, 190, 70, 70)
    pygame.draw.rect(mySurface, GREY, rect)
    rect = (715, 290, 70, 70)
    pygame.draw.rect(mySurface, GREY, rect)

def displayPlayer(mySurface, n, player):
    if (player == 1):
        textRect = player1onText.get_rect()
        textRect.topleft = (800, 200)
        mySurface.blit(player1onText, textRect)
        textRect = playeroffText.get_rect()
        textRect.topleft = (800, 300)
        mySurface.blit(playeroffText, textRect)
    if (player == 2):
        textRect = playeroffText.get_rect()
        textRect.topleft = (800, 200)
        mySurface.blit(playeroffText, textRect)
        textRect = player2onText.get_rect()
        textRect.topleft = (800, 300)
        mySurface.blit(player2onText, textRect)


def drawCell(mySurface, board, i, j, player):
    letter = ''
    clearCell(mySurface, board, i, j)
    if (board[i][j] == 1):
        x = 71 + (j * 70) + 18
        y = 71 + (i * 70) + 12
        letter = 'S'
    elif(board[i][j] == 2):
        x = 71 + (j * 70) + 22
        y = 71 + (i * 70) + 12
        letter = 'O'
    if (player == 1):
        text = cellFont.render(letter, True, BLACK)
        textRect = text.get_rect()
        textRect.topleft = (x, y)
        mySurface.blit(text, textRect)
    else:
        text = cellFont.render(letter, True, WHITE)
        textRect = text.get_rect()
        textRect.topleft = (x, y)
        mySurface.blit(text, textRect)

def clearCell(mySurface, board, i, j):
    x = 71 + (j * 70)
    y = 71 + (i * 70)
    rect = (x, y, 69, 69)
    pygame.draw.rect(mySurface, GREEN, rect)

def drawLines(mySurface, lines, player):
    if (lines):
        for i in range(len(lines)):
            # Vertical lines
            if (lines[i][1] == lines[i][3]):
                x = 70 * (lines[i][1] + 1) + 35
                y = 70 * (lines[i][0] + 1) + 35  # Adjusted starting y-coordinate
                x1 = 70 * (lines[i][3] + 1) + 35
                y1 = 70 * (lines[i][2] + 1) + 35  # Adjusted ending y-coordinate
            # Horizontal lines
            elif (lines[i][0] == lines[i][2]):
                x = 70 * (lines[i][1] + 1) + 35  # Adjusted starting x-coordinate
                y = 70 * (lines[i][0] + 1) + 35
                x1 = 70 * (lines[i][3] + 1) + 35  # Adjusted ending x-coordinate
                y1 = 70 * (lines[i][2] + 1) + 35
            # Diagonal lines
            else:
                x = 70 * (lines[i][1] + 1) + 35
                y = 70 * (lines[i][0] + 1) + 35
                x1 = 70 * (lines[i][3] + 1) + 35
                y1 = 70 * (lines[i][2] + 1) + 35
            pos1 = (x, y)
            pos2 = (x1, y1)
            if (player == 1):
                pygame.draw.line(mySurface, BLACK, pos1, pos2)
            elif (player == 2):
                pygame.draw.line(mySurface, WHITE, pos1, pos2)




def selectSquare(mySurface, board, n, size, player):
    mouse = pygame.mouse.get_pos()
    letter = ''

    i = (mouse[0] - 70) // squareSize
    j = (mouse[1] - 70) // squareSize

    # Check if mouse click is inside the board's bounds
    if 70 <= mouse[0] <= (70 + n * size) and 70 <= mouse[1] <= (70 + n * size):
        if 0 <= i < n and 0 <= j < n and possibleSquare(board, n, j, i):
            # Determine which letter to place based on mouse position
            if mouse[0] % squareSize < squareSize / 2:
                letter = 'S'
            else:
                letter = 'O'
            board[j][i] = 1 if letter == 'S' else 2
            return [i, j]

    return [-1, -1]



def gameloop(n, size):
    pygame.init()
    mySurface = pygame.display.set_mode((width, heigth))
    board = [[0] * n for _ in range(n)]
    pygame.display.set_caption('SOS')
    inProgress = True
    player = 1
    scores = [0, 0]

    mySurface.fill(GREY)
    drawBoard(mySurface, n)
    displayTeam(mySurface)

    while inProgress:
        position = [-1, -1]
        lines = [[] for _ in range(n)]
        displayScore(mySurface, n, scores)
        displayPlayer(mySurface, n, player)

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                position = selectSquare(mySurface, board, n, size, player)
                if position != [-1, -1]:
                    drawCell(mySurface, board, position[1], position[0], player)
                    lines = updateScoreS(board, n, position[1], position[0], scores, player)
                    drawLines(mySurface, lines, player)
                    lines = updateScoreO(board, n, position[1], position[0], scores, player)
                    drawLines(mySurface, lines, player)
                    displayScore(mySurface, n, scores)
                    player = 1 if player == 2 else 2

            if event.type == QUIT:
                inProgress = False

        pygame.display.update()

