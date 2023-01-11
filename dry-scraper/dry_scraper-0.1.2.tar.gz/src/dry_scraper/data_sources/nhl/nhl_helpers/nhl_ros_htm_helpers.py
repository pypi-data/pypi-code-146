import copy

from dry_scraper.shared import ROSTER_PLAYER_TEMPLATE, OFFICIAL_TEMPLATE


def strip_and_zip_player_list(tag_list):
    """
    Use strip_html_from_tag to process player_list of BeautifulSoup tags
    into list of strings.
    Then use zip_player_list to zip it into a list of tuples.

    :param tag_list: List of BeautifulSoup tags of the form
                     [jersey number, position, player name, ...]

    :return player_list: List of tuples of the form
                         [(jersey number, position, player name), ...]
    """
    string_list = [strip_html_from_tag(tag) for tag in tag_list]
    player_list = zip_player_list(string_list)
    return player_list


def strip_and_zip_official_list(tag_list):
    """
    Use strip_html_from_tag to process official_list of BeautifulSoup tags
    into list of strings.
    Then use zip_player_list to zip it into a list of tuples.

    :param tag_list: List of BeautifulSoup tags of the form
                     [jersey number, role, official name, ...]

    :return referees: List of tuples of the form
                      [(jersey number, 'Referee', official name), ...]
    :return linesmen: List of tuples of the form
                      [(jersey number, 'Linesman', official name), ...]
    """
    string_list = [strip_html_from_tag(tag) for tag in tag_list]
    referees = []
    linesmen = []
    for ref in string_list[:2]:
        split_ref = ref.split(' ')
        referees.append((split_ref[0][1], 'Referee', ' '.join(split_ref[1:])))
    for lin in string_list[2:]:
        split_lin = lin.split(' ')
        linesmen.append((split_lin[0][1], 'Linesman', ' '.join(split_lin[1:])))
    return referees, linesmen


def strip_html_from_tag(item):
    """
    Strip HTML and whitespace from BeautifulSoup tag object and return
    its string contents

    :param item: BeautifulSoup tag containing text of interest

    :return text: string of meaningful text contained within item
    """
    try:
        text = item.text.strip()
    except AttributeError:
        text = ''
    except:
        text = ''
        print(f'Encountered unknown exception while stripping {item}')
    return text


def zip_player_list(tag_list):
    """
    Zip  a list of [jersey number, position, player name, ...]
    into a list of lists using a list comprehension

    :param tag_list: list of [jersey number, position, player name, ...]

    :return : zipped list of player tuples containing jersey number, position,
              and player name
    """
    player_list = [a for a in zip(tag_list[0::3],
                                  tag_list[1::3],
                                  tag_list[2::3])]
    return player_list


def create_ros_entries(players):
    """
    Take list of lists of players of form [jersey number, position, player name]
    and returns a list of dictionaries with the same information

    :param players: list of lists of form described above
    """
    return [create_ros_entry(player) for player in players]


def create_ros_entry(player):
    """
    Return dictionary representation of player data specified by player

    :param player: list of player information of form [jersey number, position,
                   player name]
    """
    dct = copy.deepcopy(ROSTER_PLAYER_TEMPLATE)
    dct['jerseyNumber'] = player[0]
    dct['position'] = player[1]
    if '(C)' in player[2]:
        dct['name'] = player[2][:-5]
        dct['captain'] = True
    elif '(A)' in player[2]:
        dct['name'] = player[2][:-5]
        dct['alternate'] = True
    else:
        dct['name'] = player[2]
    return dct


def create_official_entries(officials):
    """
    Take list of tuples of officials of form [jersey number, position, name]
    and returns a list of dictionaries with the same information

    :param officials: list of tuples of form described above
    """
    return [create_official_entry(official) for official in officials]


def create_official_entry(official):
    """
    Return dictionary representation of official data specified by official

    :param official: list of official information of form [jersey number, position, name]
    """
    dct = copy.deepcopy(OFFICIAL_TEMPLATE)
    dct['jerseyNumber'] = official[0]
    dct['role'] = official[1]
    dct['name'] = official[2]
    return dct
