def test_affected_calls_requested_for_string_metadata(server_calls):
    calls = server_calls["MetadataProvider.Get_FCPAffectedByMetadata_StringMetadata"]
    assert any(call.successful for call in calls)


def test_affected_calls_requested_for_two_integers_metadata(server_calls):
    calls = server_calls["MetadataProvider.Get_FCPAffectedByMetadata_TwoIntegersMetadata"]
    assert any(call.successful for call in calls)
