from tomwer.gui.reconstruction.axis.radioaxis import AxisTabWidget
from tomwer.synctools.axis import QAxisRP
from silx.gui.utils.testutils import TestCaseQt
from tomwer.test.utils import skip_gui_test
import pytest


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestGetNabuCorOpts(TestCaseQt):
    def test(self):  # noqa F811
        """
        Test of retrieving nabu_cor_options
        """
        axis_params = QAxisRP()
        widget = AxisTabWidget(recons_params=axis_params)
        assert axis_params.get_nabu_cor_options() == "side='all'"
        widget._calculationWidget._corOpts.setText("low_pass=2")
        widget._calculationWidget._corOpts.editingFinished.emit()
        assert axis_params.get_nabu_cor_options() == "side='all' ; low_pass=2"
        widget._calculationWidget._corOpts.setText("low_pass=2 ; high_pass=10")
        widget._calculationWidget._sideCB.setCurrentText("left")
        widget._calculationWidget._corOpts.editingFinished.emit()
        assert (
            axis_params.get_nabu_cor_options()
            == "side='left' ; low_pass=2 ; high_pass=10"
        )
