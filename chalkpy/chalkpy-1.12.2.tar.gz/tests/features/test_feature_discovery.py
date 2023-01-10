from datetime import datetime, timedelta

import pytest

from chalk import description, is_primary, owner, tags
from chalk.features import Features, feature, feature_time, features, unwrap_feature


@features(tags="t", owner="andy@chalk.ai")
class WowFS:
    # This is a really neat description of something
    something: str

    # This is also really neat and cool
    something_else: str
    nocomment: str

    nope: str

    assigned: str = feature(tags="a")

    # bizarre
    bizarre: str

    # goofy
    goofy: str = feature(owner="yo")

    # now with feature
    assigned_comment: str = feature(tags=["3", "4"])

    # implicit comment
    explicit: str = feature(description="explicit comment")

    # Multiline
    # Neat and, verily, cool
    #
    # Hello
    assigned_comment_multiline: str = feature()

    # now with feature time
    time: datetime = feature_time()

    nope_nope: datetime  # Datetime field that is not feature time


@features(owner="elliot@chalk.ai")
class OwnerFeatures:
    plain: str
    cached: str = feature(max_staleness="3d")
    andy: str = feature(owner="andy@chalk.ai")

    ft: datetime = feature_time()


@features(tags=["1", "2"])
class TagFeatures:
    empty: str
    one: str = feature(tags="one")
    many: str = feature(tags=["a", "b"])

    ft: datetime = feature_time()


@features
class CommentBaseOwner:
    id: str
    # I'm a cool comment!
    # :owner: elliot@chalk.ai
    empty: str

    # I'm a cool comment!
    # :tags: pii group:risk
    email: str

    # :tags: pii, group:risk
    email_commas: str
    # :tags: pii
    email_single: str

    # :tags: pii
    email_all_kinds: str = feature(tags=["hello"])


@features(max_staleness="4d")
class MaxStalenessFeatures:
    id: int
    name: str = feature(max_staleness=None)
    woohoo: str = feature(max_staleness="30d")
    boop: str = feature(max_staleness=timedelta(seconds=5))


@features(max_staleness=timedelta(days=3, seconds=5))
class MaxStalenessFeatures2:
    id: int


@features(etl_offline_to_online=True)
class ETLFeatures:
    id: int
    name: str = feature(etl_offline_to_online=False)
    woohoo: str = feature(etl_offline_to_online=True)


def test_class_etl_offline_to_online():
    assert unwrap_feature(ETLFeatures.id).etl_offline_to_online is True
    assert unwrap_feature(ETLFeatures.name).etl_offline_to_online is False
    assert unwrap_feature(ETLFeatures.woohoo).etl_offline_to_online is True
    assert issubclass(ETLFeatures, Features)
    assert ETLFeatures.__chalk_etl_offline_to_online__ is True
    assert issubclass(MaxStalenessFeatures, Features)
    assert MaxStalenessFeatures.__chalk_etl_offline_to_online__ is None


def test_class_max_staleness():
    assert unwrap_feature(MaxStalenessFeatures.id).max_staleness == "4d"
    assert unwrap_feature(MaxStalenessFeatures.boop).max_staleness == "5s"
    assert unwrap_feature(MaxStalenessFeatures.name).max_staleness is None
    assert unwrap_feature(MaxStalenessFeatures.woohoo).max_staleness == "30d"
    assert issubclass(MaxStalenessFeatures, Features)
    assert MaxStalenessFeatures.__chalk_max_staleness__ == "4d"
    assert issubclass(ETLFeatures, Features)
    assert ETLFeatures.__chalk_max_staleness__ is None
    assert MaxStalenessFeatures.__chalk_max_staleness__ == "4d"
    assert ETLFeatures.__chalk_max_staleness__ is None
    assert MaxStalenessFeatures2.__chalk_max_staleness__ == "3d 5s"


def test_primary():
    assert is_primary(CommentBaseOwner.id)
    assert not is_primary(CommentBaseOwner.email)


def test_comment_based_owner():
    assert "elliot@chalk.ai" == unwrap_feature(CommentBaseOwner.empty).owner == owner(CommentBaseOwner.empty)
    assert ["pii", "group:risk"] == unwrap_feature(CommentBaseOwner.email).tags == tags(CommentBaseOwner.email)
    assert ["pii"] == unwrap_feature(CommentBaseOwner.email_single).tags == tags(CommentBaseOwner.email_single)
    assert (
        ["hello", "pii"]
        == unwrap_feature(CommentBaseOwner.email_all_kinds).tags
        == tags(CommentBaseOwner.email_all_kinds)
    )
    with pytest.raises(ValueError):

        @features
        class BadFeatureClass:
            # :owner: elliot@chalk.ai
            doubly_owned: str = feature(owner="d")


def test_parse_descriptions():
    assert "bizarre" == unwrap_feature(WowFS.bizarre).description == description(WowFS.bizarre)
    assert (
        "This is a really neat description of something"
        == unwrap_feature(WowFS.something).description
        == description(WowFS.something)
    )
    assert "explicit comment" == unwrap_feature(WowFS.explicit).description == description(WowFS.explicit)
    assert (
        "This is also really neat and cool"
        == unwrap_feature(WowFS.something_else).description
        == description(WowFS.something_else)
    )
    assert (
        "now with feature" == unwrap_feature(WowFS.assigned_comment).description == description(WowFS.assigned_comment)
    )
    assert "goofy" == unwrap_feature(WowFS.goofy).description == description(WowFS.goofy)
    assert (
        """Multiline
Neat and, verily, cool

Hello"""
        == unwrap_feature(WowFS.assigned_comment_multiline).description
        == description(WowFS.assigned_comment_multiline)
    )


def test_class_owner():
    assert "elliot@chalk.ai" == OwnerFeatures.__chalk_owner__ == owner(OwnerFeatures)
    assert "elliot@chalk.ai" == unwrap_feature(OwnerFeatures.plain).owner == owner(OwnerFeatures.plain)
    assert "elliot@chalk.ai" == unwrap_feature(OwnerFeatures.cached).owner == owner(OwnerFeatures.cached)
    assert "andy@chalk.ai" == unwrap_feature(OwnerFeatures.andy).owner == owner(OwnerFeatures.andy)


def test_class_tags():
    assert [] == tags(OwnerFeatures) == OwnerFeatures.__chalk_tags__
    assert ["1", "2"] == TagFeatures.__chalk_tags__ == tags(TagFeatures)
    assert ["1", "2"] == unwrap_feature(TagFeatures.empty).tags == tags(TagFeatures.empty)
    assert ["one", "1", "2"] == unwrap_feature(TagFeatures.one).tags == tags(TagFeatures.one)
    assert ["a", "b", "1", "2"] == unwrap_feature(TagFeatures.many).tags == tags(TagFeatures.many)
    assert ["a", "t"] == unwrap_feature(WowFS.assigned).tags == tags(WowFS.assigned)
    assert ["t"] == unwrap_feature(WowFS.nope).tags == tags(WowFS.nope)
    assert ["3", "4", "t"] == unwrap_feature(WowFS.assigned_comment).tags == tags(WowFS.assigned_comment)
