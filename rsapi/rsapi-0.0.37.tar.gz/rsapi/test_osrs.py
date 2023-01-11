import responses
import pytest

import rsapi
import rsapi.osrs as osrs


def test_hiscores():
    scores = osrs.hiscores("jakop")
    assert scores["Overall"]["level"] > 0, "Overall score mismatch"
    assert scores["Overall"]["exp"] > 0, "Overall exp mismatch"
    assert scores["Overall"]["rank"] > 0, "Overall rank mismatch"


def test_skills():
    skills = osrs.skills()

    # Minimum skill count
    assert len(skills) >= 87

    # Names are sensensible
    assert skills[0]["name"] == "Overall"
    # Has skills
    assert any(not skill["activity"] for skill in skills)
    # Has activities
    assert any(skill["activity"] for skill in skills)
    # Has aliases
    assert any(skill["aliases"] for skill in skills)


def test_player_not_found():
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            f"{rsapi.API_URL}/{rsapi.osrs.HISCORES_PATH}",
            body="NOT FOOND",
            status=404
        )
        with pytest.raises(rsapi.PlayerNotFound):
            osrs.hiscores("jakop")


def test_items():
    items = osrs.items("Iron dagger(p+)")
    assert len(items) == 1, "Expected to find Iron dagger(p+)"
    assert items[0]["lowalch"] == 14, "Expected to find item lowalch"
    assert items[0]["highalch"] == 21, "Expected to find item highalch"


def test_ge():
    items = osrs.ge("dragon bones")
    assert len(items) > 1
    assert any(i["name"] == "Dragon bones" for i in items.values())


def test_item_not_found():
    with pytest.raises(rsapi.ItemError):
        osrs.items("Not lightbearer")
