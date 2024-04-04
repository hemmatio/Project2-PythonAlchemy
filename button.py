"""
File Outline
===============================
This file is used within main.py to create buttons for our menu.

Copyright and Usage Information
===============================
This file is provided solely for the private use of the teaching staff
of CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2024 Omid Hemmati, Yianni Culmone, Neyl Nasr, Benjamin Gavriely
"""
import pygame


class Button:
    """
   A class to create interactive buttons for a Pygame window. Buttons can display text
   and change text color on hover.

   Instance Attributes:
    - image (pygame.Surface): The button's image. If None, the button displays text only.
    - x_pos (int): The x-coordinate of the button's position.
    - y_pos (int): The y-coordinate of the button's position.
    - font (pygame.font.Font): The Pygame font used for the button's text.
    - base_color (tuple[int, int, int]): The button's text color when not hovered over.
    - hovering_color (tuple[int, int, int]): The button's text color when hovered over.
    - text_input (str): The text displayed on the button.
    - rect (pygame.Rect): The rectangular area of the button.
    - text_rect (pygame.Rect): The rectangular area for the button's text.

   Representation Invariants:
   - self.x_pos and self.y_pos are integers representing the button's position on the screen.
   - self.text_input is a non-empty string.
   - self.base_color and self.hovering_color are tuples representing RGB color values.
   """
    image: pygame.Surface
    x_pos: int
    y_pos: int
    font: pygame.font
    base_color: str
    hovering_color: str
    text_input: pygame.Surface
    text: pygame.Surface
    rect: pygame.rect
    text_rect: pygame.rect

    def __init__(self, image: pygame.Surface, pos: tuple, text_input: pygame.Surface, font: pygame.font,
                 base_color: str, hovering_color: str) -> None:
        """
        Initializes a Button object.

        :param image: A Pygame Surface object to be used as the button's image.
        If None, the button will display text only.
        :param pos: A tuple containing the x and y coordinates for the button's position.
        :param text_input: The text to be displayed on the button.
        :param font: A Pygame font object for rendering the button's text.
        :param base_color: The button's text color when not being hovered over.
        :param hovering_color: The button's text color when being hovered over.
        """
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen: pygame.Surface) -> None:
        """
        Draws the button onto the given Pygame window surface, updating its appearance.

        Preconditions:
        - 'screen' must be a valid Pygame Surface object.
        """
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkforinput(self, position: tuple) -> bool:
        """
        Checks if the button is being clicked based on the mouse position.

        :param position: A tuple containing the x and y coordinates of the mouse.

        :return: True if the button is clicked, False otherwise.
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changecolor(self, position: tuple) -> None:
        """
        Changes the button's text color based on the mouse's position (hover effect).

        :param position: A tuple containing the x and y coordinates of the mouse.
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class ButtonStay(Button):
    """
    Extends the Button class to create a toggle button that visually indicates its current state
    (clicked or not clicked) through color changes.

    Representation Invariants:
    - clicked is a boolean indicating the toggle state of the button.

    Instance Attributes:
    - clicked (bool): Represents whether the button is in an active (clicked) state.

    Inherits from Button:
        - image (pygame.Surface): The button's image. If None, the button displays text only.
        - x_pos (int): The x-coordinate of the button's position.
        - y_pos (int): The y-coordinate of the button's position.
        - font (pygame.font.Font): The Pygame font used for the button's text.
        - base_color (tuple[int, int, int]): The button's text color when not hovered over.
        - hovering_color (tuple[int, int, int]): The button's text color when hovered over.
        - text_input (str): The text displayed on the button.
        - rect (pygame.Rect): The rectangular area of the button.
        - text_rect (pygame.Rect): The rectangular area for the button's text.
    """
    clicked: bool

    def __init__(self, image: pygame.Surface, pos: tuple, text_input: pygame.Surface, font: pygame.font.Font,
                 base_color: str, hovering_color: str, clicked: bool = False) -> None:
        """
        Initializes a ButtonStay object with an additional clicked state.

        :param image: The button's image. If None, the button will display text only.
        :param pos: A tuple containing the x and y coordinates for the button's position.
        :param text_input: The text to be displayed on the button.
        :param font: A Pygame font object for the button's text.
        :param base_color: (tuple[int, int, int]): The button's text color when not hovered over.
        :param hovering_color: (tuple[int, int, int]): The button's text color when being hovered over.
        :param clicked: Indicates whether the button is in an active (clicked) state. Defaults to False.
        """
        super().__init__(image, pos, text_input, font, base_color, hovering_color)
        self.clicked = clicked

    def update(self, screen: pygame.Surface) -> None:
        """
        Draws the button onto the given Pygame window surface, with its appearance adjusted
        based on its clicked state. The background color changes to indicate the button's state.

        Preconditions:
        - 'screen' must be a valid Pygame Surface object.
        """
        if self.clicked:
            current_color = (0, 255, 0)  # Green if clicked
        else:
            current_color = (255, 0, 0)  # Red otherwise

        # Set a standard size for the background rectangle
        standard_width = 170  # Example width
        standard_height = 60  # Example height

        background_rect = pygame.Rect(self.x_pos - standard_width / 2, self.y_pos - standard_height / 2, standard_width,
                                      standard_height)
        pygame.draw.rect(screen, current_color, background_rect)

        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['sys', 'pygame', 'recipeloader', 'random', 'button', ],
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120,
        'no-member': False,
        'max-args': 8
    })
