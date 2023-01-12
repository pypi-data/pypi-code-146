# SPDX-License-Identifier: MIT
# Copyright (c) 2023 David Lechner <david@lechnology.com>

from contextvars import ContextVar

from AVFoundation import (
    AVSpeechSynthesizer,
    AVSpeechUtterance,
    AVSpeechBoundaryImmediate,
    AVSpeechUtteranceDefaultSpeechRate,
)


speak_context = ContextVar[AVSpeechSynthesizer | None]("context", default=None)


def speak(text: str) -> None:
    synth = speak_context.get()

    if synth and synth.isSpeaking():
        synth.stopSpeakingAtBoundary_(AVSpeechBoundaryImmediate)

    # reusing the synth object doesn't seem to work
    # e.g. https://stackoverflow.com/q/19672814
    synth = AVSpeechSynthesizer.alloc().init()

    utterance = AVSpeechUtterance.speechUtteranceWithString_(text)
    utterance.setRate_(AVSpeechUtteranceDefaultSpeechRate / 3)

    synth.speakUtterance_(utterance)

    # have to keep reference to object for playback to continue
    speak_context.set(synth)
