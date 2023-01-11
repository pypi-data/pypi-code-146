import pytest


def pytest_collection_modifyitems(config, items):
    keywordexpr = config.option.keyword
    markexpr = config.option.markexpr
    if keywordexpr or markexpr:
        return  # let pytest handle this

    skip_spatial = pytest.mark.skip(reason='spatial not selected')
    for item in items:
        if 'spatial' in item.keywords:
            item.add_marker(skip_spatial)
