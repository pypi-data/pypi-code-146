#!/usr/bin/env python3

ID_UNTRACKED = "<untracked>"
ID_UNSTAGED = "<unstaged>"
ID_STAGED = "<staged>"
ID_STASHES_GROUP = "<stashed>"
ID_TODO = "<todo>"
SPECIAL_DETAILS_IDS = (ID_UNTRACKED, ID_UNSTAGED, ID_STAGED, ID_TODO)
SPECIAL_IDS = SPECIAL_DETAILS_IDS + (ID_STASHES_GROUP,)

VIRTUAL_ID_OTHER = "<other>"

TYPE_STASHED = "stashed"
TYPE_OTHER = "other"
TYPE_ERROR = "error"
TYPE_TAG = "tag"
TYPE_START_OF_FILE = "sof"
TYPE_NUMBERED_LINE = "numbered-line"
TYPE_UNTRACKED = "untracked"
TYPE_TODO = "todo"
