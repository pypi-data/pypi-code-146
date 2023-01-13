"""Functions for cloudwatch"""

from dai_python_commons.dai_error import DaiInputError


class CWUtils:  # pylint: disable=too-few-public-methods
    """
    Class that provides helpful CloudWatch utilities.
    """

    @staticmethod
    def put_lambda_metric(cw_client, metric_name: str, dai_code: str, function_name: str):
        """
        Increase counter for our dai-code metric for its kind of action in cloudwatch.

        :param cw_client: A boto3.client("cloudwatch") to use to write the logs
        :param metric_name: Which counter to increase
        :param dai_code: The dai_code (e.g. `tr-tms-obs-0008`) which will be used for setting the dimension of the metric
        :param function_name: The lambda name which will be used for setting the namespace of the metric
        """
        allowed_metric_names = ["invocation", "error"]
        if metric_name not in allowed_metric_names:
            raise DaiInputError(f"{metric_name} not in {allowed_metric_names}")

        cw_client.put_metric_data(
            Namespace=f"DAI/Lambda/{function_name}",
            MetricData=[
                {
                    "MetricName": metric_name,
                    "Value": 1,
                    "Unit": "Count",
                    "Dimensions": [{"Name": "daiCode", "Value": dai_code}],
                }
            ],
        )
