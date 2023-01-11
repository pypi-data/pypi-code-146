# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import cProfile
import uuid
from contrast.utils.decorators import fail_loudly

from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


MAX_ORIGINAL_PATH_LENTGH = 64


class Profiler(cProfile.Profile):
    def __init__(self, path):
        super().__init__()

        from contrast.agent.settings import Settings

        self.settings = Settings()
        self.path = path

    def __enter__(self):
        if self.settings.is_profiler_enabled:
            self.enable()
        return self

    def __exit__(self, *exc_info):
        if self.settings.is_profiler_enabled:
            self.disable()
            self._save_profile_data()

    @fail_loudly("Unable to save profile data")
    def _save_profile_data(self):
        safe_path = self._get_safe_path()
        filename = f"cprofile-{safe_path}-{uuid.uuid4().hex}.out"
        logger.debug("writing cprofile data to %s", filename)
        self.dump_stats(filename)

    def _get_safe_path(self):
        path = self.path[:MAX_ORIGINAL_PATH_LENTGH].strip("/").replace("/", "_") or "_"
        safe_path = "".join([c for c in path if c.isalpha() or c.isdigit() or c == "_"])
        return safe_path
