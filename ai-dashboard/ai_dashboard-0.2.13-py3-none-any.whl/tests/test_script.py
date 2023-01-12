from ai_dashboard import Client


def test_create_dashboard(test_client: Client):
    config = {
        "dataset_id": "steam",
        "authorizationToken": "b74993644646-4d4c-bd11-68287d0a95bb:M2Q2MzQ4MzgtZmZhMC00ZTA0LTlkMDMtZjAyNzQ5Y2QxOTc0:1e3042:EbeVbWzxXnXmFLri0UOrsvQEwI53",
    }

    dashboard = test_client.Dashboard(
        dataset_id=config["dataset_id"], name="New Cluster Dashboard"
    )

    # an instruction of silhouette score
    # dashboard.delete_all()

    tab = dashboard.DataReport(title="Cluster Confidence", name="Cluster Confidence")
    tab.add_aggregation(
        [
            {
                "agg": "category",
                "field": "_cluster_.review_translation_vector_.kmeans-25",
                "name": "category_cluster",
                "aggType": "groupby",
            }
        ],
        [
            {
                "name": "avg_voted_up",
                "field": "voted_up_int",
                "agg": "avg",
                "aggType": "metric",
            }
        ],
    )

    dashboard.append(tab)
    dashboard.push()

    # dashboard = client.Dashboard(
    #     dataset_id="iris-csv",
    #     name="My Dashboard" # Dashboard Name
    # )

    tab = dashboard.CategoryView(
        title="new Category View",
    )
    tab.set_view(
        cluster_field="_cluster_.review_translation_vector_.kmeans-25",
        # secondary_field="language",
    )

    dashboard.append(tab)
    dashboard.push()

    tab = dashboard.DocumentView(title="My Document View")
    tab.set_metric(metric="comment_count")
    dashboard.append(tab)
    dashboard.push()

    test_client.deployables[-1]

    assert True
