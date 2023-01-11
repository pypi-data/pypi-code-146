#!/usr/bin/env python3
import sys
from pathlib import Path
from typing import Optional

from libcst.metadata import CodeRange
from pygls.lsp.methods import (
    COMPLETION,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_DID_OPEN,
)
from pygls.lsp.types import (
    CompletionList,
    CompletionParams,
    DidChangeTextDocumentParams,
    DidOpenTextDocumentParams,
    Position,
    Range,
    TextDocumentContentChangeEvent,
    TextDocumentIdentifier,
)
from pygls.server import LanguageServer
from pygls.workspace import Document

from .pool import PoolManager, TrytonInitException


def pool_error_manager(f):
    def wrapped(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        except TrytonInitException as e:
            self.show_message(f"Error initializing the pool: {e}")
            sys.exit(1)

    return wrapped


class TrytonServer(LanguageServer):
    def __init__(self) -> None:
        super().__init__("tryton-ls", "v0.1")
        self._pool_manager: PoolManager = PoolManager()
        self._last_complete_position: tuple[int, int] = (0, 0)
        self._last_completion: Optional[CompletionList] = None

    @pool_error_manager
    def generate_diagnostics(
        self, document: TextDocumentIdentifier, ranges: list[Range]
    ) -> None:
        self.show_message('Test')
        text_document = self.workspace.get_document(document.uri)
        source_data = text_document.source
        document_path = Path(text_document.path)
        diagnostics = self._pool_manager.generate_diagnostics(
            document_path,
            data=source_data,
            ranges=[
                CodeRange(
                    (range.start.line, range.start.character),
                    (range.end.line, range.end.character),
                )
                for range in ranges
            ],
        )
        self.publish_diagnostics(
            document.uri, [x.to_lsp_diagnostic() for x in diagnostics]
        )

    @pool_error_manager
    def generate_completions(
        self, document: TextDocumentIdentifier, position: Position
    ) -> CompletionList:
        text_document = self.workspace.get_document(document.uri)
        completion_data = self._get_completion_data(text_document, position)
        if completion_data["position"] == self._last_complete_position:
            return self._last_completion
        self._last_completion_position = completion_data["position"]
        document_path = Path(text_document.path)
        completions = self._pool_manager.generate_completions(
            document_path,
            data=completion_data["source"],
            line=position.line + 1,
            column=position.character,
        )
        self._last_completion = CompletionList(
            is_incomplete=False, items=completions
        )
        return self._last_completion

    @pool_error_manager
    def _get_completion_data(
        self, text_document: Document, position: Position
    ) -> dict:
        lines = [x[:-1] for x in text_document.lines]
        line_data = lines[position.line]
        col = position.character - 1
        if line_data[col] == ".":
            lines[position.line] = (
                line_data[: col + 1] + "a" + line_data[col + 1 :]
            )
            col += 1
        for i in range(col):
            if line_data[col - i] == ".":
                col = col - i + 1
                break
        return {
            "source": "\n".join(lines),
            "position": (position.line + 1, col),
        }


def run() -> None:
    tryton_server = TrytonServer()

    @tryton_server.feature(
        COMPLETION,  # CompletionOptions(trigger_characters=["."])
    )
    async def completions(
        params: Optional[CompletionParams] = None,
    ) -> CompletionList:
        """Returns completion items."""
        if not params:
            return
        return tryton_server.generate_completions(
            params.text_document, params.position
        )

    @tryton_server.feature(TEXT_DOCUMENT_DID_OPEN)
    async def did_open(
        ls: LanguageServer, params: DidOpenTextDocumentParams
    ) -> None:
        """Text document did open notification."""
        tryton_server.show_message('Test')
        tryton_server.generate_diagnostics(params.text_document, [])

    @tryton_server.feature(TEXT_DOCUMENT_DID_CHANGE)
    async def did_change(
        ls: LanguageServer, params: DidChangeTextDocumentParams
    ) -> None:
        """Text document did change notification."""
        ranges = []
        for content_change in params.content_changes:
            if (
                isinstance(content_change, TextDocumentContentChangeEvent)
                and content_change.range
            ):
                ranges.append(content_change.range)
        if ranges:
            tryton_server.generate_diagnostics(params.text_document, ranges)

    tryton_server.start_io()


if __name__ == "__main__":
    run()
