from gb_ocr.grin_lib.GRINOps import GRINGet


def test_grin_get():
    test_grin = GRINGet()
    test_text = test_grin.get('_all_books')
    assert len(test_text) > 0


def test_non_get():
    try:
        test_grin = GRINGet()
        test_text = test_grin.get('_ImNotHere')

        # shouldn't get here
        assert (len(test_text) == 0)
    except Exception as eek:
        assert (eek.code == 404)
