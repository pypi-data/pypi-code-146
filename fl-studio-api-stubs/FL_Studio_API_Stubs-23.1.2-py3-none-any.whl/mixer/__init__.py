"""Mixer Module (FL Studio built-in)

Allows you to control and interact with the FL Studio Mixer, and with
effects tracks.

NOTES:
 * Mixer tracks are zero-indexed
"""


from .__selection import (
    trackNumber,
    setTrackNumber,
    isTrackSelected,
    selectTrack,
    selectAll,
    deselectAll,
)
from .__tracks import (
    getTrackName,
    setTrackName,
    getTrackColor,
    setTrackColor,
    isTrackArmed,
    armTrack,
    isTrackSolo,
    soloTrack,
    isTrackEnabled,
    isTrackAutomationEnabled,
    enableTrack,
    isTrackMuted,
    muteTrack,
    isTrackMuteLock,
    getTrackVolume,
    setTrackVolume,
    getTrackPan,
    setTrackPan,
    getTrackStereoSep,
    setTrackStereoSep,
    setRouteTo,
    getRouteSendActive,
    afterRoutingChanged,
    getTrackPeaks,
    getTrackRecordingFileName,
    linkTrackToChannel,
    getTrackDockSide,
    isTrackSlotsEnabled,
    enableTrackSlots,
    isTrackRevPolarity,
    revTrackPolarity,
    isTrackSwapChannels,
    swapTrackChannels,
    linkChannelToTrack,
)
from .__properties import (
    getTrackInfo,
    trackCount,
    getSongStepPos,
    getCurrentTempo,
    getRecPPS,
    getSongTickPos,
    getLastPeakVol,
)
from .__events import (
    getTrackPluginId,
    isTrackPluginValid,
    getEventValue,
    remoteFindEventValue,
    getEventIDName,
    getEventIDValueString,
    getAutoSmoothEventValue,
    automateEvent,
)


__all__ = [
    'trackNumber',
    'setTrackNumber',
    'isTrackSelected',
    'selectTrack',
    'selectAll',
    'deselectAll',
    'getTrackName',
    'setTrackName',
    'getTrackColor',
    'setTrackColor',
    'isTrackArmed',
    'armTrack',
    'isTrackSolo',
    'soloTrack',
    'isTrackEnabled',
    'isTrackAutomationEnabled',
    'enableTrack',
    'isTrackMuted',
    'muteTrack',
    'isTrackMuteLock',
    'getTrackVolume',
    'setTrackVolume',
    'getTrackPan',
    'setTrackPan',
    'getTrackStereoSep',
    'setTrackStereoSep',
    'setRouteTo',
    'getRouteSendActive',
    'afterRoutingChanged',
    'getTrackPeaks',
    'getTrackRecordingFileName',
    'linkTrackToChannel',
    'getTrackDockSide',
    'isTrackSlotsEnabled',
    'enableTrackSlots',
    'isTrackRevPolarity',
    'revTrackPolarity',
    'isTrackSwapChannels',
    'swapTrackChannels',
    'getTrackInfo',
    'trackCount',
    'getSongStepPos',
    'getCurrentTempo',
    'getRecPPS',
    'getSongTickPos',
    'getLastPeakVol',
    'getTrackPluginId',
    'isTrackPluginValid',
    'getEventValue',
    'remoteFindEventValue',
    'getEventIDName',
    'getEventIDValueString',
    'getAutoSmoothEventValue',
    'automateEvent',
    'linkChannelToTrack',
]
