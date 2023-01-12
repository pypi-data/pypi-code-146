import pytest
import numpy as np
from nabu.testutils import get_data as nabu_get_data
from nabu.pipeline.helical.span_strategy import SpanStrategy


@pytest.fixture(scope="class")
def bootstrap_TestStrategy(request):
    cls = request.cls
    cls.abs_tol = 1.0e-6

    # from the Paul telephone dataset
    test_data = nabu_get_data("data_test_strategy.npz")

    cls.z_pix_per_proj = test_data["z_pix_per_proj"]
    cls.x_pix_per_proj = test_data["x_pix_per_proj"]
    cls.detector_shape_vh = test_data["detector_shape_vh"]
    cls.phase_margin_pix = test_data["phase_margin_pix"]
    cls.projection_angles_deg = test_data["projection_angles_deg"]
    cls.require_redundancy = test_data["require_redundancy"]
    cls.pixel_size_mm = test_data["pixel_size_mm"]

    cls.result_angle_index_span = test_data["result_angle_index_span"]
    cls.result_angles_rad = test_data["result_angles_rad"]
    cls.result_fract_complement_to_integer_shift_v = test_data[
        "result_fract_complement_to_integer_shift_v"
    ]
    cls.result_integer_shift_v = test_data["result_integer_shift_v"]
    cls.result_span_v = test_data["result_span_v"]
    cls.result_x_pix_per_proj = test_data["result_x_pix_per_proj"]
    cls.result_z_pix_per_proj = test_data["result_z_pix_per_proj"]

    cls.test_data = test_data


@pytest.mark.usefixtures("bootstrap_TestStrategy")
class TestStrategy:
    def test_strategy(self):

        # the python implementation is slow. so we take only a p[art of the scan
        limit = 4000
        span_info = SpanStrategy(
            z_pix_per_proj=self.z_pix_per_proj[:limit],
            x_pix_per_proj=self.x_pix_per_proj[:limit],
            detector_shape_vh=self.detector_shape_vh,
            phase_margin_pix=self.phase_margin_pix,
            projection_angles_deg=self.projection_angles_deg[:limit],
            pixel_size_mm=self.pixel_size_mm,
            require_redundancy=self.require_redundancy,
        )

        print(span_info.get_informative_string())
        chunk_info = span_info.get_chunk_info(self.result_span_v)

        for key, val in chunk_info.__dict__.items():
            reference = getattr(self, "result_" + key)
            ref_array = np.array(reference)
            res_array = np.array(val)
            if res_array.dtype in [bool, np.int32, np.int64]:
                message = f" different result for {key} attribute in the chunk_info returned value  "
                assert np.array_equal(res_array, ref_array), message
            elif res_array.dtype in [np.float32, np.float64]:
                message = f" different result for {key} attribute in the chunk_info returned value  "
                assert np.all(
                    np.isclose(res_array, ref_array, atol=self.abs_tol)
                ), message
