import shutil
import subprocess


COMMAND = shutil.which("gradle")


def __virtual__(hub):
    if not COMMAND:
        return False, "gradle command not found"
    return (True,)


def run(hub, subcommand: str, project_dir: str, *args):
    proc = subprocess.Popen(
        [COMMAND, subcommand, f"--project-dir={project_dir}", *args],
        stderr=subprocess.PIPE,
        cwd=project_dir,
        encoding="ascii",
    )
    _, stderr = proc.communicate()
    for line in stderr.splitlines():
        hub.log.error(line)
    code = proc.wait()
    if code:
        raise ChildProcessError(f"Gradle command failed with status {code}")


def clean(hub, build_dir: str):
    hub.tool.gradle.run("clean", project_dir=build_dir)


def build(hub, build_dir: str):
    hub.tool.gradle.run("build", project_dir=build_dir)

    # Return the resulting openapi spec path
    return {}
