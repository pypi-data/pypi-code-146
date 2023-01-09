from absl import app
from absl import flags
import pycollimator as pycol

FLAGS = flags.FLAGS

flags.DEFINE_string("token", None, "Client token.")
flags.DEFINE_string("project_uuid", None, "Project UUID.")
flags.DEFINE_string("api_url", "https://dev.collimator.ai", "Project name.")
flags.DEFINE_string("file", None, "File to upload.")

# Required flag.
flags.mark_flag_as_required("token")
flags.mark_flag_as_required("project_uuid")
flags.mark_flag_as_required("file")


def main(argv):
    del argv  # Unused.

    pycol.global_variables.set_auth_token(FLAGS.token, api_url=FLAGS.api_url, project_uuid=FLAGS.project_uuid)

    pycol.Api.upload_file(FLAGS.file, overwrite=True)


if __name__ == "__main__":
    app.run(main)
