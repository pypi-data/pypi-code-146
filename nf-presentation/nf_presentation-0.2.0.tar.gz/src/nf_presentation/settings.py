#
# Output formatting
#

#presentation
PRESENTATION_RATIO='16:9'
#Title list

LOGO_POSITION=(0.5,0.5)
LOGO_WIDTH=(12)

NAME_POSITION=(12,12)

#Exercises
#title
TITLE_POSITION=(0.5,0.5)
TITLE_SIZE=(33,1)
TITLE_BACKGROUND=(46,117,182)
TITLE_FOREGROUND=(255,255,255)

# left side
SCHEME_POSITION=(12.0,2.0)
SCHEME_HEIGHT=8.5 # not used atm
SCHEME_WIDTH=21.5


ADDITIONAL_TABLE_POSITION=(0.5,2.0)
ADDITIONAL_TABLE_WIDTH=10.5


#right side

BASIC_TABLE_POSITION=(12.0,2.0)
BASIC_TABLE_WIDTH=21.5

LINKS_TABLE_POSTION=(12,16.8)
LINKS_TABLE_WIDTH=21.5

DEFAULT_SLIDE_TITLE='Основная часть'

# PRESENTATION SETTINGS

DEFAULT_TITLE='---' #TODO default value for non found items


DEFAULT_TABLE_WIDTH=3
DEFAULT_TABLE_ROW_HEIGHT=0.4
DEFAULT_TABLE_HORZ_BANDING=False  # rows alternates color if True
DEFAULT_TABLE_MARK_FIRST_ROW=False  # highlights first row with alternative color if True

#DATA
EMPY_DESCRIPLION_REPLACEMENT='Пустое описание'  # if description is empty or None
UNKNOWN_GROUP_ID_NAME_REPLACEMENT='?'
EMPTY_TRAINER_NAME_REPLACEMENT='ИМЯ ТРЕНЕРА НЕ ПЕРЕДАНО'


#FILES
RFS_LOGO_FILE_NAME='rfs_logo.png'

# SVG SETTINGS
svg_replacements={
    'markerwidth':'markerWidth',
    'markerheight':'markerHeight',
    'viewbox':'viewBox',
    'refx':'refX',
    'refy':'refY'
}

png_render_width=600
png_render_height=400

def add_svg_replacement(old:str,new:str):
    svg_replacements[old]=new


