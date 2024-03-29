import pygame, sys
from button import Button

pygame.init()

Screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BackGround = pygame.image.load("singed.jpeg")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def play():
    """
     This displays the main game for the classic mode of little alchemy.
     There are two text boxes to combine elements. The user types in the two
     elements they wish to combine, and the backend determines if its a valid combination.
     There will be a bar on the side containing the name of all of the elements found so far.
     """
    boxes = []
    text = get_font(45).render('GeeksForGeeks', True, green, blue)
    text_rect = text.get_rect()
    text_rect.center = (750, 400)
    while True:
        play_mouse_pos = pygame.mouse.get_pos()

        Screen.fill("black")

        display_surface.blit(text, textRect)








        play_back = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        play_back.changeColor(play_mouse_pos)
        play_back.update(Screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_back.checkForInput(play_mouse_pos):
                    main_menu()
                if box.collidepoint(event.pos):
                    active_box = num
                if event.type == pygame.MOUSEBUTTONUP:
                        active_box = None
                if event.type == pygame.MOUSEMOTION:
                    if active_box != None:
                        boxes[active_box].move_ip(event.rel)

        pygame.display.update()
def options():
    while True:
        options_mouse_pos = pygame.mouse.get_pos()

        Screen.fill("white")

        options_text = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        options_rect = options_text.get_rect(center=(640, 260))
        Screen.blit(options_text, options_rect)

        options_back = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        options_back.changeColor(options_mouse_pos)
        options_back.update(Screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if options_back.checkForInput(options_mouse_pos):
                    main_menu()

        pygame.display.update()

def main_menu():
    """
    This displays the start screen. This will include a title, start button,
    game mode, and quit button.
    """
    pygame.display.set_caption("Menu")

    while True:
        Screen.blit(BackGround, (0, 0))
        menu_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640,100))

        play_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY",font = get_font(75), base_color = "#d7fcd4", hovering_color = "White")
        options_button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                             text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        Screen.blit(menu_text, menu_rect)

        for button in [play_button, options_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(Screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    play()
                if options_button.checkForInput(menu_mouse_pos):
                    options()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

main_menu()
