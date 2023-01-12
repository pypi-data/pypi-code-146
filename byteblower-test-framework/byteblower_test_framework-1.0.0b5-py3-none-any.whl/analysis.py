"""Interfaces for traffic analysis."""
# TODO: For later:
# from ._analysis.analyseraggregator import (
#     HtmlAnalyserAggregator,
#     JsonAnalyserAggregator,
# )
from ._analysis.bufferanalyser import BufferAnalyser
# `FlowAnalyser` is not really needed, but is useful for type hinting:
from ._analysis.flow_analyser import FlowAnalyser  # noqa: F401
from ._analysis.framelossanalyser import FrameLossAnalyser, ImixLossAnalyser
from ._analysis.httpanalyser import HttpAnalyser
from ._analysis.latencyanalyser import (
    LatencyCDFFrameLossAnalyser,
    LatencyCDFImixLossAnalyser,
    LatencyFrameLossAnalyser,
    LatencyImixLossAnalyser,
)
from ._analysis.voiceanalyser import VoiceAnalyser

# Export the user interfaces.
#
# Outcomes:
# * Limits import on `from byteblower_test_framework.analysis import *`
# * Exposes the interfaces in the (Sphinx) documentation
#
# NOTE
#   Exporting imported variables does not introduce them in the (Sphinx) docs.
#   For example 'DEFAULT_LOSS_PERCENTAGE', ...
#   It does introduce their name and value in `help()` of this module though.
#
__all__ = (
    # `FrameBlastingFlow`-related analysers:
    FrameLossAnalyser.__name__,
    ImixLossAnalyser.__name__,
    LatencyFrameLossAnalyser.__name__,
    LatencyImixLossAnalyser.__name__,
    LatencyCDFFrameLossAnalyser.__name__,
    LatencyCDFImixLossAnalyser.__name__,
    VoiceAnalyser.__name__,
    # `TcpFlow`-related analysers:
    HttpAnalyser.__name__,
    BufferAnalyser.__name__,
)
