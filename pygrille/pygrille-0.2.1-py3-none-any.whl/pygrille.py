try:
    import os
    import random
    # hide the support prompt for pygame
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
except ModuleNotFoundError:
    # if the os module is not found, raise an error
    raise ModuleNotFoundError(
        "Please use a standard Windows version of Python to use Pygrille.")
try:
    import pygame
except ModuleNotFoundError:
    # if the pygame module is not found, raise an error
    raise ModuleNotFoundError(
        "Pygame is required for the use of Pygrille. Please install it for Pygrille to work correctly.")
from text import Text


class Pixel:
    def __init__(self, x_pos: int, y_pos: int, colour: tuple, extras: list = None, image: pygame.Surface = None):
        # if extras is not provided, set it to an empty list
        if extras is None:
            extras = []
        self.colour = colour
        # set extras as a dictionary of keys only
        self.extras = dict.fromkeys(extras)
        self.label = (x_pos, y_pos)
        self.pos = (x_pos, y_pos)
        self.image = image

    def __repr__(self):
        # return the string representation of the pixel's label
        return str(self.label)


class Grid:
    def __init__(self, pixel_size: int, grid_dimensions: tuple, *, window_name: str = None,
                 default_colour: tuple = None, extras: list = None, framerate: int = None, border_width: int = None,
                 border_colour: tuple = None, default_image: str = None, display_offset_x: int = 0,
                 display_offset_y: int = 0, forced_window_size: tuple = None):
        # set the window name to "pygrille window" if not provided
        if window_name is None:
            window_name = "pygrille window"
        # set the framerate to 60 if not provided
        if framerate is None:
            framerate = 60
        # set the border width to 0 if not provided
        if border_width is None:
            border_width = 0
        # set the border colour to (100,100,100) if not provided
        if border_colour is None:
            border_colour = (100, 100, 100)
        # if default_image is provided, load the image using the load_image method
        if default_image is not None:
            default_image = self.load_image(default_image, pixel_size)
        # reverse the order of grid dimensions
        grid_dimensions = (grid_dimensions[1], grid_dimensions[0])
        pygame.init()
        pygame.display.set_caption(window_name)
        # calculate the screen size
        screen_size = [2 * border_width + i * pixel_size + (i - 1) * border_width for i in grid_dimensions]
        # if a forced window size is provided, set the screen to that size
        if forced_window_size is not None:
            screen = pygame.display.set_mode((forced_window_size[0], forced_window_size[1]))
        else:
            screen = pygame.display.set_mode((screen_size[1], screen_size[0]))
        # if extras is not provided, set it to an empty list
        if extras is None:
            extras = []
        # if default_colour is not provided, set it to (0,0,0)
        if default_colour is None:
            default_colour = (0, 0, 0)
        self.screen = screen
        self.size = grid_dimensions
        self.default_colour = default_colour
        self.pixel_size = pixel_size
        self.extra_list = extras
        self.framerate = framerate
        self.lastclick = None
        self.newclick = False
        self.lastkey = None
        self.keylist = []
        self.newkey = False
        self.clicked_ui = [] # List to hold multiple ui elements if there are overlapping ones that are clicked.
        self.newclick_ui = False
        self.ui = {}
        self.screen_size = screen_size
        self.border_width = border_width
        self.border_colour = border_colour
        self.default_image = default_image
        # create a grid of Pixel objects using the provided parameters
        self.grid: list[tuple[Pixel]] = list(
            zip(*[[Pixel(i, j, default_colour, extras, default_image) for i in range(grid_dimensions[1])] for j in
                  range(grid_dimensions[0])]))
        self.clock = pygame.time.Clock()
        self.display_offset_x = display_offset_x
        self.display_offset_y = display_offset_y
        self.images = {}
        self.text = {}
        self.screenrect = pygame.Rect(0, 0, self.screen.get_size()[0], self.screen.get_size()[1])
        self.backgroundimage = None
        self.draw()

    def __repr__(self):
        # return a string representation of the grid by joining the string representation of each row in the grid
        return "\n".join([str(row) for row in self.grid])

    def __getitem__(self, key):
        # allow the grid to be accessed like a 2D list
        return self.grid[key]

    def draw_borders(self):
        # loop through each row in the grid
        for i in range(len(self.grid)):
            pass

    def draw(self, *, flip: bool = None):
        # If flip is not provided, default it to True
        if flip is None:
            flip = True

        # If there is a background image, blit it onto the screen
        if self.backgroundimage is not None:
            self.screen.blit(self.backgroundimage, (0, 0))
        # Otherwise, fill the screen with the border color
        else:
            self.screen.fill(self.border_colour)

        # Iterate through the grid of nodes
        for i, node_row in enumerate(self.grid):
            for j, node in enumerate(node_row):
                # Create a rectangle for the node using its coordinates and size
                rect = pygame.Rect(
                    self.border_width + i * self.pixel_size + i * self.border_width + self.display_offset_x,
                    self.border_width + j * self.pixel_size + + j * self.border_width + self.display_offset_y,
                    self.pixel_size, self.pixel_size)
                # Draw the rectangle on the screen with the node's color
                pygame.draw.rect(self.screen, node.colour, rect)
                # If the node has an image, blit it onto the screen
                if node.image is not None:
                    rect = node.image.get_rect()
                    rect.x = self.border_width + i * self.pixel_size + i * self.border_width + self.display_offset_x
                    rect.y = self.border_width + j * self.pixel_size + + j * self.border_width + self.display_offset_y
                    self.screen.blit(node.image, rect)

        # Iterate through the UI elements and blit their images onto the screen
        for i in self.ui.values():
            self.screen.blit(i["image"], i["coords"])
        # Iterate through the text elements and draw them onto the screen
        for i in self.text.values():
            i.draw(self.screen)
        # If flip is True, update the screen
        if flip:
            pygame.display.flip()

    def update(self, coords: tuple, *, colour: tuple = None, label: str = None, draw: bool = None,
               border_colour: tuple = None, **kwargs):
        # If draw is not provided, default it to False
        if draw is None:
            draw = False
        # Update the color of the node at the given coordinates, if a color is provided
        if colour is not None:
            self.grid[coords[0]][coords[1]].colour = colour
        # Update the label of the node at the given coordinates, if a label is provided
        if label is not None:
            self.grid[coords[0]][coords[1]].label = label
        # Update the border color of the grid, if a border color is provided
        if border_colour is not None:
            self.border_colour = border_colour
        # Iterate through any extra keyword arguments and update the appropriate attribute of the node
        for item in kwargs:
            if item in self.extra_list:
                self.grid[coords[0]][coords[1]].extras[item] = kwargs[item]
            else:
                raise KeyError(f"\"{item}\" does not exist in the possible extras for this pixel")
        # If draw is True, re-draw the grid
        if draw:
            self.draw()

    def tick(self):
        # Limit the frame rate by ticking the clock
        self.clock.tick(self.framerate)

    def check_open(self):
        # Reset the click and key event flags
        self.newclick = False
        self.newclick_ui = False
        self.newkey = False
        # Clear the list of keys that were pressed
        self.keylist = []
        # Iterate through all events in the event queue
        for event in pygame.event.get():
            # If the event is a QUIT event (user closes the window)
            if event.type == pygame.QUIT:
                # Return False to indicate the program should close
                return False
            # If the event is a MOUSEBUTTONUP event (mouse button is released)
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                # Check if the mouse click is within the grid
                if (pos[0] - self.border_width - self.display_offset_x) % (
                        self.pixel_size + self.border_width) <= self.pixel_size and (
                        pos[1] - self.border_width - self.display_offset_y) % (
                        self.pixel_size + self.border_width) <= self.pixel_size:
                    # Store the coordinates of the last click
                    self.lastclick = ((pos[0] - self.display_offset_x) // (self.pixel_size + self.border_width),
                                      (pos[1] - self.display_offset_y) // (self.pixel_size + self.border_width))
                    # Set the new click flag to indicate a new click has occurred
                    self.newclick = True
                for image_name in self.ui:
                    lower_limit = self.ui[image_name]["coords"]
                    upper_limit = [self.ui[image_name]["coords"][i] +
                                   self.ui[image_name]["image"].get_size()[i] for i in (0, 1)]
                    if all([lower_limit[i] <= pos[i] <= upper_limit[i] for i in (0, 1)]):
                        if not self.newclick_ui:
                            self.clicked_ui = []
                        self.newclick_ui = True
                        self.clicked_ui.append(image_name)

            # If the event is a KEYDOWN event (a key is pressed)
            elif event.type == pygame.KEYDOWN:
                # Add the key that was pressed to the list of keys
                self.keylist.append(pygame.key.name(event.key))
                # Store the last key that was pressed
                self.lastkey = pygame.key.name(event.key)
                # Set the new key flag to indicate a new key press has occurred
                self.newkey = True
        # Return True to indicate the program should continue running
        return True

    def set_image(self, pos: tuple, image_path: str):
        # Check if the image is already loaded in memory
        if image_path not in self.images.keys():
            # If not, load the image and store it in the images dictionary
            self.images[image_path] = self.load_image(image_path, self.pixel_size)
        # Set the image at the specified position in the game grid
        self.grid[pos[0]][pos[1]].image = self.images[image_path]

    def set_ui(self, name: str, image_path: str, window_coords: tuple, scale: tuple = None):
        # Check if the image is already loaded in memory
        if image_path not in self.images.keys():
            # If not, load the image
            self.images[image_path] = pygame.image.load(image_path)
        # Get the image from the images dictionary
        image = self.images[image_path]
        # If a scale is provided, resize the image
        if scale is not None:
            image = pygame.transform.scale(image, (scale[0], scale[1]))
        # Add the image to the UI dictionary, along with its coordinates and path
        self.ui[name] = {
            "image": image,
            "coords": window_coords,
            "path": image_path}

    def set_text(self, name: str, font: str = None, size: int = None, text: str = None, pos: tuple = None,
                 colour: tuple = None):
        # Set default values for font, size, text, pos and colour if not provided
        if font is None:
            font = "Arial"
        if size is None:
            size = 30
        if text is None:
            text = ""
        if pos is None:
            pos = (0, 0)
        if colour is None:
            colour = (0, 0, 0)
        # Create a new Text object with the provided parameters and add it to the text dictionary
        self.text[name] = Text(font, size, text, pos, colour)

    def get_text(self, name: str):
        if name in self.text.keys():
            return self.text[name]

    def del_text(self, name: str):
        self.text.pop(name)

    def del_ui(self, name: str):
        self.ui.pop(name)

    def set_background_image(self, image_path: str):
        if image_path not in self.images.keys():
            self.images[image_path] = pygame.image.load(image_path)
        image = self.images[image_path]
        scale = self.screen.get_size()
        image = pygame.transform.scale(image, (scale[0], scale[1]))
        self.backgroundimage = image

    def pixel_from_screen_pixel(self, x: int, y: int):
        if (x - self.border_width - self.display_offset_x) % (
                self.pixel_size + self.border_width) <= self.pixel_size and (
                y - self.border_width - self.display_offset_y) % (
                self.pixel_size + self.border_width) <= self.pixel_size:
            pixel = (int((x - self.display_offset_x) // (self.pixel_size + self.border_width)),
                     int((y - self.display_offset_y) // (self.pixel_size + self.border_width)))
            return pixel

    def screen_pixel_from_pixel(self, x: int, y: int):
        x = self.border_width + x * self.pixel_size + x * self.border_width + self.display_offset_x
        y = self.border_width + y * self.pixel_size + y * self.border_width + self.display_offset_y
        return (x, y)

    def load_image(self, image_path, pixel_size):
        return pygame.transform.scale(pygame.image.load(image_path), (pixel_size, pixel_size))

    def quit(self):
        pygame.quit()


def random_colour():
    return [random.randint(0, 255) for i in range(3)]
