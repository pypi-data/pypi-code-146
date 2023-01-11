"""Provides DetectDuplicates functionality"""
from . import errors
from . import schemas as T


def detect_uid_conflicts_in_item(item, uids, insert_errors, overrides) -> bool:
    """
    Detect StudyInstanceUID and SeriesInstanceUID conflicts in items
    Items should contain a single StudyInstanceUID and SeriesInstanceUID
    """
    study_instance_uid_conflict = False
    series_instance_uid_conflict = False

    study_instance_uid = None
    series_instance_uid = None
    for uid in uids:
        if study_instance_uid is None:
            study_instance_uid = uid.study_instance_uid
        if series_instance_uid is None:
            series_instance_uid = uid.series_instance_uid

        if uid.study_instance_uid != study_instance_uid and (
            not overrides or errors.DifferentStudyInstanceUID.code in overrides
        ):
            # one item multiple StudyInstanceUID -> conflict
            study_instance_uid_conflict = True

        if uid.series_instance_uid != series_instance_uid and (
            not overrides or errors.DifferentSeriesInstanceUID.code in overrides
        ):
            # one item multiple SeriesInstanceUID -> conflict
            series_instance_uid_conflict = True

        if study_instance_uid_conflict and series_instance_uid_conflict:
            break

    if study_instance_uid_conflict:
        insert_errors.push(
            T.Error(item_id=item.id, code=errors.DifferentStudyInstanceUID.code).dict(
                exclude_none=True
            )
        )

    if series_instance_uid_conflict:
        insert_errors.push(
            T.Error(item_id=item.id, code=errors.DifferentSeriesInstanceUID.code).dict(
                exclude_none=True
            )
        )

    if study_instance_uid_conflict or series_instance_uid_conflict:
        return False

    return True
