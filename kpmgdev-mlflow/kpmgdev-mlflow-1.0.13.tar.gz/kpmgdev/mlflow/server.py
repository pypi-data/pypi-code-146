import mlflow.server


def start_server(port=5000):
    mlflow.server.run(host='0.0.0.0', port=port)
