"""A collection of functions for use in the FRC API."""


def season_check(season: int, season2: int, min_year: int = 2015):
    """Check if season is None, if it is set it to season2."""
    if season is None:
        return season2
    if season >= min_year and season <= 2023:
        return season
    else:
        raise ValueError(f"Invalid season number must be between {min_year} and 2023")  # noqa: E501
