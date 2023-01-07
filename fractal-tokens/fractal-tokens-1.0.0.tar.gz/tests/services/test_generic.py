def test_fractal_service(dummy_token_service):
    assert next(dummy_token_service.__class__.install())
    assert dummy_token_service.is_healthy()
