import asyncio
from datetime import timedelta
import os
import tempfile
from typing import List, Optional

import aiohttp
from rich.console import Console
from rich.progress import track

from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models import (
    LogDownloadConfig,
    LogDownloadRequest,
    LogDownloadResult,
    LogFileChunk,
    LogFilter,
)
from anyscale.controllers.base_controller import BaseController
from anyscale.utils.logs_utils import LogGroup


# Page size for listing bucket
DEFAULT_PAGE_SIZE = 1000

# Timeout for API Requests
DEFAULT_TIMEOUT = 30

# Timeout for Downloading Files
DEFAULT_READ_TIMEOUT = 30

DEFAULT_TTL = 14400
DEFAULT_PARALLELISM = 10


class LogsController(BaseController):
    def __init__(
        self, log: Optional[BlockLogger] = None, initialize_auth_api_client: bool = True
    ):
        if log is None:
            log = BlockLogger()

        super().__init__(initialize_auth_api_client=initialize_auth_api_client)
        self.log = log
        self.console = Console()

    def render_logs(
        self, log_group: LogGroup, parallelism: int, read_timeout: timedelta, tail: int
    ):
        self._download_or_stdout(
            log_group=log_group,
            parallelism=parallelism,
            read_timeout=read_timeout,
            write_to_stdout=True,
            tail=tail,
            show_progress_bar=False,
        )

    def get_logs_for_tail(
        self,
        filter: LogFilter,  # noqa: A002
        page_size: Optional[int],
        ttl_seconds: Optional[int],
        timeout: timedelta,
    ):
        chunks = self._list_log_chunks(
            log_filter=filter,
            page_size=page_size,
            ttl_seconds=ttl_seconds,
            timeout=timeout,
        )
        groups = self._group_log_chunk_list(chunks=chunks)
        return groups

    def download_logs(
        self,
        # Provide filters
        filter: LogFilter,  # noqa: A002
        # List files config
        page_size: int = DEFAULT_PAGE_SIZE,
        ttl_seconds: int = DEFAULT_TTL,
        timeout: timedelta = timedelta(seconds=DEFAULT_TIMEOUT),
        read_timeout: timedelta = timedelta(seconds=DEFAULT_READ_TIMEOUT),
        # Download config
        parallelism: int = DEFAULT_PARALLELISM,
        download_dir: Optional[str] = None,
        write_to_stdout: bool = False,
    ):
        log_chunks: List[LogFileChunk] = self._list_log_chunks(
            log_filter=filter,
            page_size=page_size,
            ttl_seconds=ttl_seconds,
            timeout=timeout,
        )
        log_group: LogGroup = self._group_log_chunk_list(log_chunks)
        self.console.log(
            f"Discovered {len(log_group.get_files())} log files across {len(log_group.get_chunks())} chunks."
        )

        self._download_or_stdout(
            download_dir=download_dir,
            read_timeout=read_timeout,
            parallelism=parallelism,
            log_group=log_group,
            show_progress_bar=True,
            write_to_stdout=write_to_stdout,
        )

    # TODO (shomilj): Refactor this method. It's too nested.
    def _download_or_stdout(
        self,
        log_group: LogGroup,
        parallelism: int,
        read_timeout: timedelta,
        download_dir: Optional[str] = None,
        write_to_stdout: bool = False,
        tail: int = -1,
        show_progress_bar: bool = False,
    ):
        if len(log_group.get_chunks()) == 0:
            return

        with tempfile.TemporaryDirectory() as tmp_dir:
            # Download all files to a temporary directory.
            asyncio.run(
                # TODO (shomilj): Add efficient tailing method here.
                self._download_files(
                    base_folder=tmp_dir,
                    log_chunks=log_group.get_chunks(),
                    parallelism=parallelism,
                    read_timeout=read_timeout,
                    show_progress_bar=show_progress_bar,
                )
            )

            for log_file in log_group.get_files():
                is_tail = tail > 0
                chunks = log_file.get_chunks(reverse=is_tail)
                if write_to_stdout:
                    # Write to standard out
                    lines_read = 0
                    for chunk in chunks:
                        with open(os.path.join(tmp_dir, chunk.chunk_name)) as source:
                            if tail > 0:
                                # Tail is enabled, so read log lines in reverse.
                                # TODO (shomilj): Make this more efficient (don't read everything into memory before reversing it)
                                # For now, this is fine (the chunks are <10 MB, so this isn't that inefficient).
                                for line in reversed(source.readlines()):
                                    print(line.strip())
                                    lines_read += 1
                                    if lines_read >= tail:
                                        return
                            else:
                                # Read log lines normally.
                                print(source.read())
                else:
                    # Write to destination files
                    real_path = os.path.join(
                        download_dir or "", log_file.get_target_path()
                    )
                    real_dir = os.path.dirname(real_path)
                    if not os.path.exists(real_dir):
                        os.makedirs(real_dir)

                    chunks_written = 0
                    with open(real_path, "w") as dest:
                        for chunk in chunks:
                            downloaded_chunk_path = os.path.join(
                                tmp_dir, chunk.chunk_name
                            )
                            if not os.path.exists(downloaded_chunk_path):
                                self.log.error(
                                    "Download failed for file: ", chunk.chunk_name
                                )
                                continue
                            with open(downloaded_chunk_path, errors="ignore") as source:
                                for line in source:
                                    dest.write(line)
                                dest.write("\n")
                            chunks_written += 1

                    if chunks_written == 0:
                        os.remove(real_path)

            if not write_to_stdout:
                if not download_dir:
                    download_dir = os.getcwd()
                sample_chunk = log_group.get_chunks()[0]
                cluster_id = sample_chunk.cluster_id
                download_dir = download_dir + f"/logs/{cluster_id}"
                self.console.log(
                    f"Download complete! Files have been downloaded to {download_dir}"
                )

    def _group_log_chunk_list(self, chunks: List[LogFileChunk]) -> LogGroup:
        # This has to happen locally because it happens after we retrieve all file metadata through the paginated
        # backend API for listing S3/GCS buckets.
        group = LogGroup()
        for chunk in chunks:
            group.insert_chunk(chunk=chunk)
        return group

    def _list_log_chunks(
        self,
        log_filter: LogFilter,
        page_size: Optional[int],
        ttl_seconds: Optional[int],
        timeout: timedelta,
    ) -> List[LogFileChunk]:
        next_page_token: Optional[str] = None
        all_log_chunks: List[LogFileChunk] = []

        with self.console.status("Scanning available logs...") as status:
            while True:
                request = LogDownloadRequest(
                    filter=log_filter,
                    config=LogDownloadConfig(
                        next_page_token=next_page_token,
                        page_size=page_size,
                        ttl_seconds=ttl_seconds,
                    ),
                )
                result: LogDownloadResult = self.api_client.get_log_files_api_v2_logs_get_log_files_post(
                    log_download_request=request, _request_timeout=timeout
                ).result
                all_log_chunks.extend(result.log_chunks)
                if status:
                    status.update(
                        f"Scanning available logs...discovered {len(all_log_chunks)} log file chunks."
                    )
                if (
                    result.next_page_token is None
                    or result.next_page_token == next_page_token
                ):
                    break
                next_page_token = result.next_page_token

        return all_log_chunks

    async def _download_file(
        self,
        sem: asyncio.Semaphore,
        pos: int,  # noqa: ARG002
        file_name: str,
        url: str,
        size: int,  # noqa: ARG002
        session: aiohttp.ClientSession,
        read_timeout: timedelta,
    ) -> None:
        async with sem:
            download_dir = os.path.dirname(file_name)
            if download_dir and not os.path.exists(download_dir):
                os.makedirs(download_dir)

            timeout = aiohttp.ClientTimeout(
                total=None, sock_connect=30, sock_read=read_timeout.seconds
            )
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    with open(file_name, "wb") as fhand:
                        async for chunk in response.content.iter_chunked(1024):
                            fhand.write(chunk)
                else:
                    self.log.error(
                        f"Unable to download file {file_name}! response: [{response.status}, {await response.text()}]"
                    )

    async def _download_files(
        self,
        base_folder: Optional[str],
        log_chunks: List[LogFileChunk],
        parallelism: int,
        read_timeout: timedelta,
        show_progress_bar: bool = False,
    ) -> List[str]:
        sem = asyncio.Semaphore(parallelism)
        downloads = []
        connector = aiohttp.TCPConnector(limit_per_host=parallelism)
        paths = []
        async with aiohttp.ClientSession(connector=connector) as session:
            for pos, log_chunk in enumerate(log_chunks):
                path = os.path.join(base_folder or "", log_chunk.chunk_name.lstrip("/"))
                paths.append(path)
                downloads.append(
                    asyncio.create_task(
                        self._download_file(
                            sem,
                            pos,
                            path,
                            log_chunk.chunk_url,
                            log_chunk.size,
                            session,
                            read_timeout,
                        )
                    )
                )

            if show_progress_bar:
                for task in track(
                    asyncio.as_completed(downloads),
                    description="Downloading...",
                    total=len(downloads),
                    transient=True,
                ):
                    await task
            else:
                await asyncio.gather(*downloads)

        return paths
