from typing import Optional, Any
from kepingai import KepingApi


class Strategy:
    def __init__(self, strategy_id: str, api: KepingApi):
        self.api = api
        self.strategy_id = strategy_id

    def open_signal(self, signal_params: dict, **kwargs):
        """ Open a signal

            Parameters
            ----------
            signal_params: `dict`
                The signal main input parameters.

            Keyword Args
            ------------
            take_profit: `Union[dict, float]`
                Single take profit with float and dict for take profit
                checkpoints with format {"<tp_threshold>": <tp_size>}.
                e.g., {"0.005": 0.33, "0.01": 0.33, "0.015": 0.34}
                Checkpoint at 0.5%, 1% and 1.5% with 33%, 33% and 34% size each.
            checkpoint_close_position: `Optional[float]`
                The checkpoint close position threshold, in positive decimal,
                use None to disable. e.g., use 0.01 for 1% threshold
            timeout_sec: `Optional[int]`
                Timeout duration in second, use None to disable timeout.
            stop_loss: `Optional[float]`
                The stop loss position threshold, real numbers in decimal,
                use None to disable stop loss for this specific signal.
                e.g., use -0.005 for -0.5% threshold
            trailing_deviation: `Optional[float]`
                The trailing deviation threshold, positive decimal,
                use None to disable trailing.
            max_safety_order_count: `int`
                The maximum number of safety order(s), use 0 to disable safety
                order for this specific signal.
            safety_deviation: `float`
                The safety deviation, in positive decimal.
            safety_volume_scale: `float`
                The safety volume scale, in positive decimal.
            safety_step_scale: `float`
                The safety step scale, in positive decimal.

            Notes
            -----
            Please ensure the strategy allocates capital for safety order,
            total safety order size > 0%, to allow safety orders on the signal.
            If the size is 0%, the signal will not execute any safety orders
            even through SDK params.
        """
        signal_params.update({
            "strategy_id": self.strategy_id,
            "action": "open",
            "strategy_params": handle_strategy_params(**kwargs)
        })
        return self.api.post(data=signal_params, tag="strategy/publish-signal")

    def close_signal(self,
                     signal_params: dict):
        signal_params.update({"strategy_id": self.strategy_id,
                              "action": "closed"})
        return self.api.post(data=signal_params, tag="strategy/publish-signal")

    def get_active_signals(self):
        params = {"strategy_id": self.strategy_id}
        return self.api.get(params=params, tag="strategy/active-signals")


def handle_strategy_params(**kwargs) -> dict:
    """ To handle the strategy params, ensuring the correct formatting. """
    # there will be restriction in the API also!
    _available_keys = [
        "take_profit", "checkpoint_close_position", "trailing_deviation",
        "timeout_sec", "stop_loss", "max_safety_order_count",
        "safety_deviation", "safety_volume_scale", "safety_step_scale"
    ]
    # check for invalid key params
    invalid_keys = []
    for k in kwargs:
        if k not in _available_keys:
            invalid_keys.append(k)
            continue
    if len(invalid_keys):
        raise ValueError(f"Invalid strategy params: {invalid_keys} occurred! "
                         f"Please use kwargs from the available params only: "
                         f"{_available_keys}.")
    # construct the strategy params
    params = {}
    if "take_profit" in kwargs and kwargs["take_profit"] is not None:
        _tp = kwargs["take_profit"]
        if isinstance(_tp, dict):  # take profit checkpoints
            _take_profit = dict(sorted(_tp.items(), key=lambda x: float(x[0])))
            take_profit = {k: float(v) for k, v in _take_profit.items()}
            total_tp_size = sum(take_profit.values())
            if total_tp_size != 1:
                raise ValueError(
                    f"The total take profit checkpoint size ({total_tp_size}) "
                    f"is not equal to 1.0! The input checkpoints: {take_profit}")
        elif isinstance(_tp, float):  # single take profit
            take_profit = float(_tp)
        else:
            raise ValueError(f"Unknown take profit input, '{_tp}' (type: "
                             f"{type(_tp).__name__}), please use either "
                             f"float or dict (for checkpoint).")
        params["take_profit"] = take_profit

    # check for params that allow None value
    if "checkpoint_close_position" in kwargs:
        params["checkpoint_close_position"] = to_float(kwargs["checkpoint_close_position"])
    if "stop_loss" in kwargs:
        params["stop_loss"] = to_float(kwargs["stop_loss"])
    if "trailing_deviation" in kwargs:
        params["trailing_deviation"] = to_float(kwargs["trailing_deviation"])
    if "timeout_sec" in kwargs:
        params["timeout_sec"] = to_int(kwargs["timeout_sec"])

    # check for params that does NOT allow None value
    if kwargs.get("max_safety_order_count") is not None:
        params["max_safety_order_count"] = int(kwargs["max_safety_order_count"])
    if kwargs.get("safety_deviation") is not None:
        params["safety_deviation"] = float(kwargs["safety_deviation"])
    if kwargs.get("safety_volume_scale") is not None:
        params["safety_volume_scale"] = float(kwargs["safety_volume_scale"])
    if kwargs.get("safety_step_scale") is not None:
        params["safety_step_scale"] = float(kwargs["safety_step_scale"])
    return params


def to_float(num: Any, is_allow_none: bool = True) -> Optional[float]:
    if num is None and is_allow_none: return None
    return float(num)


def to_int(num: Any, is_allow_none: bool = True) -> Optional[int]:
    if num is None and is_allow_none: return None
    return int(num)
