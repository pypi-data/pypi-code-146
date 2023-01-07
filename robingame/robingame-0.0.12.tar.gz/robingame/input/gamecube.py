"""
# similar to pygame.key.get_pressed()
Usage:
```
controller1 = GamecubeController(1)
inputs = controller1.get_values()
if inputs[gamecube.A]:
    # do action for A
```
"""
import pygame

from robingame.input.queue import InputQueue

# button/input indices. These are used for lookup similarly to e.g. pygame.K_ESCAPE
# It doesn't really matter what order these are, so long as they match up to the order of the
# .get_values() method.
A = 0
B = 1
X = 2
Y = 3
Z = 4
L = 5
R = 6
START = 7
LEFT = 8
RIGHT = 9
UP = 10
DOWN = 11
C_LEFT = 12
C_RIGHT = 13
C_UP = 14
C_DOWN = 15
R_AXIS = 16
L_AXIS = 17
D_LEFT = 18
D_RIGHT = 19
D_UP = 20
D_DOWN = 21


def linear_map(input_value, input_range, output_range, limit_output=True):
    """Linearly map a set of inputs to a set of outputs. If limit_output==True, don't output any
    values outside the output range. Will still allow inputs outside the input range."""
    input_min, input_max = input_range
    output_min, output_max = output_range

    di = input_max - input_min
    do = output_max - output_min
    gradient = do / di
    offset = output_min - gradient * input_min

    # y = mx + c
    output_value = gradient * input_value + offset

    if limit_output:
        output_value = max(output_value, output_min)
        output_value = min(output_value, output_max)

    return output_value


class GamecubeControllerReader:
    """Class to read the inputs of a GameCube controller plugged into the Mayflash "GameCube
    Controller Adapter for Wii U & PC USB"

    This class
    - reads the values from the controller's buttons (binary values) axes (analog inputs such as
    control sticks and triggers) and hats (the 4-way D pad)
    - maps the values of the inputs to a 0-1 range and exposes these as named properties if the
    user wants to access a single value.
    - exposes a .get_values() method which returns a tuple of all the inputs (similar to how
    pygame deals with keyboard and mouse input.
    """

    # input ranges. Use these to set minimum (i.e. dead zone) and maximum input values
    GREY_STICK_INPUT_RANGE = (0.1, 0.77)
    YELLOW_STICK_INPUT_RANGE = (0.1, 0.67)
    TRIGGER_INPUT_RANGE = (-0.5, 1)

    def __init__(self, joystick_id: int):
        self.joystick = pygame.joystick.Joystick(joystick_id)  # get the joystick from pygame
        self.joystick.init()  # turn on the joystick

    def get_values(self):
        """Get the current state of all the inputs. This is intended to be equivalent to
        pygame.key.get_pressed so that the inputs can be processed in the same way."""
        # todo: the d-pad properties each access the d-pad values when they are called. So we're
        #  checking the status of the d-pad 4 times per tick when once would do. If the inputs
        #  ever get slow, maybe look at this.
        return (
            self.A,
            self.B,
            self.X,
            self.Y,
            self.Z,
            self.L,
            self.R,
            self.START,
            self.LEFT,
            self.RIGHT,
            self.UP,
            self.DOWN,
            self.C_LEFT,
            self.C_RIGHT,
            self.C_UP,
            self.C_DOWN,
            self.R_AXIS,
            self.L_AXIS,
            self.D_LEFT,
            self.D_RIGHT,
            self.D_UP,
            self.D_DOWN,
        )

    def grey_stick_map(self, input_value):
        return linear_map(input_value, self.GREY_STICK_INPUT_RANGE, (0, 1))

    def yellow_stick_map(self, input_value):
        return linear_map(input_value, self.YELLOW_STICK_INPUT_RANGE, (0, 1))

    def trigger_map(self, input_value):
        return linear_map(input_value, self.TRIGGER_INPUT_RANGE, (0, 1))

    # =================== AXES (=ANALOG INPUTS) =======================

    # uncalibrated internal values

    @property
    def _GREY_STICK_X_AXIS(self):
        return self.joystick.get_axis(0)

    @property
    def _GREY_STICK_Y_AXIS(self):
        return self.joystick.get_axis(1)

    @property
    def _YELLOW_STICK_X_AXIS(self):
        return self.joystick.get_axis(5)

    @property
    def _YELLOW_STICK_Y_AXIS(self):
        return self.joystick.get_axis(2)

    @property
    def _L_TRIGGER_AXIS(self):
        return self.joystick.get_axis(3)

    @property
    def _R_TRIGGER_AXIS(self):
        return self.joystick.get_axis(4)

    # calibrated external values

    @property
    def LEFT(self):
        return self.grey_stick_map(-self._GREY_STICK_X_AXIS)

    @property
    def RIGHT(self):
        return self.grey_stick_map(self._GREY_STICK_X_AXIS)

    @property
    def UP(self):
        return self.grey_stick_map(-self._GREY_STICK_Y_AXIS)

    @property
    def DOWN(self):
        return self.grey_stick_map(self._GREY_STICK_Y_AXIS)

    @property
    def C_LEFT(self):
        return self.yellow_stick_map(-self._YELLOW_STICK_X_AXIS)

    @property
    def C_RIGHT(self):
        return self.yellow_stick_map(self._YELLOW_STICK_X_AXIS)

    @property
    def C_UP(self):
        return self.yellow_stick_map(-self._YELLOW_STICK_Y_AXIS)

    @property
    def C_DOWN(self):
        return self.yellow_stick_map(self._YELLOW_STICK_Y_AXIS)

    @property
    def R_AXIS(self):
        return self.trigger_map(self._R_TRIGGER_AXIS)

    @property
    def L_AXIS(self):
        return self.trigger_map(self._L_TRIGGER_AXIS)

    # =================== 4-WAY SWITCHES =======================

    # uncalibrated internal values

    @property
    def _D_PAD(self):
        return self.joystick.get_hat(0)

    @property
    def _D_PAD_X(self):
        return self._D_PAD[0]

    @property
    def _D_PAD_Y(self):
        return self._D_PAD[1]

    # calibrated external values

    @property
    def D_LEFT(self):
        return int(self._D_PAD_X < 0)

    @property
    def D_RIGHT(self):
        return int(self._D_PAD_X > 0)

    @property
    def D_UP(self):
        return int(self._D_PAD_Y > 0)

    @property
    def D_DOWN(self):
        return int(self._D_PAD_Y < 0)

    # =================== BUTTONS (=BINARY VALUES) =======================

    # calibrated external values

    @property
    def X(self):
        return self.joystick.get_button(0)

    @property
    def A(self):
        return self.joystick.get_button(1)

    @property
    def B(self):
        return self.joystick.get_button(2)

    @property
    def Y(self):
        return self.joystick.get_button(3)

    @property
    def L(self):
        return self.joystick.get_button(4)

    @property
    def R(self):
        return self.joystick.get_button(5)

    @property
    def Z(self):
        return self.joystick.get_button(7)

    @property
    def START(self):
        return self.joystick.get_button(9)


class ButtonInput:
    def __init__(self, id: int, parent: InputQueue = None):
        """
        Class to describe a single input channel on a joystick/controller -- e.g. the "A" button
        on a gamecube controller. Implements methods which check with the parent input device
        whether this button is pressed, released, etc. This allows for the more pleasant shorthand:
        `controller.a_button.is_pressed` instead of `controller.is_pressed(controller.a_button)`

        :param int id: index of this input channel in the controller.get_values() tuple
        """
        self.id = id
        self.parent = parent

    @property
    def is_down(self):
        return self.parent.is_down(self.id)

    @property
    def is_pressed(self):
        return self.parent.is_pressed(self.id)

    @property
    def is_released(self):
        return self.parent.is_released(self.id)

    @property
    def value(self):
        """Does the same thing as is_down but makes some parts of the code more readable,
        especially for analog inputs that can be between 0-1."""
        return self.is_down

    def buffered_presses(self, buffer_length):
        return self.parent.buffered_presses(self.id, buffer_length)

    def buffered_releases(self, buffer_length):
        return self.parent.buffered_releases(self.id, buffer_length)

    def __sub__(self, other):
        return self.value - (other.value if isinstance(other, ButtonInput) else other)

    def __add__(self, other):
        return self.value + (other.value if isinstance(other, ButtonInput) else other)

    def __bool__(self):
        """This allows us to do `if input.UP` instead of `if input.UP.is_down`"""
        return bool(self.value)


class AxisInput(ButtonInput):
    smash_threshold = 0.9
    smash_window = 3  # frames in which to reach smash_threshold

    @property
    def is_smashed(self) -> bool:
        history = list(self.parent)[-1 - self.smash_window :]
        history = [inputs[self.id] for inputs in history]
        if history:
            return history[-1] >= self.smash_threshold and history[0] <= 0.1
        else:
            return False


class GamecubeController(InputQueue):
    """
    A wrapper around GamecubeControllerReader and InputQueue which leaves all the fiddly
    input-reading logic to GamecubeControllerReader, and provides a convenient interface for
    accessing the queue of inputs.

    This allows games to subclass this class and define new key mappings e.g. "A" --> "attack"
    """

    # input channels in CAPITALS to differentiate them from other methods
    LEFT = AxisInput(LEFT)
    RIGHT = AxisInput(RIGHT)
    UP = AxisInput(UP)
    DOWN = AxisInput(DOWN)
    A = ButtonInput(A)
    B = ButtonInput(B)
    X = ButtonInput(X)
    Y = ButtonInput(Y)
    Z = ButtonInput(Z)
    C_UP = AxisInput(C_UP)
    C_DOWN = AxisInput(C_DOWN)
    C_LEFT = AxisInput(C_LEFT)
    C_RIGHT = AxisInput(C_RIGHT)
    START = ButtonInput(START)
    D_PAD_UP = ButtonInput(D_UP)
    D_PAD_LEFT = ButtonInput(D_LEFT)
    D_PAD_RIGHT = ButtonInput(D_RIGHT)
    D_PAD_DOWN = ButtonInput(D_DOWN)
    L = ButtonInput(L)
    R = ButtonInput(R)
    L_AXIS = ButtonInput(L_AXIS)
    R_AXIS = ButtonInput(R_AXIS)

    def __init__(self, controller_id: int, queue_length=60):
        controller = GamecubeControllerReader(controller_id)
        self.controller_id = controller_id
        self.controller = controller
        super().__init__(queue_length)

        # for each parentless SingleInput declared on the class, create a new SingleInput
        # instance with self as parent.
        button_inputs = {
            name: attr
            for _class in self.__class__.__mro__
            for name, attr in _class.__dict__.items()
            if issubclass(_class, GamecubeController) and isinstance(attr, ButtonInput)
        }
        for name, attr in button_inputs.items():
            inp = attr.__class__(attr.id, parent=self)
            setattr(self, name, inp)

    def get_new_values(self):
        return self.controller.get_values()


if __name__ == "__main__":
    """visual input checking."""

    class TextPrint(object):
        def __init__(self):
            self.reset()
            pygame.font.init()
            self.font = pygame.font.Font(None, 30)

        def tprint(self, screen, textString):
            textBitmap = self.font.render(textString, True, BLACK)
            screen.blit(textBitmap, (self.x, self.y))
            self.y += self.line_height

        def reset(self):
            self.x = 10
            self.y = 10
            self.line_height = 20

        def indent(self):
            self.x += 10

        def unindent(self):
            self.x -= 10

    BLACK = pygame.Color("black")
    WHITE = pygame.Color("white")

    pygame.joystick.init()
    textPrint = TextPrint()

    screen = pygame.display.set_mode((500, 700))
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()
    done = False
    while not done:
        for event in pygame.event.get():  # User did something.
            if event.type == pygame.QUIT:  # If user clicked close.
                done = True  # Flag that we are done so we exit this loop.

        screen.fill(WHITE)
        textPrint.reset()
        controller = GamecubeControllerReader(joystick_id=0)

        textPrint.indent()
        textPrint.tprint(screen, "Gamecube controller 0")

        textPrint.tprint(screen, "Buttons:")
        textPrint.indent()
        for button in "A B X Y Z L R START".split():
            textPrint.tprint(screen, f"{button}: {getattr(controller, button)}")
        textPrint.unindent()

        textPrint.tprint(screen, "Axes:")
        textPrint.indent()
        for button in (
            "_L_TRIGGER_AXIS _R_TRIGGER_AXIS "
            "_GREY_STICK_X_AXIS _GREY_STICK_Y_AXIS "
            "_YELLOW_STICK_X_AXIS "
            "_YELLOW_STICK_Y_AXIS "
        ).split():
            textPrint.tprint(screen, f"{button}: {getattr(controller, button)}")
        textPrint.unindent()

        textPrint.tprint(screen, "Hats:")
        textPrint.indent()
        for button in "_D_PAD".split():
            textPrint.tprint(screen, f"{button}: {getattr(controller, button)}")
        textPrint.unindent()

        textPrint.tprint(screen, "PROCESSED INPUTS:")
        textPrint.indent()
        for button in (
            "LEFT RIGHT UP DOWN "
            "C_LEFT C_RIGHT C_UP C_DOWN "
            "R_AXIS L_AXIS "
            "D_LEFT D_RIGHT D_UP D_DOWN "
        ).split():
            textPrint.tprint(screen, f"{button}: {getattr(controller, button)}")
        textPrint.unindent()

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 20 frames per second.
        clock.tick(20)

    pygame.quit()
