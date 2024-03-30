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
    background_color = pygame.Color('grey')
    text_color = pygame.Color('white')
    font = pygame.font.Font(None, 32)


    sidebar_width = 200
    sidebar = pygame.Rect(screen_width - sidebar_width, 0, sidebar_width, screen_height)
    # Scroll variables
    scroll_y = 0  # Initial scroll position
    scroll_speed = 0  # Current scroll speed
    max_scroll_speed = 20  # Max speed the scroll can reach
    scroll_acceleration = 1  # How much the scroll speed increases per scroll
    scroll_friction = 0.9  # Friction applied to scroll speed per frame

    # Sidebar and scrollbar dimensions
    sidebar_width = 200
    sidebar = pygame.Rect(screen_width - sidebar_width, 0, sidebar_width, screen_height)
    scrollbar_width = 20

    # Trash button
    trash_button = Element(50, screen_height - 100, 140, 50, "Trash", font, text_color, pygame.Color("red"))


    # Elements
    elements = []
    active_element = None
    water = Element(50, 50,140,  50, "water", font, text_color, pygame.Color("blue"))
    fire = Element(50, 110,140,  50, "fire", font, text_color, pygame.Color("blue"))
    earth = Element(50, 170,140,  50, "earth", font, text_color, pygame.Color("blue"))
    air = Element(50, 230,140,  50, "air", font, text_color, pygame.Color("blue"))
    clone = Element(50, 1000,140,  50, "clone", font, text_color, pygame.Color("blue"))
    elements.append(water)
    elements.append(fire)
    elements.append(earth)
    elements.append(air)
    elements.append(clone)



    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for num, element in enumerate(elements):
                    if element.is_clicked(event.pos):
                        active_element = num

            if event.type == pygame.MOUSEBUTTONUP:
                active_element = None
            if event.type == pygame.MOUSEMOTION:
                if active_element != None:
                    elements[active_element].move_ip(*event.rel)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if sidebar.collidepoint(event.pos):
                    if event.button == 4:  # Scroll up
                        scroll_speed = min(scroll_speed + scroll_acceleration, max_scroll_speed)
                    if event.button == 5:  # Scroll down
                        scroll_speed = max(scroll_speed - scroll_acceleration, -max_scroll_speed)

                # Apply scroll speed and friction
            scroll_y += scroll_speed
            scroll_speed *= scroll_friction

            # Clamp the scroll_y position
            content_height = len(elements) * 60  # Adjust as needed
            scroll_y = min(0, max(screen_height - content_height, scroll_y))

            # Check if the trash button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if trash_button.is_clicked(event.pos):
                    # Clear the main area here by resetting the elements list or as required
                    pass


            if active_element != None:
                for element in elements:
                    if element != elements[active_element] and pygame.Rect.colliderect(elements[active_element].rect, element.rect):
                        if recipeloader.g.itemobtained(element.text, elements[active_element].text) != "zebi":
                            elements.append(Element(500, 50,140,  50, recipeloader.g.itemobtained(element.text, elements[active_element].text), font, text_color, pygame.Color("blue")))
                            elementremoved1 = element.text
                            elementremoved2 = elements[active_element].text
                            elements.remove(elements[active_element])
                            elements.remove(element)
                            if elementremoved2 in {"water", "fire", "air", "earth"}:
                                if elementremoved2 == "water":
                                    elements.append(Element(50, 50,140,  50, "water", font, text_color, pygame.Color("blue")))
                                if elementremoved2 == "earth":
                                    elements.append(Element(50, 170,140,  50, "earth", font, text_color, pygame.Color("blue")))
                                if elementremoved2 == "fire":
                                    elements.append(Element(50, 110,140,  50, "fire", font, text_color, pygame.Color("blue")))
                                if elementremoved2 == "air":
                                    elements.append(Element(50, 230,140,  50, "air", font, text_color, pygame.Color("blue")))
                            if elementremoved1 in {"water", "fire", "air", "earth"}:
                                if elementremoved1 == "water":
                                    elements.append(Element(50, 50,140,  50, "water", font, text_color, pygame.Color("blue")))
                                if elementremoved1 == "earth":
                                    elements.append(Element(50, 170,140,  50, "earth", font, text_color, pygame.Color("blue")))
                                if elementremoved1 == "fire":
                                    elements.append(Element(50, 110,140,  50, "fire", font, text_color, pygame.Color("blue")))
                                if elementremoved1 == "air":
                                    elements.append(Element(50, 230,140,  50, "air", font, text_color, pygame.Color("blue")))
                            break


            Screen.fill(background_color)
            for element in discov:
                element.draw(Screen)


        # Draw the sidebar
        pygame.draw.rect(Screen, pygame.Color("darkgrey"), sidebar)

        # Draw the trash button
        trash_button.draw(Screen)

        # Draw the scrollable content in the sidebar
        for i, element in enumerate(elements):
            # Calculate the position to draw based on scroll_y
            element_y = i * 60 + scroll_y  # Assuming each element is 60px high
            if 0 <= element_y < screen_height - sidebar_width:  # Check if the element is within the view
                element_sidebar_rect = pygame.Rect(screen_width - sidebar_width + 10, element_y,
                                                   sidebar_width - 20, 50)
                pygame.draw.rect(Screen, element.rectangle_color, element_sidebar_rect)
                element_text_surface = font.render(element.text, True, text_color)
                element_text_rect = element_text_surface.get_rect(center=element_sidebar_rect.center)
                Screen.blit(element_text_surface, element_text_rect)

            # Draw the scrollbar background
            scrollbar_background_rect = pygame.Rect(screen_width - scrollbar_width, 0, scrollbar_width,
                                                    screen_height)
            pygame.draw.rect(Screen, pygame.Color("darkgrey"), scrollbar_background_rect)

            # Calculate scrollbar thumb height and position
            visible_ratio = screen_height / content_height
            scrollbar_thumb_height = visible_ratio * screen_height
            scrollbar_thumb_y = -scroll_y * visible_ratio
            scrollbar_thumb_rect = pygame.Rect(screen_width - scrollbar_width, scrollbar_thumb_y, scrollbar_width,
                                               scrollbar_thumb_height)

            # Draw the scrollbar thumb
            pygame.draw.rect(Screen, pygame.Color("grey"), scrollbar_thumb_rect)

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

main_menu()
