import importlib.resources as pkg_resources
import os

from sym.flow.cli.code_generation import approval
from sym.flow.cli.helpers.config import store_login_config
from sym.flow.cli.symflow import symflow as click_command


class TestInit:
    def test_init(self, click_setup, test_org, auth_token):
        with click_setup() as runner:
            store_login_config("implementer@symops.io", test_org, auth_token)

            # Directory is empty to begin
            assert not os.listdir(".")

            result = runner.invoke(click_command, ["init", "--workspace-id", "T123ABC"])
            assert result.exit_code == 0
            assert (
                "Successfully generated your Sym Terraform configuration! Run the following to apply the Terraform:"
                in result.output
            )
            assert "terraform init && terraform apply" in result.output

            # Check that we wrote all of the Terraform files to the directory
            files = os.listdir(".")
            assert "main.tf" in files
            assert "impl.py" in files
            assert "versions.tf" in files

            # For the static files, make sure they are written as-is
            expected_impl = pkg_resources.read_text(approval, "impl.txt")
            with open("impl.py", "r") as f:
                written_impl = f.read()
            assert written_impl == expected_impl

            expected_file = pkg_resources.read_text(approval, "versions.tf")
            with open("versions.tf", "r") as f:
                written_file = f.read()
            assert written_file == expected_file

            # For main.tf, make sure that all of the expected things are filled in.
            expected_main_tf = pkg_resources.read_text(approval, "main.tf")
            expected_main_tf = expected_main_tf.replace("${var.sym_org_slug}", test_org.slug)
            expected_main_tf = expected_main_tf.replace("${var.slack_workspace_id}", "T123ABC")

            with open("main.tf", "r") as f:
                written_main_tf = f.read()

            assert written_main_tf == expected_main_tf

    def test_init_prompts(self, click_setup, test_org, auth_token):
        with click_setup() as runner:
            store_login_config("implementer@symops.io", test_org, auth_token)
            result = runner.invoke(click_command, ["init"], input="T123ABC\n")
            assert result.exit_code == 0

            assert (
                "Successfully generated your Sym Terraform configuration! Run the following to apply the Terraform:"
                in result.output
            )
            assert "terraform init && terraform apply" in result.output

    def test_init_errors_non_empty(self, click_setup, test_org, auth_token):
        with click_setup() as runner:
            store_login_config("implementer@symops.io", test_org, auth_token)

            # Write a random file so the directory isn't empty
            with open("foo.txt", "w") as f:
                f.write("Hello")

            # Directory is not empty
            assert os.listdir(".")

            result = runner.invoke(click_command, ["init", "--workspace-id", "T123ABC"])
            assert result.exit_code != 0
            assert (
                "The current directory is not empty! `symflow init` can only be run in an empty directory."
                in result.output
            )
