import logging
from pathlib import Path
from typing import Optional

import daiquiri
import typer
import yaml  # type: ignore
from pptx import Presentation as open_presentation
from pptx.presentation import Presentation
from typer import FileBinaryRead, FileBinaryWrite, Typer

from dbnomics_pptx_tools.cache import SeriesCache
from dbnomics_pptx_tools.metadata import PresentationMetadata
from dbnomics_pptx_tools.module_utils import load_python_module_from_path
from dbnomics_pptx_tools.repo import SeriesLoadError, SeriesRepo
from dbnomics_pptx_tools.slides import delete_other_slides, update_slides

app = Typer()

logger = daiquiri.getLogger(__name__)


DBNOMICS_API_CACHE_DIR_NAME = "dbnomics_api_cache"


@app.callback(context_settings={"help_option_names": ["-h", "--help"]})
def main(verbose: bool = typer.Option(False, "-v")):
    """
    DBnomics PowerPoint (pptx) tools.
    """
    daiquiri.setup()
    if verbose:
        daiquiri.set_default_log_levels([(__package__, logging.DEBUG)])


def parse_range(value: str) -> set[int]:
    """Parse ranges like "1-10,3,4,23-47"."""
    result: set[int] = set()
    for part in value.split(","):
        x = part.split("-")
        result.update(range(int(x[0]), int(x[-1]) + 1))
    return result


def parse_range_option(expr: str) -> set[int]:
    try:
        return parse_range(expr)
    except Exception:
        raise typer.BadParameter(f"Could not parse range: {expr}")


@app.command()
def fetch(
    metadata_file: Path = typer.Argument(..., exists=True, readable=True),
    dbnomics_api_cache_dir: Path = typer.Option(DBNOMICS_API_CACHE_DIR_NAME),
    skip_existing: bool = typer.Option(False, help="Do not fetch the series that are already stored in the cache."),
):
    presentation_metadata = load_presentation_metadata(metadata_file)
    series_ids = sorted(presentation_metadata.get_slide_series_ids())

    cache = SeriesCache(cache_dir=dbnomics_api_cache_dir)
    repo = SeriesRepo(auto_fetch=True, cache=cache, force=not skip_existing)

    logger.debug("Fetching all the series needed for the presentation: %r...", series_ids)

    fetched_series_ids = []
    skipped_series_ids = []
    for series_id in series_ids:
        if cache.has(series_id) and skip_existing:
            logger.debug("Series %r is already stored in the cache, skipping it", series_id)
            skipped_series_ids.append(series_id)
            continue
        repo.load(series_id)
        fetched_series_ids.append(series_id)

    logger.info(
        "Fetched %d series from DBnomics API, skipped %d series that were already stored in the cache",
        len(fetched_series_ids),
        len(skipped_series_ids),
    )


@app.command()
def update(
    input_pptx_file: FileBinaryRead,
    output_pptx_file: FileBinaryWrite,
    adhoc_module_path: Optional[Path] = typer.Option(
        None, "--adhoc-module", exists=True, readable=True, dir_okay=False
    ),
    auto_fetch: bool = typer.Option(
        True, help="Fetch series when it is not found in the cache, then add it to the cache."
    ),
    dbnomics_api_cache_dir: Path = typer.Option(DBNOMICS_API_CACHE_DIR_NAME),
    force: bool = typer.Option(False, help="Fetch a series even if it is already stored in the cache."),
    metadata_file: Optional[Path] = typer.Option(None, exists=True, readable=True),
    only_slides_expr: Optional[str] = typer.Option(None, "--slides"),
    save_processed_slides_only: bool = False,
):
    """
    Update DBnomics data in a PowerPoint (pptx) presentation.
    """
    only_slides = None
    if only_slides_expr is not None:
        logger.debug("Will process slides %s", only_slides_expr)
        only_slides = parse_range_option(only_slides_expr)

    if save_processed_slides_only and only_slides is None:
        raise typer.BadParameter("--save-processed-slides-only must be used with --slides")

    logger.debug("Loading presentation from %r...", str(input_pptx_file.name))
    prs: Presentation = open_presentation(input_pptx_file)

    if metadata_file is None:
        metadata_file = Path(input_pptx_file.name).with_suffix(".yaml")
        logger.debug(
            "Metadata file not passed as an option, using file named after the presentation, with '.yaml' suffix"
        )

    presentation_metadata = load_presentation_metadata(metadata_file)

    adhoc_module = (
        load_python_module_from_path(adhoc_module_path, module_name="dbnomics_pptx_tools.adhoc")
        if adhoc_module_path is not None
        else None
    )

    cache = SeriesCache(cache_dir=dbnomics_api_cache_dir)
    repo = SeriesRepo(auto_fetch=auto_fetch, cache=cache, force=force)

    try:
        update_slides(
            prs,
            adhoc_module=adhoc_module,
            only_slides=only_slides,
            presentation_metadata=presentation_metadata,
            repo=repo,
        )
    except SeriesLoadError as exc:
        typer.echo(f'{str(exc)} Hint: use the --auto-fetch option or run the "fetch" command first.')
        raise typer.Exit(1)

    if save_processed_slides_only:
        assert only_slides is not None
        delete_other_slides(prs, only_slides=only_slides)

    prs.save(output_pptx_file)
    logger.info("Output presentation was saved as %r", str(output_pptx_file.name))


def load_presentation_metadata(metadata_file: Path) -> PresentationMetadata:
    logger.debug("Loading presentation metadata from %r...", str(metadata_file))
    presentation_metadata_data = yaml.safe_load(metadata_file.read_text())
    return PresentationMetadata.parse_obj(presentation_metadata_data)


if __name__ == "__main__":
    app()
