import pytest
import time

from jikan4.jikan import Jikan


@pytest.fixture
def jikan():
    time.sleep(
        1
    )  # This is needed to prevent 429 Too Many Requests when resetting the rate limit

    return Jikan()


def test_get_anime(jikan: Jikan):
    resp = jikan.get_anime(1)

    assert resp.title == "Cowboy Bebop", "Response does not match expected response"


def test_get_anime_full(jikan: Jikan):
    resp = jikan.get_anime_full(1)

    assert resp.title == "Cowboy Bebop", "Response does not match expected response"
    assert len(resp.streaming) > 0, "Response streaming list is empty"


def test_get_anime_characters(jikan: Jikan):
    resp = jikan.get_anime_characters(1)

    assert len(resp.data) > 0, "Response characters is empty"
    assert len(resp.data[0].voice_actors) > 0, "Response voice actors is empty"


def test_get_anime_staff(jikan: Jikan):
    resp = jikan.get_anime_staff(1)

    assert len(resp.data) > 0, "Response staff is empty"
    assert len(resp.data[0].positions) > 0, "Response positions is empty"


def test_get_anime_episodes(jikan: Jikan):
    resp = jikan.get_anime_episodes(1)

    assert len(resp.data) > 0, "Response episodes is empty"


def test_get_anime_episode(jikan: Jikan):
    resp = jikan.get_anime_episode(1, 1)

    assert resp.synopsis is not None, "Response synopsis is empty"


def test_get_anime_news(jikan: Jikan):
    resp = jikan.get_anime_news(1)

    assert {"pagination", "data"}.issubset(
        resp.__dict__
    ), "Response does not match expected response"
    assert len(resp.data) > 0, "Response data is empty"


def test_search_anime(jikan: Jikan):
    resp = jikan.search_anime("tv", "naruto")

    assert {"pagination", "data"}.issubset(
        resp.__dict__
    ), "Response does not match expected response"
    assert len(resp.data) > 0, "Response data is empty"


def test_ratelimit(jikan: Jikan):
    start = time.time()
    for _ in range(10):
        jikan.get_anime(1)
    end = time.time()

    max_per_minute = jikan.rate_limiter.calls_limit / jikan.rate_limiter.period

    assert end - start > 10 / (60 / max_per_minute), "Rate limit not working"
