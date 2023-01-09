import webcolors

color_groups_dict = {
	'pink':['deeppink','hotpink','lightpink','mediumvioletred','palevioletred','pink'],
	'red':['crimson','darkred','darksalmon','firebrick','orangered','indianred','lightcoral','lightsalmon','red','salmon'],
	'orange':['coral','darkorange','gold','orange','tomato'],
	'yellow':['darkkhaki','khaki','lemonchiffon','lightgoldenrodyellow','lightyellow','moccasin','palegoldenrod','papayawhip','yellow'],
	'brown':['bisque','blanchedalmond','brown','burlywood','chocolate','cornsilk','darkgoldenrod','goldenrod','maroon','peru','rosybrown','saddlebrown','sandybrown','sienna','tan','wheat'],
	'green':['chartreuse','darkgreen','darkolivegreen','darkseagreen','forestgreen','green','greenyellow','lawngreen','lightgreen','lime','limegreen','mediumseagreen','lightseagreen','mediumaquamarine','mediumspringgreen','olive','olivedrab','palegreen','seagreen','springgreen','yellowgreen'],
	'cyan':['cadetblue','mediumturquoise','cyan','darkcyan','lightcyan','teal'],
	'blue':['blue','blueviolet','darkturquoise','turquoise','cornflowerblue','darkblue','deepskyblue','dodgerblue','lightblue','lightskyblue','lightsteelblue','mediumblue','midnightblue','navy','powderblue','royalblue','skyblue','steelblue'],
	'purple':['darkmagenta','darkorchid','darkslateblue','darkviolet','fuchsia','indigo','lavender','magenta','mediumorchid','mediumpurple','mediumslateblue','orchid','plum','purple','rebbecapurple','slateblue','thistle','violet'],
	'gray':['aliceblue','antiquewhite','azure','beige','darkgray','darkslategray','dimgray','floralwhite','gainsboro','ghostwhite','gray','honeydew','ivory','lavenderblush','lightgray','lightslategray','linen','mintcream','mistyrose','navajowhite','oldlace','seashell','silver','slategray','snow','whitesmoke'],
	'black':[],
	'white':[]
}

def hex_to_rgb(hex_):
	hex_ = hex_.lstrip('#')
	return tuple(int(hex_[i:i+2], 16) for i in (0, 2, 4))

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def closest_color_by_rgb(rgb_):
    try:
        closest_name = webcolors.rgb_to_name(rgb_)
    except ValueError:
        closest_name = closest_colour(rgb_)
    return closest_name

def closest_color_by_hex(hex_):
    rgb_ = hex_to_rgb(hex_)
    try:
        closest_name = webcolors.rgb_to_name(rgb_)
    except ValueError:
        closest_name = closest_colour(rgb_)
    return closest_name

def color_group_by_hex(hex_):
    """ 
    returns a color name (e.g. blue, white, red) from given hex code
    params:
        - hex: str (format #xxxxxx)

    returns str : colorname

    example: 
        name = color_group_by_hex('#ffffff')
        print(name) 
        output: 'white' 
    """

    color_name = closest_color_by_hex(hex_)

    for color in color_groups_dict.keys():
    	if color_name == color:
    		return color_name
    	else:
    		for color_ in color_groups_dict[color]:
    			if color_name == color_:
    				return color

def color_group_by_rgb(rgb_):
    """ 
    returns a color name (e.g. blue, white, red) from given rgb code
    params:
        - hex: str (format tuple(255, 255, 240))

    returns str : colorname

    example: 
        name = color_group_by_rgb((255, 255, 255))
        print(name) 
        output: 'white' 
    """

    color_name = closest_color_by_rgb(rgb_)

    for color in color_groups_dict.keys():
        if color_name == color:
            return color_name
        else:
            for color_ in color_groups_dict[color]:
                if color_name == color_:
                    return color