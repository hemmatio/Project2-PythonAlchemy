import pygame
import recipeloader
from button import Button
class Element():
    def __init__(self, x, y, width, height, text, font, text_color, rectangle_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_surface = font.render(text, True, text_color)
        self.rectangle_color = rectangle_color
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.rectangle_color, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def move_ip(self, dx, dy):
        # Move the element based on deltas
        self.rect.move_ip(dx, dy)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

pygame.init()

screen_width, screen_height = 1200, 700
Screen = pygame.display.set_mode((screen_width, screen_height))
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
    #bla
    pygame.display.set_caption("Little Alchemist")

    # Colors and Font
    background_color = pygame.Color('#f7f6f1')
    text_color = pygame.Color('white')
    font = pygame.font.Font(None, 32)
    item_color = pygame.Color("blue")

    #initializing the sidebar
    sidebar_width = 250
    sidebar = pygame.Rect(screen_width - sidebar_width, 0, sidebar_width, screen_height)

    # scroll variables
    scroll_y = 0
    scroll_speed = 0
    max_scroll_speed = 5
    scroll_acceleration = 0.5
    scroll_friction = 0.5

    # initializing elementary elements
    elements = []
    i = 0
    active_element = None
    for element in recipeloader.g.discovered:
        elements.append(Element(screen_width - 175, 50 + i, 140, 50, element.item, font, text_color, item_color))
        i += 60




    while True:
        Screen.fill(background_color)



        # drawing sidebar
        pygame.draw.rect(Screen, pygame.Color("#efebe0"), sidebar)

        #adding elements to sidebar
        for element in elements:
            element.draw(Screen)



        pygame.display.flip()
    pygame.quit()
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


recipeloader.g.combine("water", "earth")
recipeloader.g.combine("air", "water")
main_menu()
