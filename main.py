"""
File Outline
===============================
Python Alchemy is a game built using Graphs and Pygame, which simulates a virtual alchemy
experience allowing players to combine different elements to discover new ones.
The game features a main menu, options for customizing gameplay (including a chemistry mode),
and the core gameplay where elements are combined through a drag-and-drop interface.
Elements discovered are added to a sidebar, with the game progressing as more combinations are found.

Copyright and Usage Information
===============================
This file is provided solely for the private use of the teaching staff
of CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2024 Omid Hemmati, Yianni Culmone, Neyl Nasr, Benjamin Gavriely
"""

import sys
import pygame
import recipeloader
import random
from button import Button, ButtonStay


def main():
    """
    The main function that gets ran upon starting the file. This starts the program through Pygame.
    """
    pygame.init()
    pygame.display.set_caption("Menu")
    main_menu(False, [])


class Element:
    """
        A class representing an interactive element within the game. Each element has a label,
        can be clicked, moved, and drawn onto the game screen.

        Instance Attributes:
        - x: The int x-coordinate of the element's position.
        - y: The int y-coordinate of the element's position.
        - width: The int width of the element.
        - height: The int height of the element.
        - text: The str text displayed on the element.
        - font: The pygame.font.Font used for the element's text.
        - text_color: The pygame.Color of the text.
        - rectangle_color: The background pygame.Color of the element.

        Representation Invariants:
        - width and height must be positive integers representing a reasonable display resolution.
        """
    x: int
    y: int
    width: int
    height: int
    text: str
    font: pygame.font.Font
    text_color: pygame.color
    rectangle_color: pygame.color

    def __init__(self, x, y, width, height, text, font, text_color, rectangle_color):
        """
        Initializes an Element with specified properties.

        Preconditions:
        - width > 0 and height > 0.
        - text is a non-empty string.

        :param x, y: Coordinates for the element's position.
        :param width, height: Dimensions of the element.
        :param text: Text displayed on the element.
        :param font: Pygame font for the text.
        :param text_color: Color of the text.
        :param rectangle_color: Background color of the element.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text.title()
        self.font = font
        self.text_surface = self.render_with_outline(text, font, text_color, pygame.Color('black'), 1)
        self.rectangle_color = rectangle_color
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        """
        Draws the element onto the specified screen.

        Preconditions:
        - screen must be a valid Pygame Surface object.

        :param screen: the Pygame screen
        """
        pygame.draw.rect(screen, self.rectangle_color, self.rect, 2)
        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, mouse_pos):
        """
        Checks if the element is clicked based on the mouse position.
        Returns True if the element is clicked, False otherwise.

        Preconditions:
        - mouse_pos must be a tuple of (x, y) coordinates.

        :param mouse_pos: a tuple of coordinates.
        """
        return self.rect.collidepoint(mouse_pos)

    def move_ip(self, dx, dy):
        """
        Moves the element by the specified deltas in the x and y directions.

        Preconditions:
        - dx and dy are integers.

        :param dx: The delta x coordinate.
        :param dy: The delta y coordinate.
        """
        # Move the element based on deltas
        self.rect.move_ip(dx, dy)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def render_with_outline(self, text, font, text_color, outline_color, outline_width):
        """
        Renders the element's text with an outline and returns a Surface object.

        Preconditions:
        - text is a non-empty string.
        - outline_width > 0.

        :param text: Text to render.
        :param font: Pygame font used for the text.
        :param text_color: Color of the text.
        :param outline_color: Color of the outline.
        :param outline_width: Width of the outline.

        :return: A Pygame Surface object with the rendered text.
        """
        base = font.render(text, True, text_color)
        # The size of the outline surface should be larger than the base by twice the outline width on all sides
        outline_size = (base.get_width() + 2 * outline_width, base.get_height() + 2 * outline_width)
        outline = pygame.Surface(outline_size, pygame.SRCALPHA)

        # Get the positions to blit the base text onto the outline surface, centered
        base_pos = (outline_width, outline_width)

        # Render the outline by drawing the text in the outline color offset in all directions
        offsets = [(-outline_width, -outline_width), (-outline_width, outline_width),
                   (outline_width, -outline_width), (outline_width, outline_width)]
        for dx, dy in offsets:
            temp_surf = font.render(text, True, outline_color)
            outline.blit(temp_surf, (base_pos[0] + dx, base_pos[1] + dy))

        # Blit the base text onto the outline surface
        outline.blit(base, base_pos)
        return outline


def get_font(size):
    """
    Gets a font using the provided font.ttf file in the assets folder
    :param size: The size of the fonrt in pixels
    :return: pygame font object
    """
    return pygame.font.Font("assets/font.ttf", size)


def play(chemistry: bool, discovered: list[str]):
    """
    Launches the main gameplay loop.

    :param chemistry: If True, uses chemistry recipes; otherwise, uses default recipes.
    :param discovered: A list of discovered items, used to maintain the user's progress.
    """
    screen_width, screen_height = 1200, 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    if not chemistry:
        with open('recipes.json') as file:
            g = recipeloader.Graph(file)
    else:
        with open('chemistry.json') as file:
            g = recipeloader.Graph(file)

    g.update(discovered)

    pygame.display.set_caption("Python Alchemy")

    # Colors and Font
    background_color = pygame.Color('#f7f6f1')
    text_color = pygame.Color("#bc259d")
    font = pygame.font.Font("assets/Roboto-Regular.ttf", 24)
    item_color = pygame.Color(0)

    # initializing the sidebar
    sidebar_width = 250
    sidebar = pygame.Rect(screen_width - sidebar_width, 0, sidebar_width, screen_height)

    # initializing the trash bin
    trash_bin_icon = pygame.image.load("assets/trash.png")  # Load the trash bin icon
    trash_bin_rect = trash_bin_icon.get_rect(
        topleft=(10, screen_height - trash_bin_icon.get_height() - 10))  # Position it at the bottom left

    # initilazing the logo
    logo_icon = pygame.image.load("assets/Logo.png")
    logo_rect = logo_icon.get_rect(
        topleft=(5, 2))

    # initilzazing the arrows
    up_icon = pygame.image.load("assets/up.png")
    up_rect = up_icon.get_rect(topleft=(screen_width - 134, 8))
    down_icon = pygame.image.load("assets/down.png")
    down_rect = down_icon.get_rect(topleft=(screen_width - 134, screen_height - 67))

    # initializing the sounds
    combine_sound1 = pygame.mixer.Sound("assets/combine1.wav")
    combine_sound2 = pygame.mixer.Sound("assets/combine2.wav")
    combine_sound3 = pygame.mixer.Sound("assets/combine3.wav")
    combine_sounds = [combine_sound1, combine_sound2, combine_sound3]
    click_sound = pygame.mixer.Sound("assets/click.wav")

    # initializing elementary elements
    elements = []
    k = 0
    holding = False
    letgo = 0
    stock_index = 0

    while True:
        screen.fill(background_color)
        # drawing sidebar
        pygame.draw.rect(screen, pygame.Color("#efebe0"), sidebar)

        # drawing logo
        screen.blit(logo_icon, logo_rect)

        # adding elements to sidebar and the little circles
        j = 0
        discovered = []
        for i, value in enumerate(g.discovered[k:(k + 10)], start=k + 1):  # Enumerate with start=k
            # Create text surface for index
            font2 = pygame.font.Font("assets/Roboto-Regular.ttf", 22)
            index_text = font2.render(str(i), True, pygame.Color(0))

            # Adjust position if the index is double-digit
            index_x = screen_width - 225 if i < 10 else screen_width - 232
            index_y = 50 + j
            pygame.draw.circle(screen, (150, 150, 150, 50), (screen_width - 219, index_y + 14), 17)

            # Position index text beside the element
            index_rect = index_text.get_rect(topleft=(index_x, index_y))
            screen.blit(index_text, index_rect)

            # Create and draw element
            element = Element(screen_width - 190, 40 + j, 140, 45, value.item.title(), font, text_color, item_color)
            discovered.append(element)
            if element.text_surface.get_width() + 10 >= 140:
                element.rect.w = element.text_surface.get_width() + 10
                element.text_rect = element.text_surface.get_rect(center=element.rect.center)
            element.draw(screen)
            j += 60
        # prints all elements on the screen
        for element in elements:
            if element.text_surface.get_width() + 10 >= 140:
                element.rect.w = element.text_surface.get_width() + 10
                element.text_rect = element.text_surface.get_rect(center=element.rect.center)
            element.draw(screen)

        for event in pygame.event.get():

            # adding scroll when down arrow is clicked
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if k + 10 < len(g.discovered):
                        k = k + 1
                        pygame.mixer.Sound.play(click_sound)
                if event.key == pygame.K_UP:
                    if k - 1 >= 0:
                        k = k - 1
                        pygame.mixer.Sound.play(click_sound)

            # spawns the element in the middle of the screen or drags element
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # spawns in middle
                stock_index = None
                for discover in discovered:
                    if discover.is_clicked(event.pos):
                        pygame.mixer.Sound.play(click_sound)
                        elements.append(Element(400 + random.randint(-100, 100), 300 + random.randint(-100, 100),
                                                140, 45, discover.text.title(), font, text_color, item_color))

                # drags the item
                for num, element in enumerate(elements):
                    if element.is_clicked(event.pos):
                        stock_index = num
                        holding = True

            if event.type == pygame.MOUSEBUTTONUP:
                holding = False
            if event.type == pygame.MOUSEMOTION:
                if holding:
                    if len(elements) > 0:
                        elements[stock_index].move_ip(*event.rel)
                        letgo = 1

            # trash bin and arrow function and back to main menu
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if trash_bin_rect.collidepoint(event.pos):  # Check if the trash bin is clicked
                    pygame.mixer.Sound.play(click_sound)
                    elements = []
                    stock_index = None
                if up_rect.collidepoint(event.pos):
                    if k - 1 >= 0:
                        pygame.mixer.Sound.play(click_sound)
                        k = k - 1
                if down_rect.collidepoint(event.pos):
                    if k + 10 < len(g.discovered):
                        pygame.mixer.Sound.play(click_sound)
                        k = k + 1

                if logo_rect.collidepoint(event.pos):
                    if elements:
                        for element in elements:
                            if not logo_rect.colliderect(element.rect):
                                pygame.mixer.Sound.play(click_sound)
                                update_discovered = g.downdate()
                                main_menu(chemistry, update_discovered)
                    else:
                        pygame.mixer.Sound.play(click_sound)
                        update_discovered = g.downdate()
                        main_menu(chemistry, update_discovered)

            # Combine items if not holding
            if not holding and letgo == 1:
                for element in elements:
                    if (stock_index and
                            element != elements[stock_index] and
                            pygame.Rect.colliderect(elements[stock_index].rect, element.rect)):
                        valid_combo, item_created = g.combine(element.text.lower(), elements[stock_index].text.lower())
                        if valid_combo:
                            x, y = pygame.mouse.get_pos()
                            elements.append(Element(x - 70, y - 25, 140,  45,
                                                    item_created, font, text_color, item_color))
                            elements.remove(elements[stock_index])
                            elements.remove(element)
                            letgo = 0
                            pygame.mixer.Sound.play(combine_sounds[random.randint(0, 2)])
                            break

        # Draw the trash bin
        screen.blit(trash_bin_icon, trash_bin_rect)

        # Draws the little arrows when you can go up and down
        if k - 1 >= 0:
            screen.blit(up_icon, up_rect)
        if k + 10 < len(g.discovered):
            screen.blit(down_icon, down_rect)

        # Draws the number of items currently found
        font3 = pygame.font.Font("assets/Roboto-Regular.ttf", 20)
        discover_text = font3.render(f"Discovered: {len(g.discovered)} / {len(g.get_vertices())}", True, "Black")
        discover_rect = discover_text.get_rect(topleft=(screen_width - 225, screen_height - 30))
        screen.blit(discover_text, discover_rect)

        pygame.display.flip()


def options(chemistry: bool, discovered: list[str]):
    """
    Displays the options menu to toggle game settings.

    :param chemistry: The current state of chemistry mode, used to toggle the setting.
    :param discovered: A list of discovered items, used to maintain the user's progress.
    """
    background = pygame.image.load("assets/optionsbackground.png")
    screen_width, screen_height = 1200, 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    click_sound = pygame.mixer.Sound("assets/click.wav")
    chemupdate = chemistry
    while True:
        options_mouse_pos = pygame.mouse.get_pos()

        screen.blit(background, (0, 0))

        options_text = get_font(45).render("Options", True, "White")
        options_rect = options_text.get_rect(center=(screen_width // 2 + 15, 35))
        screen.blit(options_text, options_rect)

        options_back = Button(image=None, pos=(screen_width - 100, screen_height - 40),
                              text_input="BACK", font=get_font(40), base_color="White", hovering_color="Green")
        options_back.changeColor(options_mouse_pos)
        options_back.update(screen)

        # Chemistry buttons
        chemtext = get_font(40).render("Chemistry Mode:", True, "White")
        chemrect = chemtext.get_rect(topleft=(15, 170))
        screen.blit(chemtext, chemrect)

        # Save/Load text
        savetext = get_font(40).render("Write Save:", True, "White")
        saverect = savetext.get_rect(topleft=(15, 270))
        loadtext = get_font(40).render("Load Save:", True, "White")
        loadrect = savetext.get_rect(topleft=(15, 370))
        screen.blit(savetext, saverect)
        screen.blit(loadtext, loadrect)

        # New combo option

        combotext = get_font(40).render("Add a new combo", True, "White")
        comborect = chemtext.get_rect(topleft=(350, 550))
        screen.blit(combotext, comborect)

        combobutton = Button(image=None, pos=(350, 550),
                            text_input="Add new combo", font=get_font(40), base_color="Black", hovering_color="White")
        combobutton.changeColor(options_mouse_pos)
        combobutton.update(screen)

        # Save/Load buttons
        saverect = pygame.Rect(screen_width - 195, 258, 185, 60)
        pygame.draw.rect(screen, "Green", saverect)
        savebutton = Button(image=None, pos=(screen_width - 100, 290),
                            text_input="SAVE", font=get_font(40), base_color="Black", hovering_color="White")
        savebutton.changeColor(options_mouse_pos)
        savebutton.update(screen)

        loadrect = pygame.Rect(screen_width - 195, 358, 185, 60)
        pygame.draw.rect(screen, "Red", loadrect)
        loadbutton = Button(image=None, pos=(screen_width - 100, 390),
                            text_input="LOAD", font=get_font(40), base_color="Black", hovering_color="White")
        loadbutton.changeColor(options_mouse_pos)
        loadbutton.update(screen)

        if chemupdate:
            chembutton = ButtonStay(image=None, pos=(screen_width - 100, 190), text_input="ON", font=get_font(40),
                                    base_color="Black", hovering_color="White", clicked=True)
        else:
            chembutton = ButtonStay(image=None, pos=(screen_width - 100, 190), text_input="OFF", font=get_font(40),
                                    base_color="Black", hovering_color="White", clicked=False)
        chembutton.changeColor(options_mouse_pos)
        chembutton.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if options_back.checkForInput(options_mouse_pos):
                    pygame.mixer.Sound.play(click_sound)
                    if chemupdate != chemistry:
                        discovered = []
                    main_menu(chemupdate, discovered)
                if chembutton.checkForInput(options_mouse_pos):
                    pygame.mixer.Sound.play(click_sound)
                    if chembutton.clicked:
                        chembutton.clicked = False
                        chemupdate = False
                    else:
                        chembutton.clicked = True
                        chemupdate = True
                if savebutton.checkForInput(options_mouse_pos):
                    pygame.mixer.Sound.play(click_sound)
                    write_save(discovered, chemistry)
                if loadbutton.checkForInput(options_mouse_pos):
                    pygame.mixer.Sound.play(click_sound)
                    chemistry, discovered = load_save('savefile/save.csv')

        pygame.display.update()


def main_menu(chemistry: bool, discovered: list[str]):
    """
    Displays the main menu and handles user interaction with the menu options.

    :param chemistry: The current state of chemistry mode, affecting how the game is initialized.
    :param discovered: A list of discovered items, used to maintain the user's progress.
    """
    screen_width, screen_height = 1200, 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    background = pygame.image.load("assets/background.png")
    click_sound = pygame.mixer.Sound("assets/click.wav")
    pygame.display.set_caption("Menu")
    while True:
        screen.blit(background, (0, 0))
        menu_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(74).render("Python Alchemy", True, "#12CDEC")
        menu_rect = menu_text.get_rect(center=(640, 100))

        play_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        options_button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        screen.blit(menu_text, menu_rect)

        for button in [play_button, options_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    pygame.mixer.Sound.play(click_sound)
                    play(chemistry, discovered)
                if options_button.checkForInput(menu_mouse_pos):
                    pygame.mixer.Sound.play(click_sound)
                    options(chemistry, discovered)
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.mixer.Sound.play(click_sound)
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


def write_save(discovered: list[str], chemistry: bool):
    """
    Writes the currently discovered items and the gamemode into the save file save.txt
    :param discovered: The currently discovered items
    :param chemistry: The current mode
    """
    with open('savefile/save.csv', 'w') as file:
        file.write(f"{chemistry}\n")
        for item in discovered:
            file.write(f"{item}\n")


def load_save(filedirectory: str) -> tuple[bool, list[str]]:
    """
    Returns a tuple of a bool and a list, where the bool indicates the gamemode and the list indicates
    the discovered items.
    :param filedirectory:
    :return:
    """
    with open(filedirectory, 'r') as file:
        lines = file.readlines()
        chemistry = lines[0].strip() == 'True'
        discovered = [line.strip() for line in lines[1:]]
        return chemistry, discovered


if __name__ == "__main__":
    main()
