from unittest import mock

from mayan.apps.documents.tests.base import GenericDocumentTestCase

from .mixins import DocumentVersionOCRTaskTestMixin


class OCRTaskTestCase(
    DocumentVersionOCRTaskTestMixin, GenericDocumentTestCase
):
    @mock.patch(
        'mayan.apps.ocr.events.event_ocr_document_version_finished.commit'
    )
    def test_task_document_version_ocr_finished_error_create(
        self, event_ocr_document_version_finished_commit
    ):
        TEST_EXCEPTION_TEXT = 'Fake exception'

        self._silence_logger(name='mayan.apps.ocr.tasks')

        event_ocr_document_version_finished_commit.side_effect = Exception(
            TEST_EXCEPTION_TEXT
        )

        self._clear_events()

        with self.assertRaises(expected_exception=Exception):
            self._execute_task_document_version_ocr_finished()

        self.assertEqual(
            self._test_document_version.error_log.count(), 1
        )
        self.assertEqual(
            self._test_document_version.error_log.first().text,
            TEST_EXCEPTION_TEXT
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
