# SPDX-License-Identifier: MIT
# Copyright (c) 2023 David Lechner <david@lechnology.com>

from ctypes import WinError
from contextvars import ContextVar
from typing import TypeVar

from concurrent.futures import Future
from winsdk.windows.foundation import IAsyncOperation, AsyncStatus
from winsdk.windows.media.speechsynthesis import SpeechSynthesizer
from winsdk.windows.media.playback import MediaPlayer


T = TypeVar("T")
P = TypeVar("P")

speak_context = ContextVar(__name__, default=(SpeechSynthesizer(), MediaPlayer()))


def sync(op: IAsyncOperation[T]) -> T:
    """
    Calls a WinRT async method synchronously.
    """
    future = Future[T]()

    def handle_complete(op: IAsyncOperation[T], status: AsyncStatus):
        match status:
            case AsyncStatus.COMPLETED:
                future.set_result(op.get_results())
            case AsyncStatus.ERROR:
                future.set_exception(WinError(op.error_code.value))
            case AsyncStatus.CANCELED:
                future.cancel()

    op.completed = handle_complete
    future.set_running_or_notify_cancel()

    return future.result()


def speak(text: str) -> None:
    synth, media_player = speak_context.get()

    stream = sync(synth.synthesize_text_to_stream_async(text))
    media_player.set_stream_source(stream)
    media_player.play()
