import json
import grpc


def get_management_channel(
    endpoint, service="continual.rpc.management.v1.ManagementAPI", options=None
):
    options = options or []
    service_config = json.dumps(
        {
            "methodConfig": [
                {
                    "name": [
                        {
                            "service": service
                            or "continual.rpc.management.v1.ManagementAPI"
                        }
                    ],
                    "retryPolicy": {
                        "maxAttempts": 5,
                        "initialBackoff": "1s",
                        "maxBackoff": "30s",
                        "backoffMultiplier": 2,
                        "retryableStatusCodes": ["UNAVAILABLE", "RESOURCE_EXHAUSTED"],
                    },
                }
            ]
        }
    )
    options.extend(
        [
            ("grpc.max_receive_message_length", 100 * 1024 * 1024),
            ("grpc.max_send_message_length", 100 * 1024 * 1024),
            ("grpc.service_config", service_config),
        ]
    )

    if endpoint == "https://sdk.continual.ai":
        credentials = grpc.ssl_channel_credentials()
        return grpc.secure_channel("sdk.continual.ai:443", credentials, options)
    elif endpoint == "https://sdk-benchmark.continual.ai":
        credentials = grpc.ssl_channel_credentials()
        return grpc.secure_channel(
            "sdk-benchmark.continual.ai:443", credentials, options
        )
    elif endpoint == "http://localhost" or endpoint == "http://127.0.0.1":
        host = "127.0.0.1:30003"
        return grpc.insecure_channel(host, options)
    elif endpoint == "http://host.docker.internal":
        host = "host.docker.internal:30003"
        return grpc.insecure_channel(host, options)
    elif endpoint == "http://cluster":
        host = "management:3001"
        return grpc.insecure_channel(host, options)
    else:
        return grpc.insecure_channel(endpoint, options)
