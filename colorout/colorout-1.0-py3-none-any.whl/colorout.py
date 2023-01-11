import functools
import os

os.system("") # ENABLE_VIRTUAL_TERMINAL_PROCESSING on Windows


@functools.singledispatch
def dye(color, *, surface):
  """ Use dye(color, *, surface) to color your texts

  ** Int and Tuple types are expected in the color parameter, use int
     to use 256 color palette and tuple to use extended colors (RGB
     Format). *this also applies to aliases*

  ** Only <38> and <48> values ​​are expected in surface parameter.

  @aliase ``fg(color)`` same as ``dye(color, surface=38)``
  @aliase ``bg(color)`` same as ``dye(color, surface=48)``
  """
  print("\n%s" % FG_YELLOW % dye.__doc__)

@dye.register(int)
def _(color, *, surface):
  if color < 8: # ** reduce string size
    return "\x1B[{}m%s\x1B[{}m" \
           .format(surface - 8 + color, surface + 1)
  return "\x1B[{};5;{}m%s\x1B[{}m" \
         .format(surface, color, surface + 1)

@dye.register(tuple)
def _(color, *, surface):
  return "\x1B[{};2;{};{};{}m%s\x1B[{}m" \
         .format(surface, *color, surface + 1)


FG = 38
BG = 48

fg = functools.partial(dye, surface=FG)
fg.__doc__ = dye.__doc__
bg = functools.partial(dye, surface=BG)
bg.__doc__ = dye.__doc__


# Predefined colors (maximum compatibility)
FG_BLACK, FG_RED, FG_GREEN, FG_YELLOW, FG_BLUE, FG_MAGENTA, FG_CYAN, \
          FG_WHITE = [fg(i) for i in range(8)]
BG_BLACK, BG_RED, BG_GREEN, BG_YELLOW, BG_BLUE, BG_MAGENTA, BG_CYAN, \
          BG_WHITE = [bg(i) for i in range(8)]


def testing():

  print(BG_RED % "This has red bg")
  print(FG_RED % "This is red")
  print(BG_RED % FG_CYAN % "This is cyan with red bg" +
        ", this is standard")
  print(BG_CYAN % "This has cyan bg")
  print(FG_CYAN % "This is cyan")
  print(BG_CYAN % FG_RED % "This is red with cyan bg" +
        ", this is standard\n")

  for c in range(256):
    print(fg(c) % c, end=" ")
  print("\n")

  print(fg(196) % " ** " + "Official repository <%s>" % \
        fg((255, 255, 255)) % "https://github.com/goosebs/colorout")

if __name__ == "__main__":
  testing()
