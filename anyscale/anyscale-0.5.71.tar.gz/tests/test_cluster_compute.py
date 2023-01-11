from unittest.mock import ANY, Mock

from anyscale.cluster_compute import (
    get_cluster_compute_from_name,
    get_default_cluster_compute,
    register_compute_template,
)
from anyscale.sdk.anyscale_client import ArchiveStatus, CreateComputeTemplate
from anyscale.sdk.anyscale_client.models.compute_template_query import (
    ComputeTemplateQuery,
)


def test_get_default_cluster_compute():
    mock_api_client = Mock()
    mock_anyscale_api_client = Mock()
    mock_anyscale_api_client.get_default_compute_config = Mock(
        return_value=Mock(result="mock_config_obj")
    )
    mock_default_config_obj = {
        "cloud_id": "cld_1",
        "max_workers": 10,
        "region": "us-west-2",
        "allowed_azs": ["us-west-2a", "us-west-2b"],
        "head_node_type": {
            "name": "head-1",
            "instance_type": "m5.2xlarge",
            "aws_advanced_configurations": None,
            "gcp_advanced_configurations": None,
            "resources": None,
        },
        "worker_node_types": [],
    }
    mock_anyscale_api_client.get_default_compute_config = Mock(
        return_value=Mock(result=mock_default_config_obj)
    )
    mock_api_client.create_compute_template_api_v2_compute_templates_post = Mock(
        return_value=Mock(result="mock_compute_template")
    )
    mock_api_client.find_cloud_by_name_api_v2_clouds_find_by_name_post = Mock(
        return_value=Mock(result=Mock(id="test_cloud_id"))
    )

    assert (
        get_default_cluster_compute(
            "mock_cloud_name", None, mock_api_client, mock_anyscale_api_client
        )
        == "mock_compute_template"
    )
    mock_anyscale_api_client.get_default_compute_config.assert_called_once_with(
        "test_cloud_id"
    )


def test_register_compute_template():
    mock_api_client = Mock()
    mock_api_client.create_compute_template_api_v2_compute_templates_post = Mock(
        return_value=Mock(result=Mock(id="mock_template_id"))
    )

    assert (
        register_compute_template("mock_template_obj", mock_api_client).id
        == "mock_template_id"
    )
    mock_api_client.create_compute_template_api_v2_compute_templates_post.assert_called_once_with(
        create_compute_template=CreateComputeTemplate(
            name=ANY, config="mock_template_obj", anonymous=True,
        )
    )


def test_get_cluster_compute_from_name():
    mock_api_client = Mock()
    mock_api_client.search_compute_templates_api_v2_compute_templates_search_post = Mock(
        return_value=Mock(results=[Mock(id="mock_id")])
    )
    assert get_cluster_compute_from_name("mock_name", mock_api_client).id == "mock_id"

    mock_api_client.search_compute_templates_api_v2_compute_templates_search_post.assert_called_once_with(
        ComputeTemplateQuery(
            orgwide=True,
            name={"equals": "mock_name"},
            include_anonymous=True,
            archive_status=ArchiveStatus.ALL,
        )
    )
