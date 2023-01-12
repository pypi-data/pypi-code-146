"""
Dummy definition of a Finite State Machine config. It shows how a Finite State Machine
config should look like.
"""
import random

from state.finite_state_machine.config_keys import INITIAL_STATE, DEFAULT, TRANSITIONS, STATE_MACHINE

DUMMY_TRANSITIONS = {
    'transition_A': lambda prev_state, current_state: random.choice([True, False]),
    'transition_B': lambda prev_state, current_state: random.choice([True, False]),
    'transition_C': lambda prev_state, current_state: random.choice([True, False]),
}

DUMMY_STATE_MACHINE_CLASS_X = {
    INITIAL_STATE: 'state_A',
    TRANSITIONS: DUMMY_TRANSITIONS,
    STATE_MACHINE: {
                    'state_A': {'transition_A': 'state_B'},
                    'state_B': {'transition_B': 'state_C'},
                    'state_C': {'transition_C': 'state_A'},
    },
}

DUMMY_STATE_MACHINE_CONFIG = {
    'class_X': DUMMY_STATE_MACHINE_CLASS_X,
    DEFAULT: DUMMY_STATE_MACHINE_CLASS_X
}