import pygame
from pygame.locals import *
from GameLogic import *
from Layout import *


def select_board_size_gui():
    pygame.init()
    mySurface = pygame.display.set_mode((width, heigth))
    board_font = pygame.font.Font(None, 32)

    # Use the logo font and color for the title
    title_font = logoFont
    title_color = BLUE

    # Create the title surface
    title_surface = title_font.render('SOS', True, title_color)
    title_x = (width - title_surface.get_width()) // 2
    title_y = 50

    # Button configuration
    button_width = 50
    button_height = 50
    button_spacing = 10
    total_buttons_width = (7 * button_width) + (6 * button_spacing)
    start_x = (width - total_buttons_width) // 2

    board_buttons = []
    for i in range(1, 8):
        x_position = start_x + ((i - 1) * (button_width + button_spacing))
        button_rect = pygame.Rect(x_position, 200, button_width, button_height)  # Adjusted y position for buttons
        txt_surface = board_font.render(str(i), True, pygame.Color('black'))
        text_x = button_rect.x + (button_width - txt_surface.get_width()) // 2
        text_y = button_rect.y + (button_height - txt_surface.get_height()) // 2
        board_buttons.append((button_rect, txt_surface, (text_x, text_y), i))

    while True:
        mySurface.fill(GREY)

        # Draw the title
        mySurface.blit(title_surface, (title_x, title_y))

        # Draw the buttons
        for button, txt_surface, text_pos, _ in board_buttons:
            pygame.draw.rect(mySurface, pygame.Color('white'), button)
            mySurface.blit(txt_surface, text_pos)

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                for button, _, _, value in board_buttons:
                    if button.collidepoint(event.pos):
                        return value
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()


def drawPlayerTypeButtons(mySurface):
    button_width = 150
    button_height = 50
    button_spacing = 10  # Space between two buttons
    total_width = (2 * button_width) + button_spacing
    start_x = 380 + ((150 - total_width) // 2)  # Centering under the Simple/Complex buttons

    # Define global variables for button rectangles
    global p1_human_button_rect, p1_computer_button_rect, p2_human_button_rect, p2_computer_button_rect

    # Player 1 buttons
    p1_human_button_rect = pygame.Rect(start_x, 400, button_width, button_height)
    p1_computer_button_rect = pygame.Rect(start_x + button_width + button_spacing, 400, button_width, button_height)

    pygame.draw.rect(mySurface, WHITE, p1_human_button_rect)  # Human button for Player 1
    pygame.draw.rect(mySurface, WHITE, p1_computer_button_rect)  # Computer button for Player 1

    human_text = sbuttonFont.render('Human P1', True, BLACK)
    computer_text = sbuttonFont.render('Comp P1', True, BLACK)

    # Centering text on the buttons
    mySurface.blit(human_text, (p1_human_button_rect.x + (button_width - human_text.get_width()) // 2, p1_human_button_rect.y + (button_height - human_text.get_height()) // 2))
    mySurface.blit(computer_text, (p1_computer_button_rect.x + (button_width - computer_text.get_width()) // 2, p1_computer_button_rect.y + (button_height - computer_text.get_height()) // 2))

    # Player 2 buttons
    p2_human_button_rect = pygame.Rect(start_x, 460, button_width, button_height)
    p2_computer_button_rect = pygame.Rect(start_x + button_width + button_spacing, 460, button_width, button_height)

    pygame.draw.rect(mySurface, WHITE, p2_human_button_rect)  # Human button for Player 2
    pygame.draw.rect(mySurface, WHITE, p2_computer_button_rect)  # Computer button for Player 2

    human_text = sbuttonFont.render('Human P2', True, BLACK)
    computer_text = sbuttonFont.render('Comp P2', True, BLACK)

    # Centering text on the buttons
    mySurface.blit(human_text, (p2_human_button_rect.x + (button_width - human_text.get_width()) // 2, p2_human_button_rect.y + (button_height - human_text.get_height()) // 2))
    mySurface.blit(computer_text, (p2_computer_button_rect.x + (button_width - computer_text.get_width()) // 2, p2_computer_button_rect.y + (button_height - computer_text.get_height()) // 2))





def menu():
    pygame.init()
    mySurface = pygame.display.set_mode((width, heigth))
    pygame.display.set_caption('SOS')
    inProgress = True

    board_size = select_board_size_gui()

    global tableSize
    global squareSize
    tableSize = board_size
    squareSize = width // tableSize

    player1_type = None  # None, 'Human', or 'Computer'
    player2_type = None  # None, 'Human', or 'Computer'

    mySurface.fill(GREY)
    displayLogo(mySurface)

    while inProgress:
        drawButton(mySurface, BLACK, 0)
        drawPlayerTypeButtons(mySurface)  # Function to draw player type buttons

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                # Check for SIMPLE and COMPLEX game buttons
                if ((380 + 150) > mouse[0] > 380 and (240 + 50) > mouse[1] > 240):
                    game_instance = SimpleGame(tableSize)
                    game_instance.gameloop(tableSize, squareSize, player1_type, player2_type)
                    inProgress = False
                if ((380 + 150) > mouse[0] > 380 and (310 + 50) > mouse[1] > 310):
                    game_instance = ComplexGame(tableSize)
                    game_instance.gameloop(tableSize, squareSize, player1_type, player2_type)
                    inProgress = False

                # Check for Player Type buttons
                if isPlayer1HumanButtonClicked(mouse):
                    player1_type = 'Human'
                elif isPlayer1ComputerButtonClicked(mouse):
                    player1_type = 'Computer'
                elif isPlayer2HumanButtonClicked(mouse):
                    player2_type = 'Human'
                elif isPlayer2ComputerButtonClicked(mouse):
                    player2_type = 'Computer'

            if event.type == QUIT:
                inProgress = False

        pygame.display.update()



def isButtonClicked(mouse, button_rect):
    return button_rect.collidepoint(mouse)

def isPlayer1HumanButtonClicked(mouse):
    return isButtonClicked(mouse, p1_human_button_rect)

def isPlayer1ComputerButtonClicked(mouse):
    return isButtonClicked(mouse, p1_computer_button_rect)

def isPlayer2HumanButtonClicked(mouse):
    return isButtonClicked(mouse, p2_human_button_rect)

def isPlayer2ComputerButtonClicked(mouse):
    return isButtonClicked(mouse, p2_computer_button_rect)


def displayLogo(mySurface):
    textRect = logoText.get_rect()
    textRect.center = (width // 2, 110)  # Center horizontally
    mySurface.blit(logoText, textRect)

def drawButton(mySurface, textColor, option):
    pygame.draw.rect(mySurface, WHITE, (380, 240, 150, 50))
    pygame.draw.rect(mySurface, WHITE, (380, 310, 150, 50))
    textRect = sbuttonText.get_rect()
    textRect.topleft = (386, 249)
    if option == 1:
        mySurface.blit(sbuttonhoverText, textRect)
    else:
        mySurface.blit(sbuttonText, textRect)
    textRect = mbuttonText.get_rect()
    textRect.topleft = (383, 328)
    if option == 2:
        mySurface.blit(mbuttonhoverText, textRect)
    else:
        mySurface.blit(mbuttonText, textRect)

menu()