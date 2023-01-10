from __future__ import annotations

from enum import Enum


class WhatIfAnalysisOption(Enum):
    """
    Specifies the What-If analysis option.
    Start = Start What-If analysis. by locking the Schedule so that other users will not be able to update the Schedule
    in other sessions.
    SaveAndContinue = Save the changes made on the Schedule to the database and continue What-If analysis. Save What-If
    changes and continue.
    SaveAndExit = Save What-If changes and exit to the database and exit the What-If analysis mode by releasing the the
    lock on the Schedule so that other users can modify the Schedule.
    CancelAndExit = Cancel What-If analysis by discarding the changes and exit.
    """
    Start = 'Start'
    SaveAndContinue = 'SaveAndContinue'
    SaveAndExit = 'SaveAndExit'
    CancelAndExit = 'CancelAndExit'
