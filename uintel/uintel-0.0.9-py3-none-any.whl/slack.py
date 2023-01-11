"""
Quickly send messages or files to a Slack channel or person
"""

__all__ = ["post_message", "post_files"]

import random, slack_sdk, slack_sdk.errors, socket, textwrap, warnings, typing
from uintel import config as _config

_GREETINGS = ["Kia ora!", "Howdy partner.", "G'day mate.", "What up g? :sunglasses:", "Ugh finally, this shit is done.", "Kachow! :racing_car:", "Kachigga! :racing_car:", "Sup dude.", "Woaaaaahhhh, would you look at that!", "Easy peasy.", "Rock on bro. :call_me_hand:", "Leshgoooooo!", "Let's get this bread!", "You're doing great dude. :kissing_heart:", "Another one bits the dust...", "Sup, having a good day?", "Yeeeeeeehaw cowboy! :face_with_cowboy_hat:"] 


def post_message(to: str, message: str, identifier: typing.Optional[str], silent_usernames: typing.Union[str, list], domain="UI", greet=True) -> None:
    """
    Posts a message to a Slack Channel or User.
    Note: if you wish to post to a channel, a hashtag ("#") must be placed at the start of 'to', otherwise it is assumed that the message is for a person.
    """

    # Check which slack domain to post to
    try:
        tokens = _config["slack"].copy()
        token = token[domain.upper()]
    except KeyError:
        warnings.warn(f"You have provided an unsupported domain. I will assume you wish to post this to Urban Intelligence's slack. But next time, please either use one of the following: {list(tokens.keys())}.")
        token = tokens["UI"]

    # Start up the client to post to
    client = slack_sdk.WebClient(token=token)
    
    # If it is not a channel, grab the user's ID instead to DM them
    if not to.startswith("#"):
        to = _get_users_information_from_name(to, "id", client)

    # Generate the content used in the message
    if identifier:
        header, header_lines = _generate_header(identifier) 
    else:
        header, header_lines = "", []
    blocks = _generate_blocks(message, header_lines, greet)

    try:
        # Send a quiet message if requested
        if silent_usernames != None:
            if type(silent_usernames) == str:
                silent_user_ids = [_get_users_information_from_name(silent_usernames, "id", client)]
            elif type(silent_usernames) == list:
                silent_user_ids = [_get_users_information_from_name(silent_username, "id", client) for silent_username in silent_usernames]
            for silent_user_id in silent_user_ids:
                _ = client.chat_postEphemeral(channel=to, blocks=blocks, user=silent_user_id, text=header)
        # Or send it to a public/private channel
        else:
            _ = client.chat_postMessage(channel=to, blocks=blocks, text=header)
    
    except slack_sdk.errors.SlackApiError as error:
        warnings.warn(f"The message could not be posted to slack. Error: {error.response['error']}")


def _generate_header(identifier: str) -> typing.Tuple[str, list]:
    """
    Generates a header, or a list of headers depending on the length of the header, to be used to quickly summarise the message to be posted to the Slack channel or User.
    """
    # Unfortunately, there is a 150 character limit on the header length, so split and send multiple if that is the case!
    header = f'{identifier} |  Running on {socket.gethostname()}'
    if len(header) > 150:
        header_lines = textwrap.wrap(header, width=100, break_long_words=False, break_on_hyphens=False)
    else:
        header_lines = [header]

    return header, header_lines


def _generate_blocks(message_type: str, message: str, header_lines: list, greet: bool):
    """
    Generates the blocks, a JSON-based list of structured blocks presented as URL-encoded strings, to be used to display message to be posted to the Slack channel or User.
    Example:
    [{"type": "section", "text": {"type": "plain_text", "text": "Hello world"}}]    
    """

    greeting = random.sample(_GREETINGS, 1)[0] + " " if greet else ""

    blocks=[]

    if header_lines != None:
        for header_line in header_lines:
            blocks.append({"type": "header", 
                            "text":
                                {"type": "plain_text", 
                                "text": header_line, 
                                "emoji": True}
                            })
        blocks.append({"type": "divider"})

    if message_type.title() ==  "Information":
        blocks.append({ "type": "section",
                        "text": {"type": "mrkdwn",
                                "text": greeting+message}
                        })       
    elif message_type.title() == "Success":
        blocks.append({"type": "section",
                        "text": {"type": "mrkdwn",
                                "text": greeting+"It is my pleasure to inform you that the procedure has been a success."}
                        })       
    elif message_type.title() == "Failure": 
        # Strip away any output in stdout before the error message begins
        lookout_phrase = "Traceback (most recent call last):"
        if lookout_phrase in message:
            message = message[message.index(lookout_phrase)+len(lookout_phrase):].strip()

        blocks.extend([{"type": "section",
                        "text": {"type": "mrkdwn",
                                "text": f"{greeting}It is unfortunate that I must inform that something went wrong."}
                        },
                    {"type": "section",
                    "text": {"type": "mrkdwn",
                            "text": "*Error Traceback:*"}
                    },
                    {"type": "divider"},
                    {"type": "section",
                    "text": {"type": "mrkdwn",
                            "text": message.strip("\r\n")}
                    }])
    
    return blocks


def post_files(to: str, filenames: typing.Union[str, list], message=None, greet=True, domain="UI") -> None:
    """
    Posts file(s) to a Slack Channel or User, with an optional prefacing message.
    """

    # Check which slack domain to post to
    try:
        tokens = _config["slack"].copy()
        token = token[domain.upper()]
    except KeyError:
        warnings.warn(f"You have provided an unsupported domain. I will assume you wish to post this to Urban Intelligence's slack. But next time, please either use one of the following: {list(tokens.keys())}.")
        token = tokens["UI"]

    # Start up the client to post to
    client = slack_sdk.WebClient(token=token)
    
    # If it is not a channel, grab the user's ID instead to DM them
    if not where_to_post.startswith("#"):
        where_to_post = _get_users_information_from_name(where_to_post, "id", client)

    # Add a greeting if the user asked for one
    greeting = random.sample(_GREETINGS, 1)[0] + " " if greet else ""
    
    # In case only one file was passed in, then chuck the string into a list by itself
    if type(filenames) == str:
        filenames = [filenames]

    try:
        inital_comment_sent = False
        for filename in filenames:
            if not inital_comment_sent:
                # Send the files with the initial comment as it has not been sent yet
                _ = client.files_upload(channels=where_to_post, initial_comment=greeting+message, file=filename)
                inital_comment_sent = True
            else:
                # Otherwise send just the files
                _ = client.files_upload(channels=where_to_post, file=filename)
    
    except slack_sdk.errors.SlackApiError as error:
        warnings.warn("The file {} could not be posted to slack. Error: {}".format(filename, error.response["error"]), UserWarning)


def _get_users_information_from_name(user_name: str, wanted_information: str, client: slack_sdk.WebClient) -> typing.Any:
    """
    Retrieves a specified *wanted_information* attribute of a user by the name of *user_name*. The *user_name* can be the full name of the individual or their display name. If no exact matches are found, then possible matches are considered by their full name, display name and by first name and surname.    
    """

    # Change the user_name to title case so we can == compare it with the other fields
    user_name = user_name.title()
    
    # Create lists for exact and possible matches
    exact_matches = []
    possible_matches = []

    # Query the client for a list of members
    members = client.users_list()["members"]

    for member in members:
        # If inactive user or is a bot then continue to the next
        if member["deleted"] or member["is_bot"]:
            continue
        
        # Check for exact results of id! E.g. the user passed in the actual id of the person, so why bother looking any further!
        if member.get("id", "") == user_name:
            return user_name
        
        # Check for exact mataches against the profile
        profile_details = member.get("profile", {})
        if profile_details.get("real_name", "").title() == user_name:
            exact_matches.append(member)
        elif profile_details.get("display_name", "").title() == user_name:
            exact_matches.append(member)
        elif profile_details.get("real_name_normalized", "").title() == user_name:
            exact_matches.append(member)
        elif profile_details.get("display_name_normalized", "").title() == user_name:
            exact_matches.append(member)

        # Check for possible matches
        elif user_name in member.get("id", ""):
            possible_matches.append(member)
        elif user_name in profile_details.get("real_name", "").title():
            possible_matches.append(member)
        elif user_name in profile_details.get("display_name", "").title():
            possible_matches.append(member)
        elif user_name in profile_details.get("real_name_normalized", "").title():
            possible_matches.append(member)
        elif user_name in profile_details.get("display_name_normalized", "").title():
            possible_matches.append(member)
        elif user_name.split(" ")[0] in profile_details.get("first_name", "").title():
            possible_matches.append(member)
        elif user_name.split(" ")[-1] in profile_details.get("last_name", "").title():
            possible_matches.append(member)

    
    if len(exact_matches) == 1:
        # Best case scenario!
        chosen_user_details = exact_matches[0]

    elif len(exact_matches) > 1:
        print(f"Multiple users detected with the user_name '{user_name}'. Please define which user you are indending to post to from the current list:\n")
        counter = 1
        for exact_match in exact_matches:
            print(f"Possible Match {counter}:")
            print(exact_match, end="\n")
            counter +=1 
        correct_individual_number = int(input(f"From this list, which number (from 1 to {len(exact_matches)}) was the user you were wishing to post locate?"))
        chosen_user_details = exact_matches[correct_individual_number - 1]
    
    else:
        if len(possible_matches) == 1:
            chosen_user_details = possible_matches[0]
        else:
            print(f"No exact matches were found for '{user_name}. However, multiple possible matches exists. Please define which user you are indending to post to from the current list:\n")
            counter = 1
            for possible_match in possible_matches:
                print(f"Possible Match {counter}:")
                print(possible_match, end="\n")
                counter +=1 
            correct_individual_number = int(input(f"From this list, which number (from 1 to {len(possible_matches)}) was the user you were wishing to post locate?"))
            chosen_user_details = possible_matches[correct_individual_number - 1]

    # Now grab the wanted_information from the chosen_user_details
    if wanted_information in chosen_user_details:
        chosen_information = chosen_user_details[wanted_information]
    elif wanted_information in chosen_user_details["profile"]:
        chosen_information = chosen_user_details["profile"][wanted_information]
    else:
        keys = sorted(set(list(chosen_user_details.keys()) + list(chosen_user_details["profile"].keys())))
        correct_wanted_information = input(f"The user name {user_name} was found but the wanted information {wanted_information} is not within the recorded details. Please choose from the following:\n {keys}")
        if correct_wanted_information in chosen_user_details:
            chosen_information = chosen_user_details[correct_wanted_information]
        elif correct_wanted_information in chosen_user_details["profile"]:
            chosen_information = chosen_user_details["profile"][correct_wanted_information]
    
    return chosen_information
