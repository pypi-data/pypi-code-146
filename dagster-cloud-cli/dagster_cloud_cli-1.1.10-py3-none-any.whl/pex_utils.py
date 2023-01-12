# Handles python executable (pex) specific flags and wraps pex_builder

import os
import tempfile
from pathlib import Path
from typing import Any, Dict

from typer import Option

from dagster_cloud_cli import ui
from dagster_cloud_cli.core import pex_builder

DEPLOY_PEX_OPTIONS = {
    "python_version": (
        str,
        Option(
            "3.8",
            "--python-version",
            help="Target Python version specified as 'major.minor'.",
        ),
    ),
    "deps_cache_from": (
        str,
        Option(
            None,
            "--deps-cache-from",
            help=(
                "Reuse cached dependencies for this tag, "
                "if the dependency names match the cached names."
            ),
        ),
    ),
    "deps_cache_to": (
        str,
        Option(
            None,
            "--deps-cache-to",
            help=(
                "Cache dependencies and annotate with this tag. "
                "Use this tag in --deps-cache-from to reuse dependencies."
            ),
            hidden=True,
        ),
    ),
    "base_image_tag": (
        str,
        Option(
            None,
            "--base-image-tag",
            help="Tag that selects a base image uploaded using upload-base-image",
        ),
    ),
}


def build_upload_pex(
    url: str, api_token: str, location: str, python_source_dir: Path, kwargs: Dict[str, Any]
) -> Dict[str, Any]:
    # build and upload the python executable, return the modified kwargs with pex_tag and image
    kwargs = kwargs.copy()

    # pex_builder uses env vars for url and api_token, so copy these over
    if "dagster.cloud" in url:
        org_url = url[: url.find("dagster.cloud")] + "dagster.cloud"  # remove deployment suffix
    else:
        org_url = url
    os.environ["DAGSTER_CLOUD_URL"] = org_url
    os.environ["DAGSTER_CLOUD_API_TOKEN"] = api_token

    if kwargs.get("base_image_tag"):
        if kwargs.get("image"):
            raise ui.error("Only one of --base-image-tag or --image can be specified.")
        os.environ["SERVERLESS_BASE_IMAGE_TAG"] = kwargs.pop("base_image_tag")

    python_version = pex_builder.util.parse_python_version(kwargs.pop("python_version", "3.8"))
    ui.print(
        f"Building Python executable for directory {python_source_dir.absolute()!s} for Python"
        f" {python_version}."
    )
    deps_cache_tags = pex_builder.deploy.DepsCacheTags(
        kwargs.pop("deps_cache_from", None), kwargs.pop("deps_cache_to", None)
    )
    with tempfile.TemporaryDirectory() as temp_folder:
        locations = [
            pex_builder.parse_workspace.Location(
                name=location,
                directory=str(python_source_dir),
                build_folder=temp_folder,
                location_file="",  # unused
            )
        ]
        builds = pex_builder.deploy.build_locations(
            locations,
            temp_folder,
            upload_pex=True,
            deps_cache_tags=deps_cache_tags,
            python_version=python_version,
            build_sdists=True,
        )
        build = builds[0]
        kwargs["pex_tag"] = build.pex_tag
        image = kwargs.get("image")
        if not image:
            kwargs["image"] = image = pex_builder.deploy.get_base_image_for(build)
        ui.print(f"Using docker image: {image}")

        paths = [
            filepath
            for filepath in [
                build.source_pex_path,
                build.deps_pex_path,
            ]
            if filepath is not None
        ]
        if not paths:
            raise ui.error("No built files for {build.location.name}.")
        if build.source_pex_path:
            ui.print(f"Built Python executable source: {os.path.basename(build.source_pex_path)}")
        if build.deps_pex_path:
            ui.print(
                f"Built Python executable dependencies: {os.path.basename(build.deps_pex_path)}"
            )
        elif build.published_deps_pex:
            ui.print(f"Reusing cached dependencies: {build.published_deps_pex}")
        ui.print("Uploading Python executable.")
        pex_builder.pex_registry.upload_files(paths)

        # if a --deps-cache-to cache_tag is specified, set or update the cached deps details
        if deps_cache_tags.deps_cache_to_tag:
            # could be either a newly built pex or an published pex name copied from another tag
            deps_pex_name = (
                os.path.basename(build.deps_pex_path)
                if build.deps_pex_path
                else build.published_deps_pex
            )
            if not deps_pex_name:
                raise ui.error(
                    "Failed to build or find the Python executable dependencies (deps.pex)."
                )
            if not build.dagster_version:
                raise ui.error("Dagster not found in project's dependencies.")

            pex_builder.pex_registry.set_cached_deps_details(
                build.deps_requirements.hash,
                deps_cache_tags.deps_cache_to_tag,
                deps_pex_name,
                dagster_version=build.dagster_version,
            )

    return kwargs
