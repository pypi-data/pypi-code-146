import subprocess


def start_server(port="5000"):
    subprocess.Popen(["mlflow", "server", "--host", "0.0.0.0", "--port", port])
