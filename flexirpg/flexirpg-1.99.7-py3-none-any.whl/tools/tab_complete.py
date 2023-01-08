# Tab completion helpers
#
# Copyright (C) 2019 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

def tab_complete(partial, strs):
    """Tab-complete a partial string from a list of possible strings.

    Returns the longer "tab completion" string of @partial from the
    list of strings @strs, or None if there's no matching completion.

    """

    # Find all the possible matches.
    matches = []
    for s in strs:
        if s.startswith(partial):
            matches.append(s)

    # No matches.
    if not matches:
        return None

    # Single match, return the whole match.
    if len(matches) == 1:
        return matches[0]

    # Multiple matches, find the longest common prefix between all the
    # matches.
    shortest_match = min(matches, key=len)
    longest_prefix = partial
    for i in range(len(partial), len(shortest_match)):
        possible_prefix = shortest_match[:i+1]
        if all(x.startswith(possible_prefix) for x in matches):
            longest_prefix = possible_prefix
    return longest_prefix
