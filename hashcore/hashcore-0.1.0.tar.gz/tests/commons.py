import yaml, os, stat

from hash import dag

def create_resource_file(file, kind="", name="", spec="", parent="", depends_on = [], envs = [], remote = {}, env = ""):
    data = {
        "apiVersion": "hash.io/v1alpha1",
        "metadata": {}
    }
    if kind:
        data["kind"] = kind
    if name:
        data["metadata"]["name"] = name
    if parent:
        data["metadata"]["parent"] = parent
    if depends_on:
        data["metadata"]["depends_on"] = depends_on
    if envs:
        data["metadata"]["envs"] = envs
    if env:
        data["metadata"]["env"] = env
    if spec:
        data["spec"] = spec
    if remote:
        data["metadata"]["remote"] = remote
    with open(file, "w") as f:
        f.write(yaml.dump(data))

def create_local_file_store_config(output : str, org = "hashio", project = "hash") -> dict:
    return {
        "output": output,
        "org": org,
        "project": project
    }

def create_fake_file_store_config(org = "hashio", project = "hash"):
    return {
        "org": org,
        "project": project
    }

def script_ret(path, code = 1):
    path.write_text(f"""#!/bin/bash
exit {code}
""")
    st = os.stat(str(path))
    os.chmod(path, st.st_mode | stat.S_IEXEC)

def script_write_something(path, file = "test.txt", write = "1"):
    path.write_text(f"""#!/bin/bash
echo -n {write} > {file}
""")
    st = os.stat(str(path))
    os.chmod(path, st.st_mode | stat.S_IEXEC)

def script_print_json(path):
    path.write_text("""#!/bin/bash
printf '{"x": "a"}'
""")
    st = os.stat(str(path))
    os.chmod(path, st.st_mode | stat.S_IEXEC)

def template_file(path):
    path.write_text("{{x}}")

def write_yaml(file, data):
    with open(file, "w") as f:
        f.write(yaml.dump(data))

def create_k8s_pod(name, image) -> dict:
    return {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "name": name
        },
        "spec" : {
            "containers": [{
                "name": name,
                "image": image
            }]
        }
    }

# Read a graph from a file
def read_graph(file):
    d = dag.Graph()
    ret_nodes = []
    with open(file, "r") as f:
        line = f.readline()
        while line:
            nodes = line.split(" ")
            if len(nodes) != 2:
                continue
            n1 = dag.Node(nodes[0], {})
            if n1 not in ret_nodes:
                ret_nodes.append(n1)
            other_nodes = nodes[1].split(",")
            for node in other_nodes:
                other_node = dag.Node(node.strip(), {})
                if other_node not in ret_nodes:
                    ret_nodes.append(other_node)
                e = dag.Edge(n1, other_node)
                d.addEdge(e)
            line = f.readline()
    return d, ret_nodes
