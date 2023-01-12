def test_get_feature_definition_called_for_silaservice(server_calls):
    calls = server_calls["SiLAService.GetFeatureDefinition"]
    assert any(
        call.request.FeatureIdentifier.value == "org.silastandard/core/SiLAService/v1" for call in calls
    ), "Expected call with 'org.silastandard/core/SiLAService/v1'"


def test_get_feature_definition_called_for_metadataprovider(server_calls):
    calls = server_calls["SiLAService.GetFeatureDefinition"]
    assert any(
        call.request.FeatureIdentifier.value == "org.silastandard/test/MetadataProvider/v1" for call in calls
    ), "Expected call with 'org.silastandard/test/MetadataProvider/v1'"


def test_set_server_name_called_with_SiLA_is_Awesome(server_calls):
    calls = server_calls["SiLAService.SetServerName"]
    assert any(
        call.request.ServerName.value == "SiLA is Awesome" for call in calls
    ), "Expected call with 'SiLA is Awesome'"


def test_server_name_requested(server_calls):
    calls = server_calls["SiLAService.Get_ServerName"]
    assert any(call.successful for call in calls)


def test_server_type_requested(server_calls):
    calls = server_calls["SiLAService.Get_ServerType"]
    assert any(call.successful for call in calls)


def test_server_uuid_requested(server_calls):
    calls = server_calls["SiLAService.Get_ServerUUID"]
    assert any(call.successful for call in calls)


def test_server_description_requested(server_calls):
    calls = server_calls["SiLAService.Get_ServerDescription"]
    assert any(call.successful for call in calls)


def test_server_version_requested(server_calls):
    calls = server_calls["SiLAService.Get_ServerVersion"]
    assert any(call.successful for call in calls)


def test_server_vendor_url_requested(server_calls):
    calls = server_calls["SiLAService.Get_ServerVendorURL"]
    assert any(call.successful for call in calls)


def test_implemented_features_requested(server_calls):
    calls = server_calls["SiLAService.Get_ImplementedFeatures"]
    assert any(call.successful for call in calls)
