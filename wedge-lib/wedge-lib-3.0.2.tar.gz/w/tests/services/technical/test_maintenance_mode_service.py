from django.test.utils import override_settings

from w.services.technical.filesystem_service import FilesystemService
from w.services.technical.maintenance_mode_service import MaintenanceModeService
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestMaintenanceModeService(TestCaseMixin):
    def setup_method(self):
        self.clean_sandbox()

    """
    status
    """

    def test_is_on_with_maintenance_mode_off_return_false(self):
        with override_settings(BASE_DIR=self.get_sandbox_dir()):
            assert MaintenanceModeService.is_on() is False

    def test_is_on_with_maintenance_mode_on_return_true(self):
        with override_settings(BASE_DIR=self.get_sandbox_dir()):
            MaintenanceModeService.enable()
            assert MaintenanceModeService.is_on() is True

    """
    enable
    """

    def test_enable_with_maintenance_mode_on_return_none(self):
        with override_settings(BASE_DIR=self.get_sandbox_dir()):
            FilesystemService.write_file(
                self.get_sandbox_dir(MaintenanceModeService.maintenance_file), ""
            )
            assert MaintenanceModeService.is_on() is True
            assert MaintenanceModeService.enable() is None
            assert MaintenanceModeService.is_on() is True

    def test_enable_with_success_return_none(self):
        with override_settings(BASE_DIR=self.get_sandbox_dir()):
            assert MaintenanceModeService.is_on() is False
            assert MaintenanceModeService.enable() is None
            assert MaintenanceModeService.is_on() is True

    """
    disable
    """

    def test_disable_with_maintenance_mode_off_return_none(self):
        with override_settings(BASE_DIR=self.get_sandbox_dir()):
            assert MaintenanceModeService.is_on() is False
            assert MaintenanceModeService.disable() is None
            assert MaintenanceModeService.is_on() is False

    def test_disable_with_success_return_none(self):
        with override_settings(BASE_DIR=self.get_sandbox_dir()):
            FilesystemService.write_file(
                self.get_sandbox_dir(MaintenanceModeService.maintenance_file), ""
            )
            assert MaintenanceModeService.is_on() is True
            assert MaintenanceModeService.disable() is None
            assert MaintenanceModeService.is_on() is False
