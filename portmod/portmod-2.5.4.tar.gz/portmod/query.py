# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Module for performing bulk queries on the mod database and repositories
"""

import logging
import multiprocessing
import os
import re
import shutil
import sys
from collections import defaultdict
from logging import info
from multiprocessing import Process
from time import sleep
from typing import (
    AbstractSet,
    DefaultDict,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
)

from progressbar import AnimatedMarker, ProgressBar, UnknownLength, Variable

from portmodlib.atom import Atom, FQAtom, QualifiedAtom, atom_sat
from portmodlib.colour import blue, bright, cyan, green, lblue, lgreen, red, yellow
from portmodlib.l10n import l10n
from portmodlib.portmod import Group, PackageIndexData, Person
from portmodlib.portmod import query as native_query
from portmodlib.portmod import update_index as native_update_index
from portmodlib.usestr import parse_usestr

from .config import get_config
from .config.mask import is_masked
from .config.use import get_use, get_use_expand, use_reduce
from .download import get_total_download_size
from .globals import env
from .loader import load_all, load_all_installed, load_installed_pkg, load_pkg
from .prefix import get_prefixes
from .pybuild import Pybuild
from .repo import get_repo
from .repo.metadata import get_global_use
from .repo.metadata import get_package_metadata as get_native_metadata
from .repo.metadata import get_use_expand_values

Maintainer = Union[Group, Person]
Maintainers = Union[Maintainer, List[Maintainer]]


def get_maintainer_strings(maintainers: Maintainers) -> List[str]:
    if not isinstance(maintainers, list):
        maintainers = [maintainers]
    return [str(maintainer) for maintainer in maintainers]


def get_maintainer_string(maintainers: Maintainers) -> str:
    return list_maintainers_to_human_strings(get_maintainer_strings(maintainers))


def list_maintainers_to_human_strings(maintainers: List[str]) -> str:
    """return the list of maintainers as a human readible string"""
    result = ""
    for maintainer_id in range(len(maintainers)):
        maintainer = maintainers[maintainer_id]
        if maintainer_id >= len(maintainers) - 1:  # the last
            result += maintainer
        elif maintainer_id >= len(maintainers) - 2:  # the second last
            result += maintainer + " and "
        else:
            result += maintainer + ", "
    return result


def print_depgraph(
    mod: Pybuild, level: int, level_limit: int, seen: Set[Pybuild]
) -> int:
    """
    Recursively prints the dependency graph for the given mod.

    Note that use conditionals and or statements are ignored.
    This prints out all possible dependencies, not actual dependencies.
    """
    if level > level_limit:
        return level - 1

    deps = parse_usestr(mod.DEPEND + " " + mod.RDEPEND, token_class=Atom)

    if mod in seen and deps:
        print(" " * (level + 2) + "-- " + l10n("omit-already-displayed-tree"))
        return level - 1
    max_level = level

    if isinstance(seen, frozenset):
        seen = set()
    seen.add(mod)

    def print_token(token, conditionals=None):
        atom = Atom(token)
        mod = max(load_pkg(atom), key=lambda pkg: pkg.version)
        enabled, _ = get_use(mod)

        def colour(flag):
            if flag.rstrip("?").lstrip("-!") in enabled:
                return bright(red(flag))
            return bright(blue(flag))

        use = map(colour, atom.USE)
        use_str = ""
        if atom.USE:
            use_str = f'[{" ".join(use)}]'

        if conditionals:
            dep = f"( {' '.join(conditionals)} ( {atom.strip_use()} ) ) "
        else:
            dep = f"({atom.strip_use()}) "

        print(" " * (level + 1) + f"-- {bright(green(mod.ATOM.CPF))} " + dep + use_str)
        return print_depgraph(mod, level + 1, level_limit, seen)

    def print_deps(deps, conditionals: List):
        nonlocal max_level
        if isinstance(deps, list):
            if not deps:
                return
            if isinstance(deps[0], str) and deps[0] == "||":
                for inner_token in deps[1:]:
                    print_deps(inner_token, conditionals)
            elif isinstance(deps[0], str) and deps[0].endswith("?"):
                for inner_token in deps[1:]:
                    print_deps(inner_token, conditionals + [deps[0]])
            else:
                for inner_token in deps:
                    print_deps(inner_token, conditionals)
        else:
            max_level = max(max_level, print_token(deps, conditionals))

    print_deps(deps, [])

    return max_level


def str_strip(value: str) -> str:
    return re.sub("(( +- +)|(:))", "", value)


def str_squelch_sep(value: str) -> str:
    return re.sub(r"[-_\s]+", " ", value)


def query(
    value: str,
    limit: int = 10,
) -> List[PackageIndexData]:
    """
    Finds mods that contain the given value in the given field
    """
    if not env.PREFIX_NAME:
        raise RuntimeError("Queries must be done inside a prefix!")
    return native_query(env.INDEX, env.PREFIX_NAME, value, limit)


# FIXME: For this to be indexed, we'll need to add DEPEND and RDEPEND to the index
# This also means indexing individual package versions as well as aggregated data
def query_depends(atom: Atom, all_mods=False) -> List[Tuple[FQAtom, str]]:
    """
    Finds mods that depend on the given atom
    """
    if all_mods:
        mods = load_all()
    else:
        mods = load_all_installed()

    depends = []
    for mod in mods:
        if not all_mods:
            enabled, disabled = get_use(mod)
            atoms = use_reduce(
                mod.RDEPEND + " " + mod.DEPEND,
                enabled,
                disabled,
                token_class=Atom,
                flat=True,
            )
        else:
            atoms = use_reduce(
                mod.RDEPEND + " " + mod.DEPEND,
                token_class=Atom,
                matchall=True,
                flat=True,
            )

        for dep_atom in atoms:
            if dep_atom != "||" and atom_sat(dep_atom, atom):
                depends.append((mod.ATOM, dep_atom))
    return depends


def get_flag_string(
    name: Optional[str],
    enabled: Iterable[str],
    disabled: Iterable[str],
    installed: Optional[AbstractSet[str]] = None,
    *,
    verbose: bool = True,
    display_minuses=True,
):
    """
    Displays flag configuration

    Enabled flags are displayed as blue
    If the installed flag list is passed, flags that differ from the
    installed set will be green
    if name is None, the name prefix will be omitted and no quotes will
    surround the flags
    """

    def disable(string: str) -> str:
        if display_minuses:
            return "-" + string
        return string

    flags = []
    for flag in sorted(enabled):
        if installed is not None and flag not in installed:
            flags.append(bright(lgreen(flag)))
        elif verbose:
            flags.append(red(bright(flag)))

    for flag in sorted(disabled):
        if installed is not None and flag in installed:
            flags.append(bright(lgreen(disable(flag))))
        elif verbose:
            if display_minuses:
                flags.append(blue(disable(flag)))
            else:
                flags.append(lblue(disable(flag)))

    inner = " ".join(flags)

    if not flags:
        return None

    if name:
        return f'{name}="{inner}"'

    return inner


def display_search_results(
    packages: Sequence[PackageIndexData],
    summarize: bool = True,
    numbers: bool = False,
    file=sys.stdout,
):
    """
    Prettily formats a list of package metadata for use in search results
    """
    count = 0

    footnotes: Dict[str, str] = {}
    footnotenum = "a"

    def footnote(repo: str):
        nonlocal footnotenum
        if repo not in footnotes:
            footnotes[repo] = str(footnotenum)
            footnotenum = chr(ord(footnotenum) + 1)
        return lblue(f"[{footnotes[repo]}]")

    for package in packages:
        count += 1
        group = load_pkg(Atom(package.cpn))
        sortedmods = sorted(group, key=lambda pkg: pkg.version)
        newest = sortedmods[-1]
        installed = load_installed_pkg(Atom(package.cpn))
        download = get_total_download_size([newest])

        if installed is not None:
            installed_str = blue(bright(installed.PVR)) + footnote(installed.REPO)

            flags = {flag.lstrip("+") for flag in installed.IUSE if "_" not in flag}
            usestr = get_flag_string(
                None, installed.INSTALLED_USE & flags, flags - installed.INSTALLED_USE
            )
            texture_options = {
                size
                for mod in group
                for size in use_reduce(
                    installed.TEXTURE_SIZES, matchall=True, flat=True
                )
            }
            texture = next(
                (
                    use.lstrip("texture_size_")
                    for use in installed.INSTALLED_USE
                    if use.startswith("texture_size_")
                ),
                None,
            )
            if isinstance(texture, str):
                texture_string = get_flag_string(
                    "TEXTURE_SIZE", [texture], texture_options - {texture}
                )
            else:
                texture_string = None
            use_expand_strings = []
            for use in get_config().get("USE_EXPAND", []):
                if use in get_config().get("USE_EXPAND_HIDDEN", []):
                    continue
                enabled_expand, disabled_expand = get_use_expand(installed, use)
                if enabled_expand or disabled_expand:
                    string = get_flag_string(use, enabled_expand, disabled_expand, None)
                    use_expand_strings.append(string)

            all_flags: List[str] = list(
                filter(None, [usestr, texture_string] + use_expand_strings)
            )
            if all_flags:
                installed_str += " {" + " ".join(all_flags) + "}"
        else:
            installed_str = "not installed"

        # List of version numbers, prefixed by either (~) or ** depending on
        # keyword for user's arch. Followed by use flags, including use expand
        version_str = ""
        versions = []
        ARCH = env.prefix().ARCH
        for mod in sortedmods:
            if mod.INSTALLED:
                continue

            if ARCH in mod.KEYWORDS:
                version_nofmt = mod.PVR
                version = green(mod.PVR)
            elif "~" + ARCH in mod.KEYWORDS:
                version_nofmt = "(~)" + mod.PVR
                version = yellow(version_nofmt)
            else:
                version_nofmt = "**" + mod.PVR
                version = red(version_nofmt)

            repo = mod.REPO

            if is_masked(mod.ATOM, mod.REPO):
                versions.append(red("[M]" + version_nofmt) + footnote(repo))
            else:
                versions.append(version + footnote(repo))
        version_str = " ".join(versions)
        flags = {
            flag.lstrip("+") for mod in group for flag in mod.IUSE if "_" not in flag
        }
        usestr = get_flag_string(None, [], flags, display_minuses=False)
        texture_options = {
            size
            for mod in group
            for size in use_reduce(mod.TEXTURE_SIZES, matchall=True, flat=True)
        }
        texture_string = get_flag_string(
            "TEXTURE_SIZE", [], texture_options, display_minuses=False
        )
        use_expand_strings = []
        for use in get_config().get("USE_EXPAND", []):
            if use in get_config().get("USE_EXPAND_HIDDEN", []):
                continue
            flags = {
                re.sub(f"^{use.lower()}_", "", flag)
                for flag in mod.IUSE_EFFECTIVE
                for mod in group
                if flag.startswith(f"{use.lower()}_")
            }
            if flags:
                string = get_flag_string(use, [], flags, None, display_minuses=False)
                use_expand_strings.append(string)

        all_flags = list(filter(None, [usestr, texture_string] + use_expand_strings))
        if all_flags:
            version_str += " {" + " ".join(all_flags) + "}"

        # If there are multiple URLs, remove any formatting from the pybuild and
        # add padding

        if logging.root.level <= logging.DEBUG:
            if package.homepage:
                formatted_homepages = "\n                 ".join(
                    [package.homepage] + package.other_homepages
                )

                homepage_str = (
                    f"       {green(l10n('package-homepage'))} {formatted_homepages}"
                )
            print(
                f"{cyan(count) if numbers else ''} {green('*')}  {bright(package.cpn)}",
                f"       {green(l10n('package-name'))} {package.name}",
                f"       {green(l10n('package-available-versions'))} {version_str}",
                f"       {green(l10n('package-installed-version'))} {installed_str}",
                f"       {green(l10n('package-size-of-files'))} {download}",
                sep=os.linesep,
                file=file,
            )
            if package.homepage:
                print(homepage_str, file=file)
            print(
                f"       {green(l10n('package-description'))} {str_squelch_sep(newest.DESC)}",
                f"       {green(l10n('package-license'))} {newest.LICENSE}",
                sep=os.linesep,
                file=file,
            )
            if package.upstream_maintainers:
                print(
                    f"       {green(l10n('package-upstream-author'))} {list_maintainers_to_human_strings(package.upstream_maintainers)}",
                    file=file,
                )
            print(file=file)
        else:
            print(
                f"{cyan(count) if numbers else ''} {green('*')}  {bright(package.cpn)}",
                f"       {green(l10n('package-available-versions'))} {version_str}",
                f"       {green(l10n('package-installed-version'))} {installed_str}",
                sep=os.linesep,
                file=file,
            )
            if package.homepage:
                print(
                    f"       {green(l10n('package-homepage'))} {package.homepage}",
                    file=file,
                )
            print(
                f"       {green(l10n('package-description'))} {str_squelch_sep(newest.DESC)}",
                sep=os.linesep,
                file=file,
            )

    if footnotes:
        print()
        for repo in footnotes:
            print(footnote(repo), f'"{repo}"', get_repo(repo).location)

    if summarize:
        print("\n" + l10n("packages-found", num=len(packages)), file=file)


class FlagDesc:
    """Use flag descriptions"""

    def __init__(self, desc: str):
        self.desc = desc

    def __str__(self):
        return self.desc


class LocalFlagDesc(FlagDesc):
    """Local use flag description"""

    def __init__(self, pkg: Pybuild, desc: str):
        super().__init__(desc)
        self.pkg = pkg

    def __repr__(self):
        return f"LocalDesc({self.pkg}, {self.desc})"


class UseExpandDesc(FlagDesc):
    """Local use flag description"""

    def __init__(self, category: str, flag: str, desc: str):
        super().__init__(desc)
        self.flag = flag
        self.category = category

    def __repr__(self):
        return f"UseExpandDesc({self.category}, {self.desc})"


def get_flag_desc(pkg: Pybuild, flag: str) -> Optional[FlagDesc]:
    """Returns the description for the given use flag"""
    repo_root = get_repo(pkg.REPO).location

    global_use = get_global_use(repo_root)
    metadata = get_native_metadata(pkg)

    if metadata and flag in metadata.use:
        return LocalFlagDesc(pkg, metadata.use[flag])
    if flag in global_use:
        return FlagDesc(global_use[flag])
    if flag.startswith("texture_size_"):
        size = flag.replace("texture_size_", "")
        return UseExpandDesc("texture_size", size, l10n("texture-size-desc", size=size))
    if "_" in flag:  # USE_EXPAND
        use_expand = flag.rsplit("_", 1)[0]
        suffix = flag.replace(use_expand + "_", "")
        use_expand_desc = get_use_expand_values(repo_root, use_expand).get(suffix)
        if use_expand_desc:
            return UseExpandDesc(use_expand, suffix, use_expand_desc)

    return None


def get_flags(
    pkg: Pybuild,
) -> Tuple[Dict[str, str], Dict[str, str], Dict[str, Dict[str, str]]]:
    """
    Returns all use flags and their descriptions for the given package

    returns:
        Three dictionaries, one each for local flags, global flags and use_expand flags,
        in that order. The use expand flags are subdivided for each use_expand category.
    """
    repo_root = get_repo(pkg.REPO).location

    global_use = get_global_use(repo_root)
    metadata = get_native_metadata(pkg)

    local_flags = {}
    global_flags = {}
    use_expand_flags: DefaultDict[str, Dict[str, str]] = defaultdict(dict)

    for flag in pkg.IUSE_EFFECTIVE:
        if metadata and flag in metadata.use:
            local_flags[flag] = metadata.use[flag]
        elif flag in global_use:
            global_flags[flag] = global_use[flag]
        elif flag.startswith("texture_size_"):
            size = flag.replace("texture_size_", "")
            desc = l10n("texture-size-desc", size=size)
            use_expand_flags["texture_size"][size] = desc
        elif "_" in flag:  # USE_EXPAND
            use_expand = flag.rsplit("_", 1)[0]
            suffix = flag.replace(use_expand + "_", "")
            use_expand_desc = get_use_expand_values(repo_root, use_expand).get(suffix)
            if use_expand_desc:
                use_expand_flags[use_expand][suffix] = use_expand_desc
        else:
            # No description Found.
            # Might be an installed package without metadata.yaml
            continue

    return local_flags, global_flags, use_expand_flags


def get_package_metadata(package: QualifiedAtom) -> Optional[PackageIndexData]:
    packages = load_pkg(package)
    if not packages:
        return None

    pkgs = sorted(packages, key=lambda x: x.ATOM.version)
    newest = pkgs[-1]

    assert env.PREFIX_NAME, "A prefix must be specified"

    pkg_metadata = PackageIndexData(
        cpn=package.CPN,
        prefix=env.PREFIX_NAME,
        category=package.C,
        package=package.PN,
        name=newest.NAME,
        desc=newest.DESC,
    )

    homepages = use_reduce(newest.HOMEPAGE, matchall=True, flat=True)

    if homepages:
        pkg_metadata.homepage = homepages[0]
    if len(homepages) > 1:
        pkg_metadata.other_homepages = homepages[1:]

    if newest.LICENSE:
        pkg_metadata.license = newest.LICENSE

    for pkg in pkgs:
        metadata = get_native_metadata(pkg)
        if metadata:
            pkg_metadata.tags |= metadata.tags
            if metadata.longdescription:
                pkg_metadata.longdescription = metadata.longdescription
            if metadata.maintainer:
                pkg_metadata.maintainers = get_maintainer_strings(metadata.maintainer)
            if metadata.upstream:
                if metadata.upstream.maintainer:
                    pkg_metadata.upstream_maintainers = get_maintainer_strings(
                        metadata.upstream.maintainer
                    )
                if metadata.upstream.doc:
                    pkg_metadata.upstream_doc = metadata.upstream.doc
                if metadata.upstream.bugs_to:
                    pkg_metadata.upstream_bugs_to = metadata.upstream.bugs_to
                if metadata.upstream.changelog:
                    pkg_metadata.upstream_changelog = metadata.upstream.changelog

    return pkg_metadata


def _get_index_data() -> List[PackageIndexData]:
    if not env.PREFIX_NAME:
        return []

    def get_package_names():
        seen = set()
        for pkg in load_all():
            if pkg.CPN not in seen:
                seen.add(pkg.CPN)
                yield pkg.CPN
        for pkg in load_all_installed():
            if pkg.CPN not in seen:
                seen.add(pkg.CPN)
                yield pkg.CPN

    info("Beginning index update for prefix " + env.PREFIX_NAME)
    if sys.stderr.isatty() or env.TESTING:
        try:
            from progressbar import GranularBar as Bar
        except ImportError:
            from progressbar import Bar
        from progressbar import ETA, BouncingBar, Counter, ProgressBar, Timer, Variable

        package_names = set()
        bar = ProgressBar(
            redirect_stdout=True,
            widgets=[
                Variable("status", format="Collecting packages"),
                BouncingBar(),
                Counter(),
                " ",
                Timer(),
            ],
        )

        i = 0
        bar.start()
        for name in get_package_names():
            package_names.add(name)
            bar.update(i)
            i += 1
        bar.finish()

        package_data = []
        bar = ProgressBar(
            redirect_stdout=True,
            widgets=[
                Variable("status", format="Loading package data"),
                Bar(),
                Counter(),
                " ",
                ETA(),
            ],
            max_value=len(package_names),
        )
        bar.start()
        i = 0
        for cpn in package_names:
            metadata = get_package_metadata(cpn)
            if metadata:
                package_data.append(metadata)
            bar.update(i)
            i += 1
        bar.finish()
    else:
        package_data = []
        for name in get_package_names():
            metadata = get_package_metadata(name)
            if metadata:
                package_data.append(metadata)
    return package_data


def _run_progress_bar(pipe):
    bar = ProgressBar(
        widgets=[
            Variable("status", format="{variables.status}"),
            " ",
            AnimatedMarker(),
        ],
        max_value=UnknownLength,
        variables={"status": "Updating index"},
    )
    bar.start()
    while not pipe.poll():
        bar.update()
        sleep(0.1)
    bar.update(status="Done updating index.")
    bar.finish()


def _commit_index(package_data: List[PackageIndexData]):
    os.makedirs(env.INDEX, exist_ok=True)

    if sys.stderr.isatty() or env.TESTING:
        pipe, child_pipe = multiprocessing.Pipe()
        process = Process(target=_run_progress_bar, args=(child_pipe,))
        process.start()
        native_update_index(env.INDEX, package_data)
        pipe.send(True)
        process.join()
    else:
        info("Updating index...")
        native_update_index(env.INDEX, package_data)
        info("Done updating index.")


def update_index():
    orig_prefix = env.PREFIX_NAME
    if os.path.exists(env.INDEX):
        shutil.rmtree(env.INDEX)
    package_data = []
    if env.TESTING:
        package_data.extend(_get_index_data())
    else:
        for prefix in get_prefixes():
            env.set_prefix(prefix)
            package_data.extend(_get_index_data())
    _commit_index(package_data)
    env.set_prefix(orig_prefix)
