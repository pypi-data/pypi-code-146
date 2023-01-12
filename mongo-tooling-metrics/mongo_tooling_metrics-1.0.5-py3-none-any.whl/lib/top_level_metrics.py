import argparse
from datetime import datetime
import os
import sys
from typing import List, Optional
from mongo_tooling_metrics import get_hook, __version__
from mongo_tooling_metrics.base_metrics import TopLevelMetrics
from mongo_tooling_metrics.lib.hooks import ExitHook
from mongo_tooling_metrics.lib.sub_metrics import BuildInfo, GitInfo, HostInfo, SConsInfo


class ResmokeToolingMetrics(TopLevelMetrics):
    """Class to store resmoke tooling metrics."""

    source: str
    utc_starttime: datetime
    utc_endtime: datetime
    host_info: HostInfo
    git_info: GitInfo
    exit_code: Optional[int]
    command: List[str]
    module_info: List[GitInfo]
    tooling_metrics_version: str

    @classmethod
    def generate_metrics(
        cls,
        utc_starttime: datetime,
    ):
        """Get resmoke metrics to the best of our ability."""
        exit_hook = get_hook(ExitHook)
        return cls(
            source='resmoke',
            utc_starttime=utc_starttime,
            utc_endtime=datetime.utcnow(),
            host_info=HostInfo.generate_metrics(),
            git_info=GitInfo.generate_metrics('.'),
            exit_code=None if exit_hook.is_malformed() else exit_hook.exit_code,
            command=sys.argv,
            module_info=GitInfo.modules_generate_metrics(),
            tooling_metrics_version=__version__,
        )

    def is_malformed(self) -> bool:
        """Confirm whether this instance has all expected fields."""
        sub_metrics = self.module_info + [self.git_info] + [self.host_info]
        return self.exit_code is None or any(metrics.is_malformed() for metrics in sub_metrics)


class SConsToolingMetrics(TopLevelMetrics):
    """Class to store scons tooling metrics."""

    source: str
    utc_starttime: datetime
    utc_endtime: datetime
    host_info: HostInfo
    git_info: GitInfo
    exit_code: Optional[int]
    build_info: BuildInfo
    scons_info: SConsInfo
    command: List[str]
    module_info: List[GitInfo]
    tooling_metrics_version: str

    @classmethod
    def generate_metrics(
        cls,
        utc_starttime: datetime,
        artifact_dir: str,
        env_vars: "SCons.Variables.Variables",
        env: "SCons.Script.SConscript.SConsEnvironment",
        parser: "SCons.Script.SConsOptions.SConsOptionParser",
        args: List[str],
    ):
        """Get scons metrics to the best of our ability."""
        exit_hook = get_hook(ExitHook)
        return cls(
            source='scons',
            utc_starttime=utc_starttime,
            utc_endtime=datetime.utcnow(),
            host_info=HostInfo.generate_metrics(),
            git_info=GitInfo.generate_metrics('.'),
            build_info=BuildInfo.generate_metrics(utc_starttime, artifact_dir),
            scons_info=SConsInfo.generate_metrics(artifact_dir, env_vars, env, parser, args),
            exit_code=None if exit_hook.is_malformed() else exit_hook.exit_code,
            command=sys.argv,
            module_info=GitInfo.modules_generate_metrics(),
            tooling_metrics_version=__version__,
        )

    def is_malformed(self) -> bool:
        """Confirm whether this instance has all expected fields."""
        sub_metrics = self.module_info + [
            self.git_info,
            self.host_info,
            self.build_info,
            self.scons_info,
        ]
        return self.exit_code is None or any(metrics.is_malformed() for metrics in sub_metrics)


class NinjaToolingMetrics(TopLevelMetrics):
    """Class to store ninja tooling metrics."""

    source: str
    utc_starttime: datetime
    utc_endtime: datetime
    host_info: HostInfo
    git_info: GitInfo
    exit_code: Optional[int]
    build_info: BuildInfo
    command: List[str]
    module_info: List[GitInfo]
    tooling_metrics_version: str

    @classmethod
    def generate_metrics(
        cls,
        utc_starttime: datetime,
    ):
        """Get scons metrics to the best of our ability."""
        artifact_dir = cls._get_ninja_artifact_dir()
        exit_hook = get_hook(ExitHook)
        return cls(
            source='ninja',
            utc_starttime=utc_starttime,
            utc_endtime=datetime.utcnow(),
            host_info=HostInfo.generate_metrics(),
            git_info=GitInfo.generate_metrics('.'),
            build_info=BuildInfo.generate_metrics(utc_starttime, artifact_dir),
            exit_code=None if exit_hook.is_malformed() else exit_hook.exit_code,
            command=sys.argv,
            module_info=GitInfo.modules_generate_metrics(),
            tooling_metrics_version=__version__,
        )

    @classmethod
    def _get_ninja_file(cls) -> Optional[str]:
        """Get the ninja file from sys.argv -- return 'None' if this fails."""
        try:
            parser = argparse.ArgumentParser()
            parser.add_argument('-f')
            known_args, _ = parser.parse_known_args()
            ninja_file = known_args.f if known_args.f else "build.ninja"
            return ninja_file if os.path.exists(ninja_file) else ""
        except:
            return None

    @classmethod
    def _get_ninja_artifact_dir(cls) -> Optional[str]:
        """Get the artifact dir specified in the ninja file."""
        try:
            ninja_file = cls._get_ninja_file()

            if not ninja_file:
                return ninja_file

            with open(ninja_file) as file:
                for line in file:
                    if 'builddir = ' in line:
                        return os.path.abspath(line.split("builddir = ")[-1])

            # if 'builddir' doesn't exist the metrics are malformed
            return None
        except:
            return None

    def is_malformed(self) -> bool:
        """Confirm whether this instance has all expected fields."""
        sub_metrics = self.module_info + [
            self.git_info,
            self.host_info,
            self.build_info,
        ]
        return self.exit_code is None or any(metrics.is_malformed() for metrics in sub_metrics)
