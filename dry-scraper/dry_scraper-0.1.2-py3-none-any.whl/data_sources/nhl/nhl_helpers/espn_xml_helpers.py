import copy
from datetime import datetime, timedelta
from xml.etree.ElementTree import fromstring, XMLParser, ElementTree

import requests
from bs4 import BeautifulSoup

from dry_scraper.data_sources.nhl.nhl_api_sources import NhlGameLiveFeedApiSource
from dry_scraper.shared import (ESPN_EVENTS, GOAL_TEMPLATE, SHOT_TEMPLATE,
                                FACEOFF_TEMPLATE, GAME_END_TEMPLATE,
                                MISSED_SHOT_TEMPLATE, HIT_TEMPLATE, TAKEAWAY_TEMPLATE,
                                GIVEAWAY_TEMPLATE, BLOCKED_SHOT_TEMPLATE, PENALTY_TEMPLATE,
                                ESPN_PENALTIES, ESPN_PENALTIES_DICT, STOP_TEMPLATE,
                                PERIOD_START_TEMPLATE, PERIOD_END_TEMPLATE,
                                SHOOTOUT_END_TEMPLATE)


def determine_espn_play_type(play_id):
    """
    Determine the play type from the text of an ESPN event

    Args:
        play_id (str): id number from ESPN XML indicating play type

    Returns:
        play_type (str): text of type of play

    """
    play_type = ESPN_EVENTS[play_id]
    return play_type


def parse_xml_plays(xml_content):
    """
    Parse XML document into tree using etree, pull out list of plays, and create list of
    strings representing each play

    Args:
        xml_content (str): string representation of XML document

    Returns:

    """
    xml_root = fromstring(xml_content, XMLParser(encoding='UTF-8'))
    xml_tree = ElementTree(xml_root)
    xml_plays = xml_tree.getroot()[1]
    plays = [p.text.upper() for p in xml_plays][:-1]

    return plays


def fill_player_field(event, idx, player_name):
    """
    Fill event with the record associated with the player name given
    If there is no matching key, use fuzzy matching to find the closest name
    Add the unrecognized name to the roster dictionary

    Args:
        event (dict): dictionary representing an NHL-style json penalty event
        idx (int): index in play where player is to be added
        player_name (str): name of player extracted from ESPN XML

    Returns:
        event (dict): dictionary representing an NHL-style json penalty event
    """
    if player_name.strip() == '':
        event['players'][idx]['player'] = ''
        return
    event['players'][idx]['player'] = player_name
    return event


def build_goal_event(play):
    """
    Create an NHL-style json goal event from an ESPN XML goal event

    Args:
        play (str): ESPN play delimited by tildes

    Returns:
        goal_event (dict): NHL-style goal event
    """
    goal_event = copy.deepcopy(GOAL_TEMPLATE)
    play_list = play.split('~')
    desc = play_list[8]

    if 'ASSISTED BY' in desc:
        scorer_name = desc[desc.find(' BY ') + 4:
                           desc.find(' ASSISTED BY')].strip()
        if ' AND ' in desc:
            primary_name = desc[desc.find('ASSISTED BY') + 12:
                                desc.find(' AND ')].strip()
            secondary_name = desc[desc.find(' AND ') + 5:].strip()
        else:
            primary_name = desc[desc.find('ASSISTED BY') + 12:].strip()
            secondary_name = ''
    else:
        scorer_name = desc[desc.find(' BY ') + 4:].strip()
        primary_name = ''
        secondary_name = ''

    fill_player_field(goal_event, 0, scorer_name)
    if primary_name:
        fill_player_field(goal_event, 1, primary_name)
    if secondary_name:
        fill_player_field(goal_event, 2, secondary_name)
    return goal_event


def build_shot_event(play):
    """
    Create an NHL-style json shot event from an ESPN XML shot event

    Args:
        play (str): ESPN play delimited by tildes

    Returns:
        shot_event (dict): NHL-style shot event
    """
    shot_event = copy.deepcopy(SHOT_TEMPLATE)
    play_list = play.split('~')
    desc = play_list[8]

    shooter_name = desc[16:desc.find(' SAVED ')].strip()
    goalie_name = desc[desc.find(' SAVED ') + 10:].strip()
    fill_player_field(shot_event, 0, shooter_name)
    fill_player_field(shot_event, 1, goalie_name)
    return shot_event


def build_faceoff_event(play):
    """
    Create an NHL-style json faceoff event from an ESPN XML faceoff event

    Args:
        play (str): ESPN play delimited by tildes

    Returns:
        faceoff_event (dict): NHL-style faceoff event
    """
    faceoff_event = copy.deepcopy(FACEOFF_TEMPLATE)
    play_list = play.split('~')
    desc = play_list[8]

    winner_name = desc[:desc.find(' WON')].strip()
    loser_name = desc[desc.find(' AGAINST ') + 9:desc.find(' IN ')].strip()
    fill_player_field(faceoff_event, 0, winner_name)
    fill_player_field(faceoff_event, 1, loser_name)
    return faceoff_event


def build_missed_shot_event(play):
    """
    Create an NHL-style json missed_shot event from an ESPN XML missed_shot event

    Args:
        play (str): ESPN play delimited by tildes

    Returns:
        missed_shot_event (dict): NHL-style missed_shot event
    """
    missed_shot_event = copy.deepcopy(MISSED_SHOT_TEMPLATE)
    play_list = play.split('~')
    desc = play_list[8]

    shooter_name = desc[desc.find(' BY ') + 4:].strip()
    fill_player_field(missed_shot_event, 0, shooter_name)
    return missed_shot_event


def build_hit_event(play):
    """
    Create an NHL-style json hit event from an ESPN XML hit event

    Args:
        play (str): ESPN play delimited by tildes

    Returns:
        hit_event (dict): NHL-style hit event
    """
    hit_event = copy.deepcopy(HIT_TEMPLATE)
    play_list = play.split('~')
    desc = play_list[8]

    hitter_name = desc[:desc.find(' CREDITED')].strip()
    hittee_name = desc[desc.find(' HIT ON ') + 8:desc.find(' IN ')].strip()
    fill_player_field(hit_event, 0, hitter_name)
    if hittee_name.strip():
        fill_player_field(hit_event, 1, hittee_name)
    return hit_event


def build_takeaway_event(play):
    """
    Create an NHL-style json takeaway event from an ESPN XML takeaway event

    Args:
        play (str): ESPN play delimited by tildes

    Returns:
        takeaway_event (dict): NHL-style takeaway event
    """
    takeaway_event = copy.deepcopy(TAKEAWAY_TEMPLATE)
    play_list = play.split('~')
    desc = play_list[8]

    player_name = desc[12:desc.find(' IN ')].strip()
    fill_player_field(takeaway_event, 0, player_name)
    return takeaway_event


def build_giveaway_event(play):
    """
    Create an NHL-style json giveaway event from an ESPN XML giveaway event

    Args:
        play (str): ESPN play delimited by tildes

    Returns:
        giveaway_event (dict): NHL-style giveaway event
    """
    giveaway_event = copy.deepcopy(GIVEAWAY_TEMPLATE)
    play_list = play.split('~')
    desc = play_list[8]

    player_name = desc[12:desc.find(' IN ')].strip()
    fill_player_field(giveaway_event, 0, player_name)
    return giveaway_event


def build_blocked_shot_event(play):
    """
    Create an NHL-style json blocked_shot event from an ESPN XML blocked_shot event

    Args:
        play (str): ESPN play delimited by tildes

    Returns:
        blocked_shot_event (dict): NHL-style blocked_shot event
    """
    blocked_shot_event = copy.deepcopy(BLOCKED_SHOT_TEMPLATE)
    play_list = play.split('~')
    desc = play_list[8]

    shooter_name = desc[:desc.find(' SHOT BLOCKED')].strip()
    blocker_name = desc[desc.find(' BY ') + 4:].strip()
    fill_player_field(blocked_shot_event, 0, blocker_name)
    fill_player_field(blocked_shot_event, 1, shooter_name)
    return blocked_shot_event


def build_penalty_event(play):
    """
    Create an NHL-style json penalty event from an ESPN XML penalty event

    Could probably do this better by making a dict corresponding play_list[9]
    with a result dict
    Args:
        play (str): ESPN play delimited by tildes

    Returns:
        penalty_event (dict): NHL-style penalty event
    """
    penalty_event = copy.deepcopy(PENALTY_TEMPLATE)
    play_list = play.split('~')
    result = copy.deepcopy(ESPN_PENALTIES[play_list[9]])
    penalty = ESPN_PENALTIES_DICT[result['secondaryType']]
    desc = play_list[8]

    penalty_event['result'] = result
    penalty_event['result']['description'] = desc

    offender_name = desc[desc.find(' TO ') + 4:desc.find(' MINUTES') - 3]
    server_name = desc[desc.find('SERVED BY'):-1]
    if server_name:
        offendee_name = desc[desc.find(penalty) + len(penalty) + 1:
                             (desc.find('SERVED BY') - 2) if server_name else 0]
    else:
        offendee_name = desc[desc.find(penalty) + len(penalty) + 1:]
    if server_name:
        fill_player_field(penalty_event, 2, server_name[10:])
    if offender_name:
        fill_player_field(penalty_event, 0, offender_name)
    if offendee_name:
        fill_player_field(penalty_event, 1, offendee_name)

    if not penalty_event['players'][2]:
        del penalty_event['players'][2]
    if not penalty_event['players'][1]:
        del penalty_event['players'][1]
    if not penalty_event['players'][0]:
        del penalty_event['players'][0]

    return penalty_event


def build_stop_event(play):
    """
    Create an NHL-style json stoppage event from an ESPN XML stop event

    Args:
        play (str): ESPN play delimited by tildes

    Returns:
        stop_event (dict): NHL-style stop event
    """
    stop_event = copy.deepcopy(STOP_TEMPLATE)
    play_list = play.split('~')
    desc = play_list[8]
    stoppage_type = desc[desc.find(' - ') + 3:]
    stop_event['result']['description'] = stoppage_type
    return stop_event


def build_period_start_event(_):
    """
    Create an NHL-style json period start event from an ESPN XML period start event

    Returns:
        period_start_event (dict): NHL-style period start event
    """
    period_start_event = copy.deepcopy(PERIOD_START_TEMPLATE)
    return period_start_event


def build_period_end_event(_):
    """
    Create an NHL-style json period end event from an ESPN XML period end event

    Returns:
        period_end_event (dict): NHL-style period end event
    """
    period_end_event = copy.deepcopy(PERIOD_END_TEMPLATE)
    return period_end_event


def build_game_end_event(_):
    """
    Create an NHL-style json game end event from an ESPN XML game end event

    Returns:
        game_end_event (dict): NHL-style game end event
    """
    game_end_event = copy.deepcopy(GAME_END_TEMPLATE)
    return game_end_event


def build_shootout_end_event(_):
    """
    Create an NHL-style json shootout end event from an ESPN XML shootout end event

    Returns:
        shootout_end_event (dict): NHL-style shootout end event
    """
    shootout_end_event = copy.deepcopy(SHOOTOUT_END_TEMPLATE)
    return shootout_end_event


# noinspection PyArgumentList
def determine_espn_id(season, gamePk):
    """
    Determine the game ID number assigned by ESPN
        1. Determine teams and date of match from NHL API live game feed
        2. Retrieve NHL schedule page for that date from ESPN
        3. Parse HTML and search for teams to extract ESPN game ID

    Returns:
        espn_game_id (str) : espn game ID number
    """
    espn_game_id = ''
    home, away, date = (NhlGameLiveFeedApiSource(season=season, gamePk=gamePk)
                        .fetch_content()
                        .yield_teams_and_date())
    home = home[:2] if home in ['SJS', 'LAK', 'NJD', 'TBL', 'VGK'] else home
    away = away[:2] if away in ['SJS', 'LAK', 'NJD', 'TBL', 'VGS'] else away
    est_time = (datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ') - timedelta(hours=5))
    date_str = datetime.strftime(est_time, '%Y%m%d')
    url = f'https://www.espn.com/nhl/schedule/_/date/{date_str}'
    try:
        schedule_htm = requests.get(url, timeout=10)
        schedule_htm.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)
    else:
        espn_soup = BeautifulSoup(schedule_htm.text, features='html.parser')
        trs = espn_soup.find('table').findAll('tr')
        for tr in trs:
            if home in tr.get_text() and away in tr.get_text():
                tds = tr.findAll('td')
                espn_game_id = tds[2].find('a').get('href')[-9:]
    return espn_game_id
