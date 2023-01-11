import logging


class StateController:
    """ This class could confuse a little take your time reading the code.
    This class is in charge of saying which generated state is going to be processed.
    Into a Gateway Task we have multiple sampling windows for a given asset, this sampling windows
    cloud arrive to the prediction service in a random order, this class gives an order to these
    states.
    An ideal behavior should be to process sampling windows in ascending order, HOWEVER sampling windows could get
    lost during the telemetry process, this class tries to solve this problem with an slicing windows approach, this
    is:
    lets define a sequence of sampling windows as S1, S2, S3, ...., Sn, Sn+1, ...., suppose some sampling windows
    are lost somewhere and do not arrived to the service: S1, S2, X, X, X, X, S7, ..., here the X represents lost
    sampling windows, this class defines a windows tolerance, if the number of lost sampling windows is bigger than
    SAMPLING_WINDOWS_TOLERANCE then the lowest non processed sampling window is going to be processed, in the example
    shown above, suppose S1 was the last processed sampling window and S7 is the last arrived sampling window to the
    state manager, then the slicing window looks like:
    S1, S2, X, X, X, X, S7, ...,
        [l              r]
    since r - l + 1 >= SAMPLING_WINDOWS_TOLERANCE, the next sampling window to be processed is S2.

    This class also implements an states_history this is used for checking the history of states in order to decide
    if the state that is going to be processed is going to be stored in BQ and generate a notification or not. The
    size of this cache is given by MAX_NUMBER_OF_ENQUEUE_STATES

    """

    MAX_NUMBER_OF_ENQUEUE_STATES = 10
    SAMPLING_WINDOWS_TOLERANCE = 3

    def __init__(self, log_level=logging.INFO):
        logging.basicConfig(level=log_level)
        self.states_db = {}
        self.states_history = {}

    def save_state(self, state, gateway_task_id_, sampling_window_index, number_of_sampling_windows):
        logging.info(f"Storing state on StateController {state}")
        sampling_window_index_str = str(sampling_window_index)
        gateway_task_id = str(gateway_task_id_)
        if gateway_task_id in self.states_db:
            if int(sampling_window_index_str) >= self.states_db[gateway_task_id]["next"]:
                logging.info(f"Storing state on StateController db {state}")
                self.states_db[gateway_task_id]["states"][sampling_window_index_str] = state
            else:
                logging.info(
                    f'State not stored next expected state is {self.states_db[gateway_task_id]["next"]} however '
                    f'{int(sampling_window_index_str)} found. It means an already discarded state appeared. {state}')
        else:
            logging.info(f"Storing state on StateController db {state}, this is the first state received for "
                         f"{gateway_task_id}")
            self.states_db[gateway_task_id] = {
                "next": 0,
                "number_of_sampling_windows": number_of_sampling_windows,
                "states": {sampling_window_index_str: state}
            }

    def get_state(self, gateway_task_id_):

        logging.info(f"Getting new state to be processed for {gateway_task_id_}")

        def log_state_processed(observation_timestamp, index, total):
            logging.info(f'New state is going to be processed, '
                         f'observation timestamp: {observation_timestamp}, '
                         f'sampling windows index: {index}, '
                         f'total number of sampling windows: {total}')

        gateway_task_id = str(gateway_task_id_)
        if gateway_task_id not in self.states_db:
            return None
        next_index = str(self.states_db[gateway_task_id]["next"])

        if next_index in self.states_db[gateway_task_id]["states"]:
            state = self.states_db[gateway_task_id]["states"].pop(next_index)
            log_state_processed(state["observation_timestamp"], next_index,
                                self.states_db[gateway_task_id]["number_of_sampling_windows"])
            self.states_db[gateway_task_id]["next"] += 1
            if self.states_db[gateway_task_id]["next"] == self.states_db[gateway_task_id]["number_of_sampling_windows"]:
                self.states_db.pop(gateway_task_id)
            return state
        else:
            logging.info(f"Expected state with index {next_index} is not available yet. Looking for window size for "
                         f"{gateway_task_id}")
            if self.states_db[gateway_task_id]["states"]:
                upper_index = max(self.states_db[gateway_task_id]["states"], key=lambda k: int(k))
                lower_index = min(self.states_db[gateway_task_id]["states"], key=lambda k: int(k))
                if (int(upper_index) - int(next_index)) >= StateController.SAMPLING_WINDOWS_TOLERANCE:
                    logging.info(f"Current current window size for {gateway_task_id} is big enough, processing oldest "
                                 f"available state")
                    state = self.states_db[gateway_task_id]["states"].pop(lower_index)
                    self.states_db[gateway_task_id]["next"] = int(lower_index) + 1
                    log_state_processed(state["observation_timestamp"], lower_index,
                                        self.states_db[gateway_task_id]["number_of_sampling_windows"])
                    return state
            logging.info(f"Window size is not big enough for {gateway_task_id}, no state is going to be processed")
            return None

    def enqueue_state(self, state, gateway_task_id_):
        gateway_task_id = str(gateway_task_id_)
        if gateway_task_id not in self.states_history:
            self.states_history[gateway_task_id] = [state]
        else:
            self.states_history[gateway_task_id] = [state] + self.states_history[gateway_task_id]
        if len(self.states_history[gateway_task_id]) > StateController.MAX_NUMBER_OF_ENQUEUE_STATES:
            logging.info(f"Max number of states reached for {gateway_task_id}, popping oldest state")
            self.states_history[gateway_task_id].pop()

    def get_states_history(self, gateway_task_id_, number_of_states):
        gateway_task_id = str(gateway_task_id_)
        if gateway_task_id in self.states_history:
            return self.states_history[gateway_task_id][:number_of_states]
        else:
            return []

    def clear_history(self, gateway_task_id_):
        gateway_task_id = str(gateway_task_id_)
        if gateway_task_id not in self.states_db:
            logging.info(f"All states processed for {gateway_task_id}, deleting its history")
            self.states_history.pop(gateway_task_id)
