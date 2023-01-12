from munch import DefaultMunch

class Map:
    def __init__(self, min_x=-120, min_y=-120, max_x=14870, max_y=14980, name="Summoner's Rift"):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.name = name


maps = {
    11:
        Map(min_x=-120, min_y=-120, max_x=14870, max_y=14980, name="Summoner's Rift"),
    1:
        Map(min_x=-120, min_y=-120, max_x=14870, max_y=14980, name="Summoner's Rift")
}


class Position:
    def __init__(self, position_data, map):
        self.absolute = position_data
        try:
            self.normalized = DefaultMunch.fromDict({
                "x": (position_data["x"] - map.min_x) / map.max_x,
                "y": (position_data["y"] - map.min_y) / map.max_y,
            })
        except:
            #print(position_data)
            self.normalized = None
